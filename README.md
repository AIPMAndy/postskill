<div align="center">

# 🪄 PostSkill

**输入一个主题，自动生成多套文案、配图占位结果，并整理成可审核的 Markdown / 飞书协作素材。**  
**这是一个内容生产流水线原型，不只是一个文案生成脚本。**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![CI](https://img.shields.io/github/actions/workflow/status/AIPMAndy/postskill/ci.yml?branch=main&label=CI)](https://github.com/AIPMAndy/postskill/actions)
[![Auto Publish](https://img.shields.io/badge/Workflow-Auto%20Publish-brightgreen)](./.github/workflows/auto-publish.yml)

**简体中文** | [English](./README_EN.md)

</div>

---

## 这是什么

`PostSkill` 是一个 **面向内容生产与发布流程的自动化原型**。

它想解决的不是“再生成一段 AI 文案”，而是把这条链路先串起来：

> 输入主题 → 生成多风格文案 → 配图 → 整理成可审核素材 → 再接后续发布动作。

它当前更像一个 **可运行的内容流水线 MVP**，而不是已经完全打磨好的 SaaS 产品。

---

## 它解决什么问题

做内容最烦的，通常不是“写一篇文案”，而是这些重复动作：

- 一个主题要拆多套风格
- 每套内容要配图
- 团队要先看、先改、先审核
- 最后还要再发到平台

所以 PostSkill 的价值不是单点能力，而是：

**把内容生产从离散动作，拉成一个连续流程。**

---

## 当前版本真实能做什么

这里我只写仓库里**当前真实具备**的能力：

### 已实现
- ✅ 命令行输入主题，生成多套不同风格文案
- ✅ 调用 PonyFlash 为文案生成配图
- ✅ 生成图文对照的 Markdown 素材文档
- ✅ 基于 GitHub Actions 跑自动化流程
- ✅ 已有自动发布工作流骨架与健康检查

### 还在原型 / 开发中
- ⚠️ 平台发布器还主要是接口骨架，不是完整成熟发布系统
- ⚠️ 飞书目前核心是生成可协作素材文档，不是完整深度集成发布平台
- ⚠️ README 之前提到的一些命令 / docs 页面，在旧版本里和实际代码不完全一致，这次我已经按真实状态重新收敛叙事

一句话：

**它现在最像“内容自动化流水线原型”，而不是“已经全平台一键发布的成熟产品”。**

---

## 为什么这项目有价值

因为很多内容工具只解决一个点：

- 只会写文案
- 只会出图
- 只会发平台
- 只会做文档整理

而 PostSkill 在做的，是把这些点接起来。

| 能力 | 单点工具 | **PostSkill** |
|---|---|---|
| 多风格文案 | ✅ | ✅ |
| AI 配图 | 有的支持 | ✅ |
| 素材整理 | 通常手动 | ✅ |
| 流程串联 | 少 | ✅ |
| 自动化执行 | 少 | ✅ |

所以这个项目真正该卖的，不是“文案神器”，而是：

> **内容生产自动化 pipeline。**

---

## 30 秒快速开始

```bash
git clone https://github.com/AIPMAndy/postskill.git
cd postskill
pip install -r requirements.txt
playwright install chromium
```

### 生成整套内容素材

```bash
python postskill.py run --topic "AI醒觉社"
```

这会做几件事：
- 生成多套文案
- 尝试生成配图
- 输出图文整理后的 Markdown 文件

### 只生成文案

```bash
python postskill.py generate --topic "AI醒觉社" --output ./output
```

### 只生成图片

```bash
python postskill.py generate-images --config ./output/copies.json --output ./output/images
```

### 生成素材文档

```bash
python postskill.py create-doc --content ./output/copies.json --images ./output/images --output ./output
```

---

## 核心模块

```text
.
├── postskill.py                  # CLI 主入口
├── scripts/
│   ├── copy_generator.py         # 多风格文案生成
│   ├── image_generator.py        # PonyFlash 配图生成
│   ├── feishu_doc_creator.py     # 素材文档生成
│   └── publisher.py              # 平台发布骨架
├── tests/
└── .github/workflows/            # 自动化发布 / CI / 健康检查
```

---

## 当前最值得看的地方

如果你第一次打开这个项目，建议优先看：

1. `postskill.py` — CLI 主流程
2. `scripts/copy_generator.py` — 多风格文案生成
3. `scripts/image_generator.py` — 图片生成接入
4. `scripts/feishu_doc_creator.py` — 图文素材文档输出
5. `.github/workflows/auto-publish.yml` — 自动化链路

---

## 适合谁

- 想把“内容生产”做成流水线的人
- 运营 / 创作者 / AI 工作流玩家
- 想把 PonyFlash、飞书、自动化发布串起来的人
- 想基于一个可运行原型继续往上搭系统的人

---

## Roadmap

- [x] 多风格文案生成
- [x] AI 配图生成
- [x] 素材文档自动整理
- [x] GitHub Actions 自动化链路
- [ ] 完整平台发布器落地
- [ ] 更稳定的平台账号管理
- [ ] 发布结果回收与看板
- [ ] 更多平台适配
- [ ] 更强的模板库与内容策略层

---

## 贡献

欢迎补充：

- 平台发布适配器
- 更强的文案模板
- 更稳的图片生成与重试策略
- 更完善的素材审核流程
- 更真实的 demo / case

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## License

Apache-2.0

---

## 如果这个项目对你有帮助

请直接：

1. 给它一个 **⭐ Star**
2. 提一个你真正想打通的内容工作流场景

这样这个项目会更快从原型，长成真正有用的工具。
