package com.coooolfan.uniboard.error

import cn.dev33.satoken.exception.NotLoginException
import org.springframework.http.HttpStatus
import org.springframework.http.ProblemDetail
import org.springframework.http.ResponseEntity
import org.springframework.web.ErrorResponseException
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.RestControllerAdvice
import org.springframework.web.context.request.WebRequest
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler
import java.net.URI


@RestControllerAdvice
class GlobalExceptionHandler : ResponseEntityExceptionHandler() {

    @ExceptionHandler(
        NotLoginException::class,
        CommonException.AuthenticationFailed::class
    )
    fun handleNotLoginException(ex: NotLoginException, request: WebRequest): ResponseEntity<Any?>? {
        val problemDetail = ProblemDetail.forStatus(HttpStatus.UNAUTHORIZED)
        problemDetail.type = URI.create("https://www.google.com/search?q=401+Unauthorized")
        val errorResponseException =
            ErrorResponseException(
                HttpStatus.UNAUTHORIZED,
                problemDetail,
                ex.cause
            )
        return handleExceptionInternal(
            errorResponseException,
            errorResponseException.body,
            errorResponseException.headers,
            errorResponseException.statusCode,
            request
        )
    }

    @ExceptionHandler(CommonException.NotFound::class)
    fun handleNotFound(ex:Exception,request: WebRequest): ResponseEntity<Any?>? {
        val problemDetail = ProblemDetail.forStatus(HttpStatus.NOT_FOUND)
        problemDetail.type = URI.create("https://www.google.com/search?q=404+Not+Found")
        val errorResponseException =
            ErrorResponseException(
                HttpStatus.NOT_FOUND,
                problemDetail,
                ex.cause
            )
        return handleExceptionInternal(
            errorResponseException,
            errorResponseException.body,
            errorResponseException.headers,
            errorResponseException.statusCode,
            request
        )
    }
}