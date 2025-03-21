package com.coooolfan.uniboard.service

import cn.dev33.satoken.stp.StpUtil
import com.coooolfan.uniboard.error.CommonException
import com.coooolfan.uniboard.model.FileRecord
import com.coooolfan.uniboard.model.FileRecordVisibility
import com.coooolfan.uniboard.model.dto.NotePicture
import com.coooolfan.uniboard.repo.FileRecordRepo
import jakarta.servlet.http.HttpServletResponse
import org.springframework.stereotype.Service
import org.springframework.web.multipart.MultipartFile
import org.springframework.web.servlet.mvc.method.annotation.StreamingResponseBody
import java.io.File
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.util.*

@Service
class FileService(private val repo: FileRecordRepo) {
    fun downloadFileRecord(uuid: String, password: String?, resp: HttpServletResponse) {
        if (uuid.contains('-')) {
            // TODO 使用UUID直链下载文件，无需鉴权，从Redis中获取UUID对应的文件对象
            println("使用UUID直链下载文件，无需鉴权，从Redis中获取UUID对应的文件对象")
        }

        val fileRecord = getFileRecord(uuid) ?: throw CommonException.NotFound()

        if (// 已登录可直接下载
            StpUtil.isLogin() ||
            // 未登录且文件为公开
            fileRecord.visibility == FileRecordVisibility.PUBLIC ||
            // 未登录且文件为密码保护且密码正确
            (fileRecord.visibility == FileRecordVisibility.PASSWORD && fileRecord.password == password)
        )
            returnFile2Response(fileRecord.file.filepath, "filerecord", resp)

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
        return returnFile2Response(uuid, "note", resp)
    }

    fun downloadHyperLinkPicture(uuid: String, resp: HttpServletResponse): StreamingResponseBody {
        return returnFile2Response(uuid, "hyperlink", resp)
    }

    private fun returnFile2Response(uuid: String, funName: String, resp: HttpServletResponse): StreamingResponseBody {
        val programPath = System.getProperty("user.dir") + "/service/" + funName
        val filePath: Path = Paths.get(programPath, uuid)

        val file = File(filePath.toString())

        val contentType = Files.probeContentType(filePath) ?: "application/octet-stream"
        resp.contentType = contentType
        resp.setContentLength(file.length().toInt())
        resp.setHeader("Content-Disposition", "attachment; filename=\"${file.name}\"")

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