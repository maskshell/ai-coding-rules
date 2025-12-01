# Scripts 使用场景说明

本文档说明 `scripts/` 目录下各个脚本的使用时机和场景。

## 脚本分类

### 1. 自动调用（Pre-commit Hooks）

这些脚本在每次 `git commit` 时自动执行，确保代码质量：

#### `format-md.py` - Markdown 格式化

**触发时机**：提交包含 `.md` 或 `.mdc` 文件时

**功能**：

- 自动格式化 Markdown 文件
- 修复可修复的格式问题（空行、缩进等）
- 与 `.markdownlint.json` 配置保持一致

**配置位置**：`.pre-commit-config.yaml` → `markdown-format`

**使用场景**：

- ✅ 每次提交时自动运行（无需手动调用）
- ✅ 确保所有 Markdown 文件格式统一

**手动调用**（如需要）：

```bash
python scripts/format-md.py [文件或目录]
```

#### `lint-md.py` - Markdown 格式检查

**触发时机**：提交包含 `.md` 或 `.mdc` 文件时

**功能**：

- 检查 Markdown 格式问题（标题层级、代码块语言标签等）
- 验证项目特定规则（文件名格式、标题跳级等）
- 发现错误则阻止提交

**配置位置**：`.pre-commit-config.yaml` → `markdown-lint`

**使用场景**：

- ✅ 每次提交时自动运行（无需手动调用）
- ✅ 在 CI 中验证（`.github/workflows/lint-markdown.yml`）

**手动调用**（如需要）：

```bash
# 仅检查，不修复
python scripts/lint-md.py [文件或目录] --check

# 检查并显示详细信息
python scripts/lint-md.py [文件或目录]
```

#### `lint-rules.py` - 规则文件质量验证

**触发时机**：提交包含规则文件（`.md` 或 `.mdc`）时

**功能**：

- 验证规则文件格式（文件名、标题层级、代码示例等）
- 检查精简版规则的 token 消耗
- 验证规则文件结构完整性

**配置位置**：`.pre-commit-config.yaml` → `rule-lint`

**使用场景**：

- ✅ 每次提交规则文件时自动运行
- ✅ 在 CI 中验证（`.github/workflows/lint-markdown.yml`）
- ✅ 创建新规则文件后手动验证

**手动调用**（如需要）：

```bash
# 检查规则文件
python scripts/lint-rules.py [文件或目录] --check

# 检查并输出 JSON 格式
python scripts/lint-rules.py [文件或目录] --json
```

### 2. CI/CD 中使用

这些脚本在 GitHub Actions 中自动运行：

#### `generate-pr-report.py` - PR 质量报告生成

**触发时机**：创建或更新 Pull Request 时

**功能**：

- 生成 PR 质量报告
- 统计变更文件、验证结果
- 计算质量评分
- 自动评论到 PR

**配置位置**：`.github/workflows/pr-quality-gate.yml`

**使用场景**：

- ✅ PR 创建/更新时自动运行
- ✅ 帮助审查者了解 PR 质量

**手动调用**（如需要）：

```bash
# 生成 PR 报告
python scripts/generate-pr-report.py \
  --base <base-sha> \
  --head <head-sha>

# 输出 JSON 格式
python scripts/generate-pr-report.py --json
```

### 3. 手动调用（开发/维护时）

这些脚本需要手动调用，用于特定任务：

#### `calculate-tokens.py` - Token 计算

**触发时机**：创建或修改精简版规则时

**功能**：

- 计算规则文件的 token 消耗
- 对比完整版和精简版的 token 数
- 验证精简版是否达到 70-80% 的减少目标

**使用场景**：

- ✅ 创建精简版规则后验证 token 消耗
- ✅ 在 CI 中可选验证（`.github/workflows/lint-markdown.yml`）
- ✅ 优化规则文件时评估 token 影响

**使用示例**：

```bash
# 计算单个文件的 token
python scripts/calculate-tokens.py full-rules/ide-layer/rulesets/01-general.mdc

# 对比完整版和精简版
python scripts/calculate-tokens.py --compare \
  full-rules/ide-layer/rulesets/01-general.mdc \
  .concise-rules/ide-layer/01-general.mdc

# 计算目录下所有文件
python scripts/calculate-tokens.py full-rules/ide-layer/rulesets/

# 输出 Markdown 报告
python scripts/calculate-tokens.py --markdown [文件或目录]
```

#### `validate-mdc.py` - MDC 格式验证

**触发时机**：创建或修改 `.mdc` 文件时

