# React 基础规范

## 组件设计

### 组件类型选择

- 优先使用函数组件 + Hooks
- 只在需要时才使用类组件
- 组件名使用 PascalCase

### 组件结构

```tsx
// 导入语句（外部库在前，内部模块在后，按字母顺序）
import React, { useState, useEffect } from 'react';
import { Button } from './Button';

// 类型定义
interface Props {
  name: string;
}

// 组件实现
export const Component: React.FC<Props> = ({ name }) => {
  // Hooks
  const [state, setState] = useState();

  // 副作用
  useEffect(() => {
    // effect logic
  }, [dependency]);

  return <div>{name}</div>;
};
```

## Hooks 使用

### Hooks 规则

- 只在最顶层调用 Hooks
- 只在 React 函数中调用 Hooks
- 为 useState 提供明确的类型

### 自定义 Hooks

- 以 use 开头命名
- 单一职责，可复用
- 返回清晰的 API
