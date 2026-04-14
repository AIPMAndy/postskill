#!/usr/bin/env python3
"""
PostSkill - 并发控制与任务队列
避免 API 限流，智能排队执行
"""

import asyncio
import time
from typing import Callable, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    """任务定义"""
    id: str
    func: Callable
    args: tuple
    kwargs: dict
    priority: int = 0
    created_at: float = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()


class ConcurrencyController:
    """并发控制器 - 智能排队和限流"""
    
    def __init__(
        self,
        max_concurrent: int = 1,
        rate_limit: Optional[float] = None,
        retry_on_error: bool = True,
        max_retries: int = 3,
    ):
        """
        初始化并发控制器
        
        Args:
            max_concurrent: 最大并发数
            rate_limit: 速率限制（秒/请求）
            retry_on_error: 是否自动重试
            max_retries: 最大重试次数
        """
        self.max_concurrent = max_concurrent
        self.rate_limit = rate_limit
        self.retry_on_error = retry_on_error
        self.max_retries = max_retries
        
        self.queue: List[Task] = []
        self.running: List[Task] = []
        self.completed: List[Task] = []
        self.failed: List[Task] = []
        
        self.last_execution_time = 0
    
    def add_task(
        self,
        task_id: str,
        func: Callable,
        *args,
        priority: int = 0,
        **kwargs
    ):
        """添加任务到队列"""
        task = Task(
            id=task_id,
            func=func,
            args=args,
            kwargs=kwargs,
            priority=priority,
        )
        self.queue.append(task)
        
        # 按优先级排序（高优先级在前）
        self.queue.sort(key=lambda t: (-t.priority, t.created_at))
    
    def execute_all(self, progress_callback: Optional[Callable] = None) -> List[Any]:
        """
        执行所有任务
        
        Args:
            progress_callback: 进度回调函数 (current, total, task_id)
        
        Returns:
            所有任务的结果列表
        """
        results = []
        total = len(self.queue)
        
        while self.queue or self.running:
            # 检查是否可以启动新任务
            while len(self.running) < self.max_concurrent and self.queue:
                # 速率限制
                if self.rate_limit:
                    elapsed = time.time() - self.last_execution_time
                    if elapsed < self.rate_limit:
                        time.sleep(self.rate_limit - elapsed)
                
                # 取出任务
                task = self.queue.pop(0)
                self.running.append(task)
                
                # 执行任务
                try:
                    result = self._execute_task(task)
                    results.append(result)
                    self.completed.append(task)
                    
                    # 进度回调
                    if progress_callback:
                        progress_callback(len(self.completed), total, task.id)
                    
                except Exception as e:
                    # 重试逻辑
                    if self.retry_on_error and hasattr(task, 'retry_count'):
                        if task.retry_count < self.max_retries:
                            task.retry_count += 1
                            self.queue.insert(0, task)  # 重新加入队列
                            continue
                    
                    self.failed.append(task)
                    results.append({"error": str(e), "task_id": task.id})
                
                finally:
                    self.running.remove(task)
                    self.last_execution_time = time.time()
        
        return results
    
    def _execute_task(self, task: Task) -> Any:
        """执行单个任务"""
        return task.func(*task.args, **task.kwargs)
    
    def get_stats(self) -> dict:
        """获取执行统计"""
        return {
            "total": len(self.queue) + len(self.running) + len(self.completed) + len(self.failed),
            "queued": len(self.queue),
            "running": len(self.running),
            "completed": len(self.completed),
            "failed": len(self.failed),
            "success_rate": len(self.completed) / max(len(self.completed) + len(self.failed), 1),
        }


class ProgressBar:
    """进度条显示"""
    
    def __init__(self, total: int, desc: str = "Processing", width: int = 40):
        """
        初始化进度条
        
        Args:
            total: 总任务数
            desc: 描述文字
            width: 进度条宽度
        """
        self.total = total
        self.desc = desc
        self.width = width
        self.current = 0
        self.start_time = time.time()
    
    def update(self, current: int, task_id: str = ""):
        """更新进度"""
        self.current = current
        
        # 计算进度
        percent = current / self.total if self.total > 0 else 0
        filled = int(self.width * percent)
        bar = "█" * filled + "░" * (self.width - filled)
        
        # 计算速度和剩余时间
        elapsed = time.time() - self.start_time
        speed = current / elapsed if elapsed > 0 else 0
        remaining = (self.total - current) / speed if speed > 0 else 0
        
        # 显示
        print(
            f"\r{self.desc}: |{bar}| {current}/{self.total} "
            f"({percent*100:.1f}%) "
            f"[{elapsed:.1f}s<{remaining:.1f}s, {speed:.2f}it/s] "
            f"{task_id}",
            end="",
            flush=True
        )
        
        if current >= self.total:
            print()  # 完成后换行
    
    def close(self):
        """关闭进度条"""
        print()


if __name__ == "__main__":
    # 测试
    import random
    
    def mock_task(task_id: str, duration: float = 0.5):
        """模拟任务"""
        time.sleep(duration)
        if random.random() < 0.1:  # 10% 失败率
            raise Exception(f"Task {task_id} failed")
        return f"Result of {task_id}"
    
    # 创建控制器
    controller = ConcurrencyController(
        max_concurrent=2,
        rate_limit=0.5,  # 每 0.5 秒一个任务
        retry_on_error=True,
        max_retries=2,
    )
    
    # 添加任务
    for i in range(10):
        controller.add_task(
            task_id=f"task-{i:02d}",
            func=mock_task,
            duration=random.uniform(0.3, 0.8),
        )
    
    # 创建进度条
    progress = ProgressBar(total=10, desc="生成文案")
    
    # 执行
    results = controller.execute_all(
        progress_callback=lambda c, t, tid: progress.update(c, tid)
    )
    
    progress.close()
    
    # 统计
    stats = controller.get_stats()
    print(f"\n执行统计：")
    print(f"  总任务：{stats['total']}")
    print(f"  成功：{stats['completed']}")
    print(f"  失败：{stats['failed']}")
    print(f"  成功率：{stats['success_rate']*100:.1f}%")
