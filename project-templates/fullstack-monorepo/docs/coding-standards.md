# 全栈项目开发规范

## 项目架构

### 技术栈

- **前端**: React 18 + TypeScript + Vite + Tailwind CSS
- **后端**: FastAPI + Python 3.11+
- **数据库**: PostgreSQL + Redis
- **部署**: Docker + Docker Compose
- **包管理**: pnpm（前端）+ Poetry（后端）

### Monorepo 结构

```text
monorepo/
├── docker-compose.yml          # 本地开发环境
├── README.md
│
├── frontend/                   # 前端项目
│   ├── package.json
│   ├── Dockerfile
│   ├── src/
│   └── tests/
│
├── backend/                    # 后端项目
│   ├── pyproject.toml
│   ├── Dockerfile
│   ├── app/
│   └── tests/
│
├── packages/                   # 共享包
│   └── shared-types/           # 类型定义
│       ├── package.json
│       └── src/
│
└── docs/                       # 项目文档
    ├── api/
    └── deployment/
```

### Git 工作流

- Main 分支：生产环境
- Develop 分支：开发环境
- Feature 分支：功能开发
- 使用 Conventional Commits

## 前后端协作

### API 设计流程

1. 前端和后端共同设计 API 接口
2. 使用 OpenAPI / Swagger 文档
3. 后端先实现 API 端点和 Pydantic 模型
4. 使用 OpenAPI Generator 生成前端 API 客户端

### 类型共享

- 后端使用 Pydantic 定义 API 模型
- 生成 OpenAPI schema
- 前端生成 TypeScript 类型
- 共享 API 状态码、错误消息

## Docker 开发

### 本地开发环境

- 使用 docker-compose 一键启动
- 使用 volume 挂载实现热重载
- 使用相同的基础镜像作为生产环境

### 多阶段构建

- 前端：node 构建阶段 + nginx 运行阶段
- 后端：python 构建依赖 + slim 运行阶段

## 命名与语言规范

### 前端命名规范

- **所有标识符使用英语**：组件名、函数名、变量名、常量名等
- **避免拼音命名**：使用语义化的英文单词
- **技术术语保持英文**：如 Hooks、Component、Props 等
- **注释根据团队习惯选择**：可以使用中文或英文
- **文件命名**：组件文件使用 PascalCase（UserProfile.tsx），工具文件使用 camelCase（formatDate.ts）

### 后端命名规范

- **所有标识符使用英语**：包名、模块名、类名、函数名、变量名、常量名等
- **避免拼音命名**：使用语义化的英文单词
- **技术术语保持英文**：如 Repository Pattern、Service Layer、FastAPI 等
- **文档字符串（docstring）使用英语**：符合 Python 社区规范
- **注释根据团队习惯选择**：可以使用中文或英文
- **包名和模块名**：使用小写下划线（user_service、auth_service.py）
- **类名**：使用 PascalCase（UserService）
- **函数名**：使用小写下划线（get_user_by_id）

### 跨语言一致的命名

- 同一业务实体在前端和后端的命名保持一致
- 例如：前端的 `UserProfile` 组件对应后端的 `/users/profile` 端点
- 数据库表名、API 路径、前端状态管理中的命名保持一致性
- 避免因语言转换导致的命名不一致问题

### 示例

```typescript
// 前端：UserProfile.tsx
interface User {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
}
```

```python
# 后端：user_service.py
class User(Base):
    """User model."""
    __tablename__ = "users"  # 与前端概念一致

    id = Column(String, primary_key=True)
    first_name = Column(String)  # 与前端字段对应
    last_name = Column(String)
    email = Column(String)
```

## 全栈开发流程

### 新功能开发步骤

1. **需求分析**：明确功能范围和核心业务流程
2. **API 设计**：前后端共同设计接口，定义请求/响应格式
3. **后端实现**（见后端开发流程）：
   - Pydantic schemas
   - Service 层
   - API endpoints
   - Tests
4. **验证后端**：启动后端服务，使用 Swagger UI 测试 API
5. **前端实现**（见前端开发流程）：
   - 生成 TypeScript 类型
   - API 调用函数
   - 组件
   - Tests
6. **集成测试**：前后端联调，确保完整流程可用
7. **代码审查和优化**：改善性能和用户体验

### 敏捷开发原则

- 优先交付端到端可用的最小功能
- 保持前后端并行开发，通过 API 契约解耦
- 每个迭代周期（1-2天）交付可用的功能增量
- 及时集成和测试，避免长时间分支分离
- 通过重构持续改进架构和代码质量

## Git 工作流规范（Monorepo）

