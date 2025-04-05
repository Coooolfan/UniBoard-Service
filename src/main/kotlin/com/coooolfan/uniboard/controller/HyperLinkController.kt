package com.coooolfan.uniboard.controller

import cn.dev33.satoken.annotation.SaCheckLogin
import com.coooolfan.uniboard.model.HyperLink
import com.coooolfan.uniboard.model.by
import com.coooolfan.uniboard.model.dto.HyperLinkInsert
import com.coooolfan.uniboard.model.dto.HyperLinkUpdate
import com.coooolfan.uniboard.service.HyperLinkService
import org.babyfish.jimmer.client.FetchBy
import org.babyfish.jimmer.sql.kt.fetcher.newFetcher
import org.springframework.web.bind.annotation.*
import org.springframework.web.multipart.MultipartFile

@RestController
@RequestMapping("/api/hyper-link")
class HyperLinkController(private val service: HyperLinkService) {
    @GetMapping
    fun getAllHyperLinks(): List<@FetchBy("DEFAULT_HYPER_LINK") HyperLink> = service.findAll(DEFAULT_HYPER_LINK)

    @PostMapping("/")
    @SaCheckLogin
    fun insertHyperlink(
        @RequestPart insert: HyperLinkInsert,
        @RequestPart(required = true) file: MultipartFile
    ): @FetchBy("DEFAULT_HYPER_LINK") HyperLink {
        return service.insert(insert, file)
    }

    @PutMapping("/{id}")
    @SaCheckLogin
    fun updateHyperLinkById(
        @PathVariable id: Long,
        @RequestPart update: HyperLinkUpdate,
        @RequestPart(required = false) file: MultipartFile?
    ): @FetchBy("DEFAULT_HYPER_LINK") HyperLink {
        return service.update(update.toEntity { this.id = id }, file)
    }

    @DeleteMapping("/{id}")
    @SaCheckLogin
    fun deleteHyperLinkById(@PathVariable id: Long) {
        service.deleteById(id)
    }

    companion object {
        private val DEFAULT_HYPER_LINK = newFetcher(HyperLink::class).by {
            allScalarFields()
        }
    }

}