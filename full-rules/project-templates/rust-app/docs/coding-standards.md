# Rust 后端开发规范

## 技术栈

### 核心框架

- **Rust**：系统编程语言，强调内存安全和并发
- **Axum**（推荐）或 **Actix-web**：异步 Web 框架
- **Tokio**：异步运行时
- **SQLx** 或 **SeaORM**：数据库访问
- **Serde**：序列化和反序列化
- **PostgreSQL**：关系型数据库（推荐）

### 代码质量工具

- **rustfmt**：代码格式化
- **clippy**：代码检查
- **cargo test**：测试框架
- **cargo-udeps**：检查未使用的依赖

## 项目结构

```text
src/
├── main.rs                 # 程序入口
├── lib.rs                  # 库入口（如果作为库）
├── config.rs               # 配置管理
├── models/                 # 数据模型
│   ├── mod.rs
│   └── user.rs
├── handlers/               # 请求处理函数
│   ├── mod.rs
│   └── users.rs
├── services/               # 业务逻辑层
│   ├── mod.rs
│   └── user_service.rs
├── repositories/           # 数据访问层
│   ├── mod.rs
│   └── user_repository.rs
├── errors.rs               # 错误类型定义
├── middleware/             # 中间件
│   ├── mod.rs
│   └── auth.rs
└── tests/                  # 集成测试
    └── integration_test.rs

Cargo.toml                  # 项目配置和依赖
```

## 命名规范

### 基本命名规则

- **模块名**：`snake_case`（如 `user_service`）
- **函数名**：`snake_case`（如 `get_user_by_id`）
- **变量名**：`snake_case`（如 `user_name`）
- **常量名**：`SCREAMING_SNAKE_CASE`（如 `MAX_RETRIES`）
- **结构体名**：`PascalCase`（如 `UserProfile`）
- **枚举名**：`PascalCase`（如 `HttpStatus`）
- **枚举变体**：`PascalCase`（如 `HttpStatus::Ok`）
- **trait 名**：`PascalCase`（如 `Display`）
- **类型别名**：`PascalCase`（如 `UserId`）

### 命名语言选择

- **所有标识符使用英语**：模块名、函数名、变量名、结构体名等
- **避免拼音命名**：使用语义化的英文单词
- **技术术语保持英文**：如 Ownership、Borrowing、Lifetime、Trait 等
- **文档注释使用英语**：符合 Rust 社区规范（使用 `///` 和 `//!`）
- **注释根据团队习惯选择**：可以使用中文或英文，建议保持一致

**示例**：

```rust
// Good: 英文命名，清晰的文档注释
/// Represents a user in the system.
pub struct User {
    /// Unique identifier for the user.
    pub id: u64,
    /// User's display name.
    pub username: String,
}

impl User {
    /// Retrieves a user by their ID.
    ///
    /// # Arguments
    ///
    /// * `id` - The unique identifier of the user
    ///
    /// # Returns
    ///
    /// Returns `Some(User)` if found, `None` otherwise.
    ///
    /// # Examples
    ///
    /// ```
    /// let user = User::get_by_id(1);
    /// ```
    pub fn get_by_id(id: u64) -> Option<Self> {
        // 查询数据库获取用户信息
        None
    }
}

// Bad: 拼音命名
pub struct YongHu {
    pub yong_hu_id: u64, // 不符合 Rust 社区规范
}
```

## 所有权和借用

### 所有权规则

Rust 的核心特性是所有权系统，它确保内存安全而无需垃圾回收器。

**关键规则**：

1. 每个值只有一个所有者
2. 值离开作用域时自动释放
3. 移动语义：所有权转移，原变量不可用
4. 复制语义：实现 `Copy` trait 的类型（如 `i32`、`bool`）自动复制

**示例**：

```rust
// 移动语义
let s1 = String::from("hello");
let s2 = s1; // s1 的所有权移动到 s2
// println!("{}", s1); // 编译错误：s1 已不再有效

