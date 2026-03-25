<div align="center">

# 🚀 PostSkill

**一句话：输入主题，自动生成图文 + 一键发布到多平台**

[![License: PostSkill](https://img.shields.io/badge/License-PostSkill-orange.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/AIPMAndy/postskill?style=social)](https://github.com/AIPMAndy/postskill)

[English](README_EN.md) | **简体中文**

<img src="assets/demo.gif" width="700" alt="PostSkill Demo">

*端到端图文批量生产与自动发布工具*

</div>

---

## 🆚 为什么选 PostSkill？

| 能力 | 手动操作 | 其他工具 | **PostSkill** |
|------|:--------:|:--------:|:-------------:|
| 文案生成 | ❌ 人工写 | ⚠️ 单一风格 | ✅ **多风格批量生成** |
| 配图生成 | ❌ 找图/设计 | ⚠️ 需手动配 | ✅ **AI自动配图** |
| 内容审核 | ❌ 本地文件 | ⚠️ 分散管理 | ✅ **飞书文档协作** |
| 多平台发布 | ❌ 逐个登录 | ⚠️ API限制多 | ✅ **浏览器自动化** |
| 端到端流程 | ❌ 多个工具 | ❌ 部分覆盖 | ✅ **一键完成** |

**核心差异**：不是单个工具，是完整的「内容生产流水线」

---

## 🚀 30秒快速开始

```bash
# 1. 安装（一行命令）
codex skill install postskill

# 2. 配置平台账号（首次）
postskill config --platform wechat
postskill config --platform xiaohongshu

# 3. 一键生成并发布
postskill run --topic "AI醒觉社" --publish --platforms wechat,xiaohongshu
```

**完成！** 你会得到：
- ✅ 3-10 套不同风格文案
- ✅ 每套配套 AI 生成图片
- ✅ 图文对照的飞书文档
- ✅ 已发布到指定平台

---

## 📖 核心功能

### 1️⃣ 文案生成（多风格）

基于主题自动生成多种风格文案：

| 风格 | 特点 | 适用场景 |
|------|------|----------|
| 📚 干货型 | 知识点密集，实用性强 | 专业领域分享 |
| 📖 故事型 | 叙事驱动，情感共鸣 | 个人IP打造 |
| ✨ 金句型 | 短句有力，易于传播 | 朋友圈/小红书 |
| 📊 数据型 | 数据支撑，权威可信 | 行业分析 |
| ⚖️ 对比型 | 前后对比，效果突出 | 产品推广 |

### 2️⃣ 配图生成（AI驱动）

调用 PonyFlash 为每套文案生成配套图片：

- **尺寸**: 768×1024px (3:4 竖版，适合移动端)
- **分辨率**: 2K 高清
- **模型**: nano-banana-pro
- **风格**: 自动匹配文案调性

### 3️⃣ 飞书文档（协作审核）

自动创建图文对照的飞书文档：

```
📄 飞书文档结构
├── 主题：XXX
├── 文案1 + 配图1
├── 文案2 + 配图2
├── 文案3 + 配图3
└── [一键发布] 按钮
```

### 4️⃣ 自动发布（浏览器自动化）

支持平台：

- ✅ 微信公众号
- ✅ 小红书
- 🚧 抖音（开发中）
- 🚧 微博（开发中）

---

## 💡 使用场景

### 场景1：公众号内容矩阵
每周输入主题，批量生成 5-10 篇图文，定时发布，建立内容护城河。

### 场景2：小红书爆款测试
输入关键词，生成多套内容，快速测试哪个方向容易爆。

### 场景3：朋友圈素材库
批量生成金句+配图，建立个人素材库，随时取用。

### 场景4：社群运营
每周自动生成社群分享内容，保持活跃度，不用愁没东西发。

---

## 🗺️ Roadmap

- [x] 多风格文案生成
- [x] AI 配图生成
- [x] 飞书文档自动创建
- [x] 微信公众号自动发布
- [x] 小红书自动发布
- [ ] 抖音自动发布
- [ ] 微博自动发布
- [ ] 定时发布功能
- [ ] 数据分析看板
- [ ] 爆款内容模板库

---

## 📚 完整文档

- [快速开始指南](docs/quickstart.md)
- [配置说明](docs/config.md)
- [API 文档](docs/api.md)
- [常见问题](docs/faq.md)

---

## 👨‍💻 作者

**AI酋长Andy**

前腾讯/百度 AI 产品专家，现 AI 商业战略顾问。

专注：AI + 内容生产、AI + 自动化获客

[![微信](https://img.shields.io/badge/微信-AIPMAndy-brightgreen.svg)](https://github.com/AIPMAndy)
[![GitHub](https://img.shields.io/badge/GitHub-AIPMAndy-black.svg)](https://github.com/AIPMAndy)

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

<div align="center">

**如果有帮助，请给个 ⭐ Star！**

[![Star History Chart](https://api.star-history.com/svg?repos=AIPMAndy/postskill&type=Date)](https://star-history.com/#AIPMAndy/postskill&Date)

</div>
