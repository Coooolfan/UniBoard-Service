package com.coooolfan.uniboard.service

import com.coooolfan.uniboard.error.FileRecordException
import com.coooolfan.uniboard.model.FileRecord
import com.coooolfan.uniboard.model.FileRecordVisibility
import com.coooolfan.uniboard.model.dto.FileRecordDirectLinkCreate
import com.coooolfan.uniboard.model.dto.FileRecordDirectLinkResp
import com.coooolfan.uniboard.model.dto.FileRecordInsert
import com.coooolfan.uniboard.repo.FileRecordRepo
import com.coooolfan.uniboard.utils.getHashedString
import com.github.benmanes.caffeine.cache.Cache
import org.babyfish.jimmer.Page
import org.babyfish.jimmer.spring.repo.PageParam
import org.babyfish.jimmer.sql.fetcher.Fetcher
import org.springframework.stereotype.Service
import org.springframework.web.multipart.MultipartFile
import java.nio.file.Paths
import java.util.*

@Service
class FileRecordService(
    private val repo: FileRecordRepo,
    private val directLinkCache: Cache<String, Long>
) {
    fun findByPage(pageIndex: Int, pageSize: Int): Page<FileRecord> {
        return findByPage(PageParam.byNo(pageIndex, pageSize))
    }

    fun findByPage(pageParam: PageParam): Page<FileRecord> {
        return repo.findPage(pageParam)
    }

    fun deleteById(id: Long) = repo.deleteById(id)
    fun update(update: FileRecord) = repo.update(update)
    fun findByByShareCode(shareCode: String, fetcher: Fetcher<FileRecord>) = repo.findByShareCode(shareCode, fetcher)

    fun insert(insert: FileRecordInsert, file: MultipartFile): FileRecord {
        if (insert.visibility == FileRecordVisibility.PASSWORD && insert.password.trim().isEmpty())
            throw FileRecordException.EmptyPassword()

        val relativePath = Paths.get("service/filerecord/${UUID.randomUUID()}")
        val filePath = Paths.get(System.getProperty("user.dir")).resolve(relativePath)
        filePath.parent.toFile().mkdirs()
        file.transferTo(filePath.toFile())
        val shareCode = getHashedString(filePath.toString())
        return repo.insert(
            insert.toEntity {
                this.shareCode = shareCode
                this.file { this.filepath = relativePath.toString() }
            },
        ).modifiedEntity
    }

    fun createDirectLink(create: FileRecordDirectLinkCreate): FileRecordDirectLinkResp {
        val uuid = UUID.randomUUID().toString()
        // Store the mapping between UUID and file ID in the cache, expires after 5 minutes
        directLinkCache.put(uuid, create.id)
        return FileRecordDirectLinkResp(
            id = create.id,
            directUUID = uuid,
        )
    }
}
