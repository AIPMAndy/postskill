#!/usr/bin/env python3
"""
PostSkill - 文案生成模块
基于主题生成多种风格的社交媒体文案
"""

import json
import os
from typing import Dict, List, Optional


class CopyGenerator:
    """文案生成器"""
    
    # 文案风格定义
    STYLES = {
        "干货型": {
            "description": "知识点密集，实用性强，信息量大",
            "tone": "专业、权威、实用",
            "structure": "问题-解决方案-步骤-总结",
        },
        "故事型": {
            "description": "叙事驱动，情感共鸣，引人入胜",
            "tone": "亲切、真实、有代入感",
            "structure": "背景-冲突-转折-结局-启示",
        },
        "金句型": {
            "description": "短句有力，易于传播，记忆点强",
            "tone": "简洁、深刻、有冲击力",
            "structure": "核心观点+解释/延展",
        },
        "数据型": {
            "description": "数据支撑，权威可信，说服力强",
            "tone": "客观、专业、有据",
            "structure": "数据呈现-分析-结论-建议",
        },
        "对比型": {
            "description": "前后对比，效果突出，差异明显",
            "tone": "直观、对比、清晰",
            "structure": "Before-After-差异点-方法",
        },
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化文案生成器
        
        Args:
            api_key: API Key（可选，用于高级生成功能）
        """
        self.api_key = api_key
    
    def generate(
        self,
        topic: str,
        platform: str = "xiaohongshu",
        styles: Optional[List[str]] = None,
        count: int = 3,
        max_length: int = 150,
    ) -> List[Dict]:
        """
        生成文案
        
        Args:
            topic: 主题
            platform: 目标平台
            styles: 风格列表，默认使用3种风格
            count: 生成数量
            max_length: 最大长度
        
        Returns:
            文案列表
        """
        if styles is None:
            styles = ["干货型", "故事型", "金句型"][:count]
        
        styles = styles[:count]
        copies = []
        
        print(f"📝 开始生成 {len(styles)} 套文案...")
        
        for i, style in enumerate(styles):
            try:
                print(f"  [{i+1}/{len(styles)}] 生成【{style}】风格文案...", end=" ")
                
                copy = self._generate_single_copy(
                    topic=topic,
                    style=style,
                    platform=platform,
                    max_length=max_length,
                )
                
                copies.append(copy)
                print("✅")
                
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
        """生成单条文案（模板版）"""
        style_config = self.STYLES.get(style, self.STYLES["干货型"])
        
        # 根据风格生成不同文案
        templates = {
            "干货型": self._generate_ganhuo_template,
            "故事型": self._generate_gushi_template,
            "金句型": self._generate_jinju_template,
            "数据型": self._generate_shuju_template,
            "对比型": self._generate_duibi_template,
        }
        
        template_func = templates.get(style, self._generate_ganhuo_template)
        content = template_func(topic, max_length)
        
        # 生成标题
        title = self._generate_title(topic, style)
        
        # 生成标签
        tags = self._generate_tags(topic, style)
        
        return {
            "style": style,
            "title": title,
            "content": content,
            "tags": tags,
            "platform": platform,
            "length": len(content),
        }
    
    def _generate_ganhuo_template(self, topic: str, max_length: int) -> str:
        """干货型模板"""
        return f"""想学{topic}但不知从何开始？

{topic}帮你：
❶ 破除信息焦虑，聚焦核心技能
❷ 实战项目驱动，边做边学
❸ 同频伙伴同行，告别单打独斗

30天，从{topic}小白到能独立解决问题。"""
    
    def _generate_gushi_template(self, topic: str, max_length: int) -> str:
        """故事型模板"""
        return f"""以前每天加班到深夜，却做不出成绩。

接触{topic}后，学会了用AI做信息筛选、内容初稿、决策辅助。

现在上午10点完成全天工作，下午用来学习和思考。

效率翻倍，生活终于有掌控感。"""
    
    def _generate_jinju_template(self, topic: str, max_length: int) -> str:
        """金句型模板"""
        return f"""01. {topic}不会取代你，但会用{topic}的人会
02. 每天30分钟，一年后你会感谢自己
03. 先干起来，完美准备不存在
04. 认知差才是新的护城河
05. 一个人+{topic}的力量是无限的

{topic}时代，一起成长。"""
    
    def _generate_shuju_template(self, topic: str, max_length: int) -> str:
        """数据型模板"""
        return f"""根据最新调研：
• 87%的{topic}学习者3个月内放弃
• 只有13%的人掌握了核心方法

{topic}帮你突破这个魔咒：
✓ 科学的学习路径
✓ 实战项目驱动
✓ 社群互助监督

加入我们，成为那13%。"""
    
    def _generate_duibi_template(self, topic: str, max_length: int) -> str:
        """对比型模板"""
        return f"""学习{topic}前：
❌ 信息焦虑，不知从何开始
❌ 单打独斗，容易放弃
❌ 学了就忘，没有实践

学习{topic}后：
✅ 聚焦核心，高效学习
✅ 同频伙伴，互相激励
✅ 项目实战，即学即用

30天，见证改变。"""
    
    def _generate_title(self, topic: str, style: str) -> str:
        """生成标题"""
        titles = {
            "干货型": f"{topic}：3步开启你的成长之路",
            "故事型": f"接触{topic}30天，我告别了低效加班",
            "金句型": f"{topic}：5句话叫醒沉睡的你",
            "数据型": f"87%的人学{topic}都错了，你是那13%吗？",
            "对比型": f"学习{topic}前后，我发生了哪些改变？",
        }
        return titles.get(style, f"{topic}：开启新篇章")
    
    def _generate_tags(self, topic: str, style: str) -> List[str]:
        """生成标签"""
        base_tags = [f"#{topic}", "#个人成长"]
        style_tags = {
            "干货型": ["#干货分享", "#技能提升"],
            "故事型": ["#真实故事", "#职场成长"],
            "金句型": ["#金句", "#深度思考"],
            "数据型": ["#数据分析", "#行业洞察"],
            "对比型": ["#前后对比", "#改变"],
        }
        return base_tags + style_tags.get(style, [])


if __name__ == "__main__":
    # 测试
    generator = CopyGenerator()
    copies = generator.generate(
        topic="AI醒觉社",
        count=3,
        max_length=150,
    )
    
    print("\n" + "="*50)
    for i, copy in enumerate(copies):
        print(f"\n【{copy['style']}】")
        print(f"标题: {copy['title']}")
        print(f"内容:\n{copy['content']}")
        print(f"标签: {' '.join(copy['tags'])}")
        print(f"字数: {copy['length']}")