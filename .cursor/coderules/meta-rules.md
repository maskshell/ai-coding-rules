# 元规则：如何编写 AI Rules

**用途**: 本文件定义了为 Vibe Coding Rules 项目创建新规则文件的准则，确保规则的一致性、可维护性和实用性。

**优先级**: 当用户要求创建新规则或模板时，必须遵循本文件指导。

---

## 一、分层架构（必须遵循）

### 四层优先级体系

```
IDE层（通用） ← 优先级最低，最抽象
  ↓
语言层（Python/JS/TS等）
  ↓
框架层（React/Vue/FastAPI等）
  ↓
项目层（具体项目） ← 优先级最高，最具体
```

**关键规则**：下层的规则覆盖上层的规则。

### 何时创建哪一层

**创建 IDE 层规则（`ide-layer/rulesets/`）当**：

- 规则适用于所有编程语言和框架
- 规则涉及通用编程原则（代码质量、可读性、安全性）
- 规则是关于 AI 助手行为的偏好

**创建项目层规则（`project-templates/{project}/.cursor/coderules/`）当**：

- 规则特定于某个框架或技术栈
- 规则涉及具体的编码实践和模式
- 需要提供代码示例和详细步骤

**永远不要在 IDE 层放**：

- 语言特定语法规则
- 框架特定模式（如 React Hooks、Vue Composables）
- 项目目录结构

## 二、内容规范

### 1. 文件命名

**必须遵循**：

- 使用两位数字前缀（`01-`、`02-`、`03-`）
- 使用小写字母和短横线（`-`）
- 文件名清晰描述内容

**正确示例**：

```
01-general.md
02-testing.md
01-react-basics.md
02-python-fastapi.md
```

**错误示例**：

```
react.md                    # 缺少数字前缀
01_React_Rules.md           # 使用下划线和大小写混合
01 general rules.md         # 使用空格
```

### 2. 规则组织

每个 `.md` 文件必须包含：

```markdown
# 标题（使用#，不是##）

## 主要分类

### 子分类

- 具体规则
- 具体规则

**示例**:
```代码示例```
```

**不要使用**：

- 一级标题（#）作为分类
- 过深的嵌套（4级以上）

### 3. 规则表述风格

**必须使用**：

- 指导性语言，而非强制性命令
- 正面表述（应该做什么）
- 提供具体示例
- 解释"为什么"（可选但推荐）

**推荐格式**：

```markdown
### 组件命名

- 文件名使用 PascalCase（如 `UserProfile.tsx`）
- 组件名与文件名保持一致

**理由**：保持一致性，便于文件搜索和导入。

**示例**:
```tsx
// Good
export function UserProfile() { ... }

// Bad
export function user_profile() { ... }
```

```

**禁止使用**：
```markdown
❌ 你必须这样命名组件
❌ 错误的命名方式会导致问题
❌ （不提供任何示例）
```

## 三、核心原则表达

### 敏捷开发原则（必须包含）

每个项目层的 `docs/coding-standards.md` 必须包含"开发流程"部分。

**必须包含的敏捷原则**：

1. **MVP 优先**：先让代码工作，再让它干净
2. **快速验证**：每个功能完成后立即测试
3. **小步提交**：保持小的提交粒度
4. **持续重构**：通过重构改善质量，不是一次完美
5. **拥抱变化**：持续调整设计

**项目层标准模板**：

```markdown
## 开发流程

### 开发步骤

1. **先实现基本功能**：让代码能正常工作，完成核心需求
2. **添加类型和验证**：补充类型系统，处理边界情况
3. **优化用户体验**：添加加载状态、错误提示等
4. **编写测试**：单元测试和集成测试
5. **代码审查和重构**：改善代码结构和可读性

### 功能开发原则

- 优先实现 MVP，验证核心流程后再完善细节
- 每个功能完成后手动测试验证
- 保持模块的独立性和可测试性
- 通过重构逐步改善代码质量
- 及时提交代码并保持提交粒度小
```

**IDE 层标准表述**：

```markdown
### 开发流程原则

- 优先交付可工作的最小可行产品（MVP）
- 通过小步迭代和快速反馈验证想法
- 每个功能完成后立即进行基本测试
- 保持代码可随时发布状态
- 拥抱变化，持续调整设计

### 代码演进

- 先让代码工作，再让它干净，最后让它更快
- 通过重构改善代码质量，而不是一次做到完美
- 保持设计简单，需要时再引入复杂度
```

### 软件设计模式（必须区分层次）

**IDE 层（抽象原则）**：

```markdown
### 软件设计原则

- 设计新功能或重构时，寻找并应用该领域的最佳设计模式
- 使用经过验证的架构模式和最佳实践
- 保持模块低耦合、高内聚
- 优先组合而非继承
```