**功能**：

- 验证 MDC 文件的 frontmatter 格式
- 检查必需字段（description、globs 等）
- 验证 YAML 语法

**使用场景**：

- ✅ 创建新的 `.mdc` 规则文件后验证
- ✅ 修改 frontmatter 后验证
- ✅ 批量验证所有 `.mdc` 文件

**使用示例**：

```bash
# 验证单个文件
python scripts/validate-mdc.py full-rules/ide-layer/rulesets/01-general.mdc

# 验证目录下所有文件
python scripts/validate-mdc.py full-rules/ide-layer/rulesets/
```

#### `migrate-to-mdc.py` - MDC 格式迁移

**触发时机**：一次性迁移任务（从 `.md` 迁移到 `.mdc`）

**功能**：

- 将 `.md` 规则文件转换为 `.mdc` 格式
- 自动添加 frontmatter 元数据
- 根据文件路径和内容推断元数据

**使用场景**：

- ⚠️ 一次性迁移任务（项目已迁移完成）
- ⚠️ 批量转换遗留的 `.md` 文件

**使用示例**：

```bash
# 预览迁移操作（不实际修改）
python scripts/migrate-to-mdc.py [文件或目录] --dry-run

# 执行迁移
python scripts/migrate-to-mdc.py [文件或目录]

# 强制覆盖已存在的 .mdc 文件
python scripts/migrate-to-mdc.py [文件或目录] --force
```

## 使用场景总结

### 日常开发

**自动运行**（无需手动调用）：

- `format-md.py` - 提交时自动格式化
- `lint-md.py` - 提交时自动检查
- `lint-rules.py` - 提交规则文件时自动验证

**需要手动调用**：

- `calculate-tokens.py` - 创建精简版规则后验证 token
- `validate-mdc.py` - 创建新 `.mdc` 文件后验证格式

### CI/CD 流程

**自动运行**：

- `lint-md.py` - 在 `.github/workflows/lint-markdown.yml` 中运行
- `lint-rules.py` - 在 `.github/workflows/lint-markdown.yml` 中运行
- `calculate-tokens.py` - 在 `.github/workflows/lint-markdown.yml` 中可选运行
- `generate-pr-report.py` - 在 `.github/workflows/pr-quality-gate.yml` 中运行

### 维护任务

**一次性任务**：

- `migrate-to-mdc.py` - 迁移任务（已完成）

**定期检查**：

- `validate-mdc.py` - 验证所有 `.mdc` 文件格式
- `calculate-tokens.py` - 验证精简版规则 token 消耗

## 快速参考

### 提交前检查清单

在提交代码前，确保：

1. ✅ **Pre-commit hooks 已安装**：

   ```bash
   pre-commit install
   pre-commit install --hook-type commit-msg
   ```

2. ✅ **自动格式化会运行**（`format-md.py` 自动执行）

3. ✅ **自动检查会运行**（`lint-md.py` 和 `lint-rules.py` 自动执行）

4. ✅ **手动验证**（如创建了新规则）：

   ```bash
   # 验证 token 消耗（如创建了精简版规则）
   python scripts/calculate-tokens.py --compare [完整版] [精简版]
   
   # 验证 MDC 格式（如创建了 .mdc 文件）
   python scripts/validate-mdc.py [文件]
   ```

### 创建新规则文件流程

1. **创建规则文件**（`.mdc` 格式）

2. **验证格式**：

   ```bash
   python scripts/validate-mdc.py [新文件]
   python scripts/lint-rules.py [新文件] --check
   ```

3. **如创建了精简版，验证 token**：

   ```bash
   python scripts/calculate-tokens.py --compare [完整版] [精简版]
   ```

4. **提交**（pre-commit hooks 会自动运行）

### 故障排查

**如果 pre-commit hooks 未运行**：

```bash
# 检查 hooks 是否安装
ls -la .git/hooks/ | grep pre-commit

# 重新安装
pre-commit install
pre-commit install --hook-type commit-msg

# 手动运行所有检查
pre-commit run --all-files
```

**如果脚本执行失败**：

```bash
# 检查 Python 环境
python --version  # 需要 Python 3.10+

# 检查依赖
uv sync  # 或 pip install -r requirements.txt

# 检查脚本权限
chmod +x scripts/*.py
```

## 相关文档

- [Pre-commit 配置说明](../PRE_COMMIT_RULES.md)
- [规则编写指南](./rule-writing-guide.md)
- [Git 仓库管理规范](../full-rules/ide-layer/rulesets/05-git-repository.mdc)
