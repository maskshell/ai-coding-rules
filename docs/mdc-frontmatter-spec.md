# MDC Frontmatter 规范

**文档版本**: 1.0.0  
**最后更新**: 2025-11-26  
**用途**: 定义 Cursor Rules 的 MDC 格式 frontmatter 元数据规范

---

## 一、规范概述

根据 Cursor 官方文档，每个规则文件使用 **MDC**（`.mdc`）格式编写，这是一种同时支持元数据和内容的格式。

### 格式结构

```yaml
---
description: "规则描述"
globs: ["文件匹配模式"]
alwaysApply: true/false
tags: [标签列表]
version: "版本号"
author: "作者"
priority: 优先级
---

# 规则内容（Markdown）
```

---

## 二、必需字段

### 1. `description` (string, 必需)

**用途**: 描述规则的用途和适用范围

**要求**:
- 清晰、简洁地描述规则用途
- 不超过 200 字符
- 使用中文或英文

**示例**:
```yaml
description: "通用编程规范，适用于所有项目和语言"
description: "Python 基础编码规范，包括命名、类型注解、错误处理"
description: "React 组件开发规范，包括组件结构、Hooks 使用、状态管理"
```

### 2. `globs` (array, 必需)

**用途**: 定义规则适用的文件模式

**要求**:
- 使用 glob 模式匹配文件路径
- 支持多个模式（数组）
- 如果适用于所有文件，使用 `["**/*"]`

**示例**:
```yaml
globs: ["**/*"]                    # 所有文件
globs: ["**/*.py"]                 # 所有 Python 文件
globs: ["**/*.tsx", "**/*.ts"]     # TypeScript 文件
globs: ["**/components/**/*.tsx"]  # components 目录下的 TSX 文件
```

### 3. `alwaysApply` (boolean, 必需)

**用途**: 控制规则是否总是应用

**规则类型映射**:
- `alwaysApply: true` → "Always Apply"（应用于每个聊天会话）
- `alwaysApply: false` → 根据其他条件应用（Apply Intelligently / Apply to Specific Files / Apply Manually）

**示例**:
```yaml
alwaysApply: true   # 总是应用（如通用规范）
alwaysApply: false  # 按需应用（如特定框架规则）
```

---

## 三、可选字段

### 1. `tags` (array, 可选)

**用途**: 标签分类，便于组织和搜索

**常用标签**:
- `general`: 通用规则
- `language`: 语言特定（如 `python`, `typescript`, `javascript`）
- `framework`: 框架特定（如 `react`, `vue`, `fastapi`）
- `testing`: 测试相关
- `security`: 安全相关
- `performance`: 性能相关
- `style`: 代码风格

**示例**:
```yaml
tags: [general, coding-standards]
tags: [python, type-hints, error-handling]
tags: [react, hooks, components]
```

### 2. `version` (string, 可选)

**用途**: 规则版本号

**格式**: 语义化版本（SemVer）`X.Y.Z`

**示例**:
```yaml
version: "1.0.0"
version: "2.1.3"
```

### 3. `author` (string, 可选)

**用途**: 规则作者或维护者

**示例**:
```yaml
author: "ai-coding-rules-team"
author: "vibe-coding"
```

### 4. `priority` (integer, 可选)

**用途**: 规则优先级（数字越大优先级越高）

**范围**: 1-100

**默认值**: 50

**示例**:
```yaml
priority: 80  # 高优先级（如安全规则）
priority: 30  # 低优先级（如风格建议）
```

---

## 四、完整示例

### 示例 1：通用规则（Always Apply）

```yaml
---
description: "通用编程规范，适用于所有项目和语言"
globs: ["**/*"]
alwaysApply: true
tags: [general, coding-standards]
version: "1.0.0"
author: "ai-coding-rules-team"
---

# 通用编程规范

## 代码质量

- 编写清晰、可读的代码
- 遵循 DRY 原则
- 使用有意义的变量名
...
```

### 示例 2：Python 特定规则（Apply to Specific Files）

```yaml
---
description: "Python 基础编码规范，包括命名、类型注解、错误处理"
globs: ["**/*.py"]
alwaysApply: false
tags: [python, type-hints, error-handling]
version: "1.0.0"
---

# Python 编码规范

## 类型注解

- 所有函数必须包含类型注解
...
```

### 示例 3：React 组件规则（Apply Intelligently）

```yaml
---
description: "React 组件开发规范，包括组件结构、Hooks 使用、状态管理"
globs: ["**/*.tsx", "**/*.jsx"]
alwaysApply: false
tags: [react, hooks, components]
version: "1.0.0"
---

# React 组件规范

## 组件结构

- 使用函数组件
- 使用 Hooks 管理状态
...
```

---

## 五、字段选择指南

### 何时使用 `alwaysApply: true`

- 通用编程规范（适用于所有文件）
- 代码质量要求
- AI 助手行为偏好
- 项目级通用规则

### 何时使用 `alwaysApply: false`

- 语言特定规则（如 Python、TypeScript）
- 框架特定规则（如 React、Vue）
- 特定文件类型规则（如测试文件、配置文件）
- 需要手动触发的规则

### 如何选择 `globs` 模式

1. **所有文件**: `["**/*"]`
2. **特定语言**: `["**/*.py"]`, `["**/*.ts"]`, `["**/*.tsx"]`
3. **特定目录**: `["**/components/**/*"]`, `["**/tests/**/*"]`
4. **多个模式**: `["**/*.ts", "**/*.tsx"]`

---

## 六、验证规则

### Frontmatter 验证

- [ ] `description` 字段存在且非空
- [ ] `globs` 字段存在且为数组
- [ ] `alwaysApply` 字段存在且为布尔值
- [ ] `tags` 字段（如果存在）为数组
- [ ] `version` 字段（如果存在）符合 SemVer 格式
- [ ] YAML 格式正确，无语法错误

### 内容验证

- [ ] frontmatter 和内容之间有分隔符 `---`
- [ ] 内容部分为有效的 Markdown
- [ ] 文件扩展名为 `.mdc`

---

## 七、迁移指南

### 从 `.md` 迁移到 `.mdc`

1. **添加 frontmatter**:
   - 根据文件内容推断 `description`
   - 根据文件路径和内容推断 `globs`
   - 根据规则类型设置 `alwaysApply`
   - 添加适当的 `tags`

2. **保留原内容**:
   - 保持 Markdown 内容不变
   - 确保 frontmatter 和内容之间有 `---` 分隔符

3. **重命名文件**:
   - 将 `.md` 扩展名改为 `.mdc`
   - 保持文件名其他部分不变

---

## 八、参考资源

- [Cursor 官方文档 - Rules](https://cursor.com/docs/context/rules)
- [YAML 规范](https://yaml.org/spec/)
- [Semantic Versioning](https://semver.org/)

---

**文档维护者**: AI Coding Rules 团队  
**反馈渠道**: GitHub Issues / Discussions