基于 IDE 层的 Git 规范，全栈 Monorepo 项目的具体实践：

### Monorepo 结构

```
monorepo/
├── frontend/          # 前端代码（React）
├── backend/           # 后端代码（Python/FastAPI）
├── packages/          # 共享包
└── docs/              # 文档
```

### Commit Message 约定

- **语言**：推荐使用英文，便于国际化协作
- **格式**：遵循 Conventional Commits 规范
- **Scope**: 包含项目名和模块（如 `frontend/auth`, `backend/api`, `shared/types`）

**示例**：
```
feat(frontend/auth): add login page with JWT integration
  - Create LoginForm component
  - Add authentication context
  - Integrate with /auth/login API

feat(backend/api): implement JWT authentication endpoint
  - Add /auth/login endpoint
  - Create Token schema with Pydantic
  - Implement UserService.authenticate method

fix(frontend/api-client): handle 401 unauthorized error
  - Redirect to login page on auth failure
  - Clear user data from store

chore(shared): update shared types package
  - Add AuthResponse interface
  - Version bump to 1.2.0
```

### Branch 策略

#### 单分支策略（推荐）

- 所有开发在一个仓库中进行
- 使用同一分支同时修改前端和后端
- 确保前端和后端代码同步提交

**示例**：开发用户认证功能
```bash
git checkout -b feature/PROJ-123-user-authentication

# 修改后端
vim backend/app/api/v1/routes/auth.py
vim backend/app/services/user_service.py
git add backend/
git commit -m "feat(backend/api): add JWT authentication endpoints"

# 修改前端
vim frontend/src/pages/LoginPage.tsx
vim frontend/src/services/authService.ts
git add frontend/
git commit -m "feat(frontend/auth): integrate login API"

# 提交 PR
git push origin feature/PROJ-123-user-authentication
```

#### 分离分支策略（大型团队）

如果前端和后端由不同团队开发：

- `frontend/feature/{name}`: 前端功能分支
- `backend/feature/{name}`: 后端功能分支
- 通过 PR 协调合并时机

### Commit 时机建议

全栈项目特有的 commit 时机：

1. **设计 API 契约**：前后端共同设计并文档化
   ```bash
   git add docs/api/auth-endpoints.md
   git commit -m "docs(api): design authentication API contract"
   ```

2. **完成后端 API 实现**：
   ```bash
   git add backend/app/api/v1/routes/auth.py
   git add backend/app/services/user_service.py
   git add backend/tests/test_auth.py
   git commit -m "feat(backend/api): implement JWT authentication endpoints"
   ```

3. **验证 API 可用性**：使用 Swagger UI 测试
   ```bash
   git commit -m "test(backend): verify auth endpoints with Swagger UI"
   ```

4. **生成前端类型**：从 OpenAPI schema
   ```bash
   git add frontend/src/types/api.ts
   git commit -m "feat(frontend/types): generate types from OpenAPI schema"
   ```

5. **完成前端集成**：
   ```bash
   git add frontend/src/pages/LoginPage.tsx
   git add frontend/src/services/authService.ts
   git commit -m "feat(frontend/auth): implement login page with API integration"
   ```

6. **端到端测试**：
   ```bash
   git add tests/e2e/auth.spec.ts
   git commit -m "test(e2e): add authentication flow test"
   ```

### 原子提交原则

在 Monorepo 中，尽量保持前后端代码同步：

❌ 避免：前端大量提交，后端没有对应提交
```bash
# Bad
feat(frontend): add login form
feat(frontend): add auth context
feat(frontend): add API client  # 后端 API 还没准备好！
```

✅ 推荐：前后端协调提交
```bash
# Good
feat(backend): add authentication endpoints
feat(frontend): add login form and API integration
```

### 提交前的检查清单

全栈项目特有的检查项：

- [ ] 后端代码能够正常启动，Swagger UI 可访问
- [ ] 前端代码能够正常编译，无构建错误
- [ ] mypy 类型检查通过（后端）
- [ ] TypeScript 类型检查通过（前端）
- [ ] ESLint 检查通过（前端）
- [ ] ruff lint 检查通过（后端）
- [ ] 后端测试通过（pytest）
- [ ] 前端测试通过（Jest/Vitest）
- [ ] 在 Swagger UI 中测试过 API 端点
- [ ] 前端成功调用后端 API（无 CORS 等问题）
- [ ] 数据库迁移脚本可正常应用（如有）
- [ ] Docker Compose 可正常启动完整环境
- [ ] 端到端测试通过（如果有）
- [ ] Commit message 明确说明前后端改动
