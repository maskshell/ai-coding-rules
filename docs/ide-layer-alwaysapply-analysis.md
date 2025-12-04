# IDE层规则 alwaysApply 设置分析报告

## 当前状态

### alwaysApply: true（6个规则）

| 规则文件 | 描述 | 判断 | 说明 |
| --- | --- | --- | --- |
| `01-general.mdc` | 通用编程规范 | ✅ 正确 | 适用于所有文件的通用规范 |
| `03-security.mdc` | 安全规范 | ✅ 正确 | 安全要求应该总是应用 |
| `06-memory-tools.mdc` | 记忆工具使用规范 | ✅ 正确 | AI工具使用规范应该总是应用 |
| `07-ast-grep.mdc` | ast-grep工具使用 | ✅ 正确 | AI工具使用规范应该总是应用 |
| `08-development-workflow.mdc` | 开发工作流规范 | ✅ 正确 | 通用开发流程应该总是应用 |
| `09-search-optimization.mdc` | 搜索优化规范 | ✅ 正确 | AI行为偏好应该总是应用 |

### alwaysApply: false（3个规则）

| 规则文件 | 描述 | 当前设置 | 建议设置 | 说明 |
| --- | --- | --- | --- | --- |
| `02-testing.mdc` | 测试规范 | ✅ false | false | 有globs限制到测试文件，按需应用正确 |
| `04-ai-behavior.mdc` | AI助手行为偏好 | ❌ false | **true** | 根据文档，AI助手行为偏好应该总是应用 |
| `05-git-repository.mdc` | Git仓库管理规范 | ❌ false | **true** | Git规范适用于所有项目，应该总是应用 |

## 问题分析

### 问题1：`04-ai-behavior.mdc` 应该设置为 `true`

**原因**：

- 根据 `docs/mdc-frontmatter-spec.md`，AI助手行为偏好应该使用 `alwaysApply: true`
- 该规则定义了AI助手在所有场景下的行为偏好（代码生成、沟通方式、工具使用等）
- 这些偏好应该始终生效，而不是按需应用

**影响**：

- 如果设置为 `false`，AI助手可能在某些场景下不遵循这些行为偏好
- 导致行为不一致，影响用户体验

### 问题2：`05-git-repository.mdc` 应该设置为 `true`

**原因**：

- Git仓库管理规范是通用规范，适用于所有项目
- 该规则定义了commit时机、commit message格式等通用要求
- 这些规范应该始终生效，确保所有项目的Git操作都符合规范

**影响**：

- 如果设置为 `false`，AI助手可能在某些场景下不遵循Git规范
- 导致commit message格式不一致，影响项目维护

## 修复建议

### 需要修改的文件

1. **`full-rules/ide-layer/rulesets/04-ai-behavior.mdc`**
   - 将 `alwaysApply: false` 改为 `alwaysApply: true`

2. **`full-rules/ide-layer/rulesets/05-git-repository.mdc`**
   - 将 `alwaysApply: false` 改为 `alwaysApply: true`

3. **对应的精简版规则**
   - `.concise-rules/ide-layer/04-ai-behavior.mdc`
   - `.concise-rules/ide-layer/05-git-repository.mdc`

## 验证标准

根据 `docs/mdc-frontmatter-spec.md`：

**应该使用 `alwaysApply: true` 的情况**：

- ✅ 通用编程规范（适用于所有文件）
- ✅ 代码质量要求
- ✅ **AI助手行为偏好** ← `04-ai-behavior.mdc` 应该符合
- ✅ 项目级通用规则 ← `05-git-repository.mdc` 应该符合

**应该使用 `alwaysApply: false` 的情况**：

- ✅ 语言特定规则（如 Python、TypeScript）
- ✅ 框架特定规则（如 React、Vue）
- ✅ 特定文件类型规则（如测试文件）← `02-testing.mdc` 符合
- ✅ 需要手动触发的规则

## 总结

- **需要修复**：2个规则文件（`04-ai-behavior.mdc` 和 `05-git-repository.mdc`）
- **修复范围**：完整版和精简版都需要修改
- **修复后**：IDE层将有8个规则总是应用，1个规则按需应用（测试规范）
