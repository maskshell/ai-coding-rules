# Spring Boot 后端开发规范

## 技术栈

### 核心框架

- Spring Boot 3.x（应用框架，基于 Spring 6 和 Java 17）
- Spring Security 6.x（认证和授权）
- Spring Data JPA & MyBatis-Plus（数据访问层）
  - `spring-boot-starter-data-jpa`：简化 JPA 操作
  - `mybatis-plus-boot-starter`：增强 MyBatis 功能
- Spring Boot Validation（参数校验）
- MySQL 8（关系型数据库，使用 MyBatis 或 JPA）
- Redis（缓存和会话管理）

### 代码质量工具

- Lombok（减少样板代码：如 getter、setter、toString）
- MapStruct（对象映射：Entity ↔ DTO）
- AssertJ（流畅的断言库）
- Jacoco（代码覆盖率）
- SpotBugs（静态代码分析）

### API 文档与测试

- Swagger 2.x / SpringDoc OpenAPI 3（API 文档生成）
- JUnit 5 + Mockito（单元测试）
- Testcontainers（集成测试）

### 构建工具

- Maven 3.x（依赖管理和构建）
- Spring Profile（多环境配置管理）

---

## 项目结构

Spring Boot 后端采用**分层架构**，职责清晰、便于维护：

```text
src/main/java/com/example/demo/
├── DemoApplication.java              # 启动类
│
├── controller/                       # Controller 层（REST API）
│   ├── UserController.java
│   ├── AuthController.java
│   └── HealthController.java
│
├── service/                          # Service 层（业务逻辑）
│   ├── UserService.java              # Service 接口
│   ├── impl/
│   │   └── UserServiceImpl.java      # Service 实现
│   └── EmailService.java
│
├── repository/                       # Repository 层（数据访问）
│   ├── UserRepository.java           # JPA Repository
│   └── OrderRepository.java
│
├── mapper/                           # MyBatis Mapper 接口
│   ├── UserMapper.java
│   └── ProductMapper.java
│
├── entity/                           # Entity 层（数据库实体）
│   ├── User.java                     # JPA Entity
│   └── Order.java
│
├── dto/                              # DTO 层（数据传输对象）
│   ├── request/
│   │   ├── UserCreateDTO.java
│   │   └── UserUpdateDTO.java
│   └── response/
│       ├── UserDTO.java
│       └── LoginResponse.java
│
├── vo/                               # VO 层（视图对象，用于复杂查询）
├── constant/                         # 常量类
│   ├── AppConstants.java
│   └── RoleConstant.java
│
├── enums/                            # 枚举类
│   ├── OrderStatus.java
│   └── UserStatus.java
│
├── config/                           # 配置类
│   ├── SecurityConfig.java
│   ├── JpaConfig.java
│   └── SwaggerConfig.java
│
├── exception/                        # 自定义异常和全局异常处理
│   ├── BusinessException.java
│   ├── UserNotFoundException.java
│   └── handler/
│       └── GlobalExceptionHandler.java
│
├── security/                         # 安全（JWT、权限控制）
│   ├── JwtTokenProvider.java
│   └── SecurityUserDetails.java:
│
├── aspect/                           # 切面编程（日志、权限检查）
├── utils/                            # 工具类
│   ├── DateUtil.java
│   └── JwtUtil.java
│
└── annotation/                       # 自定义注解
```

---

## 命名规范

| 类型 | 命名风格 | 示例 |
|------|---------|------|
| 包名（Package） | 小写单词 | `com.example.demo.controller` |
| 类名（Class） | 大驼峰 / PascalCase | `UserService`, `UserController` |
| 接口（Interface） | 大驼峰 / PascalCase | `UserService`, `IUserService` |
| 枚举（Enum） | 大驼峰 | `OrderStatus.java` |
| 注解（Annotation） | 大驼峰 | `@RequiredPermission` |
| 方法（Method） | 小驼峰 / camelCase | `getUserById`, `createUser` |
| 变量（Variable） | 小驼峰 / camelCase | `userName`, `orderList` |
| 常量（Constant） | 全大写 + 下划线 | `MAX_PAGE_SIZE`, `DEFAULT_TIMEOUT` |

### 关键命名规则

- **分层后缀**：`Controller`, `Service`, `Repository`, `Entity`, `Mapper`
  - ✅ `UserController`, `UserServiceImpl`, `UserRepository`
  - ❌ `UserCtrl`, `UserSV`, `UserRepo`

