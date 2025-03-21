package com.coooolfan.uniboard.controller

import cn.dev33.satoken.annotation.SaCheckLogin
import com.coooolfan.uniboard.error.CommonException
import com.coooolfan.uniboard.error.ProfileException
import com.coooolfan.uniboard.model.Profile
import com.coooolfan.uniboard.model.dto.PasswordUpdate
import com.coooolfan.uniboard.model.dto.ProfileUpdate
import com.coooolfan.uniboard.service.ProfileService
import org.springframework.web.bind.annotation.*
import org.springframework.web.multipart.MultipartFile

@RestController
@RequestMapping("/api/profile")
class ProfileController(private val service: ProfileService) {
    @GetMapping
    @Throws(ProfileException.SystemUninitialized::class)
    fun getProfile(): Profile {
        return service.getProfile()
    }

    @PostMapping
    @Throws(
        ProfileException.SystemAlreadyInitialized::class,
    )
    fun createProfile(
        @RequestPart update: ProfileUpdate,
        @RequestPart(required = false) avatar: MultipartFile?,
        @RequestPart(required = false) banner: MultipartFile?,
        @RequestPart(required = false) font: MultipartFile?
    ) {
        service.createProfile(update, avatar, banner, font)
    }

    @PutMapping
    @SaCheckLogin
    @Throws(
        ProfileException.SystemUninitialized::class
    )
    fun updateProfile(
        @RequestPart update: ProfileUpdate,
        @RequestPart(required = false) avatar: MultipartFile?,
        @RequestPart(required = false) banner: MultipartFile?,
        @RequestPart(required = false) font: MultipartFile?
    ) {
        service.updateProfile(update, avatar, banner, font)
    }

    @PutMapping("/password")
    @SaCheckLogin
    @Throws(
        ProfileException.SystemUninitialized::class,
        CommonException.AuthenticationFailed::class
    )
    fun updatePassword(
        update:PasswordUpdate
    ) {
        service.updatePassword(update)
    }
}