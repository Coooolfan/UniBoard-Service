package com.coooolfan.uniboard.controller

import cn.dev33.satoken.annotation.SaCheckLogin
import com.coooolfan.uniboard.error.FileRecordException
import com.coooolfan.uniboard.model.FileRecord
import com.coooolfan.uniboard.model.by
import com.coooolfan.uniboard.model.dto.FileRecordInsert
import com.coooolfan.uniboard.model.dto.FileRecordUpdate
import com.coooolfan.uniboard.service.FileRecordService
import org.babyfish.jimmer.client.FetchBy
import org.babyfish.jimmer.sql.kt.fetcher.newFetcher
import org.springframework.web.bind.annotation.*
import org.springframework.web.multipart.MultipartFile

@RestController
@RequestMapping("/api/file-record")
class FileRecordController(private val service: FileRecordService) {
    @GetMapping
    @SaCheckLogin
    fun getAllFileRecords(): List<FileRecord> {
        return service.findAll()
    }

    @PutMapping("/{id}")
    @SaCheckLogin
    fun updateFileRecordById(@PathVariable id: Long, @RequestBody update: FileRecordUpdate) {
        service.update(update.toEntity { this.id = id })
    }

    @GetMapping("/{id}")
    fun getFileRecordById(@PathVariable id: Long): @FetchBy("PUBLIC_FILERECORD") FileRecord {
        return service.findById(id, PUBLIC_FILERECORD) ?: throw IllegalArgumentException("FileRecord not found")
    }

    @DeleteMapping("/{id}")
    @SaCheckLogin
    fun deleteFileRecordById(@PathVariable id: Long) {
        service.deleteById(id)
    }

    @PostMapping("/files")
    @SaCheckLogin
    @Throws(FileRecordException.EmptyPassword::class)
    fun uploadFile(
        @RequestPart insert: FileRecordInsert,
        @RequestPart file: MultipartFile
    ): FileRecord {
        return service.insert(insert, file)
    }

    companion object {
        private val PUBLIC_FILERECORD = newFetcher(FileRecord::class).by {
            allScalarFields()
            password(false)
        }
    }

}