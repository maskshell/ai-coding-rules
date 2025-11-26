# AI 编码工具推荐指南

本文档介绍可提升 AI 编码效率的工具和 MCP Server，帮助开发者在 AI 辅助编程时获得更好的效果。

## 🎯 工具选择指南

### 快速决策表

| 工具 | 推荐度 | 学习成本 | 核心价值 | 适用场景 |
|------|--------|----------|----------|----------|
| **Context7** | ⭐⭐⭐⭐⭐ | 低 | 实时准确文档查询 | 所有项目 |
| **ast-grep** | ⭐⭐⭐⭐☆ | 中等 | 代码验证与重构 | 中大型项目 |
| **Knowledge Graph Memory Server** | ⭐⭐⭐★☆ | 高 | 跨会话记忆保持 | 长期项目 |
| **Skill 模式** | ⭐⭐★☆☆ | 高 | 工作流程标准化 | 团队开发 |

---

## 工具详解

### 1. Context7 MCP Server ⭐⭐⭐⭐⭐

#### 功能简介

Context7 是一个专为 AI 编程助手设计的 MCP Server，提供实时、版本特定的 API 文档和代码示例，解决 AI 使用过时文档的问题。

#### 核心价值

- **消除 AI 幻觉**：提供准确的最新 API 文档
- **版本精确匹配**：避免 API 版本不兼容
- **实时文档获取**：直接从官方源获取最新信息
- **显著降低错误率**：实测代码错误率降低 55%

#### 在 AI 编码中的应用

##### 场景 1：使用最新 API

```bash
# 不使用 Context7
AI 可能使用过时的 React Query API，导致代码无法运行

# 使用 Context7
AI 自动查询 React Query v5 的最新文档，使用正确的 API
```

##### 场景 2：框架升级

```bash
# 从 Vue 2 升级到 Vue 3
use context7: "compare Vue 2 and Vue 3 composition API differences"

# AI 获取准确的迁移指南和代码示例
```

#### 系统要求

- **Node.js**: 版本 ≥ v18.0.0
- **操作系统**: 支持所有 Node.js 兼容的操作系统（Windows、macOS、Linux）
- **MCP 客户端**: Cursor、Claude Code、VS Code、Windsurf、Augment Code、Kilo Code、Amp Code、Roo Code、Google Antigravity 等

#### 安装与配置

##### 方式 1：通过 npx 直接运行（推荐）

```bash
npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```

##### 方式 2：通过 Smithery 安装

```bash
npx -y @smithery/cli@latest install @upstash/context7-mcp --client claude --key <YOUR_SMITHERY_KEY>
```

##### 获取 API Key

