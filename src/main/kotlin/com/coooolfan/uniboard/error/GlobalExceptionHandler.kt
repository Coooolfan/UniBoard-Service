package com.coooolfan.uniboard.error

import cn.dev33.satoken.exception.NotLoginException
import org.babyfish.jimmer.error.CodeBasedRuntimeException
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.RestControllerAdvice
import org.springframework.web.context.request.WebRequest

@RestControllerAdvice
class GlobalExceptionHandler {
    @ExceptionHandler(CodeBasedRuntimeException::class)
    fun handle(ex: CodeBasedRuntimeException): ResponseEntity<Map<String, Any>> {
        val statusCode = when (ex.code) {
            ProfileErrorCode.SYSTEM_UNINITIALIZED.toString() -> 404
            ProfileErrorCode.SYSTEM_ALREADY_INITIALIZED.toString() -> 403
            CommonErrorCode.NOT_FOUND.toString() -> 404
            CommonErrorCode.AUTHENTICATION_FAILED.toString() -> 401
            else -> 500
        }
        return ResponseEntity
            .status(statusCode)
            .body(resultMap(ex))
    }


    @ExceptionHandler(NotLoginException::class)
    fun handleAuthenticationFailed(ex: NotLoginException, request: WebRequest): ResponseEntity<Any>? {
        return ResponseEntity
            .status(401)
            .body(resultMap(CommonException.AuthenticationFailed()))
    }

    protected fun resultMap(ex: CodeBasedRuntimeException): Map<String, Any> {
        val resultMap: MutableMap<String, Any> = LinkedHashMap()
        resultMap["family"] = ex.family
        resultMap["code"] = ex.code
        return resultMap
    }

}