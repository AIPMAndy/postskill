#!/usr/bin/env python3
"""
PostSkill - 飞书文档创建模块
自动创建图文对照的飞书文档
"""

import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class FeishuDocCreator:
    """飞书文档创建器"""
    
    def create_document(
        self,
        title: str,
        copies: List[Dict],
        images: List[Dict],
        output_dir: str = "./output",
    ) -> Dict:
        """创建飞书文档（生成Markdown内容）"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        markdown_content = self._generate_markdown(title, copies, images)
        
        markdown_file = output_path / f"{title.replace(' ', '_')}.md"
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return {
            "title": title,
            "copies_count": len(copies),
            "images_count": len(images),
            "markdown_file": str(markdown_file),
            "markdown_content": markdown_content,
        }
    
    def _generate_markdown(self, title: str, copies: List[Dict], images: List[Dict]) -> str:
        """生成Markdown内容"""
        lines = [
            f"# {title}",
            "",
            f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
        ]
        
        for i, copy in enumerate(copies):
            style = copy.get("style", f"第{i+1}篇")
            lines.append(f"{i+1}. [{style}](#section-{i+1})")
        
        lines.extend(["", "---", ""])
        
        for i, copy in enumerate(copies):
            style = copy.get("style", "")
            title_text = copy.get("title", "")
            content = copy.get("content", "")
            tags = copy.get("tags", [])
            
            lines.extend([
                f"### {i+1}. {style} <a name='section-{i+1}'></a>",
                "",
                f"**标题:** {title_text}",
                "",
            ])
            
            if i < len(images):
                image = images[i]
                lines.extend([
                    "**配图:**",
                    "",
                    f"![配图]({image.get('local_path', '')})",
                    "",
                ])
            
            lines.extend([
                "**文案内容:**",
                "",
                content,
                "",
                f"**话题标签:** {' '.join(tags)}",
                "",
                "---",
                "",
            ])
        
        return "\n".join(lines)
