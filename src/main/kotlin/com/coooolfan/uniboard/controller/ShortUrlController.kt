package com.coooolfan.uniboard.controller

import com.coooolfan.uniboard.model.ShortUrl
import com.coooolfan.uniboard.model.dto.ShortUrlInsert
import com.coooolfan.uniboard.repo.ShortUrlRepo
import com.coooolfan.uniboard.utils.getHashedString
import org.babyfish.jimmer.Page
import org.babyfish.jimmer.spring.repo.PageParam
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/short-url")
class ShortUrlController(private val repo: ShortUrlRepo) {
    @GetMapping
    fun getShortUrl(@RequestParam pageIndex: Int, @RequestParam pageSize: Int): Page<ShortUrl> {
        return repo.findPage(PageParam.byNo(pageIndex, pageSize))
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    fun insertShortUrl(@RequestBody insert: ShortUrlInsert) {
        repo.insert(insert.toEntity { this.shortUrl = getHashedString(insert.longUrl) })
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    fun deleteShortUrl(@PathVariable(value = "id") id: Long) {
        repo.deleteById(id)
    }
}