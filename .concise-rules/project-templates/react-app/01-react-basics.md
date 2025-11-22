# React 基础规范（精简版）

## 组件设计

- 优先使用函数组件 + Hooks
- 组件名使用 PascalCase（UserProfile.tsx）
- 文件名与默认导出同名

## 组件结构

```tsx
// 导入（外部库在前，内部模块在后）
import React, { useState } from 'react'

// Props 类型
interface Props {
  name: string
}

// 组件
export const Component = ({ name }: Props) => {
  // Hooks
  const [state, setState] = useState()

  return <div>{name}</div>
}
```

## Hooks 使用

- 只在顶层调用 Hooks
- 只在 React 函数中调用 Hooks
- 自定义 Hooks 以 use 开头

## 状态管理

- 简单状态：useState
- 相关状态：useReducer
- 全局状态：Context + useReducer（小项目）或 Redux Toolkit/Zustand（大项目）

## 性能优化

- 纯展示组件用 React.memo
- 计算结果用 useMemo 缓存
- 函数用 useCallback 缓存

## 命名

- 组件：PascalCase
- hooks：use 前缀
- 工具函数：camelCase
