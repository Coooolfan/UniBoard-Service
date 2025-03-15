package com.coooolfan.uniboard.service

import com.coooolfan.uniboard.model.FileRecord
import com.coooolfan.uniboard.model.dto.FileRecordInsert
import com.coooolfan.uniboard.repo.FileRecordRepo
import org.springframework.stereotype.Service
import org.springframework.web.multipart.MultipartFile

@Service
class FileRecordService(private val repo: FileRecordRepo) {
    fun findAll() = repo.findAll()
    fun deleteById(id: Long) = repo.deleteById(id)
    fun update(update: FileRecord) = repo.update(update)
    fun insert(insert: FileRecordInsert, file: MultipartFile) {
        println(insert)
        println(file)
    }
}