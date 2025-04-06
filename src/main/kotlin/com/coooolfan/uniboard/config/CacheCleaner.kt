package com.coooolfan.uniboard.config

import com.github.benmanes.caffeine.cache.Cache
import org.slf4j.LoggerFactory
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.stereotype.Component

@Component
class CacheCleaner(
    private val directLinkCache: Cache<String, Long>,
    private val shortUrlCountCache: Cache<Long, Long>,
    private val fileRecordCountCache: Cache<Long, Long>
) {

    private val log = LoggerFactory.getLogger(CacheCleaner::class.java)

    // 每一秒执行一次定时清理
    @Scheduled(fixedDelay = 1000)
    fun cleanUpCaches() {
        directLinkCache.cleanUp()
        shortUrlCountCache.cleanUp()
        fileRecordCountCache.cleanUp()
    }
}