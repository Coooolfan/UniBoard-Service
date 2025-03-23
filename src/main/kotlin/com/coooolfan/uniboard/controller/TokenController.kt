package com.coooolfan.uniboard.controller

import cn.dev33.satoken.annotation.SaCheckLogin
import cn.dev33.satoken.stp.StpUtil
import com.coooolfan.uniboard.error.CommonException
import com.coooolfan.uniboard.model.dto.ProfileLogin
import com.coooolfan.uniboard.service.ProfileService
import org.springframework.web.bind.annotation.DeleteMapping
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/api/token")
class TokenController(private val service: ProfileService) {
    @GetMapping
    @Throws(CommonException.AuthenticationFailed::class)
    fun getToken(login: ProfileLogin) {
        service.checkLogin(login)
    }

    @DeleteMapping
    @SaCheckLogin
    fun deleteToken() {
        StpUtil.logout()
    }
}