1. 访问 [context7.com/dashboard](https://context7.com/dashboard)
2. 使用 GitHub 账号登录
3. 创建新的 API Key

##### MCP Server 配置

在 Claude Code 中配置：

```bash
claude mcp add --transport http https://mcp.context7.com/mcp --header "CONTEXT7_API_KEY=YOUR_API_KEY"
```

或在配置文件中添加：

```json
{
  "mcpServers": {
    "context7": {
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

##### 客户端特定配置

###### Cursor

添加到 `~/.cursor/mcp.json`

```json
{
  "mcpServers": {
    "context7": {
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

###### Claude Code 配置命令

```bash
claude mcp add context7 https://mcp.context7.com/mcp \
  --env CONTEXT7_API_KEY=YOUR_API_KEY
```

###### VS Code

在设置中添加 MCP 服务器配置（使用 Cline 插件）

#### 在提示中使用

在提示词中添加 `use context7`：

```text
use context7: "How to use React Query v5 useQuery with TypeScript?"
```

或在中文提示中使用：

```text
use context7: "帮我写一个 React Query v5 的 hook，用于获取用户数据"
```

#### 推荐用法

在提示词中添加 `use context7`：

```text
use context7: "帮我写一个 React Query v5 的 hook，用于获取用户数据，包括 loading 和 error 状态"
```

#### 成本与效果

- **ROI**：极高（准确代码 vs 调试错误）
- **学习成本**：极低（直接在提示词中使用）
- **推荐度**：⭐⭐⭐⭐⭐ 所有项目都应该使用

---

### 2. ast-grep ⭐⭐⭐⭐☆

#### 功能简介

ast-grep 是一个基于抽象语法树（AST）的跨语言代码搜索、lint 和重写工具，支持 40+ 种编程语言。它将传统的 grep/sed 概念提升到语法树层面，避免了文本搜索的局限性。

#### 核心价值

- **精准代码搜索**：避免正则表达式带来的误匹配
- **批量代码重构**：安全地进行大规模代码变更
- **自定义 lint 规则**：创建项目特定的代码规范检查
- **代码验证**：验证 AI 生成的代码是否符合规范

#### 在 AI 编码中的应用

**场景 1：验证 AI 生成的代码**

```bash
# 检查是否有不符合命名规范的函数
sg scan --filter='kind(function_definition)' --filter='regex("^[A-Z]")'

# 找到所有未使用的导入
sg scan --pattern='import $_ from "$A";' --filter='not referenced($A)'
```

**场景 2：批量重构 AI 建议的代码**

```yaml
# rewrite.yml
rule:
  pattern: console.log($MSG)
  fix: logger.debug($MSG)

# 执行：sg run -r rewrite.yml -U
```

**场景 3：框架升级**

```bash
# Vue 2 到 Vue 3 的 Options API 转 Composition API
# 创建转换规则，自动转换大量组件
sg run -p 'export default {methods: {$F: $_}}' -r 'const $F = () => {...}'
```

#### 安装与配置

```bash
# macOS
brew install ast-grep

# 其他平台
npm i -g @ast-grep/cli
# 或
cargo install ast-grep --locked
```

#### 在 Claude Code 中的集成

在 `.cursor/rules.md` 中添加：

```markdown
### ast-grep 使用

- 生成代码后，使用 ast-grep 验证命名规范
- 批量重构时使用 ast-grep 确保准确性
```

#### 推荐用法

1. **实时验证**：配置 VS Code 插件，在保存时自动检查
2. **CI/CD 集成**：在提交前自动验证代码质量
3. **AI 代码后处理**：AI 生成代码后立即运行 ast-grep 检查

#### 成本与效果

- **ROI**：高（减少调试时间和错误）
- **学习成本**：中等（需要理解 AST 概念和规则语法）
- **推荐度**：⭐⭐⭐⭐☆ 中大型项目推荐使用

---

### 3. Knowledge Graph Memory Server ⭐⭐⭐★☆

#### 功能简介

基于知识图谱的 MCP Server，为 AI 提供持久的跨会话记忆能力，支持实体-关系-观察值三元组存储和复杂查询。

#### 核心价值

- **跨会话记忆**：AI 记住之前的对话和项目上下文
- **知识积累**：项目经验可以被持续积累和复用
- **团队协作**：共享项目知识图谱
- **上下文连续性**：避免重复解释相同概念

#### 在 AI 编码中的应用

**场景 1：项目架构记忆**

```text
# 第一次对话
Alice: "我们的项目使用微前端架构，主应用是 host-app，子应用有 billing、user-mgmt"
AI: "已记录项目架构"

# 一周后
Bob: "如何在 billing 应用中集成新的支付网关？"
AI: "根据项目架构（微前端），你需要在 billing 子应用中实现，然后通过 shared-components 暴露接口给 host-app"
```

**场景 2：Bug 历史追踪**

```text
# 记录 Bug 修复
User: "修复了用户登录时的 JWT token 刷新问题，原因是 token 过期时间设置错误"
AI: "已记录修复方案"

# 后来遇到相似问题
User: "token 刷新又失败了"
AI: "之前遇到过类似问题（修复 ID: #123），是否检查了 token 过期时间配置？"
```

#### 安装与配置

1. 安装依赖：

```bash
npm install @modelcontextprotocol/server-memory
```

1. 配置 MCP Server（Claude Code）：

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-memory"],
      "env": {
        "MEMORY_FILE_PATH": "./memory.json"
      }
    }
  }
}
```

#### 推荐用法

1. **项目初始化时**：定义核心实体（用户、订单、产品等）和关系
2. **每日开发中**：自动记录重要决策和代码变更
3. **Code Review**：记录 review 意见和改进方案
4. **周报生成**：基于知识图谱自动生成工作汇报

#### 成本与效果

- **ROI**：高（适合长期项目）
- **学习成本**：高（需要设计知识图谱模型）
- **推荐度**：⭐⭐⭐★☆ 长期项目推荐使用

---

### 4. Skill 模式 ⭐⭐★☆☆

#### 功能简介

Claude Code 的 Skill 模式提供可复用的程序化知识，支持动态加载和智能匹配，让 AI 能够完成标准化的工作流程。

#### 核心价值

- **工作流程标准化**：封装常见的开发任务
- **上下文管理**：减少 token 浪费
- **知识复用**：避免重复描述相同任务
- **质量保证**：确保任务执行的一致性

#### 在 AI 编码中的应用

**场景 1：标准化的代码审查**

```typescript
// .claude/skills/code-review.ts
export default {
  name: "code-review",
  description: "按照项目规范进行代码审查",
  instructions: `
    1. 检查代码是否符合编码规范
    2. 检查是否有足够的测试覆盖
    3. 检查命名是否清晰
    4. 检查是否有性能问题
    5. 给出具体的改进建议
  `
}

// 使用：/skill code-review src/components/Button.tsx
```

**场景 2：项目初始化**

```typescript
// .claude/skills/init-react-app.ts
export default {
  name: "init-react-app",
  description: "初始化一个 React TypeScript 项目",
  instructions: `
    1. 检查项目目录是否为空
    2. 运行 npm create vite@latest . --template react-ts
    3. 安装依赖：npm install react-router-dom @tanstack/react-query
    4. 配置 ESLint 和 Prettier
    5. 创建目录结构：src/{components,pages,hooks,utils}
    6. 提交初始代码
  `
}

// 使用：/skill init-react-app
```

#### 使用限制

- **配额限制**：每个账号有一定数量的 skill 使用配额
- **生态成熟度**：目前可用的 skill 还比较少
- **开发成本**：需要学习 skill 的开发模式

#### 成本与效果

- **ROI**：中等（适合高度标准化的团队）
- **学习成本**：高（需要理解 skill 架构）
- **推荐度**：⭐⭐★☆☆ 适合有标准化流程的团队

---

## 工具组合策略

### 基础开发流程

```text
实际需求
   ↓
Context7 查询最新文档
   ↓
AI 生成代码
   ↓
ast-grep 验证代码质量
   ↓
commit & push
```

### 框架升级场景

```text
决策升级
   ↓
Context7 查询新旧版本差异
   ↓
AI 设计迁移方案
   ↓
ast-grep 批量替换旧 API
   ↓
手动验证关键路径
   ↓
commit & push
```

### 长期项目维护

```text
新需求
   ↓
Knowledge Graph 查询历史经验
   ↓
Context7 查询最新文档
   ↓
AI 结合历史知识和最新文档生成代码
   ↓
ast-grep 验证代码质量
   ↓
Knowledge Graph 记录新决策
   ↓
commit & push
```

---

## 实施路线图

### 第一阶段（立即开始）

部署 Context7：

- 安装 Context7 MCP Server
- 训练团队在提示词中使用 `use context7`
- **预期效果**：代码错误率降低 55%

### 第二阶段（2-4 周）

集成 ast-grep：

- 安装 ast-grep CLI 工具
- 创建项目特定的验证规则
- 集成到开发工作流
- **预期效果**：显著提升代码质量

### 第三阶段（1-2 个月）

部署 Knowledge Graph Memory：

- 设计项目知识图谱模型
- 建立知识积累流程
- 培训团队使用习惯
- **预期效果**：团队知识共享，新人上手更快

### 第四阶段（3-6 个月）

开发 Skill 模式：

- 分析标准化工作流程
- 开发定制化 skills
- 集成到日常工作
- **预期效果**：开发效率提升 30%

---

## 总结

| 工具 | 核心价值 | 优先级 | 开始时间 |
|------|----------|--------|----------|
| **Context7** | 代码准确性 | P0 | 立即 |
| **ast-grep** | 代码质量 | P1 | 2-4 周 |
| **Knowledge Graph** | 知识管理 | P2 | 1-2 月 |
| **Skill 模式** | 流程标准化 | P3 | 3-6 月 |

**建议**：从 Context7 开始，根据项目复杂度和团队规模逐步引入其他工具。

---

*本文档根据实际使用经验和官方文档编写，建议定期更新以反映最新实践。*
