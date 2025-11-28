# AI 编码工具兼容性指南

本文档说明了本项目的规则集如何与各种 AI 编码工具兼容。

## 重要提示：`.cursorrules` 已废弃

**`.cursorrules` 已被 Cursor IDE 废弃。** 本项目已迁移到现代的 `.cursor/rules/` 系统，使用 `.mdc` 文件。

**迁移状态**：✅ 完成

- 所有规则已迁移到 `.cursor/rules/*.mdc` 文件
- 项目遵循 Cursor 推荐的结构

## 当前项目结构

本项目使用模块化规则系统：

```text
vibe-coding/
├── full-rules/                    # 完整版规则（人类阅读）
│   ├── ide-layer/
│   │   └── rulesets/              # IDE 层规则（.mdc 文件）
│   └── project-templates/         # 项目模板规则
├── .concise-rules/                # 精简版规则（AI 执行，推荐日常使用）
│   ├── ide-layer/
│   └── project-templates/
└── .cursor/
    └── rules/                     # 项目级规则（如需要）
```

## 工具特定兼容性

### Cursor IDE ✅

**状态**：完全兼容

**使用的文件**：

- `.cursor/rules/*.mdc` - 详细规则文件
- 支持 `full-rules/` 和 `.concise-rules/` 目录中的规则

**格式**：带 frontmatter 的 Markdown（YAML）

```yaml
---
description: 规则描述
globs:
- '**/*'
alwaysApply: true
tags:
- general
version: 1.0.0
---
```

**工作原理**：Cursor 自动加载 `.cursor/rules/` 目录中的所有 `.mdc` 文件。

**注意**：`.cursorrules` 已被 Cursor 废弃。本项目使用现代的 `.cursor/rules/` 系统，使用 `.mdc` 文件。

**推荐使用**：

- **日常开发**：使用 `.concise-rules/` 中的精简版规则（token 消耗更少）
- **学习和理解**：参考 `full-rules/` 中的完整版规则（包含详细说明）

**配置示例**：

```bash
# 复制 IDE 层规则到全局配置（适用于所有项目）
mkdir -p ~/.cursor/rules
cp .concise-rules/ide-layer/* ~/.cursor/rules/

# 复制项目模板规则到项目目录（仅适用于当前项目）
mkdir -p .cursor/rules
cp .concise-rules/project-templates/react-app/* .cursor/rules/
```

### GitHub Copilot ✅

**状态**：兼容

**使用的文件**：

- `.github/copilot-instructions.md` - Copilot 特定指令

**格式**：Markdown

**工作原理**：GitHub Copilot 从仓库根目录读取 `.github/copilot-instructions.md`。

**注意**：确切的文件位置和命名约定可能有所不同。有些来源建议使用 `.copilot/instructions.md` 或仓库根目录的 `.copilot-instructions.md`。`.github/copilot-instructions.md` 位置在实践中常用。

**创建示例**：

```markdown
# 项目编码规范

## 代码风格

- 使用 TypeScript，启用严格模式
- 使用 ESLint 和 Prettier 进行代码格式化
- 函数保持单一职责

## 测试

- 所有新功能必须包含测试
- 使用 Jest 作为测试框架
```

### Anthropic Claude Code ✅

**状态**：兼容（社区约定）

**使用的文件**：

- `.claude.md` - Claude 特定指令

**格式**：Markdown

**工作原理**：Claude Code 在配置后可以读取 `.claude.md`。这是社区约定，而非官方标准。

**注意**：Anthropic 的官方文档可能没有明确指定 `.claude.md` 作为标准配置文件。这个约定已被社区基于实际使用模式采用。

**创建示例**：

```markdown
# 项目开发规范

## 开发原则

- 优先实现 MVP，验证核心流程后再完善细节
- 每个功能完成后立即进行基本测试
- 保持代码可随时发布状态

## 代码质量

- 函数保持单一职责
- 优先可读性，其次性能
- 提供有用的错误信息
```

### OpenAI Codex / ChatGPT Code Interpreter ⚠️

**状态**：部分兼容

**使用的文件**：

- `.ai-rules.md` - 通用 AI 助手规则
- `.cursor/rules/*.mdc` - 规则文件（如果工具支持）

**格式**：Markdown

**工作原理**：这些工具通常需要显式指令或上下文注入。`.ai-rules.md` 文件可以在提示中引用。

**建议**：在提示中包含规则引用，或使用支持基于文件的配置的工具。

### Google Gemini CLI ⚠️

**状态**：部分兼容

**使用的文件**：

- `.ai-rules.md` - 通用 AI 助手规则

**格式**：Markdown

**工作原理**：类似于 OpenAI 工具，需要显式上下文。`.ai-rules.md` 文件可以包含在提示中。

**建议**：在调用 Gemini CLI 时，将 `.ai-rules.md` 文件作为上下文使用。

## 最佳实践

### 1. 保持规则同步

