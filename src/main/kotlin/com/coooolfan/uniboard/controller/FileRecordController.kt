package com.coooolfan.uniboard.controller

import cn.dev33.satoken.annotation.SaCheckLogin
import com.coooolfan.uniboard.error.CommonException
import com.coooolfan.uniboard.error.FileRecordException
import com.coooolfan.uniboard.model.FileRecord
import com.coooolfan.uniboard.model.by
import com.coooolfan.uniboard.model.dto.FileRecordDirectLinkCreate
import com.coooolfan.uniboard.model.dto.FileRecordDirectLinkResp
import com.coooolfan.uniboard.model.dto.FileRecordInsert
import com.coooolfan.uniboard.model.dto.FileRecordUpdate
import com.coooolfan.uniboard.service.FileRecordService
import org.babyfish.jimmer.Page
import org.babyfish.jimmer.client.FetchBy
import org.babyfish.jimmer.sql.kt.fetcher.newFetcher
import org.springframework.web.bind.annotation.*
import org.springframework.web.multipart.MultipartFile

@RestController
@RequestMapping("/api/file-record")
class FileRecordController(private val service: FileRecordService) {
    @GetMapping
    @SaCheckLogin
    fun getAllFileRecords(@RequestParam pageIndex: Int, @RequestParam pageSize: Int): Page<FileRecord> {
        return service.findByPage(pageIndex, pageSize)
    }

    @PutMapping("/{id}")
    @SaCheckLogin
    fun updateFileRecordById(@PathVariable id: Long, @RequestBody update: FileRecordUpdate) {
        service.update(update.toEntity { this.id = id })
    }

    @GetMapping("/{shareCode}")
    fun getFileRecordById(@PathVariable shareCode: String): @FetchBy("PUBLIC_FILERECORD") FileRecord {
        return service.findByByShareCode(shareCode, PUBLIC_FILERECORD) ?: throw CommonException.NotFound()
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

    @PostMapping("/direct-link")
    @SaCheckLogin
    fun createDirectLink(create: FileRecordDirectLinkCreate): FileRecordDirectLinkResp {
        return service.createDirectLink(create)
    }

    companion object {
        private val PUBLIC_FILERECORD = newFetcher(FileRecord::class).by {
            allScalarFields()
            visibility(false)
            password(false)
        }
    }

}