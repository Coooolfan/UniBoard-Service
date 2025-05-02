package com.coooolfan.uniboard.controller

import cn.dev33.satoken.annotation.SaCheckLogin
import com.coooolfan.uniboard.error.CommonException
import com.coooolfan.uniboard.model.ShortUrl
import com.coooolfan.uniboard.model.by
import com.coooolfan.uniboard.model.dto.ShortUrlInsert
import com.coooolfan.uniboard.repo.ShortUrlRepo
import com.coooolfan.uniboard.utils.getHashedString
import com.github.benmanes.caffeine.cache.Cache
import jakarta.servlet.http.HttpServletResponse
import org.babyfish.jimmer.Page
import org.babyfish.jimmer.client.FetchBy
import org.babyfish.jimmer.spring.repo.PageParam
import org.babyfish.jimmer.sql.kt.fetcher.newFetcher
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/short-url")
@SaCheckLogin
class ShortUrlController(private val repo: ShortUrlRepo) {
    @GetMapping
    fun getShortUrl(
        @RequestParam pageIndex: Int,
        @RequestParam pageSize: Int
    ): Page<@FetchBy("DEFAULT_SHORT_URL") ShortUrl> {
        return repo.findPage(PageParam.byNo(pageIndex, pageSize), DEFAULT_SHORT_URL) {
            asc(ShortUrl::id)
        }
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    fun insertShortUrl(@RequestBody insert: ShortUrlInsert): @FetchBy("DEFAULT_SHORT_URL") ShortUrl {
        return repo.saveCommand(insert.toEntity { this.shortUrl = getHashedString(insert.longUrl) })
            .execute(DEFAULT_SHORT_URL).modifiedEntity
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    fun deleteShortUrl(@PathVariable(value = "id") id: Long) {
        if (repo.deleteById(id) != 1) {
            throw CommonException.NotFound()
        }
    }

    companion object {
        private val DEFAULT_SHORT_URL = newFetcher(ShortUrl::class).by {
            allScalarFields()
        }
    }
}

@RestController
@RequestMapping("/s")
@ResponseStatus(HttpStatus.FOUND)
class RedirectController(
    private val repo: ShortUrlRepo,
    private val shortUrlCountCache: Cache<Long, Long>,
    private val shortUrlCache: Cache<String, ShortUrl>
) {
    @GetMapping("/{shortUrlCode}")
    fun redirect(@PathVariable(value = "shortUrlCode") shortUrlCode: String, resp: HttpServletResponse) {
        // 尝试从缓存中获取
        var entity = shortUrlCache.getIfPresent(shortUrlCode)
        if (entity == null) {
            entity = repo.findByShortUrlCode(shortUrlCode) ?: throw CommonException.NotFound()
            shortUrlCache.put(shortUrlCode, entity)
        }
        shortUrlCountCache.asMap().compute(entity.id) { _, lastCachedIncrement ->
            // 当 lastCachedCount 为 null 时，说明是第一次访问, 从1开始计数
            (lastCachedIncrement ?: 0) + 1
        }
        resp.sendRedirect(entity.longUrl)
        resp.flushBuffer()
    }
}
