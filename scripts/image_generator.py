#!/usr/bin/env python3
"""
PostSkill - 图片生成模块
调用 PonyFlash 为文案生成配套图片
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
import time


class ImageGenerator:
    """图片生成器 - 优化版"""
    
    # 10 种风格的专业图片 Prompt
    STYLE_PROMPTS = {
        "数据驱动型": {
            "base": "professional data visualization, modern business analytics dashboard",
            "style": "clean minimalist design, blue and white color scheme, charts and graphs",
            "mood": "professional, trustworthy, authoritative",
            "elements": "data charts, statistics, infographics, business icons",
        },
        
        "故事叙述型": {
            "base": "emotional storytelling visual, warm and healing atmosphere",
            "style": "cinematic lighting, soft focus, warm color palette",
            "mood": "inspiring, hopeful, touching",
            "elements": "sunrise, journey, transformation, human connection",
        },
        
        "观点输出型": {
            "base": "bold statement visual, strong typography concept",
            "style": "high contrast, dramatic lighting, modern minimalist",
            "mood": "confident, powerful, thought-provoking",
            "elements": "abstract shapes, bold colors, geometric patterns",
        },
        
        "热点追踪型": {
            "base": "trending topic visual, social media style",
            "style": "vibrant colors, dynamic composition, modern digital art",
            "mood": "energetic, trendy, attention-grabbing",
            "elements": "social media icons, trending symbols, modern tech",
        },
        
        "知识科普型": {
            "base": "educational illustration, knowledge sharing concept",
            "style": "clean infographic style, organized layout, clear hierarchy",
            "mood": "educational, clear, approachable",
            "elements": "books, lightbulb, brain, learning symbols",
        },
        
        "创意脑洞型": {
            "base": "creative surreal concept, imaginative visual",
            "style": "surrealism, vibrant colors, unexpected combinations",
            "mood": "playful, surprising, imaginative",
            "elements": "surreal objects, creative metaphors, fantasy elements",
        },
        
        "商务专业型": {
            "base": "corporate professional visual, business concept",
            "style": "sleek modern design, navy blue and gold, premium feel",
            "mood": "professional, trustworthy, premium",
            "elements": "office, handshake, growth chart, corporate symbols",
        },
        
        "励志鸡汤型": {
            "base": "motivational inspirational visual, positive energy",
            "style": "bright uplifting colors, golden hour lighting, aspirational",
            "mood": "inspiring, hopeful, empowering",
            "elements": "mountain peak, sunrise, achievement, success symbols",
        },
        
        "反思质疑型": {
            "base": "thought-provoking philosophical visual, deep thinking concept",
            "style": "moody atmospheric, muted colors, contemplative mood",
            "mood": "reflective, questioning, profound",
            "elements": "mirror, maze, question mark, abstract thinking symbols",
        },
        
        "轻松幽默型": {
            "base": "fun playful visual, humorous concept",
            "style": "bright cheerful colors, cartoon style, friendly vibe",
            "mood": "fun, lighthearted, entertaining",
            "elements": "emoji, playful characters, comic elements",
        },
    }
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        dry_run: bool = False,
        max_retries: int = 3,
        timeout: int = 60,
    ):
        """
        初始化图片生成器
        
        Args:
            api_key: PonyFlash API Key
            dry_run: 是否为测试模式（不实际生成图片）
            max_retries: 最大重试次数
            timeout: 超时时间（秒）
        """
        self.api_key = api_key or os.getenv("PONYFLASH_API_KEY")
        self.dry_run = dry_run
        self.max_retries = max_retries
        self.timeout = timeout
        self.client = None
        
        if not self.dry_run:
            self._init_client()
    
    def _init_client(self):
        """初始化 PonyFlash 客户端"""
        if not self.api_key:
            print("⚠️  未设置 PONYFLASH_API_KEY，将使用 dry-run 模式")
            self.dry_run = True
            return
        
        try:
            from ponyflash import PonyFlash
            self.client = PonyFlash(api_key=self.api_key)
            print("✅ PonyFlash 客户端初始化成功")
        except ImportError:
            print("⚠️  未安装 ponyflash 库，将使用 dry-run 模式")
            print("   安装命令: pip install ponyflash")
            self.dry_run = True
        except Exception as e:
            print(f"⚠️  PonyFlash 客户端初始化失败: {e}")
            print("   将使用 dry-run 模式")
            self.dry_run = True
    
    def generate(
        self,
        copies: List[Dict],
        output_dir: str = "./images",
        resolution: str = "2K",
        aspect_ratio: str = "3:4",
    ) -> List[Dict]:
        """
        为文案生成配图
        
        Args:
            copies: 文案列表
            output_dir: 输出目录
            resolution: 分辨率（1K/2K/4K）
            aspect_ratio: 宽高比（1:1/3:4/4:3/16:9）
        
        Returns:
            图片信息列表
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        images = []
        print(f"\n🎨 开始生成 {len(copies)} 张配图...")
        print(f"   输出目录: {output_dir}")
        print(f"   分辨率: {resolution}")
        print(f"   宽高比: {aspect_ratio}")
        print(f"   模式: {'Dry-run（测试）' if self.dry_run else 'Production（实际生成）'}")
        print()
        
        for i, copy in enumerate(copies):
            try:
                print(f"  [{i+1}/{len(copies)}] 生成【{copy['style']}】配图...", end=" ", flush=True)
                
                if self.dry_run:
                    image_info = self._generate_mock_image(copy, i, output_path)
                else:
                    image_info = self._generate_single_image_with_retry(
                        copy, i, output_path, resolution, aspect_ratio
                    )
                
                images.append(image_info)
                print("✅")
                
                # 避免 API 限流
                if not self.dry_run and i < len(copies) - 1:
                    time.sleep(1)
                
            except Exception as e:
                print(f"❌ 失败: {e}")
                # 失败时创建占位符
                images.append(self._generate_mock_image(copy, i, output_path, error=str(e)))
        
        print(f"\n✅ 图片生成完成！成功: {len(images)}/{len(copies)}")
        return images
    
    def _generate_single_image_with_retry(
        self,
        copy: Dict,
        index: int,
        output_path: Path,
        resolution: str,
        aspect_ratio: str,
    ) -> Dict:
        """生成单张图片（带重试机制）"""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                if attempt > 0:
                    print(f"\n      重试 {attempt}/{self.max_retries}...", end=" ", flush=True)
                    time.sleep(2 ** attempt)  # 指数退避
                
                return self._generate_single_image(
                    copy, index, output_path, resolution, aspect_ratio
                )
                
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    continue
        
        # 所有重试都失败
        raise RuntimeError(f"生成失败（已重试{self.max_retries}次）: {last_error}")
    
    def _generate_single_image(
        self,
        copy: Dict,
        index: int,
        output_path: Path,
        resolution: str,
        aspect_ratio: str,
    ) -> Dict:
        """生成单张图片（核心逻辑）"""
        style = copy.get("style", "")
        title = copy.get("title", "")
        content = copy.get("content", "")
        
        # 构建高质量 prompt
        prompt = self._build_prompt(style, title, content)
        
        try:
            # 调用 PonyFlash API
            result = self.client.images.generate(
                model="nano-banana-pro",
                prompt=prompt,
                resolution=resolution,
                aspect_ratio=aspect_ratio,
            )
            
            # 下载图片
            import requests
            image_url = result.url
            image_filename = f"image_{index:03d}_{self._sanitize_filename(style)}.png"
            image_path = output_path / image_filename
            
            response = requests.get(image_url, timeout=self.timeout)
            response.raise_for_status()
            
            with open(image_path, 'wb') as f:
                f.write(response.content)
            
            return {
                "index": index,
                "style": style,
                "title": title,
                "local_path": str(image_path),
                "filename": image_filename,
                "url": image_url,
                "prompt": prompt,
                "resolution": resolution,
                "aspect_ratio": aspect_ratio,
            }
            
        except Exception as e:
            raise RuntimeError(f"PonyFlash API 调用失败: {e}")
    
    def _build_prompt(self, style: str, title: str, content: str) -> str:
        """构建高质量图片生成 prompt"""
        style_config = self.STYLE_PROMPTS.get(style, self.STYLE_PROMPTS["数据驱动型"])
        
        # 从标题和内容中提取关键词
        keywords = self._extract_keywords(title, content)
        
        # 组合 prompt
        prompt_parts = [
            style_config["base"],
            f"theme: {keywords}",
            style_config["style"],
            style_config["mood"],
            f"elements: {style_config['elements']}",
            "high quality, professional, 4k, detailed",
            "no text, no watermark, clean composition",
        ]
        
        prompt = ", ".join(prompt_parts)
        return prompt
    
    def _extract_keywords(self, title: str, content: str) -> str:
        """从标题和内容中提取关键词"""
        # 简单实现：取标题前 20 字
        text = title if title else content[:50]
        # 移除特殊字符
        keywords = "".join(c for c in text if c.isalnum() or c.isspace() or ord(c) > 127)
        return keywords[:30]
    
    def _sanitize_filename(self, filename: str) -> str:
        """清理文件名"""
        # 移除不安全字符
        safe_chars = "".join(c if c.isalnum() or c in "._- " else "_" for c in filename)
        return safe_chars[:50]
    
    def _generate_mock_image(
        self,
        copy: Dict,
        index: int,
        output_path: Path,
        error: Optional[str] = None,
    ) -> Dict:
        """生成模拟图片信息（测试模式或失败降级）"""
        style = copy.get("style", "default")
        filename = f"image_{index:03d}_{self._sanitize_filename(style)}.png"
        
        return {
            "index": index,
            "style": style,
            "title": copy.get("title", ""),
            "local_path": str(output_path / filename),
            "filename": filename,
            "mock": True,
            "error": error,
        }


if __name__ == "__main__":
    # 测试
    test_copies = [
        {
            "style": "数据驱动型",
            "title": "AI 如何改变内容创作：数据告诉你的真相",
            "content": "根据最新数据：87%的创作者在内容生产上遇到瓶颈...",
        },
        {
            "style": "故事叙述型",
            "title": "接触 AI 创作 30 天，我的改变",
            "content": "以前每天加班到深夜，却做不出成绩...",
        },
    ]
    
    generator = ImageGenerator(dry_run=True)
    images = generator.generate(test_copies, output_dir="./test_images")
    
    print("\n" + "="*60)
    for img in images:
        print(f"\n图片 {img['index']+1}:")
        print(f"  风格: {img['style']}")
        print(f"  文件: {img['filename']}")
        print(f"  路径: {img['local_path']}")
        if img.get('mock'):
            print(f"  模式: Mock（测试）")
