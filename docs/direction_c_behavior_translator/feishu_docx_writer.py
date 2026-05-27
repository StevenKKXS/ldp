#!/usr/bin/env python3
"""Small Feishu docx writer used for Direction C reports.

It avoids Markdown tables and uses the documented image flow:
create empty Image Block -> upload media to that block -> PATCH replace_image.
"""

import json
import mimetypes
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


SKILL = Path("/work-agents/ldp/workspace/.skill_sources/intern_agent_skills/intern_feishu_docs_skill/scripts")
sys.path.insert(0, str(SKILL))
from auth import get_access_token  # noqa: E402


DOCX_ENDPOINT = "https://open.feishu.cn/open-apis/docx/v1/documents"
MEDIA_ENDPOINT = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"


def request_json(url, method="POST", body=None, headers=None, timeout=30):
    token = get_access_token()
    req_headers = {"Authorization": f"Bearer {token}"}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, data=body, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"feishu HTTP {e.code}: {e.read().decode()}") from e
    if data.get("code") != 0:
        raise RuntimeError(f"feishu error: {json.dumps(data, ensure_ascii=False)}")
    return data


def create_doc(title):
    body = json.dumps({"title": title}).encode()
    data = request_json(
        DOCX_ENDPOINT,
        body=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    doc = data["data"]["document"]
    return doc["document_id"], f"https://feishu.cn/docx/{doc['document_id']}"


def text_block(text, block_type=2):
    field = {
        2: "text",
        3: "heading1",
        4: "heading2",
        5: "heading3",
        12: "bullet",
        13: "ordered",
        14: "code",
        15: "quote",
    }.get(block_type, "text")
    return {
        "block_type": block_type,
        field: {
            "elements": [{"text_run": {"content": text}}],
            "style": {},
        },
    }


def append_children(doc_id, children):
    if not children:
        return []
    url = (
        f"{DOCX_ENDPOINT}/{urllib.parse.quote(doc_id)}"
        f"/blocks/{urllib.parse.quote(doc_id)}/children"
    )
    body = json.dumps({"children": children}, ensure_ascii=False).encode()
    data = request_json(
        url,
        body=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        timeout=60,
    )
    return data["data"].get("children", [])


def patch_block(doc_id, block_id, patch_body):
    url = f"{DOCX_ENDPOINT}/{urllib.parse.quote(doc_id)}/blocks/{urllib.parse.quote(block_id)}"
    body = json.dumps(patch_body, ensure_ascii=False).encode()
    return request_json(
        url,
        method="PATCH",
        body=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        timeout=60,
    )


def multipart(fields, file_field):
    boundary = "----internldpboundary7MA4YWxkTrZu0gW"
    chunks = []
    for name, value in fields.items():
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        chunks.append(str(value).encode())
        chunks.append(b"\r\n")
    name, filename, content_type, data = file_field
    chunks.append(f"--{boundary}\r\n".encode())
    chunks.append(f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode())
    chunks.append(f"Content-Type: {content_type}\r\n\r\n".encode())
    chunks.append(data)
    chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), boundary


def upload_image_to_block(image_block_id, image_path):
    data = image_path.read_bytes()
    ctype = mimetypes.guess_type(str(image_path))[0] or "image/png"
    body, boundary = multipart(
        {
            "file_name": image_path.name,
            "parent_type": "docx_image",
            "parent_node": image_block_id,
            "size": len(data),
        },
        ("file", image_path.name, ctype, data),
    )
    result = request_json(
        MEDIA_ENDPOINT,
        body=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        timeout=60,
    )
    token = result["data"].get("file_token") or result["data"].get("token")
    if not token:
        raise RuntimeError(f"upload result missing token: {json.dumps(result, ensure_ascii=False)}")
    return token


def append_image(doc_id, image_path):
    created = append_children(doc_id, [{"block_type": 27, "image": {}}])
    if not created:
        raise RuntimeError("empty image block create response")
    block_id = created[0]["block_id"]
    token = upload_image_to_block(block_id, image_path)
    patch_block(doc_id, block_id, {"replace_image": {"token": token}})
    return block_id, token


def parse_markdown_like(root, text):
    """Parse a restrained report format into text blocks and image commands."""
    blocks = []
    para = []
    in_code = False
    code = []

    def flush():
        if para:
            blocks.append(text_block("\n".join(para).strip()))
            para.clear()

    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            if not in_code:
                flush()
                in_code = True
                code = []
            else:
                blocks.append(text_block("\n".join(code), 14))
                in_code = False
                code = []
            continue
        if in_code:
            code.append(line)
            continue
        m = re.match(r"!\[.*?\]\((.*?)\)", line.strip())
        if m:
            flush()
            blocks.append({"__image__": str(root / m.group(1))})
            continue
        if line.startswith("# "):
            flush()
            blocks.append(text_block(line[2:].strip(), 3))
        elif line.startswith("## "):
            flush()
            blocks.append(text_block(line[3:].strip(), 4))
        elif line.startswith("### "):
            flush()
            blocks.append(text_block(line[4:].strip(), 5))
        elif line.startswith("- "):
            flush()
            blocks.append(text_block(line[2:].strip(), 12))
        elif line.strip() == "":
            flush()
        else:
            para.append(line)
    flush()
    return blocks


def publish_report(report_path, title):
    root = report_path.resolve().parent
    doc_id, url = create_doc(title)
    print(f"document_id={doc_id}")
    print(f"url={url}")
    blocks = parse_markdown_like(root, report_path.read_text(encoding="utf-8"))
    buffer = []
    done = 0
    for block in blocks:
        if "__image__" in block:
            if buffer:
                append_children(doc_id, buffer)
                done += len(buffer)
                print(f"appended text blocks {done}/{len(blocks)}")
                buffer = []
                time.sleep(0.4)
            image_path = Path(block["__image__"])
            block_id, token = append_image(doc_id, image_path)
            done += 1
            print(f"appended image {image_path.name} block_id={block_id} token={token}")
            time.sleep(0.4)
        else:
            buffer.append(block)
            if len(buffer) >= 20:
                append_children(doc_id, buffer)
                done += len(buffer)
                print(f"appended text blocks {done}/{len(blocks)}")
                buffer = []
                time.sleep(0.4)
    if buffer:
        append_children(doc_id, buffer)
        done += len(buffer)
        print(f"appended text blocks {done}/{len(blocks)}")
    return doc_id, url