// 复制语义
let x = 5;
let y = x; // x 被复制，两者都有效
println!("{} {}", x, y); // 正常
```

### 借用规则

- **不可变借用**：可以有多个，但不能同时有可变借用
- **可变借用**：只能有一个，且不能同时有不可变借用
- **借用不能超过值的生命周期**

**最佳实践**：

- 优先使用引用而非移动所有权
- 函数参数优先使用 `&str` 而非 `&String`（更灵活）
- 返回引用时注意生命周期

## 错误处理

### Result 类型

Rust 使用 `Result<T, E>` 类型表示可能失败的操作，不使用异常。

**自定义错误类型**：

```rust
use std::fmt;

#[derive(Debug)]
pub enum AppError {
    NotFound(String),
    ValidationError(String),
    DatabaseError(String),
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            AppError::NotFound(msg) => write!(f, "Not found: {}", msg),
            AppError::ValidationError(msg) => write!(f, "Validation error: {}", msg),
            AppError::DatabaseError(msg) => write!(f, "Database error: {}", msg),
        }
    }
}

impl std::error::Error for AppError {}
```

**使用 `?` 操作符传播错误**：

```rust
fn get_user(id: u64) -> Result<User, AppError> {
    if id == 0 {
        return Err(AppError::ValidationError("Invalid user ID".to_string()));
    }
    Ok(User { id, username: "test".to_string() })
}

fn process_user(id: u64) -> Result<String, AppError> {
    let user = get_user(id)?; // 如果失败，自动返回错误
    Ok(format!("User: {}", user.username))
}
```

### 错误处理库

对于复杂项目，推荐使用：

- **thiserror**：用于定义错误类型
- **anyhow**：用于应用程序错误处理

**示例（使用 thiserror）**：

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Not found: {0}")]
    NotFound(String),
    
    #[error("Validation error: {0}")]
    ValidationError(String),
    
    #[error("Database error: {0}")]
    #[from]
    DatabaseError(#[from] sqlx::Error),
}
```

### 错误处理最佳实践

- 在函数边界处处理错误，不要忽略
- 使用 `match` 或 `if let` 处理 `Option` 和 `Result`
- **避免使用 `unwrap()` 和 `expect()`**（除非在测试或确定不会失败的地方）
- 提供有意义的错误消息

## 并发编程

### 异步编程

Rust 的异步编程基于 `Future` trait 和 `async/await` 语法。

**使用 Tokio**：

```rust
use tokio;

async fn fetch_user(id: u64) -> Result<User, AppError> {
    tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
    Ok(User { id, username: "test".to_string() })
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let user = fetch_user(1).await?;
    println!("User: {}", user.username);
    Ok(())
}
```

**并发执行**：

```rust
let handles: Vec<_> = (1..=10)
    .map(|id| {
        tokio::spawn(async move {
            fetch_user(id).await
        })
    })
    .collect();

for handle in handles {
    if let Ok(Ok(user)) = handle.await {
        println!("User: {}", user.username);
    }
}
```

### 共享状态并发

使用 `Arc<Mutex<T>>` 实现线程间共享可变数据：

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    let handle = thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    });
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap();
}

println!("Result: {}", *counter.lock().unwrap());
```

## API 开发流程

### 后端开发步骤

1. **设计 API 接口**：定义端点、请求/响应格式、状态码
2. **实现路由处理函数**：编写处理函数，先返回 mock 数据
3. **实现数据模型**：定义请求和响应的结构体（使用 Serde）
4. **实现业务逻辑**：编写 Service 层逻辑
5. **集成数据库**：连接数据库，实现数据访问层（Repository）
6. **添加错误处理**：统一错误响应格式
7. **添加中间件**：日志、CORS、认证等
8. **编写测试**：单元测试和集成测试
9. **代码审查和优化**：改善性能和代码质量

### 功能开发原则

- 优先实现 MVP，先让 API 能正常工作
- 每个端点实现后立即用 HTTP 客户端（如 `curl` 或 `httpie`）测试
- 保持处理函数的简洁，业务逻辑放在 Service 层
- 通过重构逐步改善代码质量
- 编写测试覆盖核心业务逻辑

## Git 工作流规范

基于 IDE 层的 Git 规范，Rust 后端项目的具体实践：

### Commit Message 约定

- **语言**：文档注释和代码注释推荐使用英文
- **格式**：遵循 Conventional Commits 规范
- **Scope**：使用模块名、服务名或 API 端点作为 scope

**示例**：

```text
feat(api): add user authentication endpoint
  - Implement /auth/login endpoint
  - Add JWT token generation
  - Create AuthService with login method

