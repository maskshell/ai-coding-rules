# 技术栈选型建议：Python vs Node.js

**文档版本**: 1.1.0  
**最后更新**: 2025-11-26  
**适用场景**: 本地开发环境下的自动化工具开发  
**更新说明**: 已更新为使用 `uv` 作为 Python 包管理工具

---

## 一、需求分析

根据改进计划，需要开发的工具包括：

1. **Token 计算器** - 计算规则文件的 token 消耗
2. **规则 Linter** - 验证规则格式、结构、内容质量
3. **精简版转换辅助工具** - 辅助完整版到精简版的转换
4. **双轨制验证工具** - 验证完整版和精简版的配对
5. **CI/CD 集成** - GitHub Actions 工作流

---

## 二、技术栈对比

### 2.1 Python 方案

#### ✅ 优势

1. **Token 计算的最佳选择**
   - `tiktoken` 是 OpenAI 官方维护的 Python 库
   - 支持 `cl100k_base` 编码（GPT-4、Claude 使用）
   - 准确、可靠、性能好
   - 改进计划中已明确使用 `tiktoken`

2. **文本处理能力强**
   - 内置 `re` 模块（正则表达式）
   - `pathlib` 提供优雅的文件操作
   - 字符串处理简单直观

3. **Markdown 处理**
   - `markdown`、`markdown-it-py` 等库成熟
   - `mistune` 性能优秀
   - `python-frontmatter` 支持 frontmatter 解析

4. **CI/CD 集成简单**
   - GitHub Actions 原生支持 Python
   - `uv` 提供快速的包管理和环境管理
   - 无需额外构建步骤

5. **代码简洁**
   - 适合快速开发脚本
   - 代码可读性强
   - 维护成本低

#### ⚠️ 劣势

1. **生态系统**
   - 前端工具生态不如 Node.js 丰富
   - 如果未来需要开发 VSCode/Cursor 插件，需要 Node.js

2. **性能**
   - 对于大规模文件处理，可能略慢于 Node.js
   - 但本项目规模小，影响可忽略

---

### 2.2 Node.js 方案

#### ✅ 优势

1. **前端工具生态**
   - 如果未来开发 VSCode/Cursor 插件，必须使用 Node.js
   - `markdownlint`、`prettier` 等工具成熟

2. **GitHub Actions 集成**
   - 同样原生支持
   - `npm install` 简单

3. **性能**
   - 对于 I/O 密集型任务，性能较好

#### ⚠️ 劣势

1. **Token 计算问题**
   - Node.js 的 token 计算库不如 Python 成熟
   - `gpt-tokenizer` 等库可能不够准确
   - 需要验证 `cl100k_base` 编码的准确性

2. **文本处理**
   - 正则表达式支持不如 Python 强大
   - 文件操作 API 相对复杂

3. **依赖管理**
   - `package.json` + `node_modules` 体积较大
   - 对于简单脚本，可能过度工程化

---

## 三、推荐方案：**Python** ✅

### 3.1 推荐理由

1. **Token 计算是核心需求**
   - 改进计划的核心工具是 Token 计算器
   - `tiktoken` 是业界标准，准确可靠
   - 这是 Python 的绝对优势

2. **工具性质匹配**
   - 这些工具本质上是**脚本工具**，不是 Web 应用
   - Python 更适合快速开发、维护脚本
   - 代码简洁，易于理解

3. **改进计划已明确**
   - 改进计划中的示例代码都是 Python
   - 使用 `uv` 进行快速依赖管理
   - 保持一致性很重要

4. **未来扩展性**
   - 如果需要开发 VSCode/Cursor 插件，可以：
     - 使用 Python 脚本作为后端工具
     - 插件调用 Python 脚本（通过命令行）
     - 或使用 Node.js 插件 + Python 子进程

### 3.2 混合方案（可选）

如果未来需要开发 VSCode/Cursor 插件：

```text
Python 脚本（核心工具）
  ├── Token 计算器
  ├── 规则 Linter
  └── 转换工具

Node.js 插件（可选）
  └── VSCode/Cursor 插件
      └── 调用 Python 脚本
```

---

## 四、具体实施建议

### 4.1 项目结构

```text
vibe-coding/
├── scripts/
│   ├── calculate-tokens.py      # Token 计算器
│   ├── lint-rules.py            # 规则 Linter
│   ├── sync-concise.py          # 精简版转换辅助
│   └── verify-sync.py           # 双轨制验证
├── pyproject.toml               # Python 项目配置（uv 使用）
├── uv.lock                      # 依赖锁定文件（uv 自动生成）
└── .github/workflows/
    └── validate.yml              # CI/CD（使用 Python + uv）
```

