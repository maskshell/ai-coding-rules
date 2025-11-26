# 测试说明

本目录包含 scripts 目录下脚本的单元测试。

## 运行测试

### 安装测试依赖

```bash
# 使用 uv
uv sync --extra dev

# 或使用 pip
pip install -e ".[dev]"
```

### 运行所有测试

```bash
pytest
```

### 运行特定测试文件

```bash
# 测试 format-md.py
pytest tests/test_format_md.py

# 测试 lint-md.py
pytest tests/test_lint_md.py
```

### 运行特定测试类或函数

```bash
# 运行特定测试类
pytest tests/test_format_md.py::TestFindMarkdownlintCommand

# 运行特定测试函数
pytest tests/test_format_md.py::TestFindMarkdownlintCommand::test_find_markdownlint_success
```

### 查看测试覆盖率

```bash
pytest --cov=scripts --cov-report=html
```

## 测试结构

- `test_format_md.py`: 测试 `format-md.py` 脚本
  - 命令检测功能
  - 文件格式化功能
  - 错误处理
  - 主函数

- `test_lint_md.py`: 测试 `lint-md.py` 脚本
  - 命令检测功能
  - markdownlint 检查功能
  - 项目特定规则检查（文件名、标题层级、代码块等）
  - 主函数

## 注意事项

测试使用 `unittest.mock` 来模拟系统命令调用，因此不需要实际安装 `markdownlint` 即可运行测试。

