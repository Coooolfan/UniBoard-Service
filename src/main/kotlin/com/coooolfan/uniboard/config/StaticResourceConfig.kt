package com.coooolfan.uniboard.config

import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Value
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

    private val log = LoggerFactory.getLogger(OpenApiFilterConfig::class.java)

    @Value("\${jimmer.client.enable:true}")
    private var openApiEnabled: Boolean = true

    @Value("\${jimmer.client.openapi.path:/openapi.yml}")
    private lateinit var openapiPath: String

    @Value("\${jimmer.client.ts.path:/openapi.zip}")
    private lateinit var tsPath: String

    @Value("\${jimmer.client.openapi.ui-path:/openapi.html}")
    private lateinit var uiPath: String

    @Bean
    fun spaRouter(): RouterFunction<ServerResponse?> {
        log.info("Service Pattern: /{path:^(?!${getPatternSlot()}).*}")
        return RouterFunctions.route()
            .GET(
                "/{path:^(?!${getPatternSlot()}).*}"
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
        } catch (e: Exception) {
            return "Error loading index.html: ${e.message}"
        }
    }

    private fun getPatternSlot(): String = buildList {
        add("api")
        if (openApiEnabled) {
            listOf(openapiPath, tsPath, uiPath)
                .filter { it.isNotBlank() }
                .mapTo(this) { it.removePrefix("/") }
        }
    }.joinToString("|")
}