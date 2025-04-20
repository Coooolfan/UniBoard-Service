package com.coooolfan.uniboard.service

import com.coooolfan.uniboard.model.HyperLink
import com.coooolfan.uniboard.model.dto.HyperLinkInsert
import com.coooolfan.uniboard.repo.HyperLinkRepo
import com.coooolfan.uniboard.utils.SaveFileResult
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

    fun update(update: HyperLink, file: MultipartFile?, fetcher: Fetcher<HyperLink>): HyperLink {
        if (file == null) {
            return repo.saveCommand(update, SaveMode.UPDATE_ONLY).execute(fetcher).modifiedEntity
        }
        val (relativePath, fileName) = saveFile(file)
        return repo.saveCommand(
            HyperLink(update) {
                this.icon {
                    this.filename = fileName
                    this.filepath = relativePath
                }
            },
            SaveMode.UPDATE_ONLY
        ).execute(fetcher).modifiedEntity
    }

    fun insert(insert: HyperLinkInsert, file: MultipartFile, fetcher: Fetcher<HyperLink>): HyperLink {
        val (relativePath, fileName) = saveFile(file)
        return repo.saveCommand(
            insert.toEntity {
                this.icon {
                    this.filename = fileName
                    this.filepath = relativePath
                }
            },
            SaveMode.INSERT_ONLY
        ).execute(fetcher).modifiedEntity
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
}
