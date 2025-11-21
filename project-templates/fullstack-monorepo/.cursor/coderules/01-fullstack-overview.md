# 全栈项目 AI 规则

## 跨层开发注意

### 同时修改前后端时

1. 首先设计 API 接口（路径、方法、请求/响应格式）
2. 先实现后端 API 端点和 Pydantic 模型
3. 运行后端并验证 API 端点工作正常
4. 实现前端组件和 API 调用
5. 集成测试

### API 错误处理

- 后端返回标准化的错误响应
- 前端根据状态码处理不同错误
- 提供用户友好的错误消息

```python
# 后端 FastAPI 错误响应模型
class ErrorResponse(BaseModel):
    code: int
    message: str
    detail: Optional[str] = None
```

```typescript
// 前端错误处理
interface ApiError {
  code: number;
  message: string;
  detail?: string;
}

async function handleApiError(error: AxiosError<ApiError>) {
  if (error.response?.status === 401) {
    // 重定向到登录页
  } else if (error.response?.status === 403) {
    // 显示无权限提示
  } else {
    // 显示通用错误消息
  }
}
```

## 代码生成规则

### 创建新功能时

1. 询问是否需要同时创建前端和后端代码
2. 如果是完整功能：
   - 先创建后端：
     - Pydantic schemas
     - Service 层
     - API endpoints
     - Tests
   - 再创建前端：
     - Types（从 OpenAPI 生成）
     - API 调用函数
     - 组件
     - Tests

### 修改现有功能

- 明确指出只修改前端或后端，还是两者都要改
- 检查对端代码是否需要同步更新
