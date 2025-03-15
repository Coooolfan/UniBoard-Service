package com.coooolfan.uniboard.controller

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

    @DeleteMapping("/{id}")
    fun deleteFileRecordById(@PathVariable id: Long) {
        service.deleteById(id)
    }

//    @ApiIgnore
    @PostMapping("/files")
    fun uploadFile(
        @RequestPart("metadata") insert: FileRecordInsert,
        @RequestPart("file") file: MultipartFile
    ) {
        service.insert(insert, file)
        // 处理逻辑
    }
}