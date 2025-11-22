# Git 仓库管理规范

## Commit 时机

### 何时提交

- **完成一个小功能点**：每个 commit 应该是逻辑上完整的工作单元
- **修复一个 bug**：包括复现、修复、验证的完整过程
- **重构一小部分代码**：确保重构前后代码行为一致
- **添加或更新测试**：包括测试代码和可能的生产代码修改
- **更新文档**：包括 README、API 文档、注释等

### Commit 粒度

- **保持小的提交粒度**：每个 commit 应该只解决一个问题
- **避免超大的 commit**：如果改动超过 20 个文件，考虑拆分
- **保持可编译状态**：每个 commit 都应该能正常编译/运行

## Commit Message

### 语言选择

**推荐使用英文**：

- 英文是国际通用语言，便于与国际团队协作
- 方便搜索和查找历史记录
- 符合开源社区惯例

**如果团队主要使用中文**：

- 可以使用中文提交
- 但要保持一致性，不要中英文混用

### 格式规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type（必需）

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响代码运行的变动）
- `refactor`: 重构（既不是新增功能，也不是修复bug）
- `test`: 添加或修改测试
- `chore`: 构建过程或辅助工具的变动

#### Scope（可选）

- 说明 commit 影响的范围，如组件名、模块名等
- 示例：`feat(auth): 添加 JWT 认证`

#### Subject（必需）

- 简短描述，不超过 50 个字符
- 使用祈使句，现在时态
- 首字母小写（除非是专有名词）
- 结尾不加句号

#### Body（可选）

- 详细说明修改内容
- 每行不超过 72 个字符
- 解释为什么进行这个修改，而不是做了什么

#### Footer（可选）

- 引用 Issue 或 PR 编号
- 示例：`Closes #123`, `Fixes #456`

### 示例

```
feat(auth): 添加用户登录功能

实现 JWT 认证机制，包括：
- 登录 API 端点
- Token 生成和验证
- 密码加密存储

Closes #123
```

```
fix(validation): 修复邮箱验证正则表达式

之前的正则表达式无法正确验证带加号的邮箱地址，
使用更严格的 RFC 5322 标准正则表达式。

Fixes #456
```

```
docs(readme): 更新部署说明

添加 Docker 部署的详细步骤，包括环境变量配置。
```

## Branch 管理

### 分支命名规范

- `main` 或 `master`: 生产环境代码
- `develop`: 开发分支（如果使用 Git Flow）
- `feature/{feature-name}`: 新功能开发
- `bugfix/{bug-description}`: Bug 修复
- `hotfix/{issue}`: 紧急修复（生产环境问题）
- `release/{version}`: 发布准备

### 分支策略

#### 简单项目（推荐）

- 只有一个 `main` 分支
- 所有开发通过 Pull Request 合并
- 使用 tag 标记版本

#### 中大型项目

使用 Git Flow 或 GitHub Flow：

**GitHub Flow**:

1. `main` 分支始终保持可发布状态
2. 从 `main` 创建 feature 分支
3. 完成后通过 PR 合并回 `main`
4. 部署 `main` 分支

**Git Flow**:

1. `main`: 生产环境
2. `develop`: 集成开发
3. `feature/*`: 功能开发
4. `release/*`: 发布准备
5. `hotfix/*`: 紧急修复

## Pull Request / Merge Request

### PR 提交时机

- 功能开发完成并通过自测
- 代码审查通过后
- 分支合并前解决所有冲突

### PR 规范

- **清晰的标题**：遵循 commit message 格式
- **详细描述**：
  - 改动原因
  - 改动内容
  - 测试方法
  - 相关 Issue 编号
- **代码审查**：
  - 至少 1-2 名团队成员审查
  - 审查通过后由项目维护者合并

### PR 模板

```markdown
## 改动内容

[简要描述改动内容]

## 改动原因

[解释为什么要做这个改动]

## 测试方法

[如何测试这个改动]

## 相关 Issue

- Closes #123
- Related to #456
```

## Tag 和 Release 管理

### 版本号规范

遵循 [Semantic Versioning](https://semver.org/)（语义化版本）：

- `MAJOR.MINOR.PATCH`
- `MAJOR`: 不兼容的 API 修改
- `MINOR`: 向下兼容的功能新增
- `PATCH`: 向下兼容的问题修复

### 打标签时机

- 每次发布生产环境时
- 重要的里程碑版本
- 备份关键节点

### 标签命名

```
v1.0.0
v2.1.3
v1.0.0-beta.1
```

## 提交前的检查清单

提交代码前，请检查：

- [ ] 代码能够正常编译/运行
- [ ] 添加了必要的测试
- [ ] 测试全部通过
- [ ] 更新了相关文档（如果需要）
- [ ] Commit message 清晰明了
- [ ] 没有提交敏感信息（密码、密钥等）
- [ ] 没有包含不必要的文件（日志、临时文件等）