- **接口与实现**：
  - Service 接口：`UserService`
  - 实现类：`UserServiceImpl`
  - Data 接口：`UserDataService`
  - Mapper 接口：`UserMapper`（MyBatis）

- **实体类**：
  - JPA：`User.java`, `Order.java`
  - DTO：`UserDTO.java`, `UserCreateDTO.java`

- **方法名**：
  - 业务方法：动词 + 对象（如 `createUser`）
  - Getter/Setter：Lombok 自动生成
  - 布尔值：`isEnabled()`, `hasPermission()`

---

## 依赖管理

### Maven 依赖管理

Spring Boot 项目使用 Maven 管理依赖（也可以使用 Gradle）。推荐使用最新稳定版本：

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>
    <relativePath/>
</parent>

<properties>
    <maven.compiler.source>17</maven.compiler.source>
    <maven.compiler.target>17</maven.compiler.target>
    <mybatis-plus.version>3.5.5</mybatis-plus.version>
    <mapstruct.version>1.5.5.Final</mapstruct.version>
    <jwt.version>0.12.3</jwt.version>
</properties>
```

### 依赖分类管理

将依赖按功能模块分组，便于维护：

```xml
<!-- Web & MVC -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>

<!-- Validation -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>

<!-- JPA -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>

<!-- MySQL Driver -->
<dependency>
    <groupId>com.mysql</groupId>
    <artifactId>mysql-connector-j</artifactId>
    <scope>runtime</scope>
</dependency>

<!-- MyBatis-Plus -->
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-boot-starter</artifactId>
    <version>${mybatis-plus.version}</version>
</dependency>

<!-- Redis -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>

<!-- JWT -->
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-api</artifactId>
    <version>${jwt.version}</version>
</dependency>

<!-- Lombok（简化代码）-->
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <optional>true</optional>
</dependency>

<!-- MapStruct（对象映射）-->
<dependency>
    <groupId>org.mapstruct</groupId>
    <artifactId>mapstruct</artifactId>
    <version>${mapstruct.version}</version>
</dependency>

<!-- Swagger -->
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.3.0</version>
</dependency>

<!-- Test -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
```

---

## 配置管理

### application.yml 配置分离

多环境配置文件分离，避免硬编码敏感信息：

```yaml
# application.yml（主配置）
spring:
  application:
    name: spring-boot-app
  profiles:
    active: dev

# application-dev.yml（开发环境）
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/demo_dev
    username: ${DB_USER:root}
    password: ${DB_PASSWORD:}
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
    properties:
      hibernate:
        format_sql: true
        dialect: org.hibernate.dialect.MySQL8Dialect

logging:
  level:
    root: INFO
    com.demo: DEBUG
    org.springframework.web: DEBUG
    org.hibernate.SQL: DEBUG

# application-prod.yml（生产环境）
spring:
  datasource:
    url: ${DB_URL}
    username: ${DB_USER}
    password: ${DB_PASSWORD}
    driver-class-name: com.mysql.cj.jdbc.Driver
    hikari:
      maximum-pool-size: 20
      minimum-idle: 10
      connection-timeout: 20000
  jpa:
    hibernate:
      ddl-auto: none
    show-sql: false

logging:
  level:
    root: WARN
    com.demo: INFO
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} - %msg%n"
    file: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"
  file:
    name: logs/application.log
    max-size: 100MB
    max-history: 30
```

---

## Controller 层规范

### RESTful API 设计原则

1. **URL 命名**：复数名词 + 连字符（可选）
   - ✅ `/api/v1/users`, `/api/v1/products`
   - ✅ `/api/v1/user-orders`（连字符更友好）
   - ❌ `/User`, `/getUser`, `/api/v1/user_orders`

2. **HTTP 方法** 语义化：

| 操作 | HTTP 方法 | URL 示例 |
|------|----------|----------|
| 查询列表 | GET | `/users` |
| 查询单个 | GET | `/users/{id}` |
| 新增 | POST | `/users` |
| 完全更新 | PUT | `/users/{id}` |
| 部分更新 | PATCH | `/users/{id}` |
| 删除 | DELETE | `/users/{id}` |

3. **控制器方法示例**：

```java
@Slf4j
@RestController
@RequestMapping("/api/v1/users")
@Validated
@Api(tags = "用户管理")
public class UserController {
    private final UserService userService;

