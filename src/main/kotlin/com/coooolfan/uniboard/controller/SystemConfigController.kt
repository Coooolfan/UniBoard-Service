package com.coooolfan.uniboard.controller

import cn.dev33.satoken.annotation.SaCheckLogin
import com.coooolfan.uniboard.error.CommonException
import com.coooolfan.uniboard.model.SystemConfig
import com.coooolfan.uniboard.model.by
import com.coooolfan.uniboard.model.dto.SystemConfigUpdate
import com.coooolfan.uniboard.repo.SystemConfigRepo
import org.babyfish.jimmer.client.FetchBy
import org.babyfish.jimmer.sql.kt.fetcher.newFetcher
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/system-config")
class SystemConfigController(private val repo: SystemConfigRepo) {
    @GetMapping
    fun getSystemConfig(): @FetchBy("DEFAULT_SYSTEM_CONFIG") SystemConfig {
        return repo.findById(1, DEFAULT_SYSTEM_CONFIG) ?: throw CommonException.NotFound()
    }

    @PutMapping
    @SaCheckLogin
    fun updateSystemConfig(
        @RequestBody update: SystemConfigUpdate
    ): @FetchBy("DEFAULT_SYSTEM_CONFIG") SystemConfig {
        return repo.update(update.toEntity { id = 1 }).modifiedEntity
    }

    companion object {
        private val DEFAULT_SYSTEM_CONFIG = newFetcher(SystemConfig::class).by {
            allScalarFields()
        }
    }
}
