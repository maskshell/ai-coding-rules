# AI Coding Rules

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**中文** | [English](README.md)

- 分层的 AI Rules 配置示例，满足不同层面的 AI 编码助手需求。
- 同时配置了元规则（编写规则的规则），方便从 AI 生成新类型的规则。

## 目录结构

```text
ai-coding-rules/
├── full-rules/                         # 完整版规则（MDC，含文档和模板）
│   ├── ide-layer/
│   │   └── rulesets/                   # IDE 层规则（最通用）
│   └── project-templates/              # 项目模板（React/Vue/Python/全栈 等）
├── .concise-rules/                     # 精简版规则（MDC，推荐日常使用）
│   ├── ide-layer/                      # IDE 层精简规则
│   └── project-templates/              # 项目层精简规则
├── .cursor/
│   └── rules/                          # 本仓库自身使用的项目级规则（MDC）
├── scripts/                            # 自动化脚本（格式化 / 校验 / 迁移 / 报告）
├── tests/                              # 脚本对应的测试代码（pytest）
├── docs/                               # 指导性文档与技术说明
│   ├── rule-writing-guide.md           # 规则编写指南
│   ├── ai-coding-tools.md              # AI 编码工具推荐（旧版）
│   ├── vibe-coding-tools.md            # AI 编码工具推荐（新版，聚焦本仓库）
│   ├── tech-stack-recommendation.md    # 技术栈推荐与选型建议
│   ├── mdc-frontmatter-spec.md         # MDC frontmatter 规范
│   └── mdc-conditional-mode-analysis.md# MDC 条件模式分析
├── .github/
│   └── workflows/                      # CI 工作流（Markdown / 规则 / PR 质量门禁）
├── .pre-commit-config.yaml             # pre-commit 钩子配置
├── PRE_COMMIT_RULES.md                 # pre-commit 配置说明
├── .markdownlint.json                  # Markdown 格式校验规则
├── .prettierrc.yaml                    # Prettier 配置（JSON/YAML）
├── pyproject.toml                      # Python 项目与 Ruff 配置
├── uv.lock                             # uv 依赖锁定文件
├── IMPROVEMENT_PLAN.md                 # 改进计划与实施进度
├── README.md                           # 英文说明
├── README.cn.md                        # 中文说明
├── CONTRIBUTING.md                     # 贡献指南
├── CHANGELOG.md                        # 更新日志
└── LICENSE                             # MIT 许可证
```

## 双轨制规则

本项目提供**两套规则系统**，平衡可读性与执行效率：

### ⚡ 精简版（.concise-rules/）【推荐日常使用】

- **用途**：AI 执行、提高效率、降低成本
- **特点**：简洁、可操作、token 消耗减少 73%
- **适用场景**：日常开发、AI 辅助编程
- **Token 消耗**：~700-1,000 tokens
- **文件数量**：13 个规则文件
- **快速开始**：

  ```bash
  # 1. 复制 IDE 层规则到全局配置（适用于所有项目）
  mkdir -p ~/.cursor/rules
  cp .concise-rules/ide-layer/* ~/.cursor/rules/
  
  # 2. 复制项目模板规则到项目目录（仅适用于当前项目）
  # 进入你的项目目录后执行：
  mkdir -p .cursor/rules
  cp /path/to/ai-coding-rules/.concise-rules/project-templates/react-app/* .cursor/rules/
  ```

### 📦 完整版（full-rules/）

- **用途**：人类阅读、学习理解、团队培训
- **特点**：详细、全面、包含丰富示例
- **适用场景**：学习规则设计思路、制定团队规范、深度理解
- **Token 消耗**：~2,600-3,900 tokens
- **文件数量**：21 个规则文件，总计 2,998 行
- **使用指南**：
  - [IDE层使用说明](./full-rules/ide-layer/README.md)
  - [规则编写指南](./docs/rule-writing-guide.md)
  - [AI 编码工具推荐](./docs/ai-coding-tools.md)

**选择建议**：

- **新用户**：先浏览完整版理解规则设计思路，切换到精简版日常使用
- **有经验的用户**：直接使用精简版，需要时查阅完整版的特定部分

## 使用原则

1. **分层管理**：IDE层（通用）→ 语言层 → 框架层 → 项目层（具体）
2. **优先级**：下层的规则覆盖上层规则
3. **渐进式**：从预设模板开始，逐步细化

## 快速开始

### 关于 Cursor 规则目录

**重要**：Cursor IDE 的官方规则目录是 `~/.cursor/rules/`（全局规则）和 `.cursor/rules/`（项目规则）。

- **全局规则**：`~/.cursor/rules/` - 适用于所有项目
- **项目规则**：`.cursor/rules/` - 仅适用于当前项目（纳入版本控制）

