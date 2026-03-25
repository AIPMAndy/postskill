<div align="center">

# 🚀 PostSkill

**One-liner: Input a topic, auto-generate content + publish to multiple platforms**

[![License: PostSkill](https://img.shields.io/badge/License-PostSkill-orange.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/AIPMAndy/postskill?style=social)](https://github.com/AIPMAndy/postskill)

**English** | [简体中文](README.md)

<img src="assets/demo.gif" width="700" alt="PostSkill Demo">

*End-to-end batch content production and auto-publishing tool*

</div>

---

## 🆚 Why PostSkill?

| Capability | Manual | Other Tools | **PostSkill** |
|------------|:------:|:-----------:|:-------------:|
| Copy Generation | ❌ Manual | ⚠️ Single style | ✅ **Multi-style batch** |
| Image Generation | ❌ Find/design | ⚠️ Manual pairing | ✅ **AI auto-match** |
| Content Review | ❌ Local files | ⚠️ Scattered | ✅ **Feishu collaboration** |
| Multi-platform | ❌ Login one-by-one | ⚠️ API limits | ✅ **Browser automation** |
| End-to-end | ❌ Multiple tools | ❌ Partial | ✅ **One-click complete** |

**Key Difference**: Not just a tool, but a complete "content production pipeline"

---

## 🚀 Quick Start (30 seconds)

```bash
# 1. Install (one command)
codex skill install postskill

# 2. Configure platforms (first time)
postskill config --platform wechat
postskill config --platform xiaohongshu

# 3. Generate and publish
postskill run --topic "AI Awakening" --publish --platforms wechat,xiaohongshu
```

**Done!** You get:
- ✅ 3-10 sets of copy in different styles
- ✅ AI-generated images for each set
- ✅ Feishu document with copy-image pairs
- ✅ Published to specified platforms

---

## 📖 Core Features

### 1️⃣ Copy Generation (Multi-style)

Auto-generate copy in multiple styles based on your topic:

| Style | Characteristics | Best For |
|-------|-----------------|----------|
| 📚 Educational | Dense knowledge, practical | Professional sharing |
| 📖 Storytelling | Narrative-driven, emotional | Personal branding |
| ✨ Quote-style | Punchy, shareable | Social media |
| 📊 Data-driven | Numbers-backed, authoritative | Industry analysis |
| ⚖️ Comparison | Before/after, results | Product promotion |

### 2️⃣ Image Generation (AI-powered)

Generate matching images for each copy set using PonyFlash:

- **Size**: 768×1024px (3:4 vertical, mobile-optimized)
- **Resolution**: 2K HD
- **Model**: nano-banana-pro
- **Style**: Auto-matched to copy tone

### 3️⃣ Feishu Document (Collaborative Review)

Auto-create Feishu documents with copy-image pairs:

```
📄 Document Structure
├── Topic: XXX
├── Copy 1 + Image 1
├── Copy 2 + Image 2
├── Copy 3 + Image 3
└── [One-click Publish] Button
```

### 4️⃣ Auto Publish (Browser Automation)

Supported platforms:

- ✅ WeChat Official Account
- ✅ Xiaohongshu (Little Red Book)
- 🚧 TikTok (in development)
- 🚧 Weibo (in development)

---

## 💡 Use Cases

### Case 1: Content Matrix for Official Accounts
Input weekly topics, batch generate 5-10 articles, schedule publishing. Build a content moat.

### Case 2: Viral Content Testing for Xiaohongshu
Input keywords, generate multiple content sets, quickly test which direction goes viral.

### Case 3: Social Media Asset Library
Batch generate quotes + images, build a personal asset library for quick access.

### Case 4: Community Operations
Auto-generate weekly community content, maintain activity without worrying about what to post.

---

## 🗺️ Roadmap

- [x] Multi-style copy generation
- [x] AI image generation
- [x] Auto Feishu document creation
- [x] WeChat Official Account auto-publish
- [x] Xiaohongshu auto-publish
- [ ] TikTok auto-publish
- [ ] Weibo auto-publish
- [ ] Scheduled publishing
- [ ] Analytics dashboard
- [ ] Viral content template library

---

## 📚 Documentation

- [Quick Start Guide](docs/quickstart.md)
- [Configuration](docs/config.md)
- [API Docs](docs/api.md)
- [FAQ](docs/faq.md)

---

## 👨‍💻 Author

**AI酋长Andy**

Former AI Product Expert at Tencent/Baidu, now AI Business Strategy Consultant.

Focus: AI + Content Production, AI + Automated Customer Acquisition

[![WeChat](https://img.shields.io/badge/WeChat-AIPMAndy-brightgreen.svg)](https://github.com/AIPMAndy)
[![GitHub](https://img.shields.io/badge/GitHub-AIPMAndy-black.svg)](https://github.com/AIPMAndy)

---

## 🤝 Contributing

Issues and PRs welcome!

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

<div align="center">

**If this helps, please give it a ⭐ Star!**

[![Star History Chart](https://api.star-history.com/svg?repos=AIPMAndy/postskill&type=Date)](https://star-history.com/#AIPMAndy/postskill&Date)

</div>
