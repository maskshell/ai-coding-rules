# 文档索引

本文档为 `docs/` 目录下的所有文档提供导航和索引。

## 📚 文档分类

### 1. 规则编写指南

#### [规则编写指南](./rule-writing-guide.md) ⭐ 核心文档

**用途**：定义如何为 AI Coding Rules 项目编写新的规则文件，确保规则的一致性、可维护性和实用性。

**主要内容**：

- 分层架构（IDE层、语言层、框架层、项目层）
- 内容规范和编写风格
- 敏捷开发原则
- 软件设计模式
- 从完整版创建精简版规则
- 验收清单

**适用对象**：规则编写者、项目维护者

#### [规则配置指南](./rule-configuration-guide.md) ⭐ 核心文档

**用途**：说明如何配置 Cursor Rules，包括 Always Applied vs Agent Requestable、规则依赖关系、Frontmatter 格式规范和验证方法。

**主要内容**：

- Always Applied vs Agent Requestable 的区别和选择
- 规则依赖关系的管理
- Frontmatter 格式规范
- 验证配置方法
- 最佳实践

**适用对象**：规则编写者、项目维护者、规则使用者

---

### 2. MDC 格式规范

#### [MDC Frontmatter 规范](./mdc-frontmatter-spec.md)

**用途**：定义 Cursor Rules 的 MDC 格式 frontmatter 元数据规范。

**主要内容**：

- Frontmatter 字段定义（description、globs、alwaysApply 等）
- 字段使用规则和最佳实践
- 示例和模板

**适用对象**：规则编写者

#### [MDC 条件模式分析](./mdc-conditional-mode-analysis.md)

**用途**：分析 MDC 条件模式的使用场景和实现方式。

**主要内容**：

- 条件模式的概念和用途
- 使用场景分析
- 实现方式对比

**适用对象**：规则编写者、技术研究者

#### [IDE层规则 alwaysApply 设置分析](./ide-layer-alwaysapply-analysis.md)

**用途**：分析 IDE 层规则的 `alwaysApply` 设置是否合理，确保规则正确应用。

**主要内容**：

- IDE 层规则 `alwaysApply` 设置检查
- 问题分析和修复建议
- 验证标准和最佳实践

**适用对象**：规则维护者、项目维护者

---

### 3. AI 工具相关

#### [AI 编码工具推荐指南](./ai-coding-tools.md) ⭐ 推荐阅读

**用途**：介绍可提升 AI 编码效率的工具和 MCP Server。

**主要内容**：

- Context7 MCP Server（实时文档查询）
- ast-grep（代码验证与重构）
- Knowledge Graph Memory Server（跨会话记忆）
- Skill 模式（工作流程标准化）
- 工具选择决策表

**适用对象**：所有开发者

#### [Vibe Coding 工具指南](./vibe-coding-tools.md)

**用途**：介绍 Vibe Coding 项目相关的工具和配置。

**主要内容**：

- 项目工具概览
- 工具配置和使用方法

**适用对象**：项目使用者

#### [AI 工具兼容性指南](./ai-tools-compatibility.md)

**用途**：说明本项目的规则集如何与各种 AI 编码工具兼容。

**主要内容**：

- Cursor IDE 兼容性
- 其他 AI 工具兼容性说明
- `.cursorrules` 废弃说明
- 项目结构说明

**适用对象**：项目使用者、工具集成者

---

### 4. 技术选型

#### [技术栈选型建议：Python vs Node.js](./tech-stack-recommendation.md)

**用途**：为项目工具开发提供技术栈选型建议。

**主要内容**：

- Python 方案优势分析
- Node.js 方案优势分析
- 工具需求分析
- 最终推荐和理由

**适用对象**：项目维护者、工具开发者

---

### 5. 工具使用

#### [Scripts 使用场景说明](./scripts-usage.md)

**用途**：说明 `scripts/` 目录下各个脚本的使用时机和场景。

**主要内容**：

- 自动调用脚本（Pre-commit Hooks）
- CI/CD 中使用的脚本
- 手动调用的脚本（开发/维护时）
- 使用场景总结和快速参考

**适用对象**：项目维护者、贡献者

---

## 🗺️ 快速导航

### 按角色导航

#### 我是规则编写者

1. 先阅读 [规则编写指南](./rule-writing-guide.md)
2. 了解 [MDC Frontmatter 规范](./mdc-frontmatter-spec.md)

#### 我是项目使用者

1. 阅读 [AI 编码工具推荐指南](./ai-coding-tools.md)
2. 查看 [AI 工具兼容性指南](./ai-tools-compatibility.md)
3. 了解 [Vibe Coding 工具指南](./vibe-coding-tools.md)

#### 我是项目维护者

1. 阅读 [规则编写指南](./rule-writing-guide.md)
2. 参考 [技术栈选型建议](./tech-stack-recommendation.md)
3. 了解 [Scripts 使用场景说明](./scripts-usage.md)

### 按主题导航

#### 想了解如何编写规则

- [规则编写指南](./rule-writing-guide.md)
- [MDC Frontmatter 规范](./mdc-frontmatter-spec.md)
- [MDC 条件模式分析](./mdc-conditional-mode-analysis.md)
- [IDE层规则 alwaysApply 设置分析](./ide-layer-alwaysapply-analysis.md)

#### 想了解 AI 工具使用

- [AI 编码工具推荐指南](./ai-coding-tools.md)
- [AI 工具兼容性指南](./ai-tools-compatibility.md)

#### 想了解技术选型

- [技术栈选型建议：Python vs Node.js](./tech-stack-recommendation.md)

#### 想了解工具使用

- [Scripts 使用场景说明](./scripts-usage.md)

---

## 📊 文档统计

| 文档名称 | 行数 | 大小 | 类型 |
| ------- | ---- | ---- | ---- |
| [规则编写指南](./rule-writing-guide.md) | 870 | 19KB | 指南 |
| [AI 编码工具推荐指南](./ai-coding-tools.md) | 548 | 13KB | 指南 |
| [Vibe Coding 工具指南](./vibe-coding-tools.md) | 495 | 12KB | 指南 |
| [Scripts 使用场景说明](./scripts-usage.md) | 329 | 7.9KB | 指南 |
| [AI 工具兼容性指南](./ai-tools-compatibility.md) | 300 | 8.7KB | 指南 |
| [技术栈选型建议](./tech-stack-recommendation.md) | 325 | 8.0KB | 建议 |
| [MDC 条件模式分析](./mdc-conditional-mode-analysis.md) | 290 | 7.3KB | 分析 |
| [MDC Frontmatter 规范](./mdc-frontmatter-spec.md) | 292 | 6.1KB | 规范 |
| [IDE层规则 alwaysApply 设置分析](./ide-layer-alwaysapply-analysis.md) | 88 | 2.2KB | 分析 |

**总计**：9 个文档，约 3,538 行，约 91.1KB

---

## 🔄 文档更新记录

- **2025-12-02**：添加 IDE层规则 alwaysApply 设置分析文档
- **2025-12-02**：添加 Scripts 使用场景说明文档
- **2025-11-30**：创建文档索引
- 各文档的更新记录请查看对应文档的 frontmatter 或文档头部

---

## 📝 贡献指南

如需添加新文档或更新现有文档：

1. 遵循 [规则编写指南](./rule-writing-guide.md) 中的格式规范
2. 更新本索引文件，添加新文档的链接和描述
3. 确保文档分类清晰，便于查找

---

## 🔗 相关资源

- [项目主 README](../README.md)
- [规则文件目录](../full-rules/)
- [精简版规则目录](../.concise-rules/)
