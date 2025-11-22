# Python 后端规范（精简版）

## 技术栈

- FastAPI（API开发）
- SQLAlchemy 2.0（ORM，使用 async）
- Pydantic v2（数据验证）
- PostgreSQL + Redis
- pytest（测试）

## 类型注解

- 函数参数和返回值必须注解
- 使用 Pydantic 进行复杂数据验证
- 优先使用 `|` 替代 Union

```python
async def get_user_by_id(user_id: int) -> User | None:
    pass
```

## 异步编程

- 数据库操作使用 async/await
- HTTP 请求使用 async
- 缓存操作使用 async

## 错误处理

- 捕获最具体的异常
- 提供有用的错误信息
- 在 FastAPI 中使用 HTTPException

## 错误模式

```python
try:
    user = await get_user_by_id(db, user_id)
except NoResultFound:
    raise HTTPException(status_code=404, detail="用户不存在")
```

## 命名

- 包名/模块名：小写下划线
- 类名：PascalCase
- 函数名：小写下划线
- 常量：大写下划线
