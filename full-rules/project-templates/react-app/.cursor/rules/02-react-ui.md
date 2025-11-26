# React UI/UX 规范

## State 管理

### 本地状态

- 简单状态使用 useState
- 相关状态使用 useReducer
- 尽量避免深层嵌套的状态

### 全局状态

- 小型应用使用 Context + useReducer
- 中大型应用使用 Redux Toolkit 或 Zustand

## 性能优化

### 减少重渲染

- 使用 React.memo 包裹纯展示组件
- 使用 useMemo 缓存计算结果
- 使用 useCallback 缓存函数引用

### 代码拆分

- 使用 React.lazy 进行路由级代码拆分
- 对大型组件进行动态导入

## UI 库使用

### 默认使用

- 组件库：shadcn/ui 或 MUI
- 样式方案：Tailwind CSS 或 styled-components
- 表单：React Hook Form + Zod