**项目层（具体应用）**：针对框架提供具体模式指导

**React 示例**：

```markdown
### 状态管理

- 小型应用使用 Context + useReducer（Reducer 模式）
- 中大型应用使用 Redux Toolkit（Flux 模式）
- 使用自定义 Hooks 封装可复用逻辑（Hooks 模式）
```

**Vue 示例**：

```markdown
### 可复用逻辑

- 提取可复用的状态逻辑到 Composables（Composables 模式）
- 全局状态使用 Pinia Store（Store 模式）
- 跨层级传递数据使用 Provide/Inject
```

**Python 后端示例**：

```markdown
### 架构模式

- 使用 Repository 模式封装数据访问
- Service 层封装业务逻辑，保持路由处理函数简洁
- 使用依赖注入管理数据库会话生命周期
```

**禁止**：在 IDE 层列举具体设计模式（如"使用工厂模式"、"使用单例模式"）。

### 错误模式的表达

当描述不应该做什么时，使用"避免"而非"禁止"：

```markdown
✅ 推荐：避免过度工程化，保持简单
✅ 推荐：避免深层次的组件嵌套
❌ 不推荐：禁止过度工程化
❌ 不推荐：不能使用深层次的嵌套
```

## 四、创建新模板的流程

### 步骤 1：确定模板类型

**需要判断**：

- 是全新的技术栈吗？（如 Svelte、Django）
- 是现有模板的变体吗？（如 React + MobX 替代 Redux）
- 是组合多个现有技术吗？（如微前端架构）

### 步骤 2：创建目录结构

**标准结构**：

```bash
project-templates/new-framework-app/
├── .cursor/
│   └── coderules/          # AI执行的规则
│       ├── 01-{framework}-basics.md
│       ├── 02-{framework}-advanced.md
│       └── ...
└── docs/
    └── coding-standards.md  # 人类阅读的完整规范
```

**coderules 文件组织**：

- `01-{framework}-basics.md`：基础概念、项目结构、命名规范
- `02-{framework}-architecture.md`：架构设计、状态管理、组件通信
- `03-{framework}-api.md`：API调用、数据获取、错误处理
- `...`：其他特定主题

**必须遵循数字前缀**，确保加载顺序合理。

### 步骤 3：编写 AI 规则（.cursor/coderules/*.md）

**内容要求**：

1. 参考现有模板的专业度和格式
2. 遵循本元规则的所有规范
3. 提供清晰的代码示例
4. 包含开发流程部分（敏捷原则）

**典型规则文件结构**：

```markdown
# {技术栈} {主题} 规范

## 主要概念

### 子概念 1

- 规则 1
- 规则 2

**示例**:
```代码示例```

## 主要概念 2

...

## 开发流程

### 开发步骤

1. 步骤 1
2. 步骤 2

### 功能开发原则

- 原则 1
- 原则 2
```

**开发流程部分是必需的**，必须包含敏捷原则的具体步骤。

### 步骤 4：编写人类文档（docs/coding-standards.md）

**内容要求**：

1. 完整的项目架构说明
2. 详细的技术栈选择
3. 每个规则的解释和背景
4. 常见问题的解决方案
5. 工具配置和调试指南
6. 代码片段和示例项目

**比 AI 规则更详细**，提供深度解释。

### 步骤 5：测试模板

**验证内容**：

1. 使用 Cursor 新建项目
2. 复制 `.cursor/coderules/` 到项目
3. 让 AI 实现一个小功能（如用户登录）
4. 检查生成的代码是否符合预期
5. 根据结果调整规则

### 步骤 6：更新文档

**必须更新**：

- 根目录 README.md：在目录结构中添加新模板
- docs/rule-writing-guide.md：在参考资料中添加新模板链接
- 在提交信息中明确说明新增内容

## 五、验证清单

创建或更新规则文件前，使用此清单检查：

### 文件规范

- [ ] 文件名有数字前缀（如 `01-`）
- [ ] 文件名使用小写和短横线（如 `react-basics.md`）
- [ ] 放在正确的层次（IDE层或项目层）
- [ ] 同一层次的文件前缀不重复

### 内容规范

- [ ] 遵循职责单一原则（不混合层次）
- [ ] 提供具体示例代码
- [ ] 规则表述清晰、无歧义
- [ ] 必要时解释"为什么"
- [ ] 使用指导性语言而非强制性命令

### 敏捷原则

- [ ] 项目层包含"开发流程"章节
- [ ] 开发步骤至少包含 5 步（功能 → 类型 → 验证 → 测试 → 重构）
- [ ] 包含 MVP 优先原则
- [ ] 包含快速验证和小步提交原则
- [ ] 包含持续重构原则

