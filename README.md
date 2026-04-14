<div align="center">

# 🪄 PostSkill

### 一个主题 → 10 套文案 + 配图 + 可发布素材，全自动

**不只是文案生成器，而是把"选题→创作→配图→审核→发布"串成一条自动化流水线**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![CI](https://img.shields.io/github/actions/workflow/status/AIPMAndy/postskill/ci.yml?branch=main&label=CI)](https://github.com/AIPMAndy/postskill/actions)

**简体中文** | [English](./README_EN.md)

<img src="https://via.placeholder.com/800x400/6366f1/ffffff?text=Demo+Coming+Soon" alt="PostSkill Demo" width="100%" />

</div>

---

## 💡 3 秒看懂

你只需要：
```bash
python postskill.py run --topic "AI 如何改变内容创作"
```

PostSkill 自动帮你：
1. ✅ 生成 10 种风格文案（专业/轻松/故事/数据驱动...）
2. ✅ 为每套文案配 AI 生成的配图
3. ✅ 整理成 Markdown 文档，可直接审核/修改
4. ✅ 一键发布到公众号/小红书/知乎（开发中）

**省下 80% 重复劳动，专注在创意和策略上。**

---

## 🔥 为什么需要 PostSkill

### 传统内容生产的痛点

| 痛点 | 传统方式 | PostSkill |
|------|---------|-----------|
| 一个选题要写多套文案 | 手动写 10 遍 | ✅ 自动生成 10 套 |
| 每套文案要配图 | 找图/设计/AI 单独出图 | ✅ 自动配图 |
| 团队协作审核 | 复制粘贴到文档 | ✅ 自动生成 Markdown |
| 发布到多平台 | 手动复制粘贴 | ✅ 一键发布（开发中）|
| 流程断裂 | 每个环节单独工具 | ✅ 一条流水线 |

### 真实场景

**场景 1：运营团队**
> "我们每周要出 20 篇内容，每篇要适配 3 个平台。以前要 2 天，现在 2 小时搞定初稿。"

**场景 2：个人创作者**
> "我只想专注写作，不想花时间找图、排版、复制粘贴。PostSkill 帮我省下 70% 时间。"

**场景 3：AI 工作流玩家**
> "这是我见过第一个把文案、配图、发布串起来的开源工具。可以直接改成自己的内容引擎。"

---

## ⚡ 30 秒快速开始

### 安装

```bash
git clone https://github.com/AIPMAndy/postskill.git
cd postskill
pip install -r requirements.txt
playwright install chromium
```

### 生成第一套内容

```bash
# 一键生成完整内容包（文案 + 配图 + 文档）
python postskill.py run --topic "AI 如何改变内容创作"

# 只生成文案
python postskill.py generate --topic "你的主题" --output ./output

# 只生成配图
python postskill.py generate-images --config ./output/copies.json --output ./output/images

# 生成可审核的 Markdown 文档
python postskill.py create-doc --content ./output/copies.json --images ./output/images --output ./output
```

### 查看结果

生成的文件在 `./output/` 目录：
- `copies.json` - 10 套文案
- `images/` - 配图
- `content-review.md` - 图文整理后的审核文档

---

## 🎯 核心能力

### 1️⃣ 多风格文案生成

一个主题，自动生成 10 种风格：

- 📊 **数据驱动型**：用数据说话，适合 B 端/专业内容
- 🎭 **故事叙述型**：讲故事，适合品牌/情感内容
- 💡 **观点输出型**：犀利观点，适合 KOL/思想领袖
- 🔥 **热点追踪型**：结合热点，适合蹭流量
- 📚 **知识科普型**：深度讲解，适合教育/科普
- 🎨 **创意脑洞型**：天马行空，适合创意/娱乐
- 💼 **商务专业型**：严谨专业，适合企业/官方
- 🌟 **励志鸡汤型**：正能量，适合个人成长
- 🤔 **反思质疑型**：批判性思考，适合深度内容
- 😄 **轻松幽默型**：段子手风格，适合娱乐/社交

### 2️⃣ AI 配图生成

- 基于 PonyFlash SDK 自动生成配图
- 支持多种风格（写实/插画/3D/概念艺术）
- 自动匹配文案主题和情绪

### 3️⃣ 素材整理

- 自动生成图文对照的 Markdown 文档
- 支持导出到飞书文档（团队协作）
- 可直接审核/修改/批注

### 4️⃣ 自动化发布（开发中）

- GitHub Actions 定时执行
- 支持公众号/小红书/知乎（接口骨架已完成）
- 发布结果回收与数据看板（规划中）

---

## 📂 项目结构

```text
postskill/
├── postskill.py                  # CLI 主入口
├── scripts/
│   ├── copy_generator.py         # 多风格文案生成
│   ├── image_generator.py        # AI 配图生成
│   ├── feishu_doc_creator.py     # 飞书文档生成
│   └── publisher.py              # 平台发布器（骨架）
├── tests/                        # 单元测试
├── examples/                     # 示例输出
│   └── ai-awakening-output.md    # 真实案例
├── .github/workflows/            # 自动化工作流
│   ├── auto-publish.yml          # 自动发布
│   └── ci.yml                    # CI/CD
└── README.md
```

---

## 🎬 真实案例

查看完整示例：[examples/ai-awakening-output.md](./examples/ai-awakening-output.md)

**输入主题**：AI 醒觉社

**输出结果**：
- ✅ 10 套不同风格文案
- ✅ 10 张配图
- ✅ 1 份可审核的 Markdown 文档

**耗时**：约 3 分钟（取决于 AI 接口速度）

---

## 🚀 适合谁

✅ **内容运营团队**：批量生产内容，提升效率  
✅ **个人创作者**：省下找图/排版时间，专注创作  
✅ **AI 工作流玩家**：可改造成自己的内容引擎  
✅ **自媒体矩阵**：一套内容适配多平台  
✅ **企业品牌**：快速产出多风格营销素材  

---

## 🛣️ Roadmap

### ✅ 已完成
- [x] 多风格文案生成
- [x] AI 配图生成（PonyFlash）
- [x] 素材文档自动整理
- [x] GitHub Actions 自动化链路
- [x] 飞书文档生成

### 🚧 开发中
- [ ] 完整平台发布器（公众号/小红书/知乎）
- [ ] 平台账号管理
- [ ] 发布结果回收与看板

### 📋 规划中
- [ ] 更多平台适配（抖音/B 站/Twitter）
- [ ] 内容策略层（选题推荐/热点追踪）
- [ ] 更强的文案模板库
- [ ] 图片生成重试策略
- [ ] 素材审核流程优化

---

## 🤝 贡献

欢迎贡献：

- 🔌 **平台适配器**：接入更多发布平台
- 📝 **文案模板**：补充更多风格模板
- 🎨 **配图策略**：优化图片生成逻辑
- 🔄 **工作流优化**：改进自动化流程
- 📚 **文档完善**：补充使用案例

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## 📄 License

Apache-2.0

---

## ⭐ 如果这个项目对你有帮助

1. 给个 **Star** 支持一下
2. 提个 **Issue** 说说你的使用场景
3. 提个 **PR** 贡献你的改进

**让内容生产从手工作坊，变成自动化工厂。**

---

<div align="center">

Made with ❤️ by [Andy | AI酋长](https://github.com/AIPMAndy)

</div>
