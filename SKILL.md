---
name: postskill
description: PostSkill - 端到端图文批量生产与自动发布工具。输入主题，自动生成文案、配图、飞书文档，并支持一键发布到微信公众号、小红书等平台。
license: MIT
metadata:
  author: AIPMAndy
  version: "1.0.0"
---

# PostSkill

**PostSkill** 是一个端到端图文批量生产与自动发布工具。

**核心理念**: 输入主题 → 自动生成多套图文内容 → 一键发布到多平台

## 快速开始

```bash
# 1. 安装Skill
codex skill install postskill

# 2. 配置平台账号
postskill config --platform wechat
postskill config --platform xiaohongshu

# 3. 一键生成并发布
postskill run --topic "AI醒觉社" --publish --platforms wechat,xiaohongshu
```

## 核心能力

### 1. 文案生成 (Copy Generation)
基于主题自动生成多种风格文案。

**支持风格**:
- 干货型 - 知识点密集，实用性强
- 故事型 - 叙事驱动，情感共鸣
- 金句型 - 短句有力，易于传播
- 数据型 - 数据支撑，权威可信
- 对比型 - 前后对比，效果突出

### 2. 配图生成 (Image Generation)
调用PonyFlash为每套文案生成配套图片。

**图片规格**:
- 尺寸: 768×1024px (3:4竖版)
- 分辨率: 2K
- 模型: nano-banana-pro

### 3. 飞书文档 (Feishu Document)
自动创建图文对照的飞书文档，便于协作审核。

### 4. 自动发布 (Auto Publish)
浏览器自动化，一键发布到多平台。

**支持平台**:
- 微信公众号
- 小红书

## 使用场景

**场景1: 公众号内容矩阵**
每周输入主题，批量生成5-10篇图文，定时发布。

**场景2: 小红书爆款测试**
输入关键词，生成多套内容，快速测试爆款方向。

**场景3: 朋友圈素材库**
批量生成金句+配图，建立个人素材库。

**场景4: 社群运营**
每周自动生成社群分享内容，保持活跃度。

## 完整工作流程

```
输入主题
    ↓
[文案生成] → 3-10套不同风格文案
    ↓
[配图生成] → 每套文案配套图片
    ↓
[飞书文档] → 图文对照排版
    ↓
[自动发布] → 一键发布到多平台
    ↓
完成 ✓
```

## 命令参考

### 全流程命令
```bash
# 生成并发布
postskill run --topic "主题" --publish --platforms wechat,xiaohongshu

# 定时发布
postskill run --topic "主题" --schedule "2024-03-25 09:00"
```

### 分步命令
```bash
# 仅生成文案
postskill generate --topic "主题" --output ./output

# 生成配图
postskill generate-images --config ./content.json

# 创建飞书文档
postskill create-doc --content ./content.json --images ./images/

# 发布内容
postskill publish --content ./content.json --platforms wechat
```

### 配置命令
```bash
# 初始化配置
postskill config --init

# 配置平台账号
postskill config --platform wechat
postskill config --platform xiaohongshu

# 查看配置
postskill config --show
```

## 配置说明

配置文件: `~/.postskill/config.json`

```json
{
  "copy": {
    "count": 3,
    "styles": ["干货型", "故事型", "金句型"],
    "max_length": 150
  },
  "image": {
    "model": "nano-banana-pro",
    "aspect_ratio": "3:4",
    "resolution": "2K"
  },
  "publish": {
    "platforms": ["wechat", "xiaohongshu"],
    "schedule": null,
    "auto_publish": false
  }
}
```

## 依赖

- Python 3.10+
- PonyFlash (图片生成)
- Playwright (浏览器自动化)
- APScheduler (定时任务)

## 安装依赖

```bash
pip install -r requirements.txt
playwright install chromium
```

## 项目地址

GitHub: https://github.com/AIPMAndy/postskill

## 作者

AI酋长Andy - 前腾讯/百度 AI 产品专家

微信: AIPMAndy