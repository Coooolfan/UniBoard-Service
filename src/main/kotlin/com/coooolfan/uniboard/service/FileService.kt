package com.coooolfan.uniboard.service

import com.coooolfan.uniboard.model.dto.NotePicture
import jakarta.servlet.http.HttpServletResponse
import org.springframework.stereotype.Service
import org.springframework.web.multipart.MultipartFile
import org.springframework.web.servlet.mvc.method.annotation.StreamingResponseBody
import java.io.File
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.util.UUID

@Service
class FileService {
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

}