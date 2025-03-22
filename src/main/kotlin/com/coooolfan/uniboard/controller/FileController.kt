package com.coooolfan.uniboard.controller

import cn.dev33.satoken.annotation.SaCheckLogin
import com.coooolfan.uniboard.model.dto.NotePicture
import com.coooolfan.uniboard.service.FileService
import jakarta.servlet.http.HttpServletResponse
import org.springframework.web.bind.annotation.*
import org.springframework.web.multipart.MultipartFile
import org.springframework.web.servlet.mvc.method.annotation.StreamingResponseBody

@RestController
@RequestMapping("/file")
class FileController(private val service: FileService) {

    @GetMapping("/{uuid}")
    fun downloadFileRecord(
        @PathVariable uuid: String,
        @RequestParam(required = false) pw: String?,
        resp: HttpServletResponse
    ) :StreamingResponseBody{
       return service.downloadFileRecord(uuid, pw, resp)
    }

    @PostMapping("/note")
    @SaCheckLogin
    fun uploadNotePicture(@RequestPart file: MultipartFile): NotePicture {
        return service.uploadNotePicture(file)
    }

    @GetMapping("/note/{uuid}")
    @SaCheckLogin
    fun downloadNotePicture(@PathVariable uuid: String, response: HttpServletResponse): StreamingResponseBody {
        return service.downloadNotePicture(uuid, response)
    }

    @GetMapping("/hyper-link/{uuid}")
    fun downloadHyperLinkPicture(@PathVariable uuid: String, response: HttpServletResponse): StreamingResponseBody {
        return service.downloadHyperLinkPicture(uuid, response)
    }
}