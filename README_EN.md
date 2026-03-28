<div align="center">

# 🪄 PostSkill

**Input a topic, automatically generate multiple copy variants, image outputs, and review-ready content materials.**  
**This is a content production pipeline prototype — not just another copywriting script.**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![CI](https://img.shields.io/github/actions/workflow/status/AIPMAndy/postskill/ci.yml?branch=main&label=CI)](https://github.com/AIPMAndy/postskill/actions)
[![Auto Publish](https://img.shields.io/badge/Workflow-Auto%20Publish-brightgreen)](./.github/workflows/auto-publish.yml)

[简体中文](./README.md) | **English**

</div>

---

## What is this?

`PostSkill` is an **automation prototype for content production and publishing workflows**.

It is not mainly trying to solve “generate one more AI caption.” It is trying to connect the whole chain:

> input a topic → generate multiple content styles → create images → organize review-ready materials → connect into downstream publishing.

At its current stage, it is best understood as a **working MVP for a content pipeline**, not a fully polished SaaS product.

---

## What problem does it solve?

The annoying part of content work is rarely “write one post.” It is the repeated operational layer around it:

- one topic needs multiple stylistic angles
- each version needs matching imagery
- teams need something reviewable and editable
- publishing is another step after asset generation

That is why PostSkill matters as a pipeline, not as a single-point tool.

**It turns content production from disconnected actions into a connected workflow.**

---

## What the current version can actually do

This section only describes what the repository **actually implements today**.

### Implemented
- ✅ Generate multiple copy variants from a topic via CLI
- ✅ Call PonyFlash to generate matching images
- ✅ Produce Markdown materials that pair copy with images
- ✅ Run automation through GitHub Actions workflows
- ✅ Include publishing workflow scaffolding and health checks

### Still prototype / in progress
- ⚠️ Platform publishers are still mostly adapter scaffolding, not a fully mature publish system
- ⚠️ Feishu is currently centered around generating reviewable materials, not a deep end-to-end publishing integration
- ⚠️ Some old README / command references used to promise more than the code delivered; this version intentionally tightens the story to match the repo

In one sentence:

**Right now, this repo is best positioned as a content automation pipeline prototype, not a fully finished one-click cross-platform publisher.**

---

## Why this project is valuable

Many tools solve only one piece:

- copy only
- image only
- publish only
- document organization only

PostSkill tries to connect them.

| Capability | Single-point tools | **PostSkill** |
|---|---|---|
| Multi-style copy | ✅ | ✅ |
| AI image generation | Sometimes | ✅ |
| Material organization | Usually manual | ✅ |
| Workflow chaining | Rare | ✅ |
| Automation execution | Rare | ✅ |

So the real pitch here is not “copywriting magic.” It is:

> **a content production automation pipeline.**

---

## 30-second quick start

```bash
git clone https://github.com/AIPMAndy/postskill.git
cd postskill
pip install -r requirements.txt
playwright install chromium
```

### Generate a full batch of content materials

```bash
python postskill.py run --topic "AI Awakening"
```

This will:
- generate multiple copy variants
- attempt to generate images
- output a Markdown material file pairing copy and images

### Generate copy only

```bash
python postskill.py generate --topic "AI Awakening" --output ./output
```

### Generate images only

```bash
python postskill.py generate-images --config ./output/copies.json --output ./output/images
```

### Generate review materials

```bash
python postskill.py create-doc --content ./output/copies.json --images ./output/images --output ./output
```

---

## Core modules

```text
.
├── postskill.py                  # CLI entrypoint
├── scripts/
│   ├── copy_generator.py         # multi-style copy generation
│   ├── image_generator.py        # PonyFlash image generation
│   ├── feishu_doc_creator.py     # review material generation
│   └── publisher.py              # publishing scaffolding
├── tests/
└── .github/workflows/            # CI / health / automation workflows
```

---

## Best places to start

If this is your first time here, start with:

1. `postskill.py` — the CLI flow
2. `scripts/copy_generator.py` — multi-style copy generation
3. `scripts/image_generator.py` — image generation integration
4. `scripts/feishu_doc_creator.py` — review material generation
5. `.github/workflows/auto-publish.yml` — automation chain
6. [examples/ai-awakening-output.md](./examples/ai-awakening-output.md) — a demo case you can show
7. [LAUNCH_PACK.md](./LAUNCH_PACK.md) — ready-to-use launch copy

---

## Who this is for

- creators and operators who want a repeatable content workflow
- people building AI-assisted media pipelines
- builders who want to connect PonyFlash, Feishu, and publishing automation
- developers who want a working prototype to extend

---

## Roadmap

- [x] Multi-style copy generation
- [x] AI image generation
- [x] Material document generation
- [x] GitHub Actions automation chain
- [ ] Fully implemented platform publishers
- [ ] More stable account/session management
- [ ] Publish result tracking and dashboards
- [ ] More platform adapters
- [ ] Stronger template and strategy layers

---

## Contributing

Contributions are especially welcome in:

- platform publishing adapters
- better copy templates
- more robust image generation / retry logic
- stronger review workflows
- real demos and case studies

See [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## License

Apache-2.0

---

## If this project helps you

Please do two simple things:

1. give it a **⭐ Star**
2. open an issue describing the content workflow you actually want to automate

That is the fastest path from prototype to useful system.
