package com.coooolfan.uniboard.controller

import cn.dev33.satoken.annotation.SaCheckLogin
import com.coooolfan.uniboard.error.CommonException
import com.coooolfan.uniboard.model.ShortUrl
import com.coooolfan.uniboard.model.dto.ShortUrlInsert
import com.coooolfan.uniboard.repo.ShortUrlRepo
import com.coooolfan.uniboard.utils.getHashedString
import jakarta.servlet.http.HttpServletResponse
import org.babyfish.jimmer.Page
import org.babyfish.jimmer.spring.repo.PageParam
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/short-url")
@SaCheckLogin
class ShortUrlController(private val repo: ShortUrlRepo) {
    @GetMapping
    fun getShortUrl(@RequestParam pageIndex: Int, @RequestParam pageSize: Int): Page<ShortUrl> {
        return repo.findPage(PageParam.byNo(pageIndex, pageSize))
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    fun insertShortUrl(@RequestBody insert: ShortUrlInsert): ShortUrl {
        return repo.insert(insert.toEntity { this.shortUrl = getHashedString(insert.longUrl) }).modifiedEntity
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    fun deleteShortUrl(@PathVariable(value = "id") id: Long) {
        if (repo.deleteById(id) != 1) {
            throw CommonException.NotFound()
        }
    }
}

@RestController
@RequestMapping("/s")
@ResponseStatus(HttpStatus.TEMPORARY_REDIRECT)
class RedirectController(private val repo: ShortUrlRepo) {
    @GetMapping("/{shortUrlCode}")
    fun redirect(@PathVariable(value = "shortUrlCode") shortUrlCode: String, resp: HttpServletResponse) {
        val entity = repo.findByShortUrlCode(shortUrlCode) ?: throw CommonException.NotFound()
        resp.sendRedirect(entity.longUrl)
        resp.flushBuffer()
    }
}
