# Golang 后端开发规范

## 技术栈

### 核心框架

- Gin（HTTP Web 框架，推荐）或 Echo（备选）
- GORM（ORM，推荐）或 SQLx（备选）
- PostgreSQL（数据库）
- Redis（缓存，可选）

### 代码质量

- `go fmt`（代码格式化）
- `goimports`（导入管理）
- `go vet`（静态分析）
- `golangci-lint`（综合 lint 工具）
- `go test`（测试）

## 项目结构

```text
project/
├── cmd/
│   └── app/
│       └── main.go              # 应用程序入口
├── internal/
│   ├── config/                  # 配置管理
│   │   └── config.go
│   ├── handler/                 # HTTP 处理器
│   │   └── user_handler.go
│   ├── service/                 # 业务逻辑
│   │   └── user_service.go
│   ├── repository/              # 数据访问
│   │   └── user_repository.go
│   └── model/                   # 数据模型
│       └── user.go
├── pkg/                         # 可被外部使用的库
│   └── utils/
│       └── validator.go
├── api/                         # API 定义（OpenAPI/Swagger）
├── configs/                     # 配置文件
│   └── config.yaml
├── docs/                        # 文档
├── migrations/                  # 数据库迁移（如使用）
├── go.mod                       # Go 模块定义
├── go.sum                       # 依赖校验和
└── README.md
```

## 命名规范

- 包名：小写字母，简短（如 `user`、`auth`）
- 函数名：驼峰命名，公开函数首字母大写（如 `GetUser`），私有函数首字母小写（如 `getUser`）
- 变量名：驼峰命名，公开变量首字母大写，私有变量首字母小写
- 常量：全大写，单词间用下划线分隔（如 `MAX_RETRIES`）
- 类型名：PascalCase（如 `UserService`、`HTTPClient`）
- 接口名：通常以 `-er` 结尾（如 `Reader`、`Writer`），或使用描述性名称

### 命名语言选择

- **所有标识符使用英语**：包名、函数名、变量名、类型名、接口名等
- **避免拼音命名**：使用语义化的英文单词
- **技术术语保持英文**：如 Context、Goroutine、Channel、Interface 等
- **注释和文档使用英语**：符合 Go 社区规范
- **代码注释根据团队习惯选择**：可以使用中文或英文，建议保持一致

**示例**：

```go
// Good: 英文命名，清晰的文档注释
// User represents a user in the system.
type User struct {
    // ID is the unique identifier for the user.
    ID   int64
    // Name is the user's display name.
    Name string
}

// GetUserByID retrieves a user by their ID.
//
// Parameters:
//   - ctx: context.Context for request cancellation
//   - id: the unique identifier of the user
//
// Returns:
//   - *User: the user if found
//   - error: error if user not found or other error occurs
func GetUserByID(ctx context.Context, id int64) (*User, error) {
    // 查询数据库获取用户信息
    return nil, nil
}

// Bad: 拼音命名
type YongHu struct {
    YongHuID int64  // 不符合 Go 社区规范
}
```

## API 开发流程

### 后端开发步骤

1. **设计 API 接口**：定义端点、请求/响应格式、状态码
2. **实现数据模型**：定义请求和响应的结构体
3. **实现 Repository 层**：编写数据访问逻辑（可先返回 mock 数据）
4. **实现 Service 层**：编写核心业务逻辑
5. **实现 Handler 层**：编写 HTTP 处理函数，调用 service 层
6. **编写自动化测试**：单元测试和集成测试
7. **集成数据库**：连接数据库，实现真实的数据访问
8. **添加中间件**：日志、CORS、认证等
9. **代码审查和优化**：改善性能和代码质量

### API 开发原则

- 优先实现 MVP，先让 API 能正常工作
- 每个端点实现后立即用 HTTP 客户端测试
- 保持 Handler 层的简洁，业务逻辑放在 Service 层
- 通过重构逐步改善代码质量
- 编写测试覆盖核心业务逻辑

## 架构模式

### 分层架构

- **Handler 层**：处理 HTTP 请求和响应，调用 Service 层
- **Service 层**：封装业务逻辑，协调 Repository 和其他服务
- **Repository 层**：封装数据访问逻辑，与数据库交互
- **Model 层**：定义数据模型和结构体

### 依赖注入

- 通过构造函数注入依赖
- 使用接口而非具体类型
- 提高可测试性和灵活性

```go
type UserService struct {
    repo   UserRepository
    logger Logger
}

func NewUserService(repo UserRepository, logger Logger) *UserService {
    return &UserService{
        repo:   repo,
        logger: logger,
    }
}
```

### Repository 模式

- 使用 Repository 模式封装数据访问逻辑
- 定义接口，提供具体实现
- 便于测试和切换数据源

```go
type UserRepository interface {
    GetByID(ctx context.Context, id int64) (*User, error)
    Create(ctx context.Context, user *User) error
    Update(ctx context.Context, user *User) error
    Delete(ctx context.Context, id int64) error
}
```

## 错误处理

