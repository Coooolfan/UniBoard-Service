# 第一阶段：构建阶段
FROM gradle:jdk23 AS build
WORKDIR /app

# 先复制Gradle配置文件以利用Docker缓存层
COPY build.gradle.kts settings.gradle.kts* ./
COPY gradle ./gradle/

# 下载所有依赖项
RUN if [ -f settings.gradle.kts ]; then gradle dependencies --no-daemon || true; fi

# 复制源代码
COPY src/ ./src/

# 构建应用(跳过测试以加快构建速度)
RUN gradle build --no-daemon --exclude-task test

# 第二阶段：运行阶段
FROM ibm-semeru-runtimes:open-23-jre-noble
WORKDIR /app

# 从构建阶段复制构建结果
COPY --from=build /app/build/libs/*.jar app.jar

# 暴露应用端口(默认Spring Boot端口)
EXPOSE 8080

# 设置JVM参数
ENV JAVA_OPTS=""

# 启动应用
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
