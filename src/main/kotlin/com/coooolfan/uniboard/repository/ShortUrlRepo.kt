package com.coooolfan.uniboard.repository

import com.coooolfan.uniboard.model.ShortUrl
import org.babyfish.jimmer.spring.repo.support.AbstractKotlinRepository
import org.babyfish.jimmer.sql.kt.KSqlClient
import org.springframework.stereotype.Repository

@Repository
class ShortUrlRepo(sql:KSqlClient) : AbstractKotlinRepository<ShortUrl, Long>(sql) {
}