# IDE 层级规则

这是 IDE 层级的 AI Rules，作用于所有项目。

## 规则文件

### 通用规则

- `01-general.md` - 编码通用原则
- `02-testing.md` - 测试约定
- `03-security.md` - 安全规范
- `04-ai-behavior.md` - AI助手行为偏好
- `05-git-repository.md` - Git仓库管理规范

## 使用方法

将这些文件复制到 Cursor 配置目录：

```bash
cp ide-layer/*.md ~/.cursor/coderules/
```

或使用符号链接（便于统一管理）：

```bash
ln -s ~/.cursor/coderules ~/path/to/this/repo/ide-layer/rulesets/
```
