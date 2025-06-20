package com.coooolfan.uniboard.config

import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Value
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.core.io.ClassPathResource
import org.springframework.http.MediaType
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer
import org.springframework.web.servlet.function.RouterFunction
import org.springframework.web.servlet.function.RouterFunctions
import org.springframework.web.servlet.function.ServerResponse


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

    // 延迟初始化缓存
    private val indexHtmlContent: String by lazy {
        loadIndexHtml()
    }

    override fun addResourceHandlers(registry: ResourceHandlerRegistry) {
        registry.addResourceHandler("/**")
            .addResourceLocations("classpath:/static/")
            .setCachePeriod(3600 * 24 * 7)
    }

    @Bean
    fun spaRouter(): RouterFunction<ServerResponse> {
        val pattern = "/{path:^(?!${getPatternSlot()}).*}"
        log.info("SPA Router Pattern: $pattern")

        return RouterFunctions.route()
            .GET(pattern) {
                ServerResponse.ok()
                    .contentType(MediaType.TEXT_HTML)
                    .body(indexHtmlContent)
            }
            .build()
    }

    private fun loadIndexHtml(): String {
        return try {
            val resource = ClassPathResource("static/index.html")
            resource.inputStream.use { inputStream ->
                inputStream.bufferedReader(Charsets.UTF_8).use { reader ->
                    reader.readText()
                }
            }
        } catch (e: Exception) {
            log.error("Failed to load index.html", e)
            """
            <!DOCTYPE html>
            <html>
            <head><title>Error</title></head>
            <body><h1>Error loading application</h1><p>${e.message}</p></body>
            </html>
            """.trimIndent()
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