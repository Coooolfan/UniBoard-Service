package com.coooolfan.uniboard.controller

import cn.dev33.satoken.annotation.SaCheckLogin
import com.coooolfan.uniboard.model.HyperLink
import com.coooolfan.uniboard.model.by
import com.coooolfan.uniboard.model.dto.HyperLinkInsert
import com.coooolfan.uniboard.model.dto.HyperLinkUpdate
import com.coooolfan.uniboard.service.HyperLinkService
import com.coooolfan.uniboard.utils.WebPageMetadata
import com.coooolfan.uniboard.utils.fetchWebPageMetadata
import org.babyfish.jimmer.client.FetchBy
import org.babyfish.jimmer.sql.kt.fetcher.newFetcher
import org.springframework.web.bind.annotation.*
import org.springframework.web.multipart.MultipartFile

/**
 * 超链接控制器
 *
 * 处理超链接的管理操作，包括创建、查询、更新和删除超链接，支持为超链接添加图片
 */
@RestController
@RequestMapping("/api/hyper-link")
class HyperLinkController(private val service: HyperLinkService) {
    /**
     * 获取所有超链接
     *
     * 获取系统中所有的超链接列表，用于展示在首页或超链接管理页面
     *
     * @return List<HyperLink> 超链接列表
     */
    @GetMapping
    fun getAllHyperLinks(): List<@FetchBy("DEFAULT_HYPER_LINK") HyperLink> = service.findAll(DEFAULT_HYPER_LINK)

    /**
     * 创建新的超链接
     *
     * 添加新的超链接到系统中，需要提供链接信息和关联的图片文件
     * 需要登录验证
     *
     * @param insert 超链接创建数据，包含标题、URL、描述等信息
     * @param file 超链接关联的图片文件（必需）
     * @return HyperLink 创建的超链接对象
     */
    @PostMapping("/")
    @SaCheckLogin
    fun insertHyperlink(
        @RequestPart insert: HyperLinkInsert,
        @RequestPart(required = true) file: MultipartFile
    ): @FetchBy("DEFAULT_HYPER_LINK") HyperLink {
        return service.insert(insert, file, DEFAULT_HYPER_LINK)
    }

    /**
     * 根据ID更新超链接
     *
     * 更新指定的超链接信息，可以修改标题、URL、描述等，也可以更新关联的图片
     * 需要登录验证
     *
     * @param id 要更新的超链接ID
     * @param update 超链接更新数据
     * @param file 可选的新图片文件，如果不提供则保持原有图片
     * @return HyperLink 更新后的超链接对象
     */
    @PutMapping("/{id}")
    @SaCheckLogin
    fun updateHyperLinkById(
        @PathVariable id: Long,
        @RequestPart update: HyperLinkUpdate,
        @RequestPart(required = false) file: MultipartFile?
    ): @FetchBy("DEFAULT_HYPER_LINK") HyperLink {
        return service.update(update.toEntity { this.id = id }, file, DEFAULT_HYPER_LINK)
    }

    /**
     * 根据ID删除超链接
     *
     * 删除指定的超链接及其关联的图片文件
     * 需要登录验证
     *
     * @param id 要删除的超链接ID
     */
    @DeleteMapping("/{id}")
    @SaCheckLogin
    fun deleteHyperLinkById(@PathVariable id: Long) {
        service.deleteById(id)
    }

    @GetMapping("/snapshot")
    @SaCheckLogin
    fun getHyperLinkSnapshot(@RequestParam url: String): WebPageMetadata {
        return fetchWebPageMetadata(url)
    }

    companion object {
        private val DEFAULT_HYPER_LINK = newFetcher(HyperLink::class).by {
            allScalarFields()
        }
    }

}