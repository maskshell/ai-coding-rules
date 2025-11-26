# Spring Boot 基础规范

## 项目结构

### 标准目录布局

```text
├── pom.xml 或 build.gradle                    # 构建配置
├── src/
│   ├── main/
│   │   ├── java/com/example/demo/
│   │   │   ├── DemoApplication.java          # 启动类
│   │   │   ├── config/                       # 配置类
│   │   │   ├── controller/                   # REST控制器
│   │   │   ├── service/                      # 业务逻辑层
│   │   │   │   ├── impl/                     # 服务实现
│   │   │   ├── repository/                   # 数据访问层
│   │   │   ├── entity/                       # JPA实体类
│   │   │   ├── dto/                          # 数据传输对象
│   │   │   ├── vo/                           # 视图对象
│   │   │   ├── constant/                     # 常量类
│   │   │   ├── exception/                    # 自定义异常
│   │   │   ├── security/                     # 安全配置
│   │   │   └── utils/                        # 工具类
│   │   └── resources/
│   │       ├── application.yml               # 主配置文件
│   │       ├── application-dev.yml           # 开发环境
│   │       ├── application-prod.yml          # 生产环境
│   │       ├── application-test.yml          # 测试环境
│   │       ├── mapper/                       # MyBatis XML映射
│   │       └── static/                       # 静态资源
│   └── test/java/com/example/demo/           # 测试代码
│       ├── controller/                       # 控制器测试
│       ├── service/                          # 服务测试
│       ├── repository/                       # 仓储测试
│       └── base/BaseTest.java                # 测试基类
```

### 代码组织原则

- 按功能模块划分包结构：`user`, `order`, `product`
- 接口和实现类分离：`UserService` 接口 + `UserServiceImpl` 实现
- DTO 和 Entity 严格分离，不混用
- 实体类标注完整 JPA 注解

**示例**:

```java
// 启动类
@SpringBootApplication
@EnableJpaRepositories("com.example.demo.repository")
@EntityScan("com.example.demo.entity")
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}

// 实体类
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

    @Column(nullable = false)
    private Boolean enabled = true;

    @Column(name = "created_at", updatable = false)
    @CreationTimestamp
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    @UpdateTimestamp
    private LocalDateTime updatedAt;
}
```

## 构建配置

### Maven 依赖管理

- 使用 Spring Boot Parent POM 管理版本
- 将依赖分类：Web、数据访问、工具、测试
- 使用 `<properties>` 统一管理第三方库版本

```xml
<properties>
    <java.version>17</java.version>
    <mybatis.version>3.0.3</mybatis.version>
    <jwt.version>0.11.5</jwt.version>
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
        <version>8.0.33</version>
    </dependency>

    <!-- MyBatis -->
    <dependency>
        <groupId>org.mybatis.spring.boot</groupId>
        <artifactId>mybatis-spring-boot-starter</artifactId>
        <version>${mybatis.version}</version>
    </dependency>

    <!-- JWT -->
    <dependency>
        <groupId>io.jsonwebtoken</groupId>
        <artifactId>jjwt-api</artifactId>
        <version>${jwt.version}</version>
    </dependency>
</dependencies>
```

## 配置文件

### application.yml 分层配置

- 使用 YAML 格式，层次清晰
- 敏感信息从环境变量读取
- 多环境配置文件分离

```yaml
# application.yml
spring:
  application:
    name: demo-service
  profiles:
    active: dev
  datasource:
    url: ${DB_URL:jdbc:mysql://localhost:3306/demo}
    username: ${DB_USERNAME:root}
    password: ${DB_PASSWORD:}
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    hibernate:
      ddl-auto: none
    show-sql: false
    properties:
      hibernate:
        format_sql: true
        dialect: org.hibernate.dialect.MySQL8Dialect

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
