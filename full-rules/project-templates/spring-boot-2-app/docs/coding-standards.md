# Spring Boot 2.0 后端开发规范

## 技术栈

### 核心框架

- **Spring Boot 2.0.x**（应用框架，基于 Spring Framework 5.0）
  - 支持 Java 8、9、10、11
  - 推荐使用 Java 11（LTS 版本）
- **Spring Security 5.x**（认证和授权）
- **Spring Data JPA & MyBatis**（数据访问层）
  - `spring-boot-starter-data-jpa`：简化 JPA 操作
  - `mybatis-spring-boot-starter`：MyBatis 集成
- **Spring Boot Validation**（参数校验）
- **MySQL 8**（关系型数据库）
- **Redis**（缓存和会话管理）

### 代码质量工具

- **Lombok**（减少样板代码：如 getter、setter、toString）
- **MapStruct**（对象映射：Entity ↔ DTO）
- **AssertJ**（流畅的断言库）
- **Jacoco**（代码覆盖率）
- **SpotBugs**（静态代码分析）

### API 文档与测试

- **Swagger 2.x**（API 文档生成）
- **JUnit 5 + Mockito**（单元测试）
- **Testcontainers**（集成测试）

### 构建工具

- **Maven 3.x** 或 **Gradle 5.x**（依赖管理和构建）
- **Spring Profile**（多环境配置管理）

## 项目结构

Spring Boot 2.0 后端采用**分层架构**，职责清晰、便于维护：

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
│   ├── SwaggerConfig.java
│   └── AppConfig.java                # 应用配置（使用 @ConfigurationProperties）
│
├── exception/                        # 自定义异常和全局异常处理
│   ├── BusinessException.java
│   ├── UserNotFoundException.java
│   └── handler/
│       └── GlobalExceptionHandler.java
│
├── security/                         # 安全（JWT、权限控制）
│   ├── JwtTokenProvider.java
│   └── SecurityUserDetails.java
│
├── aspect/                           # 切面编程（日志、权限检查）
│   └── LoggingAspect.java
│
└── utils/                            # 工具类
    ├── DateUtils.java
    └── StringUtils.java
```

## 详细规范

### 启动类规范

Spring Boot 2.0 启动类使用 `@SpringBootApplication` 注解，这是 `@Configuration`、`@EnableAutoConfiguration` 和 `@ComponentScan` 的组合。

```java
@SpringBootApplication
@EnableJpaRepositories("com.example.demo.repository")
@EntityScan("com.example.demo.entity")
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

### 构建配置（Maven）

Spring Boot 2.0 使用 Parent POM 管理版本：

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>2.0.9.RELEASE</version>
    <relativePath/>
</parent>

<properties>
    <java.version>11</java.version>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <mybatis.version>2.0.1</mybatis.version>
    <jwt.version>0.10.7</jwt.version>
</properties>

<dependencies>
    <!-- Web -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <!-- Validation -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>

    <!-- 数据库 -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <scope>runtime</scope>
    </dependency>

    <!-- MyBatis -->
    <dependency>
        <groupId>org.mybatis.spring.boot</groupId>
        <artifactId>mybatis-spring-boot-starter</artifactId>
        <version>${mybatis.version}</version>
    </dependency>

    <!-- Lombok -->
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <optional>true</optional>
    </dependency>

    <!-- 测试 -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### 配置文件（application.yml）

Spring Boot 2.0 支持 YAML 和 Properties 格式，推荐使用 YAML：

```yaml
# application.yml
spring:
  application:
    name: demo-service
  profiles:
    active: dev
  datasource:
    url: ${DB_URL:jdbc:mysql://localhost:3306/demo?useSSL=false&serverTimezone=UTC}
    username: ${DB_USERNAME:root}
    password: ${DB_PASSWORD:}
    driver-class-name: com.mysql.cj.jdbc.Driver
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
  jpa:
    hibernate:
      ddl-auto: none
    show-sql: false
    properties:
      hibernate:
        format_sql: true
        dialect: org.hibernate.dialect.MySQL8Dialect
        jdbc:
          time_zone: UTC

mybatis:
  mapper-locations: classpath:mapper/*.xml
  type-aliases-package: com.example.demo.entity
  configuration:
    map-underscore-to-camel-case: true

logging:
  level:
    com.example.demo: DEBUG
    org.springframework.web: INFO
    org.hibernate.SQL: DEBUG
```

### 配置属性绑定（Spring Boot 2.0 新特性）

Spring Boot 2.0 改进了配置属性绑定，支持类型安全的配置：

```java
@ConfigurationProperties(prefix = "app")
@Validated
@Data
public class AppProperties {
    @NotBlank
    private String name;
    
    @Valid
    private Security security = new Security();
    
    @Data
    public static class Security {
        private String jwtSecret;
        private Long jwtExpiration = 86400000L; // 24小时
    }
}

@Configuration
@EnableConfigurationProperties(AppProperties.class)
public class AppConfig {
    // 配置类内容
}
```

