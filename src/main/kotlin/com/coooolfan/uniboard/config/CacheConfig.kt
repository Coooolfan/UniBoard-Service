package com.coooolfan.uniboard.config

import com.coooolfan.uniboard.model.FileRecordDraft
import com.coooolfan.uniboard.model.ShortUrl
import com.coooolfan.uniboard.model.ShortUrlDraft
import com.coooolfan.uniboard.repo.FileRecordRepo
import com.coooolfan.uniboard.repo.ShortUrlRepo
import com.github.benmanes.caffeine.cache.Cache
import com.github.benmanes.caffeine.cache.Caffeine
import com.github.benmanes.caffeine.cache.RemovalCause
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.launch
import org.babyfish.jimmer.sql.ast.mutation.SaveMode
import org.slf4j.LoggerFactory
import org.springframework.cache.CacheManager
import org.springframework.cache.annotation.EnableCaching
import org.springframework.cache.caffeine.CaffeineCacheManager
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.scheduling.annotation.EnableScheduling
import java.util.concurrent.TimeUnit

@Configuration
@EnableCaching
@EnableScheduling
class CacheConfig(
    private val shortUrlRepo: ShortUrlRepo,
    private val fileRecordRepo: FileRecordRepo,
    private val cacheScope: CoroutineScope
) {

    @Bean
    fun cacheManager(): CacheManager {
        val cacheManager = CaffeineCacheManager()
        cacheManager.setCaffeine(
            Caffeine.newBuilder()
                .expireAfterWrite(5, TimeUnit.MINUTES)
                .maximumSize(1000)
        )
        return cacheManager
    }

    @Bean
    fun directLinkCache(): Cache<String, Long> {
        return Caffeine.newBuilder()
            .expireAfterWrite(5, TimeUnit.MINUTES)
            .build()
    }

    @Bean
    fun shortUrlCache(): Cache<String, ShortUrl> {
        return Caffeine.newBuilder()
            .expireAfterWrite(5, TimeUnit.MINUTES)
            .maximumSize(1000)
            .build()
    }

    @Bean
    fun shortUrlCountCache(): Cache<Long, Long> {
        return createCountCache { shortUrlId, count ->
            shortUrlRepo.saveCommand(ShortUrlDraft.`$`.produce {
                TimeUnit.MINUTES.sleep(1)
                id = shortUrlId
                visitCount = count
            }, SaveMode.UPDATE_ONLY).execute()
        }
    }

    @Bean
    fun fileRecordCountCache(): Cache<Long, Long> {
        return createCountCache { fileRecordId, count ->
            fileRecordRepo.saveCommand(FileRecordDraft.`$`.produce {
                id = fileRecordId
                downloadCount = count
            }, SaveMode.UPDATE_ONLY).execute()
        }
    }

    // 创建通用的计数缓存构建器
    private fun <K : Any> createCountCache(
        expirationTime: Long = 3,
        timeUnit: TimeUnit = TimeUnit.SECONDS,
        maxSize: Long = 1000,
        updateAction: suspend (K, Long) -> Unit
    ): Cache<K, Long> {
        return Caffeine.newBuilder()
            .expireAfterWrite(expirationTime, timeUnit)
            .maximumSize(maxSize)
            .removalListener<K, Long> { key, count, cause ->
                if (key == null || count == null) return@removalListener
                if (cause == RemovalCause.EXPIRED) {
                    cacheScope.launch {
                        try {
                            updateAction(key, count)
                        } catch (e: Exception) {
                            log.error("Failed to update count for key: $key", e)
                        }
                    }
                }
            }
            .build()
    }

    companion object {
        private val log = LoggerFactory.getLogger(CacheConfig::class.java)
    }
}
