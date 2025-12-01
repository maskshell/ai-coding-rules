# SQL 查询优化开发规范

## 技术栈

### 支持的数据库

- **PostgreSQL**：主要支持的数据库
- **MySQL**：支持，注意语法差异
- **SQL Server**：支持，注意语法差异
- **Oracle**：支持，注意语法差异

### 工具和最佳实践

- **查询分析工具**：使用 `EXPLAIN` 或 `EXPLAIN ANALYZE` 分析查询计划
- **版本控制**：所有SQL文件纳入Git管理
- **测试数据**：使用测试数据集验证查询结果

## 核心原则

### 渐进式重构原则

复杂SQL查询优化必须采用渐进式重构，严禁一次性全面重构。这是本规范的核心原则，旨在：

1. **降低风险**：避免一次性修改导致业务逻辑错误
2. **便于验证**：每步修改都可以独立验证
3. **易于回滚**：如果某步出现问题，可以快速回滚
4. **提高可维护性**：清晰的优化历史便于后续维护

### 为什么需要渐进式重构

复杂SQL查询通常包含多个嵌套的子查询、JOIN操作和复杂的WHERE条件。一次性重构整个查询存在以下风险：

- **业务逻辑错误**：可能改变查询的语义，导致结果不正确
- **性能退化**：优化可能适得其反，导致性能下降
- **难以定位问题**：如果出现问题，难以确定是哪部分修改导致的
- **数据不一致**：可能导致生产环境数据查询结果异常

## 项目结构

### SQL文件组织

```text
sql/
├── queries/                  # 查询文件
│   ├── user_report.sql      # 原始查询
│   ├── user_report-step1.sql
│   ├── user_report-step2.sql
│   └── ...
├── migrations/              # 数据库迁移脚本
│   └── ...
├── tests/                   # 测试查询
│   ├── user_report-step1-verify.sql
│   └── ...
└── docs/                    # 文档
    └── optimization-notes.md
```

### 文件命名规范

- **原始查询**：使用描述性名称（如 `user_report.sql`）
- **优化步骤**：使用 `原文件名-step{N}.sql` 格式
- **验证文件**：使用 `原文件名-step{N}-verify.sql` 格式
- **备份文件**：使用 `原文件名-backup-{timestamp}.sql` 格式

## 复杂查询判断标准

### 判断条件

一个查询被认为是"复杂查询"需要满足以下任一条件：

1. **嵌套层数>3层**：查询中包含超过3层的嵌套子查询
2. **子查询数量>5个**：查询中包含超过5个独立的子查询
3. **JOIN数量>5个**：查询中包含超过5个表的JOIN操作
4. **查询执行时间>1秒**：在生产环境中执行时间超过1秒

### 判断示例

**简单查询**（可以直接优化）：

```sql
SELECT u.id, u.name, u.email
FROM users u
WHERE u.created_at > '2024-01-01'
ORDER BY u.created_at DESC
LIMIT 100;
```

**复杂查询**（需要渐进式重构）：

```sql
SELECT u.id, u.name,
       (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count,
       (SELECT SUM(o.amount) FROM orders o WHERE o.user_id = u.id) as total_amount,
       (SELECT AVG(r.rating) FROM reviews r WHERE r.user_id = u.id) as avg_rating,
       (SELECT MAX(p.created_at) FROM posts p WHERE p.user_id = u.id) as last_post_date,
       (SELECT COUNT(*) FROM comments c WHERE c.user_id = u.id) as comment_count
FROM users u
WHERE u.created_at > '2024-01-01'
  AND (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) > 0
  AND (SELECT AVG(r.rating) FROM reviews r WHERE r.user_id = u.id) > 4.0;
```

这个查询包含：

- 5个子查询（嵌套层数2层）
- 需要渐进式重构

## 渐进式重构流程详解

### 步骤1：选择最小可优化单元

**原则**：

- 选择最独立、影响范围最小的单元
- 优先选择可以独立测试的子查询
- 避免选择与其他部分强耦合的单元

**示例**：