更新规则时：

1. 更新 `.cursor/rules/` 中的特定 `.mdc` 文件
2. 如果更改影响核心原则，更新工具特定文件（`.github/copilot-instructions.md`、`.claude.md`、`.ai-rules.md`）
3. 同时更新 `full-rules/` 和 `.concise-rules/` 中的对应文件

### 2. 规则组织

- **核心规则**（语言、工作流、测试）→ 更新所有工具特定文件
- **工具特定规则**（记忆工具、ast-grep）→ 仅更新相关文件
- **元规则**（规则管理）→ 仅更新 `.cursor/rules/` 文件

### 3. 测试兼容性

测试规则是否被应用：

1. **Cursor**：检查 AI 建议是否遵循规则
2. **GitHub Copilot**：审查生成的代码建议
3. **Claude Code**：使用代码生成请求进行测试
4. **其他工具**：在上下文中包含规则文件并验证输出

## 维护

### 添加新规则

1. 在 `.cursor/rules/` 中创建或更新 `.mdc` 文件
2. 如果是核心规则，更新工具特定文件
3. 同时创建完整版（`full-rules/`）和精简版（`.concise-rules/`）

### 更新现有规则

1. 更新源 `.mdc` 文件
2. 如果更改影响核心原则，更新工具特定文件以反映更改
3. 同时更新完整版和精简版

### 删除规则

1. 删除或更新 `.mdc` 文件
2. 从工具特定文件中删除

## 工具特定说明

### Cursor IDE

- 支持带 frontmatter 的 `.mdc` 文件（YAML 元数据）
- 自动从 `.cursor/rules/` 目录加载规则
- `alwaysApply: true` 确保规则始终激活
- `globs` 属性可以指定文件模式以进行条件规则应用
- 替代方案：`AGENTS.md` 文件可以用作简化的单文件方法

### GitHub Copilot

- 读取 `.github/copilot-instructions.md`
- 指令应该简洁且可操作

### Claude Code

- 配置后可以读取 `.claude.md`
- 偏好清晰、结构化的指令
- 支持 Markdown 格式

### OpenAI / Google 工具

- 需要显式上下文注入
- 使用 `.ai-rules.md` 作为参考
- 可能需要在提示中包含规则

## 未来增强

考虑添加：

- 支持这些工具的 JSON/YAML 配置文件
- 随着新工具的出现，添加工具特定的配置文件
- 自动同步脚本以保持文件同步
- 验证脚本以确保规则一致性

## 验证说明

### 已验证信息

- ✅ **Cursor IDE**：`.cursor/rules/` 目录和 `.mdc` 文件是官方支持的
- ✅ **Cursor IDE**：`.cursorrules` 已被新系统废弃
- ⚠️ **GitHub Copilot**：`.github/copilot-instructions.md` 常用，但确切文件位置可能有所不同
- ⚠️ **Claude Code**：`.claude.md` 是社区约定，未正式记录
- ⚠️ **OpenAI/Google 工具**：需要手动上下文注入，没有标准的基于文件的配置

### 建议

1. **对于 Cursor IDE**：继续使用 `.cursor/rules/*.mdc` 系统（当前方法是正确的）
2. **对于 GitHub Copilot**：监控官方文档以了解指令文件位置的任何更改
3. **对于 Claude Code**：考虑记录 `.claude.md` 是社区约定
4. **对于其他工具**：保留 `.ai-rules.md` 作为需要手动上下文的工具的通用后备

## 本项目特定说明

### 规则文件结构

本项目提供两种规则版本：

1. **完整版**（`full-rules/`）：
   - 用途：人类阅读、学习、团队培训
   - 特点：详细、全面、丰富的示例
   - Token 消耗：约 2,600-3,900 tokens

2. **精简版**（`.concise-rules/`）：
   - 用途：AI 执行，提高效率，降低成本
   - 特点：简洁、可操作，token 减少 73%
   - Token 消耗：约 700-1,000 tokens
   - **推荐用于日常开发**

### 使用建议

- **新用户**：先浏览完整版以了解规则设计概念，然后切换到精简版用于日常使用
- **有经验的用户**：直接使用精简版，需要时参考完整版的特定部分

### 规则文件位置

- **IDE 层规则**：`full-rules/ide-layer/rulesets/` 和 `.concise-rules/ide-layer/`
- **项目模板规则**：`full-rules/project-templates/{project}/.cursor/rules/` 和 `.concise-rules/project-templates/{project}/`

## 参考资料

- [Cursor Rules 文档](https://cursor.sh/docs)
- [GitHub Copilot 自定义指令](https://docs.github.com/en/copilot/customizing-github-copilot/customizing-github-copilot-settings-for-your-enterprise)
- [Anthropic Claude 文档](https://docs.anthropic.com)
- [本项目规则编写指南](./rule-writing-guide.md)
- [本项目 AI 编码工具推荐](./ai-coding-tools.md)