fix(service): fix user creation validation
  - Validate email format in UserService
  - Add test case for invalid email

docs(models): update User model documentation
  - Add examples for field validation
  - Document relationship with Post model

perf(db): optimize user query with index
  - Add index to users.email column
  - Update query to use index scan
```

### Branch 命名

- `feature/{feature-name}`：新功能开发（如 `feature/user-authentication`）
- `bugfix/{bug-description}`：Bug 修复（如 `bugfix/user-creation-validation`）
- `hotfix/{issue}`：紧急修复
- `refactor/{module-name}`：模块重构

### Commit 时机建议

Rust 后端项目特有的 commit 时机：

1. **实现路由和处理函数**：

   ```bash
   git add src/handlers/users.rs
   git commit -m "feat(handlers): add user CRUD endpoints"
   ```

2. **实现 Service 层业务逻辑**：

   ```bash
   git add src/services/user_service.rs src/services/user_service_test.rs
   git commit -m "feat(services): implement UserService with CRUD methods"
   ```

3. **添加数据模型**：

   ```bash
   git add src/models/user.rs
   git commit -m "feat(models): add User model with validation"
   ```

4. **集成数据库**：

   ```bash
   git add src/repositories/user_repository.rs migrations/
   git commit -m "feat(db): add UserRepository with SQLx integration"
   ```

5. **添加错误处理**：

   ```bash
   git add src/errors.rs
   git commit -m "feat(errors): add AppError enum with thiserror"
   ```

6. **性能优化**：

   ```bash
   git commit -m "perf(db): add index to users.email column"
   ```

7. **更新依赖**：

   ```bash
   git add Cargo.toml Cargo.lock
   git commit -m "chore(deps): update axum to 0.7.0"
   ```

### 提交前的检查清单

Rust 后端项目特有的检查项：

- [ ] 代码能够正常编译（`cargo build`）
- [ ] 所有测试通过（`cargo test`）
- [ ] Clippy 检查通过（`cargo clippy`）
- [ ] 代码格式化（`cargo fmt`）
- [ ] 没有未使用的依赖（`cargo-udeps`）
- [ ] API 端点已测试（使用 HTTP 客户端）
- [ ] 错误处理完善，返回合适的 HTTP 状态码
- [ ] 日志输出合理，不记录敏感信息
- [ ] Commit message 包含模块或 API 端点作为 scope

## 测试

### 单元测试

在源文件中使用 `#[cfg(test)]` 模块：

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_user() {
        let user = User::get_by_id(1);
        assert!(user.is_some());
    }
}
```

### 集成测试

在 `tests/` 目录下创建测试文件：

```rust
// tests/integration_test.rs
use my_app::User;

#[tokio::test]
async fn test_create_user() {
    // 测试逻辑
}
```

### 测试最佳实践

- 为每个公共函数编写测试
- 测试正常情况和边界情况
- 使用 `#[should_panic]` 测试预期会 panic 的情况
- 使用 `Result` 类型进行错误测试

## 性能优化

### 常见优化技巧

1. **避免不必要的克隆**：使用引用传递
2. **使用 `Vec::with_capacity`**：预分配容量
3. **使用 `String::with_capacity`**：预分配字符串容量
4. **使用迭代器而非循环**：更高效且更安全
5. **使用 `Box` 或 `Arc`**：减少大结构体的复制

### 性能分析

- 使用 `cargo bench` 进行基准测试
- 使用 `perf` 或 `flamegraph` 进行性能分析
- 使用 `cargo build --release` 进行发布构建

## 参考资料

- [The Rust Programming Language Book](https://doc.rust-lang.org/book/)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [Axum Documentation](https://docs.rs/axum/)
- [Tokio Documentation](https://tokio.rs/)
- [SQLx Documentation](https://docs.rs/sqlx/)
