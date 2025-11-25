# Python 后端开发规范

## 技术栈

### 核心框架

- FastAPI（API 开发）
- SQLAlchemy 2.0（ORM，使用 async 模式）
- Pydantic v2（数据验证）
- PostgreSQL（数据库）
- Alembic（数据库迁移）
- Redis（缓存）

### 代码质量

- ruff（lint 和 format）
- mypy（类型检查）
- pytest（测试）

## 项目结构

```text
app/
├── __init__.py
├── main.py                 # FastAPI 应用入口
├── config.py               # 配置
├── api/                    # API 模块
│   ├── __init__.py
│   ├── deps.py             # FastAPI 依赖注入
│   ├── v1/                 # API v1 版本
│   │   ├── __init__.py
│   │   ├── routes/         # 路由
│   │   └── schemas/        # Pydantic 模型
│
├── core/                   # 核心模块
│   ├── __init__.py
│   ├── security.py         # 认证安全
│   └── logger.py           # 日志配置
│
├── db/                     # 数据访问
│   ├── __init__.py
│   ├── base.py             # SQLAlchemy 基础
│   ├── session.py          # 数据库会话
│   └── repositories/       # 数据仓库
│
├── models/                 # SQLAlchemy 模型
│   └── __init__.py
│
├── services/               # 业务逻辑
├── tests/                  # 测试
└── utils/                  # 工具函数
```

## 命名规范

- 包名：小写下划线（`user_service`）
- 模块名：小写下划线（`auth_service.py`）
- 类名：PascalCase（`UserService`）
- 函数名：小写下划线（`get_user_by_id`）
- 常量：大写下划线（`MAX_RETRIES = 3`）
- 私有成员：前缀下划线（`__private_attr`）

### 命名语言选择

- **所有标识符使用英语**：包名、模块名、类名、函数名、变量名、常量名等
- **避免拼音命名**：使用语义化的英文单词
- **技术术语保持英文**：如 Repository Pattern、Service Layer、FastAPI 等
- **文档字符串（docstring）使用英语**：符合 Python 社区规范
- **注释根据团队习惯选择**：可以使用中文或英文，建议保持一致
- **代码可读性优先**：选择团队最舒适的语言进行注释

**示例**：

```python
# Good: 英文命名，清晰的文档字符串
class UserService:
    """Service layer for user-related business logic."""

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Retrieve a user by their ID.

        Args:
            user_id: The unique identifier of the user

        Returns:
            User object if found, None otherwise
        """
        # 查询数据库获取用户信息
        pass

# Bad: 拼音命名
class YongHuFuWu:
    def huoqu_yonghu(self, yonghu_id: int):  # 不符合 Python 社区规范
        pass
```

## API 开发流程

### 后端开发步骤

1. **设计 API 接口**：定义端点、请求/响应格式、状态码
2. **实现 Pydantic 模型**：编写请求和响应的 Schema
3. **实现 Service 层**：编写核心业务逻辑（可先返回 mock 数据）
4. **实现 API 端点**：在 routes 中调用 service 层
5. **编写自动化测试**：单元测试和集成测试
6. **实现数据库层**：编写 Repository 和 SQLAlchemy 模型
7. **连接各层**：将数据库操作接入 service 层
8. **代码审查和优化**：改善性能和代码质量

### 功能开发原则

- 优先实现 MVP，先让 API 能正常工作
- 每个端点实现后立即用 Swagger UI 测试
- 保持 Service 层的独立性和可测试性
- 通过重构逐步改善代码质量
- 编写测试覆盖核心业务逻辑

## Git 工作流规范

基于 IDE 层的 Git 规范，Python 后端项目的具体实践：

### Commit Message 约定

- **语言**：文档字符串和代码注释推荐使用英文
- **格式**：遵循 Conventional Commits 规范
- **Scope**：使用模块名、服务名或 API 端点作为 scope

**示例**：

```text
feat(api): add JWT authentication endpoint
  - Implement /auth/login endpoint
  - Add Token schema with Pydantic
  - Create JWT utility functions

fix(service): fix user creation without email
  - Validate email field in UserService.create
  - Add test case for missing email

docs(models): update User model docstring
  - Add examples for field validation
  - Document relationship with Post model
```

### Branch 命名

- `feature/{jira-ticket}-{feature-name}`：新功能开发（如 `feature/PROJ-123-jwt-auth`）
- `bugfix/{bug-description}`：Bug 修复（如 `bugfix/user-creation-without-email`）
- `hotfix/{issue}`：紧急修复
- `refactor/{module-name}`：模块重构

### Commit 时机建议

Python 后端项目特有的 commit 时机：

1. **设计并验证 Pydantic Schema**：

   ```bash
   git add app/api/v1/schemas/user.py
   git commit -m "feat(schemas): add UserCreate and UserResponse schemas"
   ```

2. **实现 Service 层业务逻辑**：

   ```bash
   git add app/services/user_service.py app/services/user_service_test.py
   git commit -m "feat(services): implement UserService with create method"
   ```

3. **添加 API 端点**：

   ```bash
   git add app/api/v1/routes/auth.py
   git commit -m "feat(api): add /auth/register endpoint"
   ```

4. **添加数据库模型和迁移**：

   ```bash
   git add app/models/user.py alembic/versions/001_add_user_table.py
   git commit -m "feat(models): add User model with Alembic migration"
   ```

5. **修复数据库查询性能**：

   ```bash
   git commit -m "perf(db): add index to users.email column"
   ```

6. **更新依赖**：

   ```bash
   git add pyproject.toml poetry.lock
   git commit -m "chore(deps): update FastAPI to 0.104.0"
   ```

### 提交前的检查清单

Python 后端项目特有的检查项：

- [ ] 代码能够正常启动，没有语法错误
- [ ] mypy 类型检查通过
- [ ] ruff lint 检查通过（无错误，警告已评估）
- [ ] 所有 Pydantic 模型验证正确
- [ ] 数据库迁移脚本可正常应用和回滚
- [ ] 添加了必要的单元测试和集成测试
- [ ] 所有测试通过（pytest）
- [ ] 在 Swagger UI 中测试过 API 端点
- [ ] SQLAlchemy queries 已优化（避免 N+1 查询）
- [ ] 日志输出合理，不记录敏感信息
- [ ] 错误处理完善，返回合适的 HTTP 状态码
- [ ] Commit message 包含模块或 API 端点作为 scope
