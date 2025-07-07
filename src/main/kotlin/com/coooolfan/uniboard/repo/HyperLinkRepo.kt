package com.coooolfan.uniboard.repo

import com.coooolfan.uniboard.model.HyperLink
import com.coooolfan.uniboard.model.public
import org.babyfish.jimmer.spring.repo.support.AbstractKotlinRepository
import org.babyfish.jimmer.sql.fetcher.Fetcher
import org.babyfish.jimmer.sql.kt.KSqlClient
import org.babyfish.jimmer.sql.kt.ast.expression.eq
import org.springframework.stereotype.Repository

@Repository
class HyperLinkRepo(sql: KSqlClient) : AbstractKotlinRepository<HyperLink, Long>(sql) {
    fun findByIsPublic(fetcher: Fetcher<HyperLink>, isPublic: Boolean): List<HyperLink> {
        return sql.createQuery(HyperLink::class) {
            where(table.public eq isPublic)
            select(table.fetch(fetcher))
        }.execute()
    }

}
