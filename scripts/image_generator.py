#!/usr/bin/env python3
"""
PostSkill - 图片生成模块
调用PonyFlash为文案生成配套图片
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
import time


class ImageGenerator:
    """图片生成器"""
    
    # 图片风格映射
    STYLE_PROMPTS = {
        "干货型": "modern minimalist, productivity and learning concept, clean lines, blue gradient, professional tech style",
        "故事型": "warm and healing, emotional storytelling, soft colors, sunrise or hope theme, inspiring",
        "金句型": "creative artistic, bold typography, black and gold color scheme, motivational poster style",
        "数据型": "data visualization, charts and graphs, blue and green gradient, professional business style",
        "对比型": "before and after comparison, transformation concept, split screen, dramatic lighting",
    }
    
    def __init__(self, api_key: Optional[str] = None, dry_run: bool = False):
        self.api_key = api_key or os.getenv("PONYFLASH_API_KEY")
        self.dry_run = dry_run
        self.client = None
        
        if not self.dry_run:
            self._init_client()
    
    def _init_client(self):
        """初始化PonyFlash客户端"""
        try:
            from ponyflash import PonyFlash
            self.client = PonyFlash(api_key=self.api_key)
        except ImportError:
            raise ImportError("请安装 ponyflash 库: pip install ponyflash")
        except Exception as e:
            raise RuntimeError(f"初始化PonyFlash客户端失败: {e}")
    
    def generate(self, copies: List[Dict], output_dir: str = "./images") -> List[Dict]:
        """为文案生成配图"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        images = []
        print(f"🎨 开始生成 {len(copies)} 张配图...")
        
        for i, copy in enumerate(copies):
            try:
                print(f"  [{i+1}/{len(copies)}] 生成图片...", end=" ")
                
                if self.dry_run:
                    image_info = self._generate_mock_image(copy, i, output_path)
                else:
                    image_info = self._generate_single_image(copy, i, output_path)
                
                images.append(image_info)
                print("✅")
                
                if not self.dry_run and i < len(copies) - 1:
                    time.sleep(1)
                
            except Exception as e:
                print(f"❌ 失败: {e}")
        
        print(f"\n✅ 图片生成完成！成功: {len(images)}/{len(copies)}")
        return images
    
    def _generate_single_image(self, copy: Dict, index: int, output_path: Path) -> Dict:
        """生成单张图片"""
        style = copy.get("style", "")
        topic = copy.get("topic", copy.get("title", ""))
        style_prompt = self.STYLE_PROMPTS.get(style, "modern minimalist")
        
        prompt = f"Create an image for social media content about '{topic}'. Style: {style_prompt}. Professional, high-quality, no text."
        
        try:
            result = self.client.images.generate(
                model="nano-banana-pro",
                prompt=prompt,
                resolution="2K",
                aspect_ratio="3:4"
            )
            
            import requests
            image_url = result.url
            image_filename = f"image_{index:03d}_{style}.png"
            image_path = output_path / image_filename
            
            response = requests.get(image_url, timeout=60)
            response.raise_for_status()
            
            with open(image_path, 'wb') as f:
                f.write(response.content)
            
            return {
                "index": index,
                "style": style,
                "topic": topic,
                "local_path": str(image_path),
                "filename": image_filename,
            }
            
        except Exception as e:
            raise RuntimeError(f"生成图片失败: {e}")
    
    def _generate_mock_image(self, copy: Dict, index: int, output_path: Path) -> Dict:
        """生成模拟图片信息"""
        style = copy.get("style", "default")
        return {
            "index": index,
            "style": style,
            "local_path": str(output_path / f"image_{index:03d}_{style}.png"),
            "filename": f"image_{index:03d}_{style}.png",
            "mock": True,
        }
