#!/usr/bin/env python3
"""
PostSkill - Self-Evolution 质量反馈系统
学习用户反馈，自动优化生成质量
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class QualityFeedbackSystem:
    """质量反馈系统 - Self-Evolution 核心"""
    
    def __init__(self, feedback_dir: str = "./feedback"):
        """
        初始化反馈系统
        
        Args:
            feedback_dir: 反馈数据存储目录
        """
        self.feedback_dir = Path(feedback_dir)
        self.feedback_dir.mkdir(parents=True, exist_ok=True)
        
        self.feedback_file = self.feedback_dir / "feedback.jsonl"
        self.stats_file = self.feedback_dir / "stats.json"
    
    def record_feedback(
        self,
        copy_id: str,
        style: str,
        topic: str,
        content: str,
        rating: int,
        comment: Optional[str] = None,
        issues: Optional[List[str]] = None,
    ) -> Dict:
        """
        记录用户反馈
        
        Args:
            copy_id: 文案 ID
            style: 风格
            topic: 主题
            content: 内容
            rating: 评分（1-5）
            comment: 评论
            issues: 问题列表
        
        Returns:
            反馈记录
        """
        feedback = {
            "id": copy_id,
            "style": style,
            "topic": topic,
            "content": content,
            "rating": rating,
            "comment": comment,
            "issues": issues or [],
            "timestamp": datetime.now().isoformat(),
        }
        
        # 追加到 JSONL 文件
        with open(self.feedback_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(feedback, ensure_ascii=False) + '\n')
        
        # 更新统计
        self._update_stats()
        
        return feedback
    
    def get_style_stats(self, style: str) -> Dict:
        """获取某个风格的统计数据"""
        stats = self._load_stats()
        return stats.get("by_style", {}).get(style, {
            "total": 0,
            "avg_rating": 0.0,
            "common_issues": [],
        })
    
    def get_improvement_suggestions(self, style: str) -> List[str]:
        """
        基于反馈数据生成改进建议
        
        Args:
            style: 风格
        
        Returns:
            改进建议列表
        """
        stats = self.get_style_stats(style)
        suggestions = []
        
        avg_rating = stats.get("avg_rating", 0)
        common_issues = stats.get("common_issues", [])
        
        # 基于平均评分
        if avg_rating < 3.0:
            suggestions.append(f"⚠️  {style} 平均评分较低（{avg_rating:.1f}/5.0），需要优化")
        
        # 基于常见问题
        for issue, count in common_issues[:3]:
            suggestions.append(f"🔧 常见问题：{issue}（出现 {count} 次）")
        
        # 基于历史数据生成具体建议
        if "内容太短" in [i[0] for i in common_issues]:
            suggestions.append("💡 建议：增加内容长度，目标 120-150 字")
        
        if "缺少数据" in [i[0] for i in common_issues]:
            suggestions.append("💡 建议：添加具体数据支撑观点")
        
        if "不够吸引人" in [i[0] for i in common_issues]:
            suggestions.append("💡 建议：优化开头，使用更吸引人的钩子")
        
        return suggestions
    
    def _update_stats(self):
        """更新统计数据"""
        feedbacks = self._load_all_feedbacks()
        
        if not feedbacks:
            return
        
        # 按风格统计
        by_style = {}
        for fb in feedbacks:
            style = fb["style"]
            if style not in by_style:
                by_style[style] = {
                    "total": 0,
                    "ratings": [],
                    "issues": [],
                }
            
            by_style[style]["total"] += 1
            by_style[style]["ratings"].append(fb["rating"])
            by_style[style]["issues"].extend(fb.get("issues", []))
        
        # 计算平均分和常见问题
        for style, data in by_style.items():
            data["avg_rating"] = sum(data["ratings"]) / len(data["ratings"])
            
            # 统计问题频率
            issue_counts = {}
            for issue in data["issues"]:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
            
            # 排序
            data["common_issues"] = sorted(
                issue_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            # 清理临时数据
            del data["ratings"]
            del data["issues"]
        
        # 全局统计
        stats = {
            "total_feedbacks": len(feedbacks),
            "avg_rating": sum(fb["rating"] for fb in feedbacks) / len(feedbacks),
            "by_style": by_style,
            "last_updated": datetime.now().isoformat(),
        }
        
        # 保存
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    
    def _load_all_feedbacks(self) -> List[Dict]:
        """加载所有反馈"""
        if not self.feedback_file.exists():
            return []
        
        feedbacks = []
        with open(self.feedback_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    feedbacks.append(json.loads(line))
        
        return feedbacks
    
    def _load_stats(self) -> Dict:
        """加载统计数据"""
        if not self.stats_file.exists():
            return {}
        
        with open(self.stats_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_report(self) -> str:
        """生成质量报告"""
        stats = self._load_stats()
        
        if not stats:
            return "暂无反馈数据"
        
        report = []
        report.append("=" * 60)
        report.append("PostSkill 质量报告")
        report.append("=" * 60)
        report.append(f"\n总反馈数：{stats['total_feedbacks']}")
        report.append(f"平均评分：{stats['avg_rating']:.2f}/5.0")
        report.append(f"更新时间：{stats['last_updated']}")
        
        report.append("\n" + "-" * 60)
        report.append("各风格表现：")
        report.append("-" * 60)
        
        for style, data in stats.get("by_style", {}).items():
            report.append(f"\n【{style}】")
            report.append(f"  反馈数：{data['total']}")
            report.append(f"  平均分：{data['avg_rating']:.2f}/5.0")
            
            if data.get("common_issues"):
                report.append(f"  常见问题：")
                for issue, count in data["common_issues"][:3]:
                    report.append(f"    • {issue}（{count} 次）")
        
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)


if __name__ == "__main__":
    # 测试
    system = QualityFeedbackSystem()
    
    # 模拟反馈
    system.record_feedback(
        copy_id="test-001",
        style="数据驱动型",
        topic="AI 创作",
        content="测试内容...",
        rating=4,
        comment="不错，但数据可以更多",
        issues=["缺少数据"],
    )
    
    system.record_feedback(
        copy_id="test-002",
        style="数据驱动型",
        topic="AI 创作",
        content="测试内容...",
        rating=3,
        issues=["内容太短", "缺少数据"],
    )
    
    # 生成报告
    print(system.generate_report())
    
    # 获取改进建议
    print("\n改进建议：")
    for suggestion in system.get_improvement_suggestions("数据驱动型"):
        print(f"  {suggestion}")