    @GetMapping
    @ApiOperation("查询用户列表")
    public Result<List<UserDTO>> getAllUsers() {
        List<UserDTO> users = userService.getAllUsers();
        return Result.success(users);
    }

    @GetMapping("/{id}")
    @ApiOperation("根据ID查询用户")
    public Result<UserDTO> getUser(@PathVariable @Min(1) Long id) {
        UserDTO user = userService.getUserById(id);
        return Result.success(user);
    }

    @PostMapping
    @ApiOperation("创建用户")
    @ResponseStatus(HttpStatus.CREATED)
    public Result<UserDTO> createUser(@Valid @RequestBody UserCreateDTO userDTO) {
        UserDTO createdUser = userService.createUser(userDTO);
        return Result.success(createdUser);
    }

    @PutMapping("/{id}")
    @ApiOperation("更新用户信息")
    public Result<UserDTO> updateUser(
            @PathVariable Long id,
            @Valid @RequestBody UserUpdateDTO userDTO) {
        UserDTO updatedUser = userService.updateUser(id, userDTO);
        return Result.success(updatedUser);
    }

    @DeleteMapping("/{id}")
    @ApiOperation("删除用户")
    public Result<Void> deleteUser(@PathVariable Long id) {
        userService.deleteUser(id);
        return Result.success();
    }
}
```

### API 版本管理

- 使用 URL 路径版本：`/api/v1`, `/api/v2`
- 或请求头版本：`Accept: application/vnd.company.v1+json`
- 推荐 URL 版本，更直观、易于调试

---

## Service 层规范

### 业务逻辑管理

Service 层是业务逻辑核心，负责：

1. **调用 Repository** 进行数据访问
2. **管理事务**：使用 `@Transactional`
3. **参数校验**：业务规则验证
4. **异常处理**：抛出业务异常

```java
@Slf4j
@Service
@Transactional
@RequiredArgsConstructor  // Lombok 构造函数注入
public class UserServiceImpl implements UserService {
    private final UserRepository userRepository;
    private final UserMapper userMapper;
    private final PasswordEncoder passwordEncoder;

    @Override
    public UserDTO getUserById(Long id) {
        return userRepository.findById(id)
            .map(userMapper::toDTO)
            .orElseThrow(() -> new UserNotFoundException("用户不存在: " + id));
    }

    @Override
    public UserDTO createUser(UserCreateDTO dto) {
        // 业务验证
        if (userRepository.existsByUsername(dto.getUsername())) {
            throw new UserAlreadyExistsException("用户名已存在");
        }

        // 数据转换 + 业务处理
        User user = userMapper.toEntity(dto);
        user.setPassword(passwordEncoder.encode(dto.getPassword()));
        user.setEnabled(true);

        User savedUser = userRepository.save(user);
        log.info("创建用户成功: id={}", savedUser.getId());

        return userMapper.toDTO(savedUser);
    }

    @Override
    @Transactional(readOnly = true)
    public PageResult<UserDTO> getUsers(UserQuery query) {
        Pageable pageable = PageRequest.of(
            query.getPage() - 1,
            query.getPageSize(),
            Sort.by(Sort.Direction.DESC, "createdAt")
        );

        Page<User> page = userRepository.findAll(pageable);

        return PageResult.<UserDTO>builder()
            .total(page.getTotalElements())
            .page(query.getPage())
            .pageSize(query.getPageSize())
            .items(page.getContent().stream()
                .map(userMapper::toDTO)
                .collect(Collectors.toList()))
            .build();
    }
}
```

### 事务管理最佳实践

```java
// 只读事务（查询）
@Transactional(readOnly = true)
public List<ProductDTO> getProducts() { ... }

// 新事务（独立提交）
@Transactional(propagation = Propagation.REQUIRES_NEW)
public void logAsync(UserActionLog log) { ... }

// 避免回滚异常
@Transactional(rollbackFor = Exception.class)
public void processWithExternalApi() throws Exception { ... }
```

---

## Repository & Mapper 层

### Spring Data JPA Repository

```java
public interface UserRepository extends JpaRepository<User, Long> {
    // 根据命名约定自动生成查询
    Optional<User> findByUsername(String username);

    boolean existsByUsername(String username);

