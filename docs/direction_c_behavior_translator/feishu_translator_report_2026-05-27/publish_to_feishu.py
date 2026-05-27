#!/usr/bin/env python3
import json
import mimetypes
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SKILL = Path("/work-agents/ldp/workspace/.skill_sources/intern_agent_skills/intern_feishu_docs_skill/scripts")
sys.path.insert(0, str(SKILL))
from auth import get_access_token  # noqa: E402


DOCX_ENDPOINT = "https://open.feishu.cn/open-apis/docx/v1/documents"
MEDIA_ENDPOINT = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "source_report.md"


def request_json(url, method="POST", body=None, headers=None, timeout=30):
    token = get_access_token()
    req_headers = {"Authorization": f"Bearer {token}"}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(
        url,
        data=body,
        headers=req_headers,
        method=method,
    )
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
    chunks.append(
        f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode())
    chunks.append(f"Content-Type: {content_type}\r\n\r\n".encode())
    chunks.append(data)
    chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), boundary


def upload_image(doc_id, image_path):
    data = image_path.read_bytes()
    ctype = mimetypes.guess_type(str(image_path))[0] or "image/png"
    body, boundary = multipart(
        {
            "file_name": image_path.name,
            "parent_type": "docx_image",
            "parent_node": doc_id,
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


def text_block(text, block_type=2):
    field = {
        2: "text",
        3: "heading1",
        4: "heading2",
        5: "heading3",
    }.get(block_type, "text")
    return {
        "block_type": block_type,
        field: {
            "elements": [{"text_run": {"content": text}}],
            "style": {},
        },
    }


def image_block(token, image_path):
    return {
        "block_type": 27,
        "image": {
            "file_token": token,
        },
    }


def append_children(doc_id, children):
    if not children:
        return
    url = (
        f"{DOCX_ENDPOINT}/{urllib.parse.quote(doc_id)}"
        f"/blocks/{urllib.parse.quote(doc_id)}/children"
    )
    body = json.dumps({"children": children}, ensure_ascii=False).encode()
    request_json(
        url,
        body=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        timeout=60,
    )


def flush_paragraph(children, para):
    if para:
        children.append(text_block("\n".join(para).strip()))
        para.clear()


def markdown_to_children(doc_id, text):
    children = []
    para = []
    in_code = False
    code = []
    lines = text.splitlines()
    for line in lines:
        if line.startswith("```"):
            if not in_code:
                flush_paragraph(children, para)
                in_code = True
                code = [line]
            else:
                code.append(line)
                children.append(text_block("\n".join(code)))
                in_code = False
                code = []
            continue
        if in_code:
            code.append(line)
            continue

        m = re.match(r"!\[.*?\]\((.*?)\)", line.strip())
        if m:
            flush_paragraph(children, para)
            image_path = ROOT / m.group(1)
            token = upload_image(doc_id, image_path)
            children.append(image_block(token, image_path))
            continue

        if line.startswith("# "):
            flush_paragraph(children, para)
            children.append(text_block(line[2:].strip(), block_type=3))
        elif line.startswith("## "):
            flush_paragraph(children, para)
            children.append(text_block(line[3:].strip(), block_type=4))
        elif line.startswith("### "):
            flush_paragraph(children, para)
            children.append(text_block(line[4:].strip(), block_type=5))
        elif line.strip() == "":
            flush_paragraph(children, para)
        else:
            para.append(line)
    flush_paragraph(children, para)
    return children


def main():
    title = "Behavior Translator 方向探索更新 - 2026-05-27"
    doc_id, url = create_doc(title)
    print(f"document_id={doc_id}")
    print(f"url={url}")
    children = markdown_to_children(doc_id, REPORT.read_text(encoding="utf-8"))
    for start in range(0, len(children), 20):
        append_children(doc_id, children[start:start + 20])
        print(f"appended {min(start + 20, len(children))}/{len(children)}")


if __name__ == "__main__":
    main()
