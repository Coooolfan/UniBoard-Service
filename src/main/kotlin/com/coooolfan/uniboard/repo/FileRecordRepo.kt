package com.coooolfan.uniboard.repo

import com.coooolfan.uniboard.model.FileRecord
import com.coooolfan.uniboard.model.FileRecordVisibility
import com.coooolfan.uniboard.model.shareCode
import com.coooolfan.uniboard.model.visibility
import org.babyfish.jimmer.spring.repo.support.AbstractKotlinRepository
import org.babyfish.jimmer.sql.fetcher.Fetcher
import org.babyfish.jimmer.sql.kt.KSqlClient
import org.babyfish.jimmer.sql.kt.ast.expression.eq
import org.babyfish.jimmer.sql.kt.ast.expression.ne
import org.springframework.stereotype.Repository

@Repository
class FileRecordRepo(sql: KSqlClient) : AbstractKotlinRepository<FileRecord, Long>(sql) {

    fun findByShareCode(shareCode: String, fetcher: Fetcher<FileRecord>): FileRecord? {
        return this.sql.createQuery(FileRecord::class) {
            where(table.shareCode eq shareCode)
            where(table.visibility ne FileRecordVisibility.PRIVATE)
            select(table.fetch(fetcher))
        }.execute().firstOrNull()
    }

    fun findByShareCode(shareCode: String): FileRecord? {
        return this.sql.createQuery(FileRecord::class) {
            where(table.shareCode eq shareCode)
            select(table)
        }.execute().firstOrNull()
    }

}