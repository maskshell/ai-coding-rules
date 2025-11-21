# Vibe Coding Rules

分层的 AI Rules 配置示例，满足不同层面的 AI 编码助手需求。

## 目录结构

```text
vibe-coding/
├── ide-layer/                          # IDE 层级规则（最通用）
├── project-templates/                  # 项目模板
│   ├── react-app/                      # React应用
│   ├── vue-app/                        # Vue应用
│   ├── python-backend/                 # Python后端
│   └── fullstack-monorepo/             # 全栈项目
```

## 使用原则

1. **分层管理**：IDE层（通用）→ 语言层 → 框架层 → 项目层（具体）
2. **优先级**：下层的规则覆盖上层规则
3. **渐进式**：从预设模板开始，逐步细化

## 快速开始

1. 将 `ide-layer/rulesets/` 中的所有 `.md` 文件复制到 `~/.cursor/coderules/`
2. 根据项目类型，复制对应模板的 `.cursor/coderules/` 到项目根目录
3. 在项目的 `.cursor/coderules/` 中添加项目特定的规则

## 详细文档

- [IDE层使用说明](./ide-layer/README.md)
- [React应用](./project-templates/react-app/docs/coding-standards.md)
- [Vue应用](./project-templates/vue-app/docs/coding-standards.md)
- [Python后端](./project-templates/python-backend/docs/coding-standards.md)
- [全栈项目](./project-templates/fullstack-monorepo/docs/coding-standards.md)
- [规则编写指南（含敏捷和设计模式指导）](./docs/rule-writing-guide.md)

## 如何贡献

如果你想添加新的项目模板或改进现有规则，请参考 [规则编写指南](./docs/rule-writing-guide.md)。该文档详细说明了：

- 规则的分层架构和优先级
- 文件命名和组织规范
- 敏捷开发原则的表达方式
- 软件设计模式的层次区分
- 创建新模板的完整流程
- 常见错误及避免方法