### 错误类型

- 使用 `error` 接口表示错误
- 定义错误变量用于错误比较
- 创建自定义错误类型提供更多上下文

```go
var (
    ErrUserNotFound    = errors.New("user not found")
    ErrInvalidInput     = errors.New("invalid input")
    ErrPermissionDenied = errors.New("permission denied")
)

type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error on field %s: %s", e.Field, e.Message)
}
```

### 错误处理最佳实践

- 错误应该被处理，不要忽略
- 在函数边界处处理错误
- 使用 `errors.Is()` 检查特定错误
- 使用 `errors.As()` 提取错误类型
- 提供有意义的错误上下文

## 并发编程

### Goroutines

- 使用 `go` 关键字启动 goroutine
- 注意 goroutine 的生命周期管理
- 避免 goroutine 泄漏

### Channels

- 使用 channel 在 goroutine 间通信
- 明确 channel 的方向（发送、接收、双向）
- 使用 `close()` 关闭 channel

### Context

- 使用 `context.Context` 传递请求范围的值和取消信号
- 作为函数第一个参数传递
- 使用 `context.WithCancel`、`context.WithTimeout`、`context.WithDeadline` 创建派生 context

## 数据库集成

### GORM

- 功能丰富的 ORM
- 支持多种数据库
- 提供迁移、关联、钩子等功能

### SQLx

- 轻量级 SQL 工具包
- 更接近原生 SQL
- 更好的性能控制

## Git 工作流规范

基于 IDE 层的 Git 规范，Golang 后端项目的具体实践：

### Commit Message 约定

- **语言**：代码注释和文档推荐使用英文
- **格式**：遵循 Conventional Commits 规范
- **Scope**：使用包名、服务名或 API 端点作为 scope

**示例**：

```text
feat(handler): add user creation endpoint
  - Implement POST /api/v1/users endpoint
  - Add CreateUserRequest struct
  - Create UserHandler.CreateUser method

fix(service): fix user validation logic
  - Validate email format in UserService
  - Add test case for invalid email

docs(model): update User model documentation
  - Add field descriptions
  - Document JSON tags
```

### Branch 命名

- `feature/{feature-name}`：新功能开发（如 `feature/user-authentication`）
- `bugfix/{bug-description}`：Bug 修复（如 `bugfix/user-validation-error`）
- `hotfix/{issue}`：紧急修复
- `refactor/{module-name}`：模块重构

### Commit 时机建议

Golang 后端项目特有的 commit 时机：

1. **实现数据模型**：

   ```bash
   git add internal/model/user.go
   git commit -m "feat(model): add User model with JSON tags"
   ```

2. **实现 Repository 层**：

   ```bash
   git add internal/repository/user_repository.go
   git commit -m "feat(repository): implement UserRepository interface"
   ```

3. **实现 Service 层**：

   ```bash
   git add internal/service/user_service.go internal/service/user_service_test.go
   git commit -m "feat(service): implement UserService with business logic"
   ```

4. **添加 API 端点**：

   ```bash
   git add internal/handler/user_handler.go
   git commit -m "feat(handler): add user CRUD endpoints"
   ```

5. **添加中间件**：

   ```bash
   git add internal/middleware/auth.go
   git commit -m "feat(middleware): add JWT authentication middleware"
   ```

6. **更新依赖**：

   ```bash
   git add go.mod go.sum
   git commit -m "chore(deps): update gin to v1.9.1"
   ```

### 提交前的检查清单

Golang 后端项目特有的检查项：

- [ ] 代码能够正常编译，没有语法错误
- [ ] `go fmt ./...` 格式化检查通过
- [ ] `go vet ./...` 静态分析通过
- [ ] `golangci-lint run` lint 检查通过（如使用）
- [ ] 所有错误都被正确处理，没有忽略
- [ ] 添加了必要的单元测试和集成测试
- [ ] 所有测试通过（`go test ./...`）
- [ ] 使用 HTTP 客户端测试过 API 端点
- [ ] 数据库查询已优化（避免 N+1 查询）
- [ ] 日志输出合理，不记录敏感信息
- [ ] 错误处理完善，返回合适的 HTTP 状态码
- [ ] Commit message 包含包名或 API 端点作为 scope
- [ ] 代码遵循 Go 社区最佳实践

## 开发流程

### 开发步骤

1. **先实现基本功能**：让代码能正常工作，完成核心需求
2. **添加错误处理**：使用 `error` 类型，定义错误变量和类型
3. **优化类型设计**：设计清晰的接口和结构体
4. **代码格式化**：运行 `go fmt` 确保代码格式正确
5. **编写测试**：单元测试和集成测试
6. **代码审查和重构**：改善代码结构和可读性

### 功能开发原则

- 优先实现 MVP，验证核心流程后再完善细节
- 每个功能完成后手动测试验证
- 保持包的独立性和可测试性
- 通过重构逐步改善代码质量
- 及时提交代码并保持提交粒度小
- **代码变更后必须运行 `go fmt ./...`**，确保格式正确
