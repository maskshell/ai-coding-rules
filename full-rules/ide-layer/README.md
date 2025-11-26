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

将这些文件复制到 Cursor 全局配置目录（适用于所有项目）：

```bash
# 注意：Cursor IDE 官方规则目录是 ~/.cursor/rules/
mkdir -p ~/.cursor/rules
cp ide-layer/rulesets/*.md ~/.cursor/rules/
```

或使用符号链接（便于统一管理）：

```bash
mkdir -p ~/.cursor/rules
ln -s $(pwd)/ide-layer/rulesets/* ~/.cursor/rules/
```
