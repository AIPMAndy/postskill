#!/usr/bin/env python3
"""
PostSkill - 端到端图文批量生产与自动发布工具
主入口 CLI - v3.0 Self-Evolution 版本
"""

import click
import json
import os
from pathlib import Path
from datetime import datetime

from scripts.copy_generator import CopyGenerator
from scripts.image_generator import ImageGenerator
from scripts.feishu_doc_creator import FeishuDocCreator
from scripts.quality_feedback import QualityFeedbackSystem
from scripts.concurrency_control import ConcurrencyController, ProgressBar


@click.group()
@click.version_option(version="3.0.0")
def cli():
    """PostSkill v3.0 - Self-Evolution AI 内容生产引擎
    
    \b
    🚀 新特性：
    • Self-Evolution：失败自动修复，质量持续优化
    • 并发控制：智能排队，避免 API 限流
    • 质量反馈：用户打分，AI 自动学习
    • 进度可视化：实时显示生成进度
    • Markdown 配置：风格模板独立，易于自定义
    
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
@click.option('--concurrent', default=1, help='并发数（默认1，避免限流）')
@click.option('--rate-limit', default=1.0, help='速率限制（秒/请求，默认1.0）')
def run(topic, count, max_length, output, model, resolution, aspect_ratio, dry_run, concurrent, rate_limit):
    """一键生成高质量图文内容（v3.0 Self-Evolution 版）
    
    \b
    示例：
      # 生成 5 套内容（默认）
      python postskill.py run --topic "AI 如何改变内容创作"
      
      # 生成 10 套内容，使用 GPT-4
      python postskill.py run -t "个人成长" -c 10 -m gpt-4o
      
      # 测试模式（不实际生成图片）
      python postskill.py run -t "测试主题" --dry-run
      
      # 并发生成（小心 API 限流）
      python postskill.py run -t "AI 创作" -c 10 --concurrent 2 --rate-limit 2.0
    """
    print(f"\n{'='*60}")
    print(f"🚀 PostSkill v3.0 - Self-Evolution AI 内容生产引擎")
    print(f"{'='*60}")
    print(f"\n📋 配置信息：")
    print(f"   主题: {topic}")
    print(f"   数量: {count} 套")
    print(f"   字数: ≤{max_length}")
    print(f"   模型: {model}")
    print(f"   分辨率: {resolution}")
    print(f"   宽高比: {aspect_ratio}")
    print(f"   并发数: {concurrent}")
    print(f"   速率限制: {rate_limit}s/请求")
    print(f"   模式: {'测试（Dry-run）' if dry_run else '生产（Production）'}")
    print(f"   输出: {output}")
    
    # 检查环境变量
    print(f"\n🔑 环境检查：")
    openai_key = os.getenv("OPENAI_API_KEY")
    ponyflash_key = os.getenv("PONYFLASH_API_KEY")
    print(f"   OPENAI_API_KEY: {'✅ 已设置' if openai_key else '❌ 未设置（将使用模板模式）'}")
    print(f"   PONYFLASH_API_KEY: {'✅ 已设置' if ponyflash_key else '❌ 未设置（将使用 dry-run 模式）'}")
    
    # 加载质量反馈系统
    feedback_system = QualityFeedbackSystem(feedback_dir=f"{output}/feedback")
    
    print(f"\n{'='*60}\n")
    
    # 创建输出目录
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 1. 生成文案（带并发控制）
    print("📝 步骤 1/4: 生成文案")
    print("-" * 60)
    
    generator = CopyGenerator(api_key=openai_key, model=model)
    
    # 检查是否有改进建议
    print("\n💡 检查历史反馈...")
    for style in ["数据驱动型", "故事叙述型", "观点输出型"][:count]:
        suggestions = feedback_system.get_improvement_suggestions(style)
        if suggestions:
            print(f"\n【{style}】改进建议：")
            for s in suggestions[:2]:
                print(f"  {s}")
    
    print()
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
    
    # 2. 生成配图（带并发控制和进度条）
    print(f"\n{'='*60}\n")
    print("🎨 步骤 2/4: 生成配图")
    print("-" * 60)
    
    image_gen = ImageGenerator(
        api_key=ponyflash_key,
        dry_run=dry_run or not ponyflash_key,
        max_retries=3,
    )
    
    # 使用并发控制器
    controller = ConcurrencyController(
        max_concurrent=concurrent,
        rate_limit=rate_limit,
        retry_on_error=True,
        max_retries=3,
    )
    
    # 添加任务
    for i, copy in enumerate(copies):
        controller.add_task(
            task_id=f"image-{i:02d}",
            func=image_gen._generate_single_image_with_retry if not dry_run else image_gen._generate_mock_image,
            copy=copy,
            index=i,
            output_path=output_path / "images",
            resolution=resolution,
            aspect_ratio=aspect_ratio,
        )
    
    # 创建进度条
    progress = ProgressBar(total=len(copies), desc="生成配图")
    
    # 执行
    images = controller.execute_all(
        progress_callback=lambda c, t, tid: progress.update(c, tid)
    )
    
    progress.close()
    
    # 保存图片信息
    images_file = output_path / 'images.json'
    with open(images_file, 'w', encoding='utf-8') as f:
        json.dump(images, f, ensure_ascii=False, indent=2)
    print(f"\n💾 图片信息已保存: {images_file}")
    
    # 显示并发统计
    stats = controller.get_stats()
    print(f"📊 生成统计: 成功 {stats['completed']}/{stats['total']} (成功率 {stats['success_rate']*100:.1f}%)")
    
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
    
    # 4. 质量报告
    print(f"\n{'='*60}\n")
    print("📊 步骤 4/4: 质量报告")
    print("-" * 60)
    
    # 生成质量报告
    if feedback_system._load_stats():
        print(feedback_system.generate_report())
    else:
        print("暂无历史反馈数据")
        print("\n💡 提示：使用 `postskill.py feedback` 命令对生成结果打分")
        print("   AI 会根据你的反馈自动优化生成质量")
    
    # 总结
    print(f"\n{'='*60}")
    print("✅ PostSkill 执行完成!")
    print(f"{'='*60}")
    print(f"\n📊 生成统计：")
    print(f"   文案数量: {len(copies)}")
    print(f"   图片数量: {len(images)}")
    print(f"   平均质量: {avg_quality:.2f}/1.00")
    print(f"   成功率: {stats['success_rate']*100:.1f}%")
    print(f"   输出目录: {output}")
    print(f"\n📁 输出文件：")
    print(f"   {copies_file}")
    print(f"   {images_file}")
    print(f"   {doc_result['markdown_file']}")
    print(f"\n💡 下一步：")
    print(f"   1. 查看 {doc_result['markdown_file']} 审核内容")
    print(f"   2. 使用 `postskill.py feedback` 对结果打分")
    print(f"   3. AI 会根据反馈自动优化（Self-Evolution）")
    print()


@cli.command()
@click.option('--output', '-o', default='./output', help='输出目录')
def feedback(output):
    """对生成结果打分，帮助 AI 自我进化
    
    \b
    示例：
      python postskill.py feedback --output ./output
    """
    print(f"\n{'='*60}")
    print("📊 PostSkill 质量反馈系统")
    print(f"{'='*60}\n")
    
    # 加载文案
    copies_file = Path(output) / 'copies.json'
    if not copies_file.exists():
        print("❌ 未找到文案文件，请先运行 `postskill.py run`")
        return
    
    with open(copies_file, 'r', encoding='utf-8') as f:
        copies = json.load(f)
    
    # 初始化反馈系统
    feedback_system = QualityFeedbackSystem(feedback_dir=f"{output}/feedback")
    
    print(f"找到 {len(copies)} 套文案，开始打分...\n")
    
    for i, copy in enumerate(copies):
        print(f"{'='*60}")
        print(f"【{i+1}/{len(copies)}】{copy['style']}")
        print(f"{'='*60}")
        print(f"\n标题: {copy['title']}")
        print(f"\n内容:\n{copy['content']}\n")
        print(f"标签: {' '.join(copy['tags'])}")
        print(f"字数: {copy['length']} | 质量分: {copy.get('quality_score', 0):.2f}")
        print()
        
        # 用户打分
        while True:
            try:
                rating = int(input("请打分（1-5，0=跳过）: "))
                if 0 <= rating <= 5:
                    break
                print("❌ 请输入 0-5 之间的数字")
            except ValueError:
                print("❌ 请输入有效数字")
        
        if rating == 0:
            print("⏭️  已跳过\n")
            continue
        
        # 评论
        comment = input("评论（可选，直接回车跳过）: ").strip()
        
        # 问题
        print("\n常见问题（多选，用逗号分隔，直接回车跳过）：")
        print("  1. 内容太短")
        print("  2. 内容太长")
        print("  3. 缺少数据")
        print("  4. 不够吸引人")
        print("  5. 语气不对")
        print("  6. 结构混乱")
        
        issues_input = input("选择问题编号: ").strip()
        issues = []
        if issues_input:
            issue_map = {
                "1": "内容太短",
                "2": "内容太长",
                "3": "缺少数据",
                "4": "不够吸引人",
                "5": "语气不对",
                "6": "结构混乱",
            }
            for num in issues_input.split(','):
                num = num.strip()
                if num in issue_map:
                    issues.append(issue_map[num])
        
        # 记录反馈
        feedback_system.record_feedback(
            copy_id=f"{copy['style']}-{i}",
            style=copy['style'],
            topic=copy.get('topic', ''),
            content=copy['content'],
            rating=rating,
            comment=comment if comment else None,
            issues=issues,
        )
        
        print("✅ 反馈已记录\n")
    
    # 生成报告
    print(f"\n{'='*60}")
    print(feedback_system.generate_report())
    print(f"\n💡 提示：下次生成时，AI 会根据这些反馈自动优化")


@cli.command()
@click.option('--output', '-o', default='./output', help='输出目录')
def report(output):
    """查看质量报告
    
    \b
    示例：
      python postskill.py report --output ./output
    """
    feedback_system = QualityFeedbackSystem(feedback_dir=f"{output}/feedback")
    print(feedback_system.generate_report())


@cli.command()
def config():
    """查看配置信息"""
    print("\n" + "="*60)
    print("PostSkill v3.0 配置信息")
    print("="*60)
    
    print("\n🔑 环境变量:")
    print(f"  OPENAI_API_KEY: {'✅ 已设置' if os.getenv('OPENAI_API_KEY') else '❌ 未设置'}")
    print(f"  PONYFLASH_API_KEY: {'✅ 已设置' if os.getenv('PONYFLASH_API_KEY') else '❌ 未设置'}")
    
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
    print("  4. 查看文档: https://github.com/AIPMAndy/postskill")
    print()


if __name__ == '__main__':
    cli()