### 4.2 依赖管理

**pyproject.toml**（推荐使用 uv）:

```toml
[project]
name = "vibe-coding-tools"
version = "0.1.0"
description = "AI Coding Rules automation tools"
requires-python = ">=3.10"
dependencies = [
    "tiktoken>=0.5.0",
    "markdown>=3.4.0",
    "python-frontmatter>=1.0.0",
    "pyyaml>=6.0",
]
```

### 4.3 开发环境设置

**使用 uv**:

```bash
# 安装 uv（如果未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh
# 或使用 pip: pip install uv

# 创建虚拟环境并安装依赖
uv venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 安装依赖（使用 pyproject.toml）
uv sync

# 运行工具（方式 1：激活环境后运行）
python scripts/calculate-tokens.py

# 运行工具（方式 2：使用 uv run，无需激活环境）
uv run python scripts/calculate-tokens.py
```

### 4.4 CI/CD 配置

**使用 uv**:

```yaml
# .github/workflows/validate.yml
name: Validate Rules

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install uv
        uses: astral-sh/setup-uv@v3
        with:
          version: "latest"
      
      - name: Set up Python
        run: uv python install 3.10
      
      - name: Install dependencies
        run: uv sync
        # 或使用: uv pip install -r requirements.txt
      
      - name: Calculate tokens
        run: uv run python scripts/calculate-tokens.py
      
      - name: Lint rules
        run: uv run python scripts/lint-rules.py
```

---

## 五、如果选择 Node.js（不推荐）

如果坚持使用 Node.js，需要解决以下问题：

### 5.1 Token 计算

**选项 1**: 使用 `gpt-tokenizer`

```bash
npm install gpt-tokenizer
```

**问题**：

- 需要验证 `cl100k_base` 编码的准确性
- 可能不如 `tiktoken` 准确

**选项 2**: 调用 Python 脚本

```javascript
const { execSync } = require('child_process');
// 使用 uv run（如果使用 uv）
const tokens = execSync('uv run python scripts/calculate-tokens.py', { encoding: 'utf-8' });
```

**问题**：

- 需要系统安装 Python 和 uv（如果使用 uv）
- 跨平台兼容性问题

### 5.2 项目结构

```text
vibe-coding/
├── scripts/
│   ├── calculate-tokens.js
│   ├── lint-rules.js
│   └── ...
├── package.json
└── node_modules/
```

---

## 六、最终建议

### ✅ **推荐：Python**

**理由**：

1. Token 计算是核心需求，Python + tiktoken 是最佳选择
2. 工具性质是脚本工具，Python 更适合
3. 改进计划已明确使用 Python
4. 代码简洁，维护成本低
5. CI/CD 集成简单

**实施步骤**：

1. 安装 `uv`：`curl -LsSf https://astral.sh/uv/install.sh | sh`
2. 创建 `pyproject.toml` 或 `requirements.txt`
3. 使用 `uv sync` 安装依赖
4. 开发核心工具（Token 计算器、Linter）
5. 集成到 CI/CD（使用 `astral-sh/setup-uv@v3`）

### ⚠️ **如果未来需要插件**

- 开发 VSCode/Cursor 插件时使用 Node.js
- 插件通过命令行调用 Python 脚本
- 或使用 Python 的 HTTP 服务，插件通过 API 调用

---

## 七、总结

| 维度 | Python | Node.js | 推荐 |
|-----|--------|---------|------|
| Token 计算 | ⭐⭐⭐⭐⭐ (tiktoken) | ⭐⭐⭐ (gpt-tokenizer) | **Python** |
| 文本处理 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **Python** |
| 脚本开发 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | **Python** |
| 插件开发 | ⭐⭐ | ⭐⭐⭐⭐⭐ | Node.js |
| CI/CD 集成 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 平手 |
| 维护成本 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | **Python** |

**结论**：**选择 Python**，除非未来需要开发 VSCode/Cursor 插件，再考虑混合方案。

---

**文档维护者**: AI Coding Rules 团队  
**反馈渠道**: [GitHub Issues](https://github.com/maskshell/ai-coding-rules/issues) / [Discussions](https://github.com/maskshell/ai-coding-rules/discussions)
