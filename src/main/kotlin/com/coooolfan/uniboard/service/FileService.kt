package com.coooolfan.uniboard.service

import cn.dev33.satoken.stp.StpUtil
import com.coooolfan.uniboard.error.CommonException
import com.coooolfan.uniboard.model.FileRecord
import com.coooolfan.uniboard.model.FileRecordVisibility
import com.coooolfan.uniboard.model.dto.NotePicture
import com.coooolfan.uniboard.repo.FileRecordRepo
import com.github.benmanes.caffeine.cache.Cache
import jakarta.servlet.http.HttpServletResponse
import org.springframework.stereotype.Service
import org.springframework.web.multipart.MultipartFile
import org.springframework.web.servlet.mvc.method.annotation.StreamingResponseBody
import java.io.File
import java.net.URLEncoder
import java.nio.charset.StandardCharsets
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.util.*

@Service
class FileService(
    private val repo: FileRecordRepo,
    private val directLinkCache: Cache<String, Long>
) {
    fun downloadFileRecord(key: String, password: String?, resp: HttpServletResponse): StreamingResponseBody {
        if (key.contains('-')) {
            // Use UUID direct link to download file without authentication
            val fileId = directLinkCache.getIfPresent(key) ?: throw CommonException.NotFound()
            val fileRecord = repo.findById(fileId) ?: throw CommonException.NotFound()
            return returnFile2Response(fileRecord.file.filepath, resp, fileRecord.file.filename)
        }

        val fileRecord = getFileRecord(key) ?: throw CommonException.NotFound()
        if (// 已登录可直接下载
            StpUtil.isLogin() ||
            // 未登录且文件为公开
            fileRecord.visibility == FileRecordVisibility.PUBLIC ||
            // 未登录且文件为密码保护且密码正确
            (fileRecord.visibility == FileRecordVisibility.PASSWORD && fileRecord.password == password)
        )
            return returnFile2Response(fileRecord.file.filepath, resp, fileRecord.file.filename)

        throw CommonException.NotFound()
    }

    fun uploadNotePicture(file: MultipartFile): NotePicture {
        val fileFormat = file.originalFilename?.substringAfterLast('.') ?: "jpg"
        val relativePath = Paths.get("service/note/${UUID.randomUUID()}.$fileFormat")
        val filePath = Paths.get(System.getProperty("user.dir")).resolve(relativePath)
        filePath.parent.toFile().mkdirs()
        file.transferTo(filePath.toFile())
        return NotePicture(relativePath.toString())
    }

    fun downloadNotePicture(uuid: String, resp: HttpServletResponse): StreamingResponseBody {
        return returnFile2Response(uuid, resp)
    }

    fun downloadHyperLinkPicture(uuid: String, resp: HttpServletResponse): StreamingResponseBody {
        return returnFile2Response(uuid, resp)
    }

    private fun returnFile2Response(
        uuid: String,
        resp: HttpServletResponse,
        fileName: String? = null
    ): StreamingResponseBody {
        val programPath = System.getProperty("user.dir")
        val filePath: Path = Paths.get(programPath, uuid)

        val file = File(filePath.toString())
        val encodedFileName: String = URLEncoder.encode(fileName ?: file.name, StandardCharsets.UTF_8)
            .replace("+", "%20")

        val contentType = Files.probeContentType(filePath) ?: "application/octet-stream"

        resp.contentType = contentType
        resp.setContentLength(file.length().toInt())
        resp.setHeader(
            "Content-Disposition",
            "attachment; filename=\"${encodedFileName}\"; filename*=UTF-8''${encodedFileName}"
        )
        return StreamingResponseBody { outputStream ->
            Files.copy(filePath, outputStream)
            outputStream.flush()
        }
    }

    private fun getFileRecord(key: String): FileRecord? {
        if (key.all { it.isDigit() })
            return repo.findById(key.toLong())
        return repo.findByShareCode(key)
    }

}