    // JPQL 查询
    @Query("SELECT u FROM User u WHERE u.enabled = true AND u.createdAt BETWEEN ?1 AND ?2")
    List<User> findActiveUsersBetween(LocalDateTime start, LocalDateTime end);

    // 分页 + 排序
    Page<User> findByUsernameContaining(String username, Pageable pageable);
}
```

### MyBatis Mapper

```java
@Mapper
public interface ProductMapper extends BaseMapper<Product> {
    // 自定义查询
    @Select("SELECT * FROM products WHERE name LIKE CONCAT('%', #{name}, '%')")
    List<Product> searchByName(@Param("name") String name);
}

<!-- XML 方式 -->
<!-- resources/mapper/ProductMapper.xml -->
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
  "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.example.demo.mapper.ProductMapper">
    <select id="searchByName" resultType="com.example.demo.entity.Product">
        SELECT * FROM products WHERE name LIKE CONCAT('%', #{name}, '%')
    </select>
</mapper>
```

---

## DTO & Entity

### DTO 设计模式（Data Transfer Object）

目的：隔离内部模型（Entity）和外部 API 模型

```java
// 创建 DTO
@Data
public class UserCreateDTO {
    @NotBlank(message = "用户名不能为空")
    @Size(min = 3, max = 50, message = "用户名长度3-50")
    private String username;

    @NotBlank(message = "邮箱不能为空")
    @Email(message = "邮箱格式不正确")
    private String email;

    @NotBlank(message = "密码不能为空")
    @Size(min = 8, max = 20, message = "密码长度8-20")
    private String password;
}

// 更新 DTO
@Data
public class UserUpdateDTO {
    @Size(min = 3, max = 50)
    private String username;

    @Email
    private String email;

    private String phone;
}

// 响应 DTO
@Data
public class UserDTO {
    private Long id;
    private String username;
    private String email;
    private String phone;
    private Boolean enabled;
    private LocalDateTime createdAt;
}
```

### Entity 设计

```java
@Entity
@Table(name = "users")
@Data
@EntityListeners(AuditingEntityListener.class)
public class User implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 50)
    private String username;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String password;

    @Column(nullable = false)
    private Boolean enabled = true;

    @Column(name = "created_by")
    @CreatedBy
    private String createdBy;

    @Column(name = "created_at", updatable = false)
    @CreatedDate
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    @LastModifiedDate
    private LocalDateTime updatedAt;
}
```

---

## 异常处理

### 全局异常处理器

```java
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    // 业务异常
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<Result<Void>> handleBusinessException(BusinessException ex) {
        log.warn("业务异常: {}", ex.getMessage());
        return ResponseEntity
            .status(HttpStatus.BAD_REQUEST)
            .body(Result.error(ex.getCode(), ex.getMessage()));
    }

    // 资源未找到
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<Result<Void>> handleNotFound(ResourceNotFoundException ex) {
        log.warn("资源未找到: {}", ex.getMessage());
        return ResponseEntity
            .status(HttpStatus.NOT_FOUND)
            .body(Result.error(404, ex.getMessage()));
    }

    // 参数验证失败
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Result<Map<String, String>>> handleValidation(
            MethodArgumentNotValidException ex) {
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(error ->
            errors.put(error.getField(), error.getDefaultMessage())
        );
        return ResponseEntity
            .status(HttpStatus.BAD_REQUEST)
            .body(Result.error(400, "参数验证失败", errors));
    }

    // 系统异常
    @ExceptionHandler(Exception.class)
    public ResponseEntity<Result<Void>> handleException(Exception ex) {
        log.error("系统异常:", ex);
        return ResponseEntity
            .status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(Result.error(500, "服务器内部错误"));
    }
}
```

### 自定义异常类

```java
// 基础业务异常
public class BusinessException extends RuntimeException {
    private final int code;

    public BusinessException(int code, String message) {
        super(message);
        this.code = code;
    }

    public int getCode() {
        return code;
    }
}

// 具体业务异常
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

---

## 响应格式统一

### 标准响应格式

