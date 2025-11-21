# Vue 项目编码规范

## 项目架构

### 技术栈

- Vue 3（Composition API）
- TypeScript
- Vite
- Pinia（状态管理）
- Vue Router

### 项目结构

```text
src/
├── components/         # 公共组件
├── views/              # 页面组件
├── composables/        # 组合式函数
├── stores/             # Pinia stores
├── router/             # 路由配置
├── utils/              # 工具函数
├── types/              # 类型定义
└── assets/             # 静态资源
```

## 组件规范

### 组件结构

```vue
<template>
  <div class="component-name">
    <!-- 模板内容 -->
  </div>
</template>

<script setup lang="ts">
// 导入语句
import { ref, computed } from 'vue'

// Props 定义
interface Props {
  modelValue: string
}

// Emits 定义
interface Emits {
  (e: 'update:modelValue', value: string): void
}

// 实现
const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const localValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})
</script>

<style scoped>
/* 样式 */
</style>
```

### 组件命名

- 文件名：PascalCase（UserProfile.vue）
- 组件名：与文件名一致

### 命名语言选择

- **所有标识符使用英语**：组件名、composable 名、变量名、函数名等
- **避免拼音命名**：使用语义化的英文单词
- **技术术语保持英文**：如 Composition API、Props、Emits 等
- **注释根据团队习惯选择**：可以使用中文或英文，建议保持一致
- **代码可读性优先**：选择团队最舒适的语言进行注释

### 使用组合式函数

- 将相关逻辑提取到 composables 中
- 以 use 作为前缀命名（useAuth.ts）

**示例**：
```vue
<script setup lang="ts">
/**
 * 用户资料卡片组件
 * 使用组合式 API 实现
 */

// 定义 Props 接口
interface Props {
  userId: string
}

// 组件状态
const isLoading = ref(false) // 数据加载状态
const userData = ref<User | null>(null) // 用户数据

// 初始化数据
onMounted(async () => {
  await loadUserData()
})
</script>
```

## 开发流程

### 组件开发步骤

1. **先实现基本功能**：让组件能正常工作，完成核心需求
2. **提取可复用逻辑**：识别可复用的状态逻辑并提取为 composables
3. **添加类型验证**：补充 TypeScript 类型，使用 props/emits 验证
4. **优化用户体验**：添加加载状态、错误提示、过渡动画等
5. **编写测试**：单元测试和端到端测试
6. **代码审查和重构**：改善代码结构和可读性

### 功能开发原则

- 优先实现 MVP，验证核心流程后再完善细节
- 每个功能完成后手动测试验证
- 保持组件的独立性和可测试性
- 通过重构逐步改善代码质量
- 及时提交代码并保持提交粒度小

## Git 工作流规范

基于 IDE 层的 Git 规范，Vue 项目的具体实践：

### Commit Message 约定

- **语言**：推荐使用英文，便于国际化协作
- **格式**：遵循 Conventional Commits 规范
- **Scope**：使用组件名、composable 名或功能模块作为 scope

**示例**：
```
feat(components): add UserProfileCard component
  - Implement template with Composition API
  - Add props validation using TypeScript
  - Include loading and error states

fix(composables): fix memory leak in usePolling
  - Clear interval on component unmount
  - Add cleanup function for better resource management

docs(store): update Pinia store documentation
  - Add example for action usage
  - Document state structure
```

### Branch 命名

- `feature/{jira-ticket}-{feature-name}`：新功能开发（如 `feature/PROJ-123-user-dashboard`）
- `bugfix/{bug-description}`：Bug 修复（如 `bugfix/pinia-store-rehydration`）
- `hotfix/{issue}`：紧急修复
- `refactor/{module-name}`：模块重构

### Commit 时机建议

Vue 项目特有的 commit 时机：

1. **完成一个 Vue 组件的开发**：模板、脚本、样式、测试
   ```bash
   git add src/components/UserProfileCard/
   git commit -m "feat(components): add UserProfileCard with Composition API"
   ```

2. **添加一个 composable**：逻辑、类型、测试
   ```bash
   git add src/composables/useAuth.ts src/composables/useAuth.test.ts
   git commit -m "feat(composables): add useAuth for authentication"
   ```

3. **添加 Pinia store**：state、getters、actions
   ```bash
   git add src/stores/userStore.ts
   git commit -m "feat(store): add userStore with auth actions"
   ```

4. **更新 Vue Router 配置**：
   ```bash
   git add src/router/index.ts
   git commit -m "feat(router): add protected route guards"
   ```

5. **修复响应式问题**：
   ```bash
   git commit -m "fix(reactivity): update ref handling in usePolling"
   ```

### 提交前的检查清单

Vue 项目特有的检查项：

- [ ] Vue 组件能够正常渲染，没有报错
- [ ] TypeScript 类型检查通过
- [ ] ESLint 检查通过（无错误，警告已评估）
- [ ] 响应式数据正常工作
- [ ] 添加了必要的单元测试和组件测试
- [ ] 所有测试通过
- [ ] 组件 props 和 emits 定义正确
- [ ] Pinia store 的 actions 和 getters 测试通过
- [ ] Vue Router 路由配置正确
- [ ] Composables 的通用性已验证
- [ ] Commit message 包含组件或功能模块作为 scope
