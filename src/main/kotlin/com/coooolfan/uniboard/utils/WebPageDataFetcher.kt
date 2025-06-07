package com.coooolfan.uniboard.utils

import org.jsoup.Jsoup
import org.jsoup.nodes.Document
import java.net.URI

/**
 * 获取并提取网页元数据
 * @param url 要获取的网页URL
 * @param timeout 超时时间（毫秒）
 * @return 包含标题、描述和图标URL的WebPageMetadata对象
 */
fun fetchWebPageMetadata(url: String, timeout: Int = 30000): WebPageMetadata {
    val normalizedUrl = normalizeUrl(url)
    // 尝试使用Jsoup直接连接
    val doc: Document =
        Jsoup.connect(normalizedUrl)
            .userAgent(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            .timeout(timeout)
            .followRedirects(true)
            .get()

    val title = doc.title()

    // 从meta标签中提取描述
    val description =
        doc.select("meta[name=description], meta[property=og:description]")
            .firstOrNull()
            ?.attr("content")
            ?: ""

    // 查找网站图标
    val iconUrl = findIconUrl(doc, normalizedUrl)

    return WebPageMetadata(title, description, iconUrl)
}


/** 从文档中查找图标URL */
private fun findIconUrl(doc: Document, baseUrl: String): String? {
    // 尝试以多种方式查找图标
    val iconLinks = doc.select("link[rel~=(?i)^(shortcut )?icon$], link[rel=apple-touch-icon]")

    if (iconLinks.isNotEmpty()) {
        val iconHref = iconLinks.first()?.attr("href")
        if (!iconHref.isNullOrBlank()) {
            return resolveUrl(baseUrl, iconHref)
        }
    }

    // 尝试默认的favicon位置
    return try {
        val uri = URI(baseUrl)
        val defaultIconUrl = "${uri.scheme}://${uri.host}/favicon.ico"
        defaultIconUrl // 直接返回URL，不检查它是否存在
    } catch (_: Exception) {
        null
    }
}

/** 解析相对URL为绝对URL */
private fun resolveUrl(baseUrl: String, relativeUrl: String): String {
    if (relativeUrl.startsWith("http://") || relativeUrl.startsWith("https://")) {
        return relativeUrl
    }

    return try {
        val base = URI.create(baseUrl).toString()
        URI.create(base).resolve(relativeUrl).toString()
    } catch (_: Exception) {
        // 如果URI失败，回退到旧的URL方法
        val base = URI(baseUrl).toURL()
        val resolved = base.toURI().resolve(relativeUrl)
        resolved.toString()
    }
}

/** 确保URL包含协议 */
private fun normalizeUrl(url: String): String {
    return if (!url.startsWith("http://") && !url.startsWith("https://")) {
        "https://$url"
    } else {
        url
    }
}
