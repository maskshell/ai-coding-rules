# Pre-commit 配置说明

本文档说明 `.pre-commit-config.yaml` 如何遵循项目的 Git 仓库管理规范。

## 配置与规则的对应关系

### 1. Commit Message 格式检查

**规则要求**（来自 `full-rules/ide-layer/rulesets/05-git-repository.md`）：

- 遵循 Conventional Commits 规范
- 格式：`type(scope): subject`
- Type: feat, fix, docs, style, refactor, test, chore

**Pre-commit 配置**：

```yaml
- repo: https://github.com/compilerla/conventional-pre-commit
  rev: v3.0.0
  hooks:
    - id: conventional-pre-commit
      stages: [commit-msg]
      args: [--strict]
```

**作用**：在提交时自动检查 commit message 是否符合规范，不符合则阻止提交。

### 2. 敏感信息检查

**规则要求**（来自 `full-rules/ide-layer/rulesets/05-git-repository.md`）：

- 提交前检查清单：没有提交敏感信息（密码、密钥等）

**Pre-commit 配置**：

```yaml
- repo: https://github.com/Yelp/detect-secrets
  rev: v1.4.0
  hooks:
    - id: detect-secrets
      args: ['--baseline', '.secrets.baseline']
```

**作用**：检测代码中可能包含的敏感信息（API 密钥、密码、令牌等），防止意外提交。

**注意**：首次使用需要创建 baseline 文件：

```bash
detect-secrets scan > .secrets.baseline
```

### 3. Markdown 格式化

**规则要求**（来自项目 Markdown 格式规范）：

- 确保所有 Markdown 文档格式一致
- 自动修复可修复的格式问题

**Pre-commit 配置**：

```yaml
- id: markdown-format
  name: Format Markdown files
  entry: python scripts/format-md.py
  types: [markdown]
```

**作用**：在提交前自动格式化 Markdown 文件，确保格式符合 `.markdownlint.json` 配置。

### 4. Markdown Linting

**规则要求**（来自项目 Markdown 格式规范）：

- 检查 Markdown 格式问题
- 验证项目特定规则（文件名格式、标题层级等）

**Pre-commit 配置**：

```yaml
- id: markdown-lint
  name: Lint Markdown files
  entry: python scripts/lint-md.py
  types: [markdown]
  args: [--check]
```

**作用**：检查 Markdown 文件格式，发现错误则阻止提交。

### 5. Python 代码检查和格式化（Ruff）

**规则要求**（来自 `full-rules/ide-layer/rulesets/05-git-repository.md` 和 Python 编码规范）：

- 提交前检查清单：代码可编译/运行
- 代码风格符合项目规范
- 与 IDE 中使用的 Ruff 扩展保持一致

**Pre-commit 配置**：

```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.6.1
  hooks:
    - id: ruff
      args: [--fix]
      types: [python]
    - id: ruff-format
      types: [python]
```

**作用**：

- `ruff`：检查 Python 代码问题（lint），自动修复可修复的问题
- `ruff-format`：格式化 Python 代码，确保代码风格一致

**配置位置**：Ruff 配置在 `pyproject.toml` 的 `[tool.ruff]` 部分。

### 6. JSON 文件检查和格式化

**规则要求**：

- JSON 文件语法正确
- JSON 文件格式统一（与 IDE 内置格式化保持一致）

**Pre-commit 配置**：

```yaml
# JSON 语法检查
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v4.6.0
  hooks:
    - id: check-json
      types: [json]

# JSON 格式化
- repo: https://github.com/pre-commit/mirrors-prettier
  rev: v4.0.0-alpha.8
  hooks:
    - id: prettier
      types: [json]
      args: [--write]
```

**作用**：

- `check-json`：检查 JSON 文件语法，确保文件格式正确
- `prettier`：自动格式化 JSON 文件，确保格式统一

### 7. YAML 文件检查和格式化

**规则要求**：

- YAML 文件语法正确
- YAML 文件格式统一（与 `redhat.vscode-yaml` 扩展保持一致）

**Pre-commit 配置**：

```yaml
# YAML 语法检查
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v4.6.0
  hooks:
    - id: check-yaml
      types: [yaml]
    - id: end-of-file-fixer
      types: [yaml]

# YAML 格式化
- repo: https://github.com/pre-commit/mirrors-prettier
  rev: v4.0.0-alpha.8
  hooks:
    - id: prettier
      types: [yaml]
      args: [--write]
```

**作用**：

- `check-yaml`：检查 YAML 文件语法，确保文件格式正确
- `end-of-file-fixer`：确保文件末尾有换行符
- `prettier`：自动格式化 YAML 文件，确保格式统一

## 使用说明

### 安装 Pre-commit Hooks

```bash
# 安装 pre-commit（如果未安装）
pip install pre-commit
# 或使用 uv
uv pip install pre-commit

# 安装 Git hooks
pre-commit install

# 安装 commit-msg hook（用于检查 commit message）
pre-commit install --hook-type commit-msg
```

### 手动运行检查

```bash
# 检查所有文件
pre-commit run --all-files

# 检查特定类型的文件
pre-commit run --files *.md
pre-commit run --files scripts/*.py
```

### 跳过 Pre-commit 检查（不推荐）

```bash
# 跳过所有检查（仅在紧急情况下使用）
git commit --no-verify -m "紧急修复"
```

## 与 CI/CD 的配合

Pre-commit 在本地提交时进行检查，CI/CD 在远程仓库进行验证：

- **Pre-commit**：快速反馈，在提交前发现问题
- **CI/CD**：最终验证，确保合并到主分支的代码符合规范

两者配合使用，确保代码质量。

## 注意事项

1. **首次使用 detect-secrets**：需要创建 `.secrets.baseline` 文件
2. **Commit message 检查**：如果使用 `--no-verify` 跳过检查，CI/CD 仍会验证
3. **性能考虑**：Pre-commit 检查应该快速，避免影响开发效率
4. **团队协作**：所有团队成员都应该安装并启用 pre-commit hooks

## 工具配置

### Ruff 配置

Ruff 配置位于 `pyproject.toml` 的 `[tool.ruff]` 部分，包括：

- 启用的规则集（E, W, F, I, B, C4, UP）
- 行长度限制（88 字符）
- 排除的目录
- 格式化选项（引号风格、缩进风格、行尾风格）

### Prettier 配置

Prettier 使用默认配置，与 IDE 内置格式化保持一致：

- JSON：使用 IDE 内置格式化规则
- YAML：与 `redhat.vscode-yaml` 扩展保持一致

## 相关文档

- Git 仓库管理规范：`full-rules/ide-layer/rulesets/05-git-repository.md`
- Markdown 格式规范：`.cursor/rules/meta-rules.md`（三、Markdown 格式规范）
- Python 编码规范：`.cursor/rules/01-python-basics.md`
- CI/CD 配置：`.github/workflows/lint-markdown.yml`
