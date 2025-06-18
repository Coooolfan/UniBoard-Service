package com.coooolfan.uniboard.config

import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.core.io.ClassPathResource
import org.springframework.http.MediaType
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer
import org.springframework.web.servlet.function.RouterFunction
import org.springframework.web.servlet.function.RouterFunctions
import org.springframework.web.servlet.function.ServerRequest
import org.springframework.web.servlet.function.ServerResponse
import java.nio.file.Files


@Configuration
class StaticResourceConfig : WebMvcConfigurer {

    @Bean
    fun spaRouter(): RouterFunction<ServerResponse?> {
        return RouterFunctions.route()
            .GET(
                "/{path:^(?!api|actuator|openapi).*}"
            ) { request: ServerRequest? ->
                ServerResponse.ok()
                    .contentType(MediaType.TEXT_HTML)
                    .body(getIndexHtml())
            }
            .build()
    }

    private fun getIndexHtml(): String {
        try {
            val resource = ClassPathResource("static/index.html")
            return Files.readString(resource.getFile().toPath())
        } catch (_: Exception) {
            return "Error loading index.html"
        }
    }
}