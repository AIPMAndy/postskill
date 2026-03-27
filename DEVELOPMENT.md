# PostSkill 开发指南

## 🚀 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/AIPMAndy/postskill.git
cd postskill

# 2. 初始化开发环境
make setup

# 3. 验证环境
make check
```

## 🛠️ 可用命令

| 命令 | 说明 |
|------|------|
| `make setup` | 初始化开发环境（安装依赖 + pre-commit） |
| `make format` | 格式化代码（Black + isort） |
| `make lint` | 代码检查（Ruff + MyPy） |
| `make security` | 安全扫描（Bandit） |
| `make test` | 运行测试 |
| `make test-cov` | 运行测试并生成覆盖率报告 |
| `make check` | 完整检查（format + lint + security + test） |
| `make dry-run` | 本地测试运行（不发布） |
| `make clean` | 清理临时文件 |

## 🧪 测试

### 运行测试
```bash
# 运行所有测试
make test

# 带覆盖率
make test-cov

# 只运行单元测试
pytest tests/ -v -m unit

# 跳过慢测试
pytest tests/ -v -m "not slow"
```

### 添加新测试
在 `tests/` 目录下创建 `test_*.py` 文件：

```python
import pytest

def test_example():
    assert True

@pytest.mark.unit
def test_unit():
    # 单元测试标记
    pass

@pytest.mark.integration
def test_integration():
    # 集成测试标记
    pass
```

## 🔒 Pre-commit Hooks

提交前会自动运行：
- 代码格式化（Black + isort）
- 代码检查（Ruff）
- 安全扫描（Bandit）
- 文件检查（YAML/JSON 语法、大文件、私钥）

手动运行：
```bash
pre-commit run --all-files
```

跳过检查（不推荐）：
```bash
git commit -m "xxx" --no-verify
```

## 📝 提交规范

### Commit Message 格式
```
<type>: <subject>

<body>
```

**类型说明：**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具链

**示例：**
```
feat: 添加小红书发布功能

- 实现 xhs 平台 API 调用
- 添加图片裁剪适配
- 更新 README
```

## 🔍 调试技巧

### 本地调试发布流程
```bash
# 使用 dry-run 模式（不实际发布）
python postskill.py run --topic "测试" --platforms wechat --dry-run

# 详细日志
python postskill.py run --topic "测试" -v
```

### 检查 GitHub Actions
```bash
# 查看最近运行
gh run list

# 查看日志
gh run view <ID> --log

# 重新运行
gh run rerun <ID>
```

## 📊 监控

### 查看发布历史
查看 [RELEASE_LOG.md](./RELEASE_LOG.md)

### 健康检查
- 自动每 6 小时运行
- 检查外部服务可用性
- 失败时自动创建 Issue

### 告警规则
- **发布失败**: 自动创建 Issue
- **服务异常**: 自动创建 Issue
- **依赖更新**: Dependabot PR

## 🔧 常见问题

### Q: Pre-commit 安装失败？
```bash
pip install pre-commit
pre-commit install
```

### Q: 测试需要 API Key？
使用 Mock 模式：
```bash
pytest tests/ -v  # Mock 测试不需要真实 Key
```

### Q: CI 失败但本地正常？
检查：
1. 是否运行了 `make check`
2. Python 版本是否一致（3.10+）
3. 依赖是否更新 `pip install -r requirements.txt`

## 📞 帮助

- Issues: https://github.com/AIPMAndy/postskill/issues
- Actions: https://github.com/AIPMAndy/postskill/actions
