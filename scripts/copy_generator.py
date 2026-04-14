#!/usr/bin/env python3
"""
PostSkill - 文案生成模块
基于主题生成多种风格的社交媒体文案
"""

import json
import os
from typing import Dict, List, Optional
import time


class CopyGenerator:
    """文案生成器 - 真正的 AI 驱动版本"""
    
    # 10 种专业文案风格的 Prompt 模板
    STYLE_PROMPTS = {
        "数据驱动型": {
            "description": "用数据说话，权威可信，适合 B 端/专业内容",
            "system_prompt": """你是一位数据分析专家和内容营销专家。
你的文案特点：
- 必须包含具体数据/百分比/统计结果
- 用数据支撑观点，增强说服力
- 结构：数据呈现 → 分析 → 结论 → 行动建议
- 语气：客观、专业、权威
- 字数：120-150字""",
            "user_prompt": "请为主题「{topic}」创作一篇数据驱动型文案。要求：1) 包含至少2个具体数据点 2) 数据真实可信或合理推测 3) 突出数据背后的洞察 4) 给出明确的行动建议。"
        },
        
        "故事叙述型": {
            "description": "讲故事，情感共鸣，适合品牌/情感内容",
            "system_prompt": """你是一位故事叙述大师和情感营销专家。
你的文案特点：
- 用真实或虚构的故事引发共鸣
- 结构：背景 → 冲突 → 转折 → 结局 → 启示
- 语气：亲切、真实、有代入感
- 情感：温暖、励志、治愈
- 字数：120-150字""",
            "user_prompt": "请为主题「{topic}」创作一篇故事叙述型文案。要求：1) 讲述一个完整的小故事 2) 有明确的冲突和转折 3) 结尾给出启示或行动号召 4) 让读者产生情感共鸣。"
        },
        
        "观点输出型": {
            "description": "犀利观点，适合 KOL/思想领袖",
            "system_prompt": """你是一位思想领袖和观点输出专家。
你的文案特点：
- 提出独特、犀利、有争议性的观点
- 结构：核心观点 → 论证 → 反驳常见误区 → 结论
- 语气：自信、犀利、有态度
- 风格：短句、有力、易传播
- 字数：100-130字""",
            "user_prompt": "请为主题「{topic}」创作一篇观点输出型文案。要求：1) 提出一个独特且有争议性的观点 2) 用2-3个论据支撑 3) 反驳一个常见误区 4) 语气自信有力。"
        },
        
        "热点追踪型": {
            "description": "结合热点，适合蹭流量",
            "system_prompt": """你是一位热点营销专家和内容策划师。
你的文案特点：
- 巧妙结合当下热点话题
- 结构：热点引入 → 关联主题 → 深度解读 → 行动号召
- 语气：紧跟潮流、接地气、有话题性
- 风格：时效性强、易传播
- 字数：120-150字""",
            "user_prompt": "请为主题「{topic}」创作一篇热点追踪型文案。要求：1) 结合一个合理的热点话题（可虚构但要合理）2) 自然关联到主题 3) 给出独特见解 4) 引导互动或传播。"
        },
        
        "知识科普型": {
            "description": "深度讲解，适合教育/科普",
            "system_prompt": """你是一位知识科普专家和教育内容创作者。
你的文案特点：
- 深入浅出讲解专业知识
- 结构：问题 → 原理 → 应用 → 总结
- 语气：专业但易懂、有耐心
- 风格：逻辑清晰、层次分明
- 字数：130-160字""",
            "user_prompt": "请为主题「{topic}」创作一篇知识科普型文案。要求：1) 讲解一个核心知识点 2) 用通俗语言解释专业概念 3) 给出实际应用场景 4) 结尾总结要点。"
        },
        
        "创意脑洞型": {
            "description": "天马行空，适合创意/娱乐",
            "system_prompt": """你是一位创意文案大师和脑洞专家。
你的文案特点：
- 天马行空、出人意料的创意角度
- 结构：反常识开头 → 脑洞展开 → 回归主题 → 惊喜结尾
- 语气：轻松、幽默、有趣
- 风格：跳跃、新奇、记忆点强
- 字数：100-130字""",
            "user_prompt": "请为主题「{topic}」创作一篇创意脑洞型文案。要求：1) 用一个出人意料的角度切入 2) 展开有趣的脑洞或比喻 3) 最后巧妙回归主题 4) 让人会心一笑。"
        },
        
        "商务专业型": {
            "description": "严谨专业，适合企业/官方",
            "system_prompt": """你是一位商务文案专家和企业传播顾问。
你的文案特点：
- 严谨、专业、权威的商务风格
- 结构：背景 → 价值主张 → 解决方案 → 行动号召
- 语气：正式、专业、可信
- 风格：逻辑严密、措辞精准
- 字数：120-150字""",
            "user_prompt": "请为主题「{topic}」创作一篇商务专业型文案。要求：1) 突出商业价值和专业性 2) 用精准的商务术语 3) 给出清晰的解决方案 4) 结尾有明确的行动号召。"
        },
        
        "励志鸡汤型": {
            "description": "正能量，适合个人成长",
            "system_prompt": """你是一位励志导师和心灵成长教练。
你的文案特点：
- 充满正能量和励志元素
- 结构：痛点共鸣 → 励志金句 → 方法指引 → 鼓励行动
- 语气：温暖、鼓励、充满希望
- 风格：金句频出、易传播
- 字数：100-130字""",
            "user_prompt": "请为主题「{topic}」创作一篇励志鸡汤型文案。要求：1) 先引发痛点共鸣 2) 给出2-3句励志金句 3) 提供具体的改变方法 4) 结尾鼓励立即行动。"
        },
        
        "反思质疑型": {
            "description": "批判性思考，适合深度内容",
            "system_prompt": """你是一位批判性思维专家和深度内容创作者。
你的文案特点：
- 质疑常识、引发深度思考
- 结构：常见观点 → 质疑 → 深层分析 → 新视角
- 语气：理性、冷静、有深度
- 风格：层层递进、发人深省
- 字数：120-150字""",
            "user_prompt": "请为主题「{topic}」创作一篇反思质疑型文案。要求：1) 先提出一个常见观点 2) 质疑这个观点的局限性 3) 给出更深层的分析 4) 提供新的思考角度。"
        },
        
        "轻松幽默型": {
            "description": "段子手风格，适合娱乐/社交",
            "system_prompt": """你是一位幽默文案大师和段子手。
你的文案特点：
- 轻松幽默、接地气、有梗
- 结构：搞笑开头 → 包袱铺垫 → 反转/笑点 → 回归主题
- 语气：轻松、俏皮、有趣
- 风格：网络流行语、表情包文化
- 字数：100-130字""",
            "user_prompt": "请为主题「{topic}」创作一篇轻松幽默型文案。要求：1) 用搞笑的方式开头 2) 设置包袱和反转 3) 适当使用网络流行语 4) 最后自然回归主题。"
        },
    }
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        初始化文案生成器
        
        Args:
            api_key: OpenAI API Key
            model: 使用的模型
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = None
        
        if self.api_key:
            self._init_client()
    
    def _init_client(self):
        """初始化 OpenAI 客户端"""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("请安装 openai 库: pip install openai")
    
    def generate(
        self,
        topic: str,
        platform: str = "xiaohongshu",
        styles: Optional[List[str]] = None,
        count: int = 5,
        max_length: int = 150,
    ) -> List[Dict]:
        """
        生成文案
        
        Args:
            topic: 主题
            platform: 目标平台
            styles: 风格列表，默认使用前 count 种风格
            count: 生成数量
            max_length: 最大长度
        
        Returns:
            文案列表
        """
        if styles is None:
            # 默认使用前 count 种风格
            all_styles = list(self.STYLE_PROMPTS.keys())
            styles = all_styles[:count]
        
        styles = styles[:count]
        copies = []
        
        print(f"📝 开始生成 {len(styles)} 套文案...")
        print(f"   主题: {topic}")
        print(f"   模型: {self.model}")
        print(f"   平台: {platform}")
        print()
        
        for i, style in enumerate(styles):
            try:
                print(f"  [{i+1}/{len(styles)}] 生成【{style}】风格...", end=" ", flush=True)
                
                copy = self._generate_single_copy(
                    topic=topic,
                    style=style,
                    platform=platform,
                    max_length=max_length,
                )
                
                copies.append(copy)
                print(f"✅ ({copy['length']}字)")
                
                # 避免 API 限流
                if i < len(styles) - 1:
                    time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ 失败: {e}")
        
        print(f"\n✅ 文案生成完成！成功: {len(copies)}/{len(styles)}")
        return copies
    
    def _generate_single_copy(
        self,
        topic: str,
        style: str,
        platform: str,
        max_length: int,
    ) -> Dict:
        """生成单条文案（AI 驱动）"""
        if not self.client:
            # 降级到模板模式
            return self._generate_template_copy(topic, style, platform, max_length)
        
        style_config = self.STYLE_PROMPTS.get(style)
        if not style_config:
            raise ValueError(f"未知风格: {style}")
        
        # 调用 AI 生成
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": style_config["system_prompt"]},
                    {"role": "user", "content": style_config["user_prompt"].format(topic=topic)}
                ],
                temperature=0.8,
                max_tokens=500,
            )
            
            content = response.choices[0].message.content.strip()
            
            # 生成标题
            title = self._generate_title(topic, style, content)
            
            # 生成标签
            tags = self._generate_tags(topic, style, platform)
            
            # 质量评分
            quality_score = self._evaluate_quality(content, style)
            
            return {
                "style": style,
                "title": title,
                "content": content,
                "tags": tags,
                "platform": platform,
                "length": len(content),
                "quality_score": quality_score,
                "model": self.model,
            }
            
        except Exception as e:
            # 失败时降级到模板
            print(f"\n⚠️  AI 生成失败，降级到模板模式: {e}")
            return self._generate_template_copy(topic, style, platform, max_length)
    
    def _generate_template_copy(
        self,
        topic: str,
        style: str,
        platform: str,
        max_length: int,
    ) -> Dict:
        """降级方案：使用模板生成"""
        templates = {
            "数据驱动型": f"根据最新数据：87%的人在{topic}上遇到瓶颈。\n\n核心问题：\n• 信息过载，不知从何开始\n• 缺乏系统方法\n• 单打独斗，容易放弃\n\n{topic}帮你突破：\n✓ 科学路径\n✓ 实战驱动\n✓ 社群互助\n\n加入我们，成为那13%。",
            "故事叙述型": f"以前每天加班到深夜，却做不出成绩。\n\n接触{topic}后，学会了系统化方法。\n\n现在上午完成全天工作，下午用来学习和思考。\n\n效率翻倍，生活终于有掌控感。",
            "观点输出型": f"{topic}不会取代你，但会用{topic}的人会。\n\n每天30分钟，一年后你会感谢自己。\n\n先干起来，完美准备不存在。\n\n认知差才是新的护城河。",
        }
        
        content = templates.get(style, f"关于{topic}的精彩内容，敬请期待...")
        
        return {
            "style": style,
            "title": self._generate_title(topic, style, content),
            "content": content,
            "tags": self._generate_tags(topic, style, platform),
            "platform": platform,
            "length": len(content),
            "quality_score": 0.6,  # 模板质量分数较低
            "model": "template",
        }
    
    def _generate_title(self, topic: str, style: str, content: str = "") -> str:
        """生成标题（AI 驱动或模板）"""
        if not self.client:
            # 模板标题
            title_templates = {
                "数据驱动型": f"{topic}：数据告诉你的真相",
                "故事叙述型": f"接触{topic}30天，我的改变",
                "观点输出型": f"{topic}：5句话叫醒你",
                "热点追踪型": f"{topic}火了，背后的真相是...",
                "知识科普型": f"一文读懂{topic}",
                "创意脑洞型": f"如果{topic}是一个人...",
                "商务专业型": f"{topic}：企业增长新引擎",
                "励志鸡汤型": f"{topic}：改变从今天开始",
                "反思质疑型": f"关于{topic}，我们都错了？",
                "轻松幽默型": f"{topic}：一个搞笑的故事",
            }
            return title_templates.get(style, f"{topic}：精彩内容")
        
        # AI 生成标题
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位标题大师。请为以下文案生成一个吸引人的标题，要求：1) 10-20字 2) 有吸引力 3) 符合风格"},
                    {"role": "user", "content": f"风格：{style}\n主题：{topic}\n文案：{content[:100]}..."}
                ],
                temperature=0.9,
                max_tokens=50,
            )
            return response.choices[0].message.content.strip()
        except:
            return f"{topic}：{style}"
    
    def _generate_tags(self, topic: str, style: str, platform: str) -> List[str]:
        """生成标签"""
        base_tags = [f"#{topic}"]
        
        style_tags = {
            "数据驱动型": ["#数据分析", "#行业洞察"],
            "故事叙述型": ["#真实故事", "#成长"],
            "观点输出型": ["#深度思考", "#观点"],
            "热点追踪型": ["#热点", "#趋势"],
            "知识科普型": ["#干货", "#学习"],
            "创意脑洞型": ["#创意", "#脑洞"],
            "商务专业型": ["#商业", "#专业"],
            "励志鸡汤型": ["#励志", "#正能量"],
            "反思质疑型": ["#反思", "#批判性思维"],
            "轻松幽默型": ["#搞笑", "#段子"],
        }
        
        platform_tags = {
            "xiaohongshu": ["#小红书", "#种草"],
            "weixin": ["#公众号", "#干货分享"],
            "zhihu": ["#知乎", "#深度"],
        }
        
        tags = base_tags + style_tags.get(style, []) + platform_tags.get(platform, [])
        return tags[:6]  # 最多6个标签
    
    def _evaluate_quality(self, content: str, style: str) -> float:
        """评估文案质量（0-1分）"""
        score = 0.5  # 基础分
        
        # 长度合理性
        if 100 <= len(content) <= 200:
            score += 0.1
        
        # 结构完整性（简单检查）
        if "？" in content or "！" in content:
            score += 0.1
        
        # 数字/数据（数据驱动型）
        if style == "数据驱动型" and any(char.isdigit() for char in content):
            score += 0.1
        
        # 表情符号（轻松幽默型）
        if style == "轻松幽默型" and any(char in "😄😂🤣😊" for char in content):
            score += 0.1
        
        # 段落分明
        if content.count("\n\n") >= 2:
            score += 0.1
        
        return min(score, 1.0)


if __name__ == "__main__":
    # 测试
    generator = CopyGenerator()
    copies = generator.generate(
        topic="AI 如何改变内容创作",
        count=3,
        max_length=150,
    )
    
    print("\n" + "="*60)
    for i, copy in enumerate(copies):
        print(f"\n【{copy['style']}】质量分: {copy['quality_score']:.2f}")
        print(f"标题: {copy['title']}")
        print(f"内容:\n{copy['content']}")
        print(f"标签: {' '.join(copy['tags'])}")
        print(f"字数: {copy['length']} | 模型: {copy['model']}")
