package com.coooolfan.uniboard.service

import com.coooolfan.uniboard.model.HyperLink
import com.coooolfan.uniboard.model.HyperLinkDraft
import com.coooolfan.uniboard.model.dto.HyperLinkInsert
import com.coooolfan.uniboard.repo.HyperLinkRepo
import org.babyfish.jimmer.sql.ast.mutation.SaveMode
import org.babyfish.jimmer.sql.fetcher.Fetcher
import org.springframework.stereotype.Service
import org.springframework.web.multipart.MultipartFile
import java.nio.file.Paths
import java.util.*

@Service
class HyperLinkService(private val repo: HyperLinkRepo) {
    fun findAll(fetcher: Fetcher<HyperLink>) = repo.findAll(fetcher)
    fun deleteById(id: Long) = repo.deleteById(id)

    fun update(update: HyperLink, file: MultipartFile?): HyperLink {
        if (file == null) return repo.save(update, SaveMode.UPDATE_ONLY).modifiedEntity
        val (relativePath, fileName) = saveFile(file)
        return repo.save(
            HyperLinkDraft.`$`.produce(update) {
                this.icon {
                    this.filename = fileName
                    this.filepath = relativePath
                }
            },
            SaveMode.UPDATE_ONLY
        ).modifiedEntity
    }

    fun insert(insert: HyperLinkInsert, file: MultipartFile): HyperLink {
        val (relativePath, fileName) = saveFile(file)
        return repo.save(
            insert.toEntity {
                this.icon {
                    this.filename = fileName
                    this.filepath = relativePath
                }
            },
            SaveMode.INSERT_ONLY
        ).modifiedEntity
    }

    /**
     * 保存文件并返回相对路径
     */
    private fun saveFile(file: MultipartFile): SaveFileResult {
        val fileFormat = file.originalFilename?.substringAfterLast('.') ?: "jpg"
        val fileName = "${UUID.randomUUID()}.$fileFormat"
        val relativePath = Paths.get("service/hyper-link/${fileName}")
        val filePath = Paths.get(System.getProperty("user.dir")).resolve(relativePath)
        filePath.parent.toFile().mkdirs()
        file.transferTo(filePath.toFile())
        return SaveFileResult("file/hyper-link/${fileName}", fileName)
    }

    data class SaveFileResult(val relativePath: String, val fileName: String)

}