### 设计模式

- [ ] IDE层只包含抽象原则（不列举具体模式）
- [ ] 项目层提供具体模式指导
- [ ] 模式指导与框架匹配（React用Hooks/Reducer，Vue用Composables/Pinia）
- [ ] 不教条化，提供选择依据

### 文档更新

- [ ] 根目录 README.md 更新目录结构（新项目）
- [ ] 根目录 README.md 更新详细文档链接
- [ ] docs/rule-writing-guide.md 的参考资料章节更新
- [ ] 提交信息使用 Conventional Commits 格式

## 六、常见错误及避免

### 错误 1：在 IDE 层放框架特定规则

**错误示例**（在 `ide-layer/rulesets/01-general.md`）：

```markdown
❌ 错误
### React Hooks 使用

- 使用 useState 管理组件状态
- 使用 useEffect 处理副作用
```

**为什么错误**：IDE层是所有项目通用的，不应包含框架特定内容。

**正确做法**：

```markdown
✅ 正确（在 IDE 层）
### 代码质量

- 函数保持单一职责，一个函数做一件事
```

```markdown
✅ 正确（在项目层）
project-templates/react-app/.cursor/coderules/01-react-basics.md:

### Hooks 使用

- 使用 useState 管理组件状态
```

### 错误 2：规则过于教条

**错误示例**：

```markdown
❌ 错误
### 状态管理

- 必须使用 Redux，不能使用 Context
- 所有组件必须写成函数组件
```

**为什么错误**：过于绝对，没有考虑不同场景。

**正确做法**：

```markdown
✅ 正确
### 状态管理

- 小型应用：优先使用 Context + useReducer（简单、无额外依赖）
- 中大型应用：使用 Redux Toolkit 或 Zustand（更好的调试、中间件支持）
- 根据应用复杂度和团队协作需求选择
```

### 错误 3：缺少具体示例

**错误示例**：

```markdown
❌ 错误
### 组件命名

- 组件应该有描述性的名字
- 名字应该清晰表达用途
```

**为什么错误**：太模糊，AI 无法确定具体怎么做。

**正确做法**：

```markdown
✅ 正确
### 组件命名

- 组件文件名使用 PascalCase（如 `UserProfile.tsx`）
- 组件名与文件名一致

**示例**:
```tsx
// Good
export function UserProfile() { ... }
export function ProductCard() { ... }

// Bad
export function user_profile() { ... }
export function Card() { ... }  // 太泛化
```

```

### 错误 4：缺少敏捷原则

**错误示例**（在项目层的 docs/coding-standards.md）：
```markdown
❌ 错误（缺少开发流程章节）
## 技术栈

...

## 命名规范

...
```

**为什么错误**：没有指导如何通过迭代方式开发。

**正确做法**：

```markdown
✅ 正确
## 技术栈

...

## 命名规范

...

## 开发流程

### 开发步骤

1. **先实现基本功能**：让代码能正常工作
2. **添加类型验证**：补充类型系统
3. **优化用户体验**：添加加载状态和错误提示
4. **编写测试**：单元测试和集成测试
5. **代码审查和重构**：改善代码结构

### 功能开发原则

- 优先实现 MVP，验证核心流程后再完善细节
- 每个功能完成后手动测试验证
- 通过重构逐步改善代码质量
```

## 七、参考资料和进一步阅读

### 本项目的规则示例

- [IDE 层规则](./ide-layer/rulesets/)
- React 项目：
  - AI规则：[.cursor/coderules](./project-templates/react-app/.cursor/coderules/)
  - 文档：[coding-standards.md](./project-templates/react-app/docs/coding-standards.md)
- Vue 项目：
  - AI规则：[.cursor/coderules](./project-templates/vue-app/.cursor/coderules/)
  - 文档：[coding-standards.md](./project-templates/vue-app/docs/coding-standards.md)
- Python 后端：
  - AI规则：[.cursor/coderules](./project-templates/python-backend/.cursor/coderules/)
  - 文档：[coding-standards.md](./project-templates/python-backend/docs/coding-standards.md)
- 全栈项目：
  - AI规则：[.cursor/coderules](./project-templates/fullstack-monorepo/.cursor/coderules/)
  - 文档：[coding-standards.md](./project-templates/fullstack-monorepo/docs/coding-standards.md)

### 外部参考

- [Cursor Rules 官方文档](https://cursor.sh/)
- [GitHub Copilot Instructions](https://docs.github.com/en/copilot)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

**维护者注意**：本文档应在每次有效讨论后及时更新。
