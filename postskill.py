#!/usr/bin/env python3
"""
PostSkill - 端到端图文批量生产与自动发布工具
主入口 CLI - 优化版
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
@click.version_option(version="2.0.0")
def cli():
    """PostSkill - 输入主题，自动生成高质量图文并发布
    
    \b
    核心能力：
    • 10 种专业文案风格（AI 驱动）
    • 智能配图生成（PonyFlash）
    • 质量评分系统
    • 自动重试机制
    • 飞书文档协作
    
    \b
    快速开始：
      python postskill.py run --topic "AI 如何改变内容创作"
    
    \b
    环境变量：
      OPENAI_API_KEY      - OpenAI API Key（文案生成）
      PONYFLASH_API_KEY   - PonyFlash API Key（图片生成）
    """
    pass


@cli.command()
@click.option('--topic', '-t', required=True, help='内容主题')
@click.option('--count', '-c', default=5, help='生成数量（默认5套）')
@click.option('--max-length', '-l', default=150, help='最大字数（默认150）')
@click.option('--output', '-o', default='./output', help='输出目录')
@click.option('--model', '-m', default='gpt-4o-mini', help='AI 模型（默认 gpt-4o-mini）')
@click.option('--resolution', default='2K', help='图片分辨率（1K/2K/4K）')
@click.option('--aspect-ratio', default='3:4', help='图片宽高比（1:1/3:4/4:3/16:9）')
@click.option('--dry-run', is_flag=True, help='测试模式（不实际生成图片）')
@click.option('--publish', '-p', is_flag=True, help='自动发布（开发中）')
@click.option('--platforms', help='发布平台（逗号分隔，开发中）')
def run(topic, count, max_length, output, model, resolution, aspect_ratio, dry_run, publish, platforms):
    """一键生成高质量图文内容
    
    \b
    示例：
      # 生成 5 套内容（默认）
      python postskill.py run --topic "AI 如何改变内容创作"
      
      # 生成 10 套内容，使用 GPT-4
      python postskill.py run -t "个人成长" -c 10 -m gpt-4o
      
      # 测试模式（不实际生成图片）
      python postskill.py run -t "测试主题" --dry-run
    """
    print(f"\n{'='*60}")
    print(f"🚀 PostSkill v2.0 - AI 驱动的内容生产引擎")
    print(f"{'='*60}")
    print(f"\n📋 配置信息：")
    print(f"   主题: {topic}")
    print(f"   数量: {count} 套")
    print(f"   字数: ≤{max_length}")
    print(f"   模型: {model}")
    print(f"   分辨率: {resolution}")
    print(f"   宽高比: {aspect_ratio}")
    print(f"   模式: {'测试（Dry-run）' if dry_run else '生产（Production）'}")
    print(f"   输出: {output}")
    
    # 检查环境变量
    print(f"\n🔑 环境检查：")
    openai_key = os.getenv("OPENAI_API_KEY")
    ponyflash_key = os.getenv("PONYFLASH_API_KEY")
    print(f"   OPENAI_API_KEY: {'✅ 已设置' if openai_key else '❌ 未设置（将使用模板模式）'}")
    print(f"   PONYFLASH_API_KEY: {'✅ 已设置' if ponyflash_key else '❌ 未设置（将使用 dry-run 模式）'}")
    
    print(f"\n{'='*60}\n")
    
    # 创建输出目录
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 1. 生成文案
    print("📝 步骤 1/4: 生成文案")
    print("-" * 60)
    generator = CopyGenerator(api_key=openai_key, model=model)
    copies = generator.generate(
        topic=topic,
        count=count,
        max_length=max_length,
    )
    
    # 保存文案 JSON
    copies_file = output_path / 'copies.json'
    with open(copies_file, 'w', encoding='utf-8') as f:
        json.dump(copies, f, ensure_ascii=False, indent=2)
    print(f"\n💾 文案已保存: {copies_file}")
    
    # 显示质量统计
    avg_quality = sum(c.get('quality_score', 0) for c in copies) / len(copies)
    print(f"📊 平均质量分: {avg_quality:.2f}/1.00")
    
    # 2. 生成配图
    print(f"\n{'='*60}\n")
    print("🎨 步骤 2/4: 生成配图")
    print("-" * 60)
    image_gen = ImageGenerator(
        api_key=ponyflash_key,
        dry_run=dry_run or not ponyflash_key,
        max_retries=3,
    )
    images = image_gen.generate(
        copies,
        output_dir=str(output_path / "images"),
        resolution=resolution,
        aspect_ratio=aspect_ratio,
    )
    
    # 保存图片信息
    images_file = output_path / 'images.json'
    with open(images_file, 'w', encoding='utf-8') as f:
        json.dump(images, f, ensure_ascii=False, indent=2)
    print(f"\n💾 图片信息已保存: {images_file}")
    
    # 3. 创建飞书文档
    print(f"\n{'='*60}\n")
    print("📄 步骤 3/4: 创建审核文档")
    print("-" * 60)
    doc_creator = FeishuDocCreator()
    doc_result = doc_creator.create_document(
        title=f"{topic} - 图文内容",
        copies=copies,
        images=images,
        output_dir=str(output_path),
    )
    print(f"✅ Markdown 文档: {doc_result['markdown_file']}")
    
    # 4. 自动发布（如果启用）
    if publish and platforms:
        print(f"\n{'='*60}\n")
        print("📤 步骤 4/4: 自动发布")
        print("-" * 60)
        platform_list = [p.strip() for p in platforms.split(',')]
        print(f"目标平台: {', '.join(platform_list)}")
        print("⚠️  自动发布功能开发中...")
    
    # 总结
    print(f"\n{'='*60}")
    print("✅ PostSkill 执行完成!")
    print(f"{'='*60}")
    print(f"\n📊 生成统计：")
    print(f"   文案数量: {len(copies)}")
    print(f"   图片数量: {len(images)}")
    print(f"   平均质量: {avg_quality:.2f}/1.00")
    print(f"   输出目录: {output}")
    print(f"\n📁 输出文件：")
    print(f"   {copies_file}")
    print(f"   {images_file}")
    print(f"   {doc_result['markdown_file']}")
    print(f"\n💡 下一步：")
    print(f"   1. 查看 {doc_result['markdown_file']} 审核内容")
    print(f"   2. 修改不满意的文案")
    print(f"   3. 使用 --publish 参数发布（开发中）")
    print()


@cli.command()
@click.option('--topic', '-t', required=True, help='内容主题')
@click.option('--count', '-c', default=5, help='生成数量')
@click.option('--max-length', '-l', default=150, help='最大字数')
@click.option('--model', '-m', default='gpt-4o-mini', help='AI 模型')
@click.option('--output', '-o', default='./output', help='输出目录')
def generate(topic, count, max_length, model, output):
    """仅生成文案（不生成图片）
    
    \b
    示例：
      python postskill.py generate --topic "AI 创作" --count 10
    """
    print(f"\n📝 生成文案...")
    generator = CopyGenerator(model=model)
    copies = generator.generate(
        topic=topic,
        count=count,
        max_length=max_length,
    )
    
    # 保存 JSON
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    with open(output_path / 'copies.json', 'w', encoding='utf-8') as f:
        json.dump(copies, f, ensure_ascii=False, indent=2)
    
    avg_quality = sum(c.get('quality_score', 0) for c in copies) / len(copies)
    print(f"\n✅ 文案已保存: {output_path / 'copies.json'}")
    print(f"📊 平均质量分: {avg_quality:.2f}/1.00")


@cli.command()
@click.option('--config', '-c', required=True, help='文案配置文件（JSON）')
@click.option('--output', '-o', default='./output/images', help='输出目录')
@click.option('--resolution', default='2K', help='分辨率（1K/2K/4K）')
@click.option('--aspect-ratio', default='3:4', help='宽高比（1:1/3:4/4:3/16:9）')
@click.option('--dry-run', is_flag=True, help='测试模式')
def generate_images(config, output, resolution, aspect_ratio, dry_run):
    """仅生成配图（需要先生成文案）
    
    \b
    示例：
      python postskill.py generate-images --config ./output/copies.json
    """
    print(f"\n🎨 生成配图...")
    with open(config, 'r', encoding='utf-8') as f:
        copies = json.load(f)
    
    image_gen = ImageGenerator(dry_run=dry_run, max_retries=3)
    images = image_gen.generate(
        copies,
        output_dir=output,
        resolution=resolution,
        aspect_ratio=aspect_ratio,
    )
    
    print(f"\n✅ 图片已保存: {output}")


@cli.command()
@click.option('--content', '-c', required=True, help='内容 JSON 文件')
@click.option('--images', '-i', required=True, help='图片目录')
@click.option('--output', '-o', default='./output', help='输出目录')
def create_doc(content, images, output):
    """创建飞书审核文档
    
    \b
    示例：
      python postskill.py create-doc \\
        --content ./output/copies.json \\
        --images ./output/images
    """
    print(f"\n📄 创建文档...")
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
    
    print(f"\n✅ 文档已创建: {result['markdown_file']}")


@cli.command()
def config():
    """查看配置信息
    
    \b
    检查环境变量和依赖安装情况
    """
    print("\n" + "="*60)
    print("PostSkill 配置信息")
    print("="*60)
    
    print("\n🔑 环境变量:")
    print(f"  OPENAI_API_KEY: {'✅ 已设置' if os.getenv('OPENAI_API_KEY') else '❌ 未设置'}")
    print(f"  PONYFLASH_API_KEY: {'✅ 已设置' if os.getenv('PONYFLASH_API_KEY') else '❌ 未设置'}")
    print(f"  FEISHU_APP_ID: {'✅ 已设置' if os.getenv('FEISHU_APP_ID') else '❌ 未设置'}")
    
    print("\n📦 依赖检查:")
    deps = {
        'openai': 'OpenAI SDK（文案生成）',
        'ponyflash': 'PonyFlash SDK（图片生成）',
        'click': 'CLI 框架',
        'requests': 'HTTP 请求',
    }
    
    for pkg, desc in deps.items():
        try:
            __import__(pkg)
            print(f"  ✅ {pkg}: {desc}")
        except ImportError:
            print(f"  ❌ {pkg}: {desc} - 未安装")
    
    print("\n💡 提示:")
    print("  1. 设置环境变量: export OPENAI_API_KEY=your_key")
    print("  2. 安装依赖: pip install -r requirements.txt")
    print("  3. 运行测试: python postskill.py run --topic '测试' --dry-run")
    print()


if __name__ == '__main__':
    cli()
