package com.coooolfan.uniboard.repo

import com.coooolfan.uniboard.model.HyperLink
import org.babyfish.jimmer.spring.repo.support.AbstractKotlinRepository
import org.babyfish.jimmer.sql.kt.KSqlClient
import org.springframework.stereotype.Repository

@Repository
class HyperLinkRepo(sql:KSqlClient):AbstractKotlinRepository<HyperLink,Long>(sql) {
}