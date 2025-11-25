# React 项目编码规范

## 项目结构

```text
src/
├── components/          # 公共组件
│   ├── ui/             # UI基础组件
│   └── shared/         # 业务组件
├── pages/              # 页面组件
├── hooks/              # 自定义 Hooks
├── utils/              # 工具函数
├── services/           # API 服务
├── store/              # 状态管理
├── types/              # 类型定义
└── constants/          # 常量
```

## 命名规范

- 组件：PascalCase（UserProfile.tsx）
- 文件：与默认导出同名
- hooks：use 前缀（useAuth.ts）
- 工具函数：camelCase（formatDate.ts）

### 命名语言选择

- **所有标识符使用英语**：组件名、函数名、变量名、常量名等
- **避免拼音命名**：使用语义化的英文单词
- **技术术语保持英文**：如 Custom Hooks、Component、Props 等
- **注释根据团队习惯选择**：可以使用中文或英文，建议保持一致
- **代码可读性优先**：选择团队最舒适的语言进行注释

**示例**：

```tsx
// Good: 英文命名，中文注释
/**
 * 用户资料卡片组件
 * @param user - 用户信息
 */
export function UserProfileCard({ user }: Props) {
  const [isLoading, setIsLoading] = useState(false); // 加载状态
  // ...
}

// Bad: 拼音命名
export function YongHuZiLiao({ yonghu }: Props) {
  const [jiazaizhuangtai, setJiazaizhuangtai] = useState(false);
  // ...
}
```

## 开发工具

### 必需工具

- TypeScript
- ESLint + Prettier
- React Developer Tools

### 推荐配置

```json
{
  "compilerOptions": {
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

## 开发流程

### 组件开发步骤

1. **先实现基本功能**：让组件能正常工作，完成核心需求
2. **添加类型和错误处理**：补充 TypeScript 类型，处理边界情况
3. **优化用户体验**：添加加载状态、错误提示等
4. **编写测试**：单元测试和集成测试
5. **代码审查和重构**：改善代码结构和可读性

### 功能开发原则

- 优先实现 MVP，验证核心流程后再完善细节
- 每个功能完成后手动测试验证
- 保持组件的独立性和可测试性
- 通过重构逐步改善代码质量
- 及时提交代码，保持小的提交粒度

## Git 工作流规范

基于 IDE 层的 Git 规范，React 项目的具体实践：

### Commit Message 约定

- **语言**：推荐使用英文，便于国际化协作
- **格式**：遵循 Conventional Commits 规范
- **Scope**：使用组件名或功能模块作为 scope

**示例**：

```text
feat(auth): 添加 JWT 登录认证
  - 实现 LoginForm 组件
  - 添加 authService 处理 API 调用
  - 使用 Context 管理认证状态

fix(user-profile): 修复头像上传失败问题
  - 更新 uploadAvatar API 的 content type
  - 添加文件大小限制提示

docs(components): 更新 Button 组件文档
  - 添加 variant 属性说明
  - 提供使用示例
```

### Branch 命名

- `feature/{jira-ticket}-{feature-name}`：新功能开发（如 `feature/LOGIN-123-add-jwt-auth`）
- `bugfix/{bug-description}`：Bug 修复（如 `bugfix/avatar-upload-fail`）
- `hotfix/{issue}`：紧急修复
- `refactor/{component-name}`：组件重构

### Commit 时机建议

React 项目特有的 commit 时机：

1. **完成一个组件的开发**：包括组件、样式、测试

   ```bash
   git add src/components/LoginForm/
   git commit -m "feat(components): add LoginForm component with validation"
   ```

2. **添加一个自定义 Hook**：逻辑和测试

   ```bash
   git add src/hooks/useAuth.ts src/hooks/useAuth.test.ts
   git commit -m "feat(hooks): add useAuth hook for authentication"
   ```

3. **集成一个 API 端点**：服务层和组件更新

   ```bash
   git add src/services/authService.ts src/pages/LoginPage.tsx
   git commit -m "feat(auth): integrate login API endpoint"
   ```

4. **修复渲染问题**：

   ```bash
   git commit -m "fix(dashboard): resolve memory leak in data polling"
   ```

5. **性能优化**：

   ```bash
   gt commit -m "perf(list): memoize list items to reduce re-renders"
   ```

### 提交前的检查清单

React 项目特有的检查项：

- [ ] 组件能够正常渲染，没有报错
- [ ] TypeScript 类型检查通过
- [ ] ESLint 检查通过（无错误，警告已评估）
- [ ] 添加了必要的单元测试和集成测试
- [ ] 所有测试通过
- [ ] 在支持的目标浏览器中测试过
- [ ] 组件文档已更新（如果需要）
- [ ] Storybook 示例已添加（如果使用 Storybook）
- [ ] Commit message 包含组件或功能模块作为 scope
