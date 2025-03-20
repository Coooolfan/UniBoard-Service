package com.coooolfan.uniboard.controller

import cn.dev33.satoken.annotation.SaCheckLogin
import cn.dev33.satoken.stp.StpUtil
import com.coooolfan.uniboard.model.dto.ProfileLogin
import com.coooolfan.uniboard.repo.ProfileRepo
import org.springframework.web.bind.annotation.DeleteMapping
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/api/token")
class TokenController(private val repo: ProfileRepo) {
    @GetMapping
    fun getToken(login: ProfileLogin) {
        val profile = repo.findById(0)
        if (profile?.loginName == login.loginName && profile.loginPassword == login.loginPassword) {
            StpUtil.login(0)
        }
    }

    @DeleteMapping
    @SaCheckLogin
    fun deleteToken() {
        StpUtil.logout()
    }
}