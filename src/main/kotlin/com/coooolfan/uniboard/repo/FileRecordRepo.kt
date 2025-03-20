package com.coooolfan.uniboard.repo

import com.coooolfan.uniboard.model.FileRecord
import org.babyfish.jimmer.spring.repo.support.AbstractKotlinRepository
import org.babyfish.jimmer.sql.kt.KSqlClient
import org.springframework.stereotype.Repository

@Repository
class FileRecordRepo(sql: KSqlClient) : AbstractKotlinRepository<FileRecord, Long>(sql)