```sql
-- 原始查询
SELECT u.id, u.name,
       (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count,
       (SELECT SUM(o.amount) FROM orders o WHERE o.user_id = u.id) as total_amount
FROM users u
WHERE u.created_at > '2024-01-01';

-- 选择优化单元：两个相关的子查询可以合并为一个CTE
-- 这是最小可优化单元
```

### 步骤2：进行最小化修改

**原则**：

- 只修改选定的单元
- 保持其他部分不变
- 确保修改后的逻辑与原查询等价

**示例**：

```sql
-- 步骤1：提取子查询到CTE
WITH user_orders AS (
  SELECT user_id, 
         COUNT(*) as order_count,
         SUM(amount) as total_amount
  FROM orders
  GROUP BY user_id
)
SELECT u.id, u.name,
       COALESCE(uo.order_count, 0) as order_count,
       COALESCE(uo.total_amount, 0) as total_amount
FROM users u
LEFT JOIN user_orders uo ON u.id = uo.user_id
WHERE u.created_at > '2024-01-01';
```

### 步骤3：验证结果一致性

**验证方法**：

1. **行数验证**：确保结果行数一致
2. **列数验证**：确保结果列数一致
3. **数据值验证**：确保每行数据值一致
4. **性能验证**：检查执行时间是否改善

**验证SQL示例**：

```sql
-- user_report-step1-verify.sql
-- 验证步骤1的优化结果

-- 1. 行数验证
SELECT 
  (SELECT COUNT(*) FROM (
    -- 原始查询
    SELECT u.id, u.name,
           (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count,
           (SELECT SUM(o.amount) FROM orders o WHERE o.user_id = u.id) as total_amount
    FROM users u
    WHERE u.created_at > '2024-01-01'
  ) original) as original_count,
  (SELECT COUNT(*) FROM (
    -- 优化后查询
    WITH user_orders AS (
      SELECT user_id, 
             COUNT(*) as order_count,
             SUM(amount) as total_amount
      FROM orders
      GROUP BY user_id
    )
    SELECT u.id, u.name,
           COALESCE(uo.order_count, 0) as order_count,
           COALESCE(uo.total_amount, 0) as total_amount
    FROM users u
    LEFT JOIN user_orders uo ON u.id = uo.user_id
    WHERE u.created_at > '2024-01-01'
  ) optimized) as optimized_count;

-- 2. 数据值验证（使用EXCEPT或NOT EXISTS）
-- PostgreSQL示例
SELECT * FROM (
  -- 原始查询结果
  SELECT u.id, u.name,
         (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count,
         (SELECT SUM(o.amount) FROM orders o WHERE o.user_id = u.id) as total_amount
  FROM users u
  WHERE u.created_at > '2024-01-01'
) original
EXCEPT
SELECT * FROM (
  -- 优化后查询结果
  WITH user_orders AS (
    SELECT user_id, 
           COUNT(*) as order_count,
           SUM(amount) as total_amount
    FROM orders
    GROUP BY user_id
  )
  SELECT u.id, u.name,
         COALESCE(uo.order_count, 0) as order_count,
         COALESCE(uo.total_amount, 0) as total_amount
  FROM users u
  LEFT JOIN user_orders uo ON u.id = uo.user_id
  WHERE u.created_at > '2024-01-01'
) optimized;
```

### 步骤4：确认无误后继续

**检查清单**：

- [ ] 行数一致
- [ ] 列数一致
- [ ] 数据值一致
- [ ] 性能改善（或至少不退化）
- [ ] 代码可读性改善

**确认后**：

- 提交当前步骤的修改
- 选择下一个最小可优化单元
- 重复步骤1-4

## 常见优化模式

### 模式1：子查询转CTE

**适用场景**：多个相关子查询可以合并

**示例**：

```sql
-- 优化前
SELECT u.id,
       (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count,
       (SELECT SUM(o.amount) FROM orders o WHERE o.user_id = u.id) as total_amount
FROM users u;

-- 优化后
WITH user_orders AS (
  SELECT user_id, 
         COUNT(*) as order_count,
         SUM(amount) as total_amount
  FROM orders
  GROUP BY user_id
)
SELECT u.id,
       COALESCE(uo.order_count, 0) as order_count,
       COALESCE(uo.total_amount, 0) as total_amount
FROM users u
LEFT JOIN user_orders uo ON u.id = uo.user_id;
```

