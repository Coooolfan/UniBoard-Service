package com.coooolfan.uniboard.config

import com.coooolfan.uniboard.model.FileRecord
import com.coooolfan.uniboard.model.ShortUrl
import com.coooolfan.uniboard.repo.FileRecordRepo
import com.coooolfan.uniboard.repo.ShortUrlRepo
import com.github.benmanes.caffeine.cache.Cache
import com.github.benmanes.caffeine.cache.Caffeine
import com.github.benmanes.caffeine.cache.RemovalCause
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.launch
import org.babyfish.jimmer.sql.ast.mutation.SaveMode
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
    fun directDownloadLinkCache(): Cache<String, Long> {
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
        return commonCountCache { shortUrlId, count ->
            shortUrlRepo.saveCommand(ShortUrl {
                id = shortUrlId
                visitCount = count
            }, SaveMode.UPDATE_ONLY).execute()
        }
    }

    @Bean
    fun fileRecordCountCache(): Cache<Long, Long> {
        return commonCountCache { fileRecordId, count ->
            fileRecordRepo.saveCommand(FileRecord {
                id = fileRecordId
                downloadCount = count
            }, SaveMode.UPDATE_ONLY).execute()
        }
    }

    // 创建通用的计数缓存构建器
    private fun commonCountCache(
        expirationTime: Long = 3,
        timeUnit: TimeUnit = TimeUnit.SECONDS,
        maxSize: Long = 1000,
        updateAction: suspend (Long, Long) -> Unit
    ): Cache<Long, Long> {
        return Caffeine.newBuilder()
            .expireAfterWrite(expirationTime, timeUnit)
            .maximumSize(maxSize)
            .removalListener<Long, Long> { key, count, cause ->
                if (key == null || count == null) return@removalListener
                if (cause == RemovalCause.EXPIRED) {
                    cacheScope.launch { updateAction(key, count) }
                }
            }
            .build()
    }

}
