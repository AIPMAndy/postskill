# PostSkill 开发命令速查
# 使用: make <command>

.PHONY: help install dev-install format lint test test-cov clean publish dry-run

help: ## 显示帮助信息
	@echo "可用命令:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## 安装生产依赖
	pip install -r requirements.txt

dev-install: ## 安装开发依赖
	pip install -e ".[dev]"
	pre-commit install

format: ## 格式化代码 (Black + isort)
	black . --line-length=100
	isort . --profile=black

lint: ## 运行代码检查 (Ruff + MyPy)
	ruff check . --fix
	mypy . || true

security: ## 安全扫描
	bandit -r scripts -c pyproject.toml

test: ## 运行测试
	pytest tests/ -v

test-cov: ## 运行测试并生成覆盖率报告
	pytest tests/ -v --cov=. --cov-report=term --cov-report=html
	@echo "覆盖率报告: htmlcov/index.html"

check: format lint security test ## 运行完整检查 (格式化 + 检查 + 安全 + 测试)

ci: lint test ## CI 流程 (检查 + 测试)

clean: ## 清理临时文件
	rm -rf .pytest_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

dry-run: ## 本地测试运行 (不发布)
	python postskill.py run --topic "AI醒觉社" --platforms wechat

publish: ## 手动发布
	python postskill.py run --topic "AI醒觉社" --publish --platforms wechat,xiaohongshu

pre-commit: ## 手动运行 pre-commit hooks
	pre-commit run --all-files

setup: ## 初始化开发环境
	pip install -e ".[dev]"
	pre-commit install
	@echo "✅ 开发环境初始化完成"
	@echo "运行 'make check' 验证环境"
