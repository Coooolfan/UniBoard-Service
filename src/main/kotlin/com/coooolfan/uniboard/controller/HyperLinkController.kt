package com.coooolfan.uniboard.controller

import cn.dev33.satoken.annotation.SaCheckLogin
import com.coooolfan.uniboard.model.HyperLink
import com.coooolfan.uniboard.model.dto.HyperLinkInsert
import com.coooolfan.uniboard.model.dto.HyperLinkUpdate
import com.coooolfan.uniboard.service.HyperLinkService
import org.springframework.web.bind.annotation.*
import org.springframework.web.multipart.MultipartFile

@RestController
@RequestMapping("/api/hyper-link")
class HyperLinkController(private val service: HyperLinkService) {
    @GetMapping
    fun getAllHyperLinks() = service.findAll()

    @PostMapping("/")
    @SaCheckLogin
    fun insertHyperlink(
        @RequestPart insert: HyperLinkInsert,
        @RequestPart file: MultipartFile
    ): HyperLink {
        return service.insert(insert, file)
    }

    @PutMapping("/{id}")
    @SaCheckLogin
    fun updateHyperLinkById(@PathVariable id: Long, @RequestBody update: HyperLinkUpdate) {
        service.update(update.toEntity { this.id = id })
    }

    @DeleteMapping("/{id}")
    @SaCheckLogin
    fun deleteHyperLinkById(@PathVariable id: Long) {
        service.deleteById(id)
    }


}