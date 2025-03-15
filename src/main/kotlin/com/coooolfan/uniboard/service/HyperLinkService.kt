package com.coooolfan.uniboard.service

import com.coooolfan.uniboard.model.HyperLink
import com.coooolfan.uniboard.model.dto.HyperLinkInsert
import com.coooolfan.uniboard.repo.HyperLinkRepo
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional
import org.springframework.web.multipart.MultipartFile
import java.io.File
import java.util.*

@Service
class HyperLinkService(private val repo:HyperLinkRepo) {
    fun findAll() = repo.findAll()
    fun deleteById(id: Long) = repo.deleteById(id)
    fun update(update: HyperLink) = repo.update(update)

    @Transactional
    fun insert(insert: HyperLinkInsert, file: MultipartFile): HyperLink {
        val programPath = System.getProperty("user.dir") + "/service/hyperlink"
        val path = File(programPath)
        val fileFormat = file.originalFilename?.split(".")?.last() ?: "icon"
        val filePath = File(path, UUID.randomUUID().toString() + "." + fileFormat)
        file.transferTo(filePath)
        return repo.insert(
            insert.toEntity {
                this.icon { this.filepath = filePath.path }
            },
        ).modifiedEntity
    }
}