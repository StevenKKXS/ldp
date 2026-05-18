# intern_method_developer - 个人知识库

<!-- METADATA:SESSION=0 -->

---

## 知识条目

### Storage Policy: small files and repositories

- 后续小文件和 git 仓库默认放到 `/mnt/nfs/tingwen/intern_method_developer/`。
- 推荐结构：
  - `repos/`: git repositories
  - `tasks/<task_id>/`: task-scoped scripts, reports, notes, configs, manifests
  - `docs/`: cross-task documents and notes
  - `logs/`: small command logs or text logs
  - `tmp/`: short-lived scratch files
- `/mnt/nfs/tingwen` 是临时存储；每个 task 的小文件应在约 24h 或若干 session 后打包到 `/mnt/cephfs/home/tinwen.du/intern_method_developer/archives/by_task/`。
- CephFS durable area: `/mnt/cephfs/home/tinwen.du/intern_method_developer/`。
- 除非用户明确指定，不额外保存 ckpt、rollout 输出、大数据集、大视频；报告、配置、脚本、README、yaml/json/md/txt 这类小文件优先保存。
- 多 agent CephFS 归档入口：`/mnt/cephfs/home/tinwen.du/AGENT_ARCHIVE_GUIDE.md`。
- 多 agent 规则与 schema 管理目录：`/mnt/cephfs/home/tinwen.du/_agent_archive_admin/`；更新规则时改 `RULES.md` / `SCHEMA.md` / `CHANGELOG.md`，重构时在 `migrations/` 留迁移说明。
- 本 agent 在 CephFS 的 schema-v1 新归档路径优先使用 `/mnt/cephfs/home/tinwen.du/intern_method_developer/task_archives/<task_id>/`；旧的 `archives/by_task/` 保持可读但不作为新默认。

### Idea Backlog: encoder training hypotheses

Status: unvalidated, do not treat as adopted design. Remove this section if later discussion or experiments decide to abandon it.

Context:
- We want to revisit the visual/action encoder (`enc`) design, especially if moving toward a transformer encoder.
- Important reminder for future discussion: verify the claim/hypothesis that diffusion-policy loss backpropagated into an upstream transformer/encoder may provide a weak or mismatched training signal. Do not assume this is true without evidence.

Idea 1: encoder as image-to-coordinate-sequence translation
- Treat encoder training like a translation task: image encoding -> coordinate/action-related sequence.
- Potential form: transformer encoder over image tokens or multi-frame visual tokens, trained to produce a coordinate sequence or structured trajectory tokens.
- Concern: this is immature; if diffusion loss does not backpropagate useful signal into upstream transformer/encoder, end-to-end diffusion training may not sufficiently shape the encoder.
- Follow-up needed: search literature / existing ablations and run a small controlled test comparing frozen pretrained enc, end-to-end finetuned enc, and separately supervised enc.

Idea 2: task-specialized contrastive encoder for current small specialist model
- Train a specialist encoder for current task/model instead of a general visual encoder.
- Use future and past action windows as supervision to shape embedding distribution.
- Input preference: multi-frame images. If multi-frame implementation is inconvenient, use single frame plus action history.
- Objective sketch: embeddings should be pulled closer when their future ground-truth action sequences are behaviorally similar, and pushed apart when execution/action futures differ.
- Desired effect: current or near-identical visual observations with different histories/futures should not collapse to the same embedding if they imply different actions.
- After pretraining, plug this encoder into diffusion policy and test:
  - frozen encoder + diffusion head
  - encoder finetuned during diffusion training
  - baseline encoder trained only through diffusion
- This idea is motivated by the hypothesis that diffusion objective gradients into upstream encoder may be mismatched or insufficient; that hypothesis must be explicitly tested.

Possible validation plan:
- Define action-similarity metric over future ground-truth chunks, optionally conditioned on past action/history.
- Train contrastive encoder on square or another controlled task.
- Evaluate representation quality with retrieval/nearest-neighbor future-action consistency before policy training.
- Evaluate downstream success and action MSE with frozen vs finetuned encoder ablations.
- Compare against standard diffusion end-to-end encoder training to see whether separate representation training helps.