对应的配置文件：

```yaml
app:
  name: demo-service
  security:
    jwt-secret: ${JWT_SECRET:your-secret-key}
    jwt-expiration: 86400000
```

### 分层架构

#### Controller 层

- 只处理 HTTP 请求和响应
- 参数验证使用 `@Valid` 和 Bean Validation
- 返回统一的响应格式

```java
@RestController
@RequestMapping("/api/v1/users")
@Validated
@Api(tags = "用户管理")
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/{id}")
    @ApiOperation("根据ID获取用户")
    public ResponseEntity<Result<UserDTO>> getUser(@PathVariable @Min(1) Long id) {
        UserDTO user = userService.getUserById(id);
        return ResponseEntity.ok(Result.success(user));
    }

    @PostMapping
    @ApiOperation("创建用户")
    public ResponseEntity<Result<UserDTO>> createUser(@Valid @RequestBody UserCreateDTO userDTO) {
        UserDTO createdUser = userService.createUser(userDTO);
        return ResponseEntity.status(HttpStatus.CREATED).body(Result.success(createdUser));
    }
}
```

#### Service 层

- 业务逻辑实现
- 事务管理（`@Transactional`）
- 异常处理

```java
public interface UserService {
    UserDTO getUserById(Long id);
    UserDTO createUser(UserCreateDTO userCreateDTO);
    PageResult<UserDTO> getUsers(PageQuery pageQuery);
}

@Slf4j
@Service
@Transactional
public class UserServiceImpl implements UserService {
    private final UserRepository userRepository;
    private final UserMapper userMapper;

    public UserServiceImpl(UserRepository userRepository, UserMapper userMapper) {
        this.userRepository = userRepository;
        this.userMapper = userMapper;
    }

    @Override
    @Transactional(readOnly = true)
    public UserDTO getUserById(Long id) {
        return userRepository.findById(id)
                .map(userMapper::toDTO)
                .orElseThrow(() -> new UserNotFoundException("用户不存在"));
    }

    @Override
    public UserDTO createUser(UserCreateDTO userCreateDTO) {
        if (userRepository.existsByUsername(userCreateDTO.getUsername())) {
            throw new UserAlreadyExistsException("用户名已存在");
        }

        User user = userMapper.toEntity(userCreateDTO);
        user.setPassword(BCrypt.hashpw(userCreateDTO.getPassword(), BCrypt.gensalt()));

        User savedUser = userRepository.save(user);
        log.info("创建新用户: {}", savedUser.getUsername());

        return userMapper.toDTO(savedUser);
    }
}
```

#### Repository 层

- 数据访问接口
- 使用 Spring Data JPA 命名查询或 `@Query` 注解

```java
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(String username);
    boolean existsByUsername(String username);
    
    @Query("SELECT u FROM User u WHERE u.enabled = true")
    List<User> findActiveUsers();
}
```

### 异常处理

使用 `@RestControllerAdvice` 统一处理异常：

```java
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<Result<Void>> handleBusinessException(BusinessException ex) {
        log.warn("业务异常: {}", ex.getMessage());
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(Result.error(ex.getCode(), ex.getMessage()));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Result<Map<String, String>>> handleValidationException(
            MethodArgumentNotValidException ex) {
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(error ->
            errors.put(error.getField(), error.getDefaultMessage())
        );
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(Result.error(400, "参数验证失败", errors));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<Result<Void>> handleException(Exception ex) {
        log.error("系统异常:", ex);
        return ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Result.error(500, "服务器内部错误"));
    }
}
```

### 数据访问

#### JPA Repository

```java
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(String username);
    
    @Query("SELECT u FROM User u WHERE u.enabled = true AND u.createdAt BETWEEN ?1 AND ?2")
    List<User> findActiveUsersBetweenDate(Date start, Date end);
    
    Page<User> findByEnabled(Boolean enabled, Pageable pageable);
}
```

#### MyBatis Mapper

```java
@Mapper
public interface UserMapper {
    @Select("SELECT * FROM users WHERE id = #{id}")
    User findById(Long id);
    
    @Insert("INSERT INTO users(username, email, password) VALUES(#{username}, #{email}, #{password})")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(User user);
}
```

### 事务管理

```java
@Service
@Transactional
public class OrderService {
    @Transactional
    public OrderDTO createOrder(OrderCreateDTO dto) {
        // 业务逻辑
    }
    
    @Transactional(readOnly = true)
    public OrderDTO getOrder(Long id) {
        // 只读操作
    }
}
```

## 开发流程

### 开发步骤

1. **设计数据库表**：根据需求设计数据库表结构
2. **创建实体类**：在 entity 包创建 JPA Entity，添加注解
3. **创建 DTO**：在 dto 包定义请求和响应的数据结构
4. **创建 Repository**：定义数据访问接口，继承 JpaRepository
5. **创建 Service**：编写业务逻辑接口和实现类
6. **创建 Controller**：编写 REST API 接口，处理 HTTP 请求
7. **编写测试**：单元测试和集成测试
8. **运行验证**：启动应用，使用 Postman 测试 API

