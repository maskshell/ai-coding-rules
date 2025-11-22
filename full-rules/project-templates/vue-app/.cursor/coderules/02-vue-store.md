# Vue 状态管理规范

## Pinia Store

### Store 结构

- 使用 options store 或 setup store
- 将 state, getters, actions 分离
- 文件名：use + 功能名 + Store（useUserStore.ts）

```typescript
// Setup Store 示例
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref<User | null>(null)
  const loading = ref(false)

  // Getters
  const isAuthenticated = computed(() => !!user.value)
  const fullName = computed(() => {
    return user.value ? `${user.value.firstName} ${user.value.lastName}` : ''
  })

  // Actions
  async function login(credentials: LoginCredentials) {
    loading.value = true
    try {
      const response = await api.login(credentials)
      user.value = response.data
    } finally {
      loading.value = false
    }
  }

  function logout() {
    user.value = null
  }

  return {
    // State
    user,
    loading,
    // Getters
    isAuthenticated,
    fullName,
    // Actions
    login,
    logout
  }
})
```

### Getter 使用

- 使用箭头函数访问 this
- 复杂的计算可以返回函数接收参数

```typescript
// Options Store
export const useStore = defineStore('main', {
  state: () => ({
    items: [] as Item[]
  }),
  getters: {
    getItemById: (state) => {
      return (id: number) => state.items.find(item => item.id === id)
    }
  }
})
```

## Store 使用最佳实践

### 组件中使用

- 在 setup 中调用 useStore
- 使用 storeToRefs 访问 store 的响应式属性

```vue
<script setup lang="ts">
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'

const userStore = useUserStore()
const { user, isAuthenticated } = storeToRefs(userStore)
const { login, logout } = userStore
</script>
```

### 何时使用 Store

- ✅ 跨组件共享状态
- ✅ 需要持久化的状态
- ✅ 复杂的状态逻辑
- ❌ 组件内部状态（使用 ref/reactive）
- ❌ 一次性传递数据（使用 props）