### 模式2：相关子查询转JOIN

**适用场景**：子查询只返回单个值

**示例**：

```sql
-- 优化前
SELECT u.id, u.name
FROM users u
WHERE EXISTS (
  SELECT 1 FROM orders o 
  WHERE o.user_id = u.id AND o.status = 'completed'
);

-- 优化后
SELECT DISTINCT u.id, u.name
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed';
```

### 模式3：优化WHERE子句中的子查询

**适用场景**：WHERE子句中的子查询可以提前过滤

**示例**：

```sql
-- 优化前
SELECT u.id, u.name
FROM users u
WHERE u.id IN (
  SELECT user_id FROM orders 
  WHERE created_at > '2024-01-01'
);

-- 优化后
SELECT u.id, u.name
FROM users u
INNER JOIN (
  SELECT DISTINCT user_id 
  FROM orders 
  WHERE created_at > '2024-01-01'
) o ON u.id = o.user_id;
```

## 性能分析工具

### PostgreSQL

```sql
-- 分析查询计划
EXPLAIN ANALYZE
SELECT ...;

-- 详细分析
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT ...;
```

### MySQL

```sql
-- 分析查询计划
EXPLAIN
SELECT ...;

-- 详细分析
EXPLAIN FORMAT=JSON
SELECT ...;
```

### SQL Server

```sql
-- 分析查询计划
SET STATISTICS IO ON;
SET STATISTICS TIME ON;
SELECT ...;
```

## 常见问题解决

### 问题1：优化后结果不一致

**原因**：

- NULL值处理不当
- JOIN类型选择错误（INNER vs LEFT）
- 聚合函数处理NULL的方式不同

**解决方案**：

- 使用COALESCE处理NULL值
- 仔细选择JOIN类型
- 验证聚合函数的行为

### 问题2：优化后性能反而下降

**原因**：

- 缺少必要的索引
- 查询计划选择不当
- 数据分布不均匀

**解决方案**：

- 添加必要的索引
- 使用查询提示（如果数据库支持）
- 分析查询计划，找出瓶颈

### 问题3：如何选择优化顺序

**建议顺序**：

1. 先优化逻辑结构（子查询、JOIN）
2. 再优化索引
3. 最后考虑数据库特定的优化技巧

## 开发流程

### 开发步骤

1. **分析原始查询**：理解业务逻辑，识别性能瓶颈
2. **识别优化单元**：找出可以独立优化的子查询或JOIN
3. **选择最小单元**：从最简单的单元开始
4. **进行最小化修改**：只修改选定的单元
5. **执行验证**：确保结果与原查询完全一致
6. **记录变更**：在验证文件中记录修改内容
7. **继续下一步**：验证通过后选择下一个单元
8. **最终验证**：所有优化完成后进行全面测试

### 功能开发原则

- 优先保证正确性，再考虑性能优化
- 每个优化步骤都要有独立的验证
- 保持原始查询文件作为参考
- 通过小步迭代逐步改善查询性能
- 及时提交代码，保持提交粒度小
- 在测试环境充分验证后再应用到生产环境

### 性能优化原则

- 先优化逻辑结构（子查询、JOIN），再优化索引
- 使用EXPLAIN分析查询计划
- 避免过度优化，保持查询可读性
- 考虑数据库特定的优化技巧（如PostgreSQL的CTE、MySQL的索引提示）

## 最佳实践

### 代码组织

- 每个优化步骤都有独立的文件
- 保留原始查询作为参考
- 验证文件与优化文件一一对应

### 版本控制

- 使用Git管理所有SQL文件
- 每次优化步骤单独提交
- 提交信息清晰描述优化内容

### 文档记录

- 记录每次优化的原因和目标
- 记录性能改善情况
- 记录遇到的问题和解决方案

### 测试策略

- 使用测试数据集验证
- 在生产环境的小数据集上验证
- 逐步推广到完整数据集

## 参考资源

- [PostgreSQL查询优化指南](https://www.postgresql.org/docs/current/performance-tips.html)
- [MySQL查询优化](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)
- [SQL Server查询优化](https://docs.microsoft.com/en-us/sql/relational-databases/performance/query-optimization)
