package com.coooolfan.uniboard.controller

import com.coooolfan.uniboard.error.FileRecordException
import com.coooolfan.uniboard.model.FileRecord
import com.coooolfan.uniboard.model.dto.FileRecordInsert
import com.coooolfan.uniboard.model.dto.FileRecordUpdate
import com.coooolfan.uniboard.service.FileRecordService
import org.springframework.web.bind.annotation.*
import org.springframework.web.multipart.MultipartFile

@RestController
@RequestMapping("/api/file-record")
class FileRecordController(private val service: FileRecordService) {
    @GetMapping
    fun getAllFileRecords(): List<FileRecord> {
        return service.findAll()
    }

    @PutMapping("/{id}")
    fun updateFileRecordById(@PathVariable id: Long, @RequestBody update: FileRecordUpdate) {
        service.update(update.toEntity { this.id = id })
    }

    @GetMapping("/{id}")
    fun getFileRecordById(@PathVariable id: Long): FileRecord {
        return service.findById(id) ?: throw IllegalArgumentException("FileRecord not found")
    }

    @DeleteMapping("/{id}")
    fun deleteFileRecordById(@PathVariable id: Long) {
        service.deleteById(id)
    }

    @PostMapping("/files")
    @Throws(FileRecordException.EmptyPassword::class)
    fun uploadFile(
        @RequestPart insert: FileRecordInsert,
        @RequestPart file: MultipartFile
    ): FileRecord {
        return service.insert(insert, file)
    }
}