#!/usr/bin/env python3
"""
PostSkill - 对抗式内容生成系统
三 Agent 协作：生成者 → 批判者 → 评估者 → 迭代优化
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import time


@dataclass
class GenerationResult:
    """生成结果"""
    content: str
    version: int
    generator_reasoning: str
    critic_feedback: Optional[str] = None
    evaluator_score: Optional[float] = None
    evaluator_reasoning: Optional[str] = None


class AdversarialContentGenerator:
    """对抗式内容生成器 - 三 Agent 协作"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        初始化对抗式生成器
        
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
    
    def generate_with_adversarial(
        self,
        topic: str,
        style: str,
        style_prompt: Dict,
        max_iterations: int = 3,
        target_score: float = 0.85,
        verbose: bool = True,
    ) -> GenerationResult:
        """
        对抗式生成内容
        
        Args:
            topic: 主题
            style: 风格
            style_prompt: 风格 Prompt 配置
            max_iterations: 最大迭代次数
            target_score: 目标分数（达到后停止）
            verbose: 是否显示详细过程
        
        Returns:
            最终生成结果
        """
        if not self.client:
            raise RuntimeError("OpenAI 客户端未初始化")
        
        if verbose:
            print(f"\n🎯 对抗式生成【{style}】")
            print(f"   主题: {topic}")
            print(f"   目标分数: {target_score}")
            print(f"   最大迭代: {max_iterations}")
            print()
        
        best_result = None
        
        for iteration in range(1, max_iterations + 1):
            if verbose:
                print(f"{'='*60}")
                print(f"第 {iteration}/{max_iterations} 轮")
                print(f"{'='*60}\n")
            
            # 1. 生成者：生成内容
            if verbose:
                print("🤖 生成者：创作内容...", end=" ", flush=True)
            
            content, generator_reasoning = self._generator_agent(
                topic=topic,
                style_prompt=style_prompt,
                previous_feedback=best_result.critic_feedback if best_result else None,
            )
            
            if verbose:
                print("✅")
                print(f"   内容: {content[:50]}...")
                print(f"   推理: {generator_reasoning[:80]}...")
            
            # 2. 批判者：找出问题
            if verbose:
                print("\n🔍 批判者：分析问题...", end=" ", flush=True)
            
            critic_feedback, issues = self._critic_agent(
                content=content,
                style=style,
                topic=topic,
            )
            
            if verbose:
                print("✅")
                print(f"   反馈: {critic_feedback[:80]}...")
                print(f"   问题数: {len(issues)}")
            
            # 3. 评估者：打分
            if verbose:
                print("\n⚖️  评估者：质量评分...", end=" ", flush=True)
            
            score, evaluator_reasoning = self._evaluator_agent(
                content=content,
                style=style,
                topic=topic,
                critic_feedback=critic_feedback,
            )
            
            if verbose:
                print("✅")
                print(f"   分数: {score:.2f}/1.00")
                print(f"   评价: {evaluator_reasoning[:80]}...")
            
            # 记录结果
            result = GenerationResult(
                content=content,
                version=iteration,
                generator_reasoning=generator_reasoning,
                critic_feedback=critic_feedback,
                evaluator_score=score,
                evaluator_reasoning=evaluator_reasoning,
            )
            
            # 更新最佳结果
            if best_result is None or score > best_result.evaluator_score:
                best_result = result
                if verbose:
                    print(f"\n✨ 新的最佳结果！分数: {score:.2f}")
            
            # 检查是否达到目标
            if score >= target_score:
                if verbose:
                    print(f"\n🎉 达到目标分数 {target_score}，停止迭代")
                break
            
            if verbose:
                print()
            
            # 避免 API 限流
            if iteration < max_iterations:
                time.sleep(1)
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"✅ 对抗式生成完成")
            print(f"{'='*60}")
            print(f"最佳版本: v{best_result.version}")
            print(f"最终分数: {best_result.evaluator_score:.2f}/1.00")
            print(f"迭代次数: {iteration}/{max_iterations}")
            print()
        
        return best_result
    
    def generate(
        self,
        topic: str,
        style: str,
        system_prompt: str,
        user_prompt: str,
        max_iterations: int = 3,
    ) -> Dict:
        """
        对抗式生成（简化接口）
        
        Args:
            topic: 主题
            style: 风格
            system_prompt: 系统 Prompt
            user_prompt: 用户 Prompt 模板
            max_iterations: 最大迭代次数
        
        Returns:
            {"content": str, "final_score": float}
        """
        style_prompt = {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
        }
        
        result = self.generate_with_adversarial(
            topic=topic,
            style=style,
            style_prompt=style_prompt,
            max_iterations=max_iterations,
            verbose=True,
        )
        
        return {
            "content": result.content,
            "final_score": result.evaluator_score or 0.8,
        }
    
    def _generator_agent(
        self,
        topic: str,
        style_prompt: Dict,
        previous_feedback: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        生成者 Agent：创作内容
        
        Returns:
            (content, reasoning)
        """
        system_prompt = style_prompt["system_prompt"]
        user_prompt = style_prompt["user_prompt"].format(topic=topic)
        
        # 如果有上一轮反馈，加入 prompt
        if previous_feedback:
            user_prompt += f"\n\n【上一轮批判反馈】\n{previous_feedback}\n\n请根据反馈改进内容。"
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=500,
        )
        
        content = response.choices[0].message.content.strip()
        
        # 生成推理（为什么这样写）
        reasoning_prompt = f"你刚才生成了这段文案：\n\n{content}\n\n请用一句话解释你的创作思路。"
        
        reasoning_response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一位内容创作专家。"},
                {"role": "user", "content": reasoning_prompt}
            ],
            temperature=0.3,
            max_tokens=100,
        )
        
        reasoning = reasoning_response.choices[0].message.content.strip()
        
        return content, reasoning
    
    def _critic_agent(
        self,
        content: str,
        style: str,
        topic: str,
    ) -> Tuple[str, List[str]]:
        """
        批判者 Agent：找出问题
        
        Returns:
            (feedback, issues)
        """
        critic_system_prompt = """你是一位严格的内容批评家和质量审核专家。

你的职责：
- 用批判性思维审视内容
- 找出所有问题和不足
- 给出具体的改进建议
- 不要客气，要严格

评审维度：
1. 内容质量：是否有价值、有深度
2. 结构完整：是否逻辑清晰、层次分明
3. 语言表达：是否流畅、有感染力
4. 风格匹配：是否符合目标风格
5. 吸引力：是否能抓住读者注意力"""
        
        critic_user_prompt = f"""请批判性审视以下文案：

【主题】{topic}
【风格】{style}
【内容】
{content}

请指出所有问题，并给出改进建议。格式：
1. 问题1：xxx
   改进：xxx
2. 问题2：xxx
   改进：xxx
..."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": critic_system_prompt},
                {"role": "user", "content": critic_user_prompt}
            ],
            temperature=0.5,
            max_tokens=500,
        )
        
        feedback = response.choices[0].message.content.strip()
        
        # 提取问题列表
        issues = []
        for line in feedback.split('\n'):
            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                issues.append(line.strip())
        
        return feedback, issues
    
    def _evaluator_agent(
        self,
        content: str,
        style: str,
        topic: str,
        critic_feedback: str,
    ) -> Tuple[float, str]:
        """
        评估者 Agent：客观打分
        
        Returns:
            (score, reasoning)
        """
        evaluator_system_prompt = """你是一位客观公正的内容质量评估专家。

你的职责：
- 综合考虑内容质量、批判反馈、风格匹配度
- 给出 0-1 之间的客观分数
- 解释评分理由

评分标准：
- 0.9-1.0：优秀，几乎无可挑剔
- 0.8-0.9：良好，有小瑕疵但整体优秀
- 0.7-0.8：中等偏上，有明显改进空间
- 0.6-0.7：及格，问题较多
- 0.0-0.6：不及格，需要大幅改进"""
        
        evaluator_user_prompt = f"""请评估以下文案的质量：

【主题】{topic}
【风格】{style}
【内容】
{content}

【批判者反馈】
{critic_feedback}

请给出 0-1 之间的分数，并解释理由。格式：
分数：0.xx
理由：xxx"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": evaluator_system_prompt},
                {"role": "user", "content": evaluator_user_prompt}
            ],
            temperature=0.3,
            max_tokens=300,
        )
        
        result = response.choices[0].message.content.strip()
        
        # 提取分数
        score = 0.5  # 默认分数
        reasoning = result
        
        for line in result.split('\n'):
            if '分数' in line or 'Score' in line.lower():
                # 提取数字
                import re
                numbers = re.findall(r'0\.\d+', line)
                if numbers:
                    score = float(numbers[0])
                    break
        
        return score, reasoning


if __name__ == "__main__":
    # 测试
    generator = AdversarialContentGenerator()
    
    style_prompt = {
        "system_prompt": """你是一位数据分析专家和内容营销专家。
你的文案特点：
- 必须包含具体数据/百分比/统计结果
- 用数据支撑观点，增强说服力
- 结构：数据呈现 → 分析 → 结论 → 行动建议
- 语气：客观、专业、权威
- 字数：120-150字""",
        "user_prompt": "请为主题「{topic}」创作一篇数据驱动型文案。要求：1) 包含至少2个具体数据点 2) 数据真实可信或合理推测 3) 突出数据背后的洞察 4) 给出明确的行动建议。"
    }
    
    result = generator.generate_with_adversarial(
        topic="AI 如何改变内容创作",
        style="数据驱动型",
        style_prompt=style_prompt,
        max_iterations=3,
        target_score=0.85,
        verbose=True,
    )
    
    print("\n" + "="*60)
    print("最终结果")
    print("="*60)
    print(f"\n版本: v{result.version}")
    print(f"分数: {result.evaluator_score:.2f}/1.00")
    print(f"\n内容:\n{result.content}")
    print(f"\n生成者推理:\n{result.generator_reasoning}")
    print(f"\n批判者反馈:\n{result.critic_feedback}")
    print(f"\n评估者评价:\n{result.evaluator_reasoning}")
