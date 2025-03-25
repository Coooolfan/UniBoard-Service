package com.coooolfan.uniboard.service

import com.coooolfan.uniboard.model.HyperLink
import com.coooolfan.uniboard.model.dto.HyperLinkInsert
import com.coooolfan.uniboard.repo.HyperLinkRepo
import org.springframework.stereotype.Service
import org.springframework.web.multipart.MultipartFile
import java.nio.file.Paths
import java.util.*

@Service
class HyperLinkService(private val repo: HyperLinkRepo) {
    fun findAll() = repo.findAll()
    fun deleteById(id: Long) = repo.deleteById(id)
    fun update(update: HyperLink) = repo.update(update)

    fun insert(insert: HyperLinkInsert, file: MultipartFile): HyperLink {
        val fileFormat = file.originalFilename?.substringAfterLast('.') ?: "jpg"
        val relativePath = Paths.get("file/hyperlink/${UUID.randomUUID()}.$fileFormat")
        val filePath = Paths.get(System.getProperty("user.dir")).resolve(relativePath)
        filePath.parent.toFile().mkdirs()
        file.transferTo(filePath.toFile())
        return repo.insert(
            insert.toEntity {
                this.icon { this.filepath = relativePath.toString() }
            },
        ).modifiedEntity
    }
}