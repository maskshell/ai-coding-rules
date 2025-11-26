# Spring Boot 基础规范（精简版）

## 项目结构

```text
src/main/java/com/example/demo/
├── DemoApplication.java              # 启动类
├── controller/                       # REST控制器
├── service/                          # 业务逻辑
│   └── impl/                         # 服务实现
├── repository/                       # 数据访问（JPA）
├── mapper/                           # 数据访问（MyBatis）
├── entity/                           # JPA实体
├── dto/                              # 数据传输对象
│   ├── request/
│   └── response/
├── vo/                               # 视图对象
├── constant/                         # 常量
├── enums/                            # 枚举
├── config/                           # 配置类
├── exception/                        # 异常处理
│   └── handler/
├── security/                         # 安全配置
├── aspect/                           # 切面
├── utils/                            # 工具类
└── annotation/                       # 自定义注解

src/main/resources/
├── application.yml                   # 主配置
├── application-dev.yml               # 开发环境
├── application-prod.yml              # 生产环境
├── application-test.yml              # 测试环境
└── mapper/                           # MyBatis XML
```

## 构建配置

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>
</parent>

<properties>
    <java.version>17</java.version>
    <mybatis-plus.version>3.5.5</mybatis-plus.version>
    <mapstruct.version>1.5.5.Final</mapstruct.version>
</properties>
```

依赖分类：

- Web: `spring-boot-starter-web`
- Validation: `spring-boot-starter-validation`
- JPA: `spring-boot-starter-data-jpa`
- MySQL: `mysql-connector-j`
- MyBatis-Plus: `mybatis-plus-boot-starter`
- Redis: `spring-boot-starter-data-redis`
- Lombok: 简化代码
- MapStruct: 对象映射
- Swagger: API文档

## 配置文件

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
  jpa:
    hibernate:
      ddl-auto: none
    show-sql: false

mybatis:
  mapper-locations: classpath:mapper/*.xml
  type-aliases-package: com.example.demo.entity
  configuration:
    map-underscore-to-camel-case: true

logging:
  level:
    com.example.demo: DEBUG
```

## 开发流程

1. **设计数据库表**：创建表结构，添加索引
2. **创建实体类**：在entity包创建JPA Entity
3. **创建DTO**：定义请求和响应结构
4. **创建Repository**：继承JpaRepository或定义Mapper
5. **编写Service**：实现业务逻辑，添加@Transactional
6. **创建Controller**：编写REST API接口
7. **处理异常**：创建自定义异常和全局处理器
8. **编写测试**：单元测试和集成测试

**原则**：

- 优先实现MVP，验证核心流程
- Controller简洁，只做参数验证
- 业务逻辑放在Service层
- 每个API添加Swagger注解
- 及时提交代码，保持小提交
