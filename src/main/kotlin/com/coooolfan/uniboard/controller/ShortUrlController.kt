package com.coooolfan.uniboard.controller

import com.coooolfan.uniboard.model.ShortUrl
import com.coooolfan.uniboard.model.dto.ShortUrlInsert
import com.coooolfan.uniboard.repository.ShortUrlRepo
import org.springframework.stereotype.Controller
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController

@Controller
@RestController("/api/short-url")
class ShortUrlController(private val shortUrlRepo: ShortUrlRepo) {
    @GetMapping
    fun getShortUrl(): List<ShortUrl> {
        return shortUrlRepo.findAll();
    }

    @PostMapping
    fun insertShortUrl(@RequestBody insert: ShortUrlInsert) {
        shortUrlRepo.save(insert);
    }
}