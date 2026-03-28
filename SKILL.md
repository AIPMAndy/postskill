---
name: postskill
description: End-to-end content production workflow skill for generating multiple copy variants, creating matching images, organizing review-ready materials, and automating downstream publishing steps. Use when the user wants to turn a topic into reusable social content assets, batch content materials, or a semi-automated publishing pipeline.
---

# PostSkill

Use this skill to turn a single topic into a small content production workflow.

## What it is good at

- generate multiple copy variants from one topic
- pair copy with generated images
- organize materials into review-ready Markdown output
- support downstream publishing automation workflows

## Current repo reality

Treat the current implementation as a **working pipeline prototype**.

Implemented today:
- copy generation
- image generation via PonyFlash
- material document generation
- workflow automation via GitHub Actions

Still partial / scaffolded:
- platform publishing adapters
- some end-to-end publishing flows
- broader platform coverage

Do not claim capabilities that the codebase does not actually implement.

## Main workflow

1. Generate multiple content variants from a topic.
2. Generate matching images for each variant.
3. Export review-ready materials.
4. Optionally connect into publishing workflows.

## Entry points

### Full pipeline
```bash
python postskill.py run --topic "Your Topic"
```

### Copy only
```bash
python postskill.py generate --topic "Your Topic" --output ./output
```

### Images only
```bash
python postskill.py generate-images --config ./output/copies.json --output ./output/images
```

### Review material document
```bash
python postskill.py create-doc --content ./output/copies.json --images ./output/images --output ./output
```

## Important guidance

- Present PostSkill as a content pipeline, not as a finished all-platform publishing SaaS.
- Be explicit about which parts are production-ready vs scaffolded.
- Prefer accurate claims over impressive claims.
- When describing outcomes, separate implemented behavior from roadmap behavior.
