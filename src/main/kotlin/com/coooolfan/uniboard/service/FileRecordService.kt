package com.coooolfan.uniboard.service

import com.coooolfan.uniboard.model.FileRecord
import com.coooolfan.uniboard.model.dto.FileRecordInsert
import com.coooolfan.uniboard.repo.FileRecordRepo
import com.coooolfan.uniboard.utils.getHashedString
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional
import org.springframework.web.multipart.MultipartFile
import java.io.File
import java.util.*

@Service
class FileRecordService(private val repo: FileRecordRepo) {
    fun findAll() = repo.findAll()
    fun deleteById(id: Long) = repo.deleteById(id)
    fun update(update: FileRecord) = repo.update(update)

    @Transactional
    fun insert(insert: FileRecordInsert, file: MultipartFile): FileRecord {
        val programPath = System.getProperty("user.dir") + "/service/filerecord"
        val path = File(programPath)
        path.mkdirs()
        val filePath = File(path, UUID.randomUUID().toString())
        file.transferTo(filePath)
        val shareCode = getHashedString(filePath.path)
        return repo.insert(
            insert.toEntity {
                this.shareCode = shareCode
                this.file { this.filepath = filePath.path }
            },
        ).modifiedEntity
    }
}