### 步骤 1：安装 IDE 层规则

将 IDE 层规则复制到 Cursor 配置目录：

```bash
# 使用精简版（推荐）
# 注意：Cursor IDE 官方规则目录是 ~/.cursor/rules/
mkdir -p ~/.cursor/rules
cp .concise-rules/ide-layer/* ~/.cursor/rules/

# 或使用完整版
cp full-rules/ide-layer/rulesets/* ~/.cursor/rules/
```

### 步骤 2：添加项目模板规则

根据项目类型，复制对应的模板规则到项目根目录：

```bash
# 进入你的项目目录
cd /path/to/your/project

# 创建 .cursor/rules 目录（Cursor 官方规则目录）
mkdir -p .cursor/rules

# 复制项目模板规则（以 React 为例）
cp /path/to/ai-coding-rules/.concise-rules/project-templates/react-app/* .cursor/rules/
```

### 步骤 3：自定义项目规则

在项目的 `.cursor/rules/` 目录中添加项目特定的规则文件。

**提示**：使用符号链接可以保持规则同步更新：

```bash
# 使用符号链接（推荐）
# 注意：Cursor IDE 官方规则目录是 ~/.cursor/rules/
mkdir -p ~/.cursor/rules
ln -s /path/to/ai-coding-rules/.concise-rules/ide-layer/* ~/.cursor/rules/
```

## 详细文档

- [IDE层使用说明](./full-rules/ide-layer/README.md)
- [React应用](./full-rules/project-templates/react-app/docs/coding-standards.md)
- [Vue应用](./full-rules/project-templates/vue-app/docs/coding-standards.md)
- [Python后端](./full-rules/project-templates/python-backend/docs/coding-standards.md)
- [全栈项目](./full-rules/project-templates/fullstack-monorepo/docs/coding-standards.md)
- [规则编写指南（含敏捷和设计模式指导）](./docs/rule-writing-guide.md)

## 使用 AI 生成新类型规则的提示词示例

当你希望基于现有元规则生成新的规则文件（例如为某个框架或工具新增一套规范），只需要告诉 AI「目标」和「应遵守哪些规则文件」，无需在提示词中重复具体格式细节。

```text
你是本仓库的规则协作者，请严格遵守
`.cursor/rules/meta-rules.mdc` 中的元规则，
以及 `full-rules/ide-layer/rulesets/` 的风格，
为「{技术栈/场景名}」生成一套新的规则（包含完整版和精简版）。

要求：
- 使用与现有规则一致的 MDC 格式和结构
- 文件命名、frontmatter、目录层级、精简版转换等细节都按 meta-rules 执行
- 先给出目录大纲，再补全各小节内容
```

## 🔧 工具推荐

为了获得更好的 AI 编码体验，我们推荐使用以下工具：

- **[Context7 MCP Server](https://github.com/upstash/context7)** ⭐⭐⭐⭐⭐
  - 实时获取最新 API 文档和代码示例
  - 消除 AI 幻觉，确保代码准确性
  - 降低代码错误率 55%
  - **系统要求**: Node.js ≥ v18.0.0
  - **快速安装**: `npx -y @upstash/context7-mcp --api-key YOUR_API_KEY`
  - **配置**: [详细配置指南](./docs/ai-coding-tools.md#context7-mcp-server-)

- **[ast-grep](https://ast-grep.github.io/)** ⭐⭐⭐⭐☆
  - 基于 AST 的代码搜索和重构工具
  - 验证 AI 生成代码的质量
  - 支持 40+ 种编程语言
  - **安装**: `npm i -g @ast-grep/cli`
  - **配置**: [详细配置指南](./docs/ai-coding-tools.md#ast-grep-)

- **[Knowledge Graph Memory Server](https://github.com/modelcontextprotocol/servers/tree/main/src/memory)** ⭐⭐⭐⭐☆
  - 跨会话保持项目上下文
  - 积累项目知识和经验
  - 适合长期项目开发
  - **安装**: `npm install @modelcontextprotocol/server-memory`
  - **配置**: [详细配置指南](./docs/ai-coding-tools.md#knowledge-graph-memory-server-)

详细使用指南请参考 [AI 编码工具推荐指南](./docs/ai-coding-tools.md)。

## 如何贡献

如果你想添加新的项目模板或改进现有规则，请参考：

- [贡献指南](./CONTRIBUTING.md) - 了解贡献流程和规范
- [规则编写指南](./docs/rule-writing-guide.md) - 详细的规则编写说明

规则编写指南包含：

- 规则的分层架构和优先级
- 文件命名和组织规范
- 敏捷开发原则的表达方式
- 软件设计模式的层次区分
- 创建新模板的完整流程
- 常见错误及避免方法

## 许可证

本项目采用 [MIT License](./LICENSE) 许可证。
