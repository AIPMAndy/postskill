#!/usr/bin/env python3
"""
PostSkill - 端到端图文批量生产与自动发布工具
主入口CLI
"""

import click
import json
import os
from pathlib import Path
from datetime import datetime

from scripts.copy_generator import CopyGenerator
from scripts.image_generator import ImageGenerator
from scripts.feishu_doc_creator import FeishuDocCreator


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """PostSkill - 输入主题，自动生成图文并发布"""
    pass


@cli.command()
@click.option('--topic', '-t', required=True, help='内容主题')
@click.option('--count', '-c', default=3, help='生成数量')
@click.option('--max-length', '-l', default=150, help='最大字数')
@click.option('--output', '-o', default='./output', help='输出目录')
@click.option('--publish', '-p', is_flag=True, help='自动发布')
@click.option('--platforms', help='发布平台（逗号分隔）')
def run(topic, count, max_length, output, publish, platforms):
    """一键生成图文并发布"""
    print(f"\n🚀 PostSkill 启动")
    print(f"主题: {topic}")
    print(f"数量: {count}")
    print(f"字数: ≤{max_length}")
    print("="*50)
    
    # 1. 生成文案
    print("\n📄 步骤1: 生成文案...")
    generator = CopyGenerator()
    copies = generator.generate(
        topic=topic,
        count=count,
        max_length=max_length,
    )
    
    # 2. 生成配图
    print("\n🎨 步骤2: 生成配图...")
    image_gen = ImageGenerator(
        api_key=os.getenv("PONYFLASH_API_KEY"),
        dry_run=False
    )
    images = image_gen.generate(copies, output_dir=f"{output}/images")
    
    # 3. 创建飞书文档
    print("\n📄 步骤3: 创建飞书文档...")
    doc_creator = FeishuDocCreator()
    doc_result = doc_creator.create_document(
        title=f"{topic} - 图文内容",
        copies=copies,
        images=images,
        output_dir=output,
    )
    print(f"✅ 文档已创建: {doc_result['markdown_file']}")
    
    # 4. 自动发布（如果启用）
    if publish and platforms:
        print(f"\n📤 步骤4: 自动发布到 {platforms}...")
        platform_list = [p.strip() for p in platforms.split(',')]
        print(f"发布到: {', '.join(platform_list)}")
        print("⚠️  自动发布功能开发中...")
    
    print("\n" + "="*50)
    print("✅ PostSkill 执行完成!")
    print(f"输出目录: {output}")
    print(f"文案数量: {len(copies)}")
    print(f"图片数量: {len(images)}")
    if publish:
        print(f"发布平台: {platforms}")


@cli.command()
@click.option('--topic', '-t', required=True, help='内容主题')
@click.option('--count', '-c', default=3, help='生成数量')
@click.option('--max-length', '-l', default=150, help='最大字数')
@click.option('--output', '-o', default='./output', help='输出目录')
def generate(topic, count, max_length, output):
    """仅生成文案"""
    generator = CopyGenerator()
    copies = generator.generate(
        topic=topic,
        count=count,
        max_length=max_length,
    )
    
    # 保存JSON
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    with open(output_path / 'copies.json', 'w', encoding='utf-8') as f:
        json.dump(copies, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 文案已保存到: {output_path / 'copies.json'}")


@cli.command()
@click.option('--config', '-c', required=True, help='文案配置文件')
@click.option('--output', '-o', default='./output/images', help='输出目录')
def generate_images(config, output):
    """仅生成配图"""
    with open(config, 'r', encoding='utf-8') as f:
        copies = json.load(f)
    
    image_gen = ImageGenerator(
        api_key=os.getenv("PONYFLASH_API_KEY"),
        dry_run=False
    )
    images = image_gen.generate(copies, output_dir=output)
    
    print(f"✅ 图片已保存到: {output}")


@cli.command()
@click.option('--content', '-c', required=True, help='内容JSON文件')
@click.option('--images', '-i', required=True, help='图片目录')
@click.option('--output', '-o', default='./output', help='输出目录')
def create_doc(content, images, output):
    """创建飞书文档"""
    with open(content, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    copies = data.get('copies', data)
    
    # 加载图片信息
    image_dir = Path(images)
    image_files = sorted(image_dir.glob('*.png'))
    images_info = [{"local_path": str(f), "filename": f.name} for f in image_files]
    
    doc_creator = FeishuDocCreator()
    result = doc_creator.create_document(
        title=data.get('title', '图文内容'),
        copies=copies,
        images=images_info,
        output_dir=output,
    )
    
    print(f"✅ 文档已创建: {result['markdown_file']}")


@cli.command()
def config():
    """配置管理"""
    print("PostSkill 配置管理")
    print("="*50)
    print("环境变量:")
    print(f"  PONYFLASH_API_KEY: {'已设置' if os.getenv('PONYFLASH_API_KEY') else '未设置'}")
    print(f"  FEISHU_APP_ID: {'已设置' if os.getenv('FEISHU_APP_ID') else '未设置'}")
    print("="*50)


if __name__ == '__main__':
    cli()