```java
@Data
public class Result<T> {
    private int code;           // 状态码：200成功，400参数错误，500系统错误
    private String message;     // 提示消息
    private T data;             // 响应数据

    public static <T> Result<T> success() {
        Result<T> result = new Result<>();
        result.setCode(200);
        result.setMessage("success");
        return result;
    }

    public static <T> Result<T> success(T data) {
        Result<T> result = new Result<>();
        result.setCode(200);
        result.setMessage("success");
        result.setData(data);
        return result;
    }

    public static <T> Result<T> success(String message, T data) {
        Result<T> result = new Result<>();
        result.setCode(200);
        result.setMessage(message);
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

// 分页结果
@Data
@Builder
public class PageResult<T> implements Serializable {
    private long total;         // 总记录数
    private int page;           // 当前页码
    private int pageSize;       // 每页数量
    private List<T> items;      // 数据列表
}
```

---

## API 文档（Swagger / OpenAPI）

配置 SpringDoc OpenAPI 3：

```java
@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI springDocOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("API 文档")
                .description("Spring Boot 3 + SpringDoc OpenAPI 3")
                .version("1.0.0")
                .contact(new Contact()
                    .name("技术支持")
                    .email("support@example.com")));
    }
}

// Controller 中使用
@RestController
@RequestMapping("/api/v1/users")
@Tag(name = "用户管理", description = "用户增删改查接口")
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

---

## 安全规范（Spring Security + JWT）

### JWT 认证示例

```java
@Configuration
@EnableWebSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final JwtTokenFilter jwtTokenFilter;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/v1/auth/**").permitAll()
                .requestMatchers("/api/v1/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtTokenFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}

// JWT Token Provider
@Component
public class JwtTokenProvider {
    private final String secretKey = "your-secret-key";
    private final long validityInMilliseconds = 3600000; // 1h

    public String createToken(String username, List<String> roles) {
        Claims claims = Jwts.claims().setSubject(username);
        claims.put("roles", roles);

        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + validityInMilliseconds);

        return Jwts.builder()
            .setClaims(claims)
            .setIssuedAt(now)
            .setExpiration(expiryDate)
            .signWith(SignatureAlgorithm.HS256, secretKey)
            .compact();
    }

    public boolean validateToken(String token) {
        try {
            Jwts.parser().setSigningKey(secretKey).parseClaimsJws(token);
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    public String getUsername(String token) {
        return Jwts.parser()
            .setSigningKey(secretKey)
            .parseClaimsJws(token)
            .getBody()
            .getSubject();
    }
}
```

---

## 测试规范

### 分层测试策略

| 测试类型 | 测试范围 | 使用工具 | 运行速度 |
|---------|---------|---------|---------|
| 单元测试 | Service、Repository | JUnit 5 + Mockito | 毫秒级 |
| 集成测试 | Controller + Service + Repository | JUnit 5 + Testcontainers | 秒级 |
| 端到端测试 | 完整系统 | Selenium / RestAssured | 分钟级 |

### 单元测试示例

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    @Mock
    private UserRepository userRepository;

    @Mock
    private UserMapper userMapper;

    @InjectMocks
    private UserServiceImpl userService;

    @Test
    void shouldReturnUser_WhenUserExists() {
        // Given
        Long userId = 1L;
        User user = new User();
        user.setId(userId);
        user.setUsername("testuser");

        UserDTO userDTO = new UserDTO();
        userDTO.setId(userId);
        userDTO.setUsername("testuser");

        given(userRepository.findById(userId)).willReturn(Optional.of(user));
        given(userMapper.toDTO(user)).willReturn(userDTO);

        // When
        UserDTO result = userService.getUserById(userId);

        // Then
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(userId);
        assertThat(result.getUsername()).isEqualTo("testuser");
        verify(userRepository).findById(userId);
    }

    @Test
    void shouldThrowException_WhenUserNotFound() {
        // Given
        Long userId = 999L;
        given(userRepository.findById(userId)).willReturn(Optional.empty());

        // When & Then
        assertThatThrownBy(() -> userService.getUserById(userId))
            .isInstanceOf(UserNotFoundException.class)
            .hasMessage("用户不存在: " + userId);
    }
}
```

### 集成测试示例

```java
@SpringBootTest
@AutoConfigureMockMvc
@Testcontainers
class UserControllerIntegrationTest {
    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private UserRepository userRepository;

    @Container
    static MySQLContainer<?> mysql = new MySQLContainer<>("mysql:8.0");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", mysql::getJdbcUrl);
        registry.add("spring.datasource.username", mysql::getUsername);
        registry.add("spring.datasource.password", mysql::getPassword);
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    void shouldCreateUser_WhenValidInput() throws Exception {
        UserCreateDTO dto = new UserCreateDTO();
        dto.setUsername("newuser");
        dto.setEmail("newuser@example.com");
        dto.setPassword("password123");

        mockMvc.perform(post("/api/v1/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(dto)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.code").value(200))
            .andExpect(jsonPath("$.data.username").value("newuser"));

        assertThat(userRepository.findByUsername("newuser")).isPresent();
    }
}
```

---

## 开发流程（敏捷开发）

### 后端开发步骤（迭代式开发）

1. **设计数据库表结构**（关键第一步）
   - 分析业务需求
   - 设计合理的表结构（遵循 3NF）
   - 添加必要的索引
   - 编写建表 SQL

2. **创建实体类（Entity）**
   - 创建 JPA Entity 或 MyBatis Model
   - 添加完整注解（表映射、字段约束）
   - 测试实体映射是否正确

3. **定义 DTO（Request/Response）**
   - 创建请求 DTO（参数验证）
   - 创建响应 DTO（敏感信息脱敏）
   - 使用 Bean Validation 注解（如 `@NotBlank`）

4. **实现 Repository / Mapper**
   - JPA：继承 `JpaRepository`
   - MyBatis：定义 `@Mapper` 接口 + XML

5. **编写 Service 层**
   - 定义 Service 接口
   - 实现业务逻辑
   - 添加事务管理（`@Transactional`）
   - 创建 Mapper（Entity ↔ DTO）

6. **编写 Controller 层**
   - 创建 REST API（RESTful 风格）
   - 验证请求参数
   - 调用 Service 方法
   - 返回统一响应格式

7. **异常处理**
   - 创建自定义业务异常
   - 创建全局异常处理器（`@RestControllerAdvice`）
   - 返回统一错误格式

8. **API 文档**
   - 配置 Swagger / OpenAPI
   - 为 Controller 添加文档注解

9. **编写测试**
   - 单元测试（Service、Repository）
   - 集成测试（Controller + 真实数据库）
   - 验证测试覆盖率

10. **代码审查 & 重构**
    - 团队成员互相 Review
    - 重构重复代码
    - 优化性能（SQL、缓存）

> **MVP 优先原则**：先实现核心功能、验证主流程，再完善细节、添加测试

---

## 日志规范

### 日志级别

| 级别 | 使用场景 | 示例 |
|------|----------|------|
| TRACE | 最详细的调试信息 | 入参、返回值 |
| DEBUG | 调试信息 | SQL 查询、业务逻辑 |
| INFO | 业务执行流程 | 用户注册、订单创建 |
| WARN | 警告（非致命） | 参数异常、业务失败 |
| ERROR | 错误（需处理） | 系统异常、数据库连接失败 |

### 日志记录规范

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
            throw new SystemException("创建订单失败，请稍后重试");
        }
    }
}
```

---

## 性能优化

### 常见优化策略

1. **数据库优化**
   - 为常用查询字段添加索引（`@Index`）
   - 避免 N+1 查询（`JOIN FETCH`）
   - 批量操作（`saveAll`）

2. **缓存策略**
   - Spring Cache：`@Cacheable`, `@CacheEvict`
   - 合理使用 Redis 缓存热点数据

3. **异步处理**
   - `@Async` 异步方法（发送邮件、短信）
   - Spring Event 事件机制（解耦业务）

4. **日志优化**
   - 生产环境关闭 SQL 日志
   - 异步日志（Logback AsyncAppender）

---

## 推荐的 IDEA 插件

| 插件名称 | 用途 |
|---------|------|
| **Lombok** | 注解生成代码 |
| **RestfulToolkit** | REST API 快速定位 |
| **MyBatisX** | MyBatis 接口与 XML 跳转 |
| **SonarLint** | 代码质量检查 |
| **Spring Boot Assistant** | Spring 特性支持 |

---

## 参考资料

- [Spring Boot 官方文档](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/)
- [Spring Security 官方文档](https://docs.spring.io/spring-security/reference/index.html)
- [Spring Data JPA 官方文档](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
- [MyBatis-Plus 官方文档](https://baomidou.com/)
- [SpringDoc OpenAPI 3 文档](https://springdoc.org/)
- [MapStruct 官方文档](https://mapstruct.org/)
