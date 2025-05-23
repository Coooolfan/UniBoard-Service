# UniBoard-Service

UniBoard 的后端服务，提供个人主页、导航页、笔记、短链接等功能。基于Spring Boot和Kotlin构建的RESTful API服务。

**项目介绍与生产部署请参照前端仓库的`README.md`文件**

<https://github.com/Coooolfan/UniBoard>

## 技术栈

- **语言:** Kotlin (JDK 23)
- **框架:** Spring Boot
- **ORM:** Jimmer ORM
- **认证:** Sa-Token
- **缓存:** Caffeine
- **构建工具:** Gradle
- **数据库迁移:** Flyway

## 项目结构

```
src/main/kotlin/com/coooolfan/uniboard/
├── config/        # 应用配置
├── controller/    # RESTful API控制器
├── error/         # 异常声明处理
├── model/         # 数据模型
├── repo/          # 数据持久层
├── service/       # 业务逻辑层
└── utils/         # 工具类
```

## 开发环境设置

### 前置条件

- JDK 23+
- Docker 和 Docker Compose

### 本地开发

1. 克隆仓库
   ```bash
   git clone https://github.com/yourusername/UniBoard-Service.git
   cd UniBoard-Service
   ```

2. 配置环境变量
   ```bash
   # 编辑.env文件
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   ```

3. 使用Docker Compose启动开发环境（其实就一个Postgres）
   ```bash
   docker compose postgres up -d
   ```

4. 应用环境变量（与 Docker Compose 同一份）
   ```bash
   export $(cat .env | xargs)
   ```

5. 本地运行应用
   ```bash
   ./gradlew bootRun
   ```

## 构建与部署

### Docker构建
```bash
docker build -t uniboard-service .
```

### Docker Compose部署
```bash
docker compose up -d
```

## API文档

项目启动后访问 [<http://localhost:8080/openapi.html>](http://localhost:8080/openapi.html)

## 许可证

本项目使用MIT许可证 - 详见LICENSE文件