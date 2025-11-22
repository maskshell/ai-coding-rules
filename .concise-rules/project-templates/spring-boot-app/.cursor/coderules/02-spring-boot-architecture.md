# Spring Boot 架构设计（精简版）

## 分层架构

Request → Controller → Service → Repository → Database

**职责**：
- **Controller**：接收请求，参数验证，返回响应
- **Service**：业务逻辑，事务管理，调用Repository
- **Repository**：数据访问，CRUD操作
- **Entity**：JPA实体，映射数据库
- **DTO**：数据传输，隔离内外模型

**示例**:
```java
// Controller
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    @GetMapping("/{id}")
    public Result<UserDTO> getUser(@PathVariable Long id) {
        UserDTO user = userService.getUserById(id);
        return Result.success(user);
    }
}

// Service
@Service
@Transactional
public class UserServiceImpl implements UserService {
    public UserDTO getUserById(Long id) {
        return userRepository.findById(id)
            .map(userMapper::toDTO)
            .orElseThrow(() -> new UserNotFoundException("用户不存在"));
    }
}

// Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(String username);
    boolean existsByUsername(String username);
}

// DTO
@Data
public class UserCreateDTO {
    @NotBlank
    @Size(min = 3, max = 50)
    private String username;

    @NotBlank
    @Email
    private String email;

    @NotBlank
    @Size(min = 8)
    private String password;
}
```

## RESTful API设计

**URL规范**：
- 使用复数名词：`/users`, `/products`
- 使用连字符：`-`
- 版本号：`/api/v1/`
- 嵌套资源：`/users/{id}/orders`
- 动作接口：`/users/{id}/change-password`

**HTTP方法**：
- GET: 查询列表或单个
- POST: 创建资源
- PUT: 完全更新
- PATCH: 部分更新
- DELETE: 删除资源

**响应格式**：
```java
@Data
public class Result<T> {
    private int code;
    private String message;
    private T data;

    public static <T> Result<T> success(T data) {
        Result<T> result = new Result<>();
        result.setCode(200);
        result.setMessage("success");
        result.setData(data);
        return result;
    }

    public static <T> Result<T> error(int code, String message) {
        Result<T> result = new Result<>();
        result.setCode(code);
        result.setMessage(message);
        return result;
    }
}
```

## 异常处理

**全局异常处理器**：
```java
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(BusinessException.class)
    public Result<Void> handleBusinessException(BusinessException ex) {
        log.warn("业务异常: {}", ex.getMessage());
        return Result.error(ex.getCode(), ex.getMessage());
    }

    @ExceptionHandler(ResourceNotFoundException.class)
    public Result<Void> handleNotFound(ResourceNotFoundException ex) {
        return Result.error(404, ex.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public Result<Map<String, String>> handleValidation(Exception ex) {
        Map<String, String> errors = new HashMap<>();
        // 提取字段错误
        return Result.error(400, "参数验证失败", errors);
    }

    @ExceptionHandler(Exception.class)
    public Result<Void> handleException(Exception ex) {
        log.error("系统异常:", ex);
        return Result.error(500, "服务器内部错误");
    }
}
```

**自定义异常**：
```java
public class BusinessException extends RuntimeException {
    private final int code;
    public BusinessException(int code, String message) {
        super(message);
        this.code = code;
    }
    public int getCode() { return code; }
}

public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String message) {
        super(message);
    }
}

public class UserAlreadyExistsException extends BusinessException {
    public UserAlreadyExistsException(String message) {
        super(400, message);
    }
}
```

## 日志记录

**规范**：
```java
@Slf4j
@Service
public class OrderService {
    public OrderDTO createOrder(OrderCreateDTO dto) {
        log.info("开始创建订单: userId={}, amount={}", dto.getUserId(), dto.getAmount());

        try {
            // 业务逻辑...
            log.info("订单创建成功: orderNo={}", savedOrder.getOrderNo());
            return orderMapper.toDTO(savedOrder);
        } catch (BusinessException e) {
            log.warn("创建订单失败: {}", e.getMessage());
            throw e;
        } catch (Exception e) {
            log.error("创建订单异常: userId={}", dto.getUserId(), e);
            throw new SystemException("创建订单失败");
        }
    }
}
```

## 事务管理

```java
@Service
public class OrderService {
    // 只读事务
    @Transactional(readOnly = true)
    public OrderDTO getOrder(Long id) { ... }

    // 默认事务
    @Transactional
    public OrderDTO createOrder(OrderCreateDTO dto) { ... }

    // 新事务（独立提交）
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void logAsync(UserActionLog log) { ... }
}
```

## API文档

**Swagger注解**：
```java
@RestController
@RequestMapping("/api/v1/users")
@Tag(name = "用户管理")
public class UserController {
    @Operation(summary = "创建用户")
    @ApiResponses({
        @ApiResponse(responseCode = "201", description = "创建成功"),
        @ApiResponse(responseCode = "400", description = "参数错误")
    })
    @PostMapping
    public Result<UserDTO> createUser(@Valid @RequestBody UserCreateDTO dto) {
        return Result.success(userService.createUser(dto));
    }
}
```

## 开发流程

1. **设计接口**：定义API路径、请求/响应格式
2. **创建DTO**：定义请求和响应结构
3. **实现Controller**：处理HTTP请求
4. **实现Service**：编写业务逻辑，添加验证
5. **实现Repository**：定义数据访问
6. **处理异常**：在Service层抛出业务异常
7. **验证测试**：手动测试API功能
8. **添加测试**：编写单元测试和集成测试

**原则**：
- Controller只做参数验证和响应封装
- Service层负责业务逻辑和事务
- Repository只负责数据访问
- 使用Mapper转换Entity和DTO
- 添加必要的日志记录
