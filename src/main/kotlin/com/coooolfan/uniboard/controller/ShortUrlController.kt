package com.coooolfan.uniboard.controller

import com.coooolfan.uniboard.model.ShortUrl
import com.coooolfan.uniboard.model.dto.ShortUrlInsert
import com.coooolfan.uniboard.repository.ShortUrlRepo
import com.coooolfan.uniboard.service.ShortUrlService
import org.babyfish.jimmer.Page
import org.babyfish.jimmer.spring.repo.PageParam
import org.springframework.http.HttpStatus
import org.springframework.stereotype.Controller
import org.springframework.web.bind.annotation.*

@Controller
@RestController("/api/short-url")
class ShortUrlController(private val shortUrlRepo: ShortUrlRepo, private val shortUrlService: ShortUrlService) {
    @GetMapping
    fun getShortUrl(@RequestParam pageIndex: Int, @RequestParam pageSize: Int): Page<ShortUrl> {
        return shortUrlRepo.findPage(PageParam.byNo(pageIndex, pageSize))
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    fun insertShortUrl(@RequestBody insert: ShortUrlInsert) {
        shortUrlService.insert(insert)
    }

    @DeleteMapping("{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    fun deleteShortUrl(@PathVariable(value = "id") id: Long) {
        shortUrlRepo.deleteById(id)
    }
}