### 功能开发原则

- 优先实现核心功能，验证业务流程
- 保持 Controller 简洁，只处理请求和响应
- 业务逻辑放在 Service 层，可单元测试
- 每个 API 添加 Swagger 文档注解
- 及时提交代码，保持小的提交粒度
- 使用 Spring Boot 2.0 的新特性（配置属性绑定、改进的自动配置）

## 工具配置

### Swagger 2 配置

```java
@Configuration
@EnableSwagger2
public class SwaggerConfig {
    @Bean
    public Docket createRestApi() {
        return new Docket(DocumentationType.SWAGGER_2)
                .apiInfo(apiInfo())
                .select()
                .apis(RequestHandlerSelectors.basePackage("com.example.demo.controller"))
                .paths(PathSelectors.any())
                .build();
    }

    private ApiInfo apiInfo() {
        return new ApiInfoBuilder()
                .title("API 文档")
                .description("Spring Boot 2.0 项目 API 文档")
                .version("1.0")
                .build();
    }
}
```

### Logback 配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <include resource="org/springframework/boot/logging/logback/base.xml"/>
    
    <logger name="com.example.demo" level="DEBUG"/>
    <logger name="org.springframework.web" level="INFO"/>
    <logger name="org.hibernate.SQL" level="DEBUG"/>
    
    <root level="INFO">
        <appender-ref ref="CONSOLE"/>
        <appender-ref ref="FILE"/>
    </root>
</configuration>
```

## 示例脚本

### 完整的用户管理示例

```java
// Entity
@Entity
@Table(name = "users")
@Data
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, unique = true, length = 50)
    private String username;
    
    @Column(nullable = false, unique = true)
    private String email;
    
    @Column(nullable = false)
    private String password;
    
    @Column(name = "created_at", updatable = false)
    @CreationTimestamp
    private LocalDateTime createdAt;
}

// DTO
@Data
public class UserCreateDTO {
    @NotBlank(message = "用户名不能为空")
    @Size(min = 3, max = 50, message = "用户名长度必须在3-50之间")
    private String username;
    
    @NotBlank(message = "邮箱不能为空")
    @Email(message = "邮箱格式不正确")
    private String email;
    
    @NotBlank(message = "密码不能为空")
    @Size(min = 8, message = "密码长度至少8位")
    private String password;
}

// Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(String username);
    boolean existsByUsername(String username);
}

// Service
@Service
@Transactional
public class UserServiceImpl implements UserService {
    private final UserRepository userRepository;
    
    @Override
    public UserDTO createUser(UserCreateDTO userCreateDTO) {
        if (userRepository.existsByUsername(userCreateDTO.getUsername())) {
            throw new UserAlreadyExistsException("用户名已存在");
        }
        
        User user = new User();
        user.setUsername(userCreateDTO.getUsername());
        user.setEmail(userCreateDTO.getEmail());
        user.setPassword(BCrypt.hashpw(userCreateDTO.getPassword(), BCrypt.gensalt()));
        
        User savedUser = userRepository.save(user);
        return userMapper.toDTO(savedUser);
    }
}

// Controller
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    private final UserService userService;
    
    @PostMapping
    public ResponseEntity<Result<UserDTO>> createUser(@Valid @RequestBody UserCreateDTO userDTO) {
        UserDTO createdUser = userService.createUser(userDTO);
        return ResponseEntity.status(HttpStatus.CREATED).body(Result.success(createdUser));
    }
}
```

## Spring Boot 2.0 特性说明

### 主要改进

1. **配置属性绑定**：使用 `@ConfigurationProperties` 进行类型安全的配置绑定
2. **HikariCP 默认连接池**：Spring Boot 2.0 默认使用 HikariCP 替代 Tomcat JDBC
3. **改进的自动配置**：更智能的自动配置机制
4. **Actuator 改进**：新的端点和管理功能
5. **Java 版本支持**：支持 Java 8、9、10、11

### 与 Spring Boot 1.x 的区别

- 配置属性绑定方式改进
- 默认连接池从 Tomcat JDBC 改为 HikariCP
- 某些配置属性名称变更（如 `spring.datasource.*`）
- 更好的 Java 9+ 支持

## 参考资料

- [Spring Boot 2.0 官方文档](https://docs.spring.io/spring-boot/docs/2.0.9.RELEASE/reference/html/)
- [Spring Framework 5.0 文档](https://docs.spring.io/spring-framework/docs/5.0.x/spring-framework-reference/)
- [Spring Data JPA 文档](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
- [MyBatis Spring Boot Starter](https://mybatis.org/spring-boot-starter/mybatis-spring-boot-autoconfigure/)
