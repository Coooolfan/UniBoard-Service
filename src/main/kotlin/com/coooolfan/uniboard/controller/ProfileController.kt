package com.coooolfan.uniboard.controller

import cn.dev33.satoken.annotation.SaCheckLogin
import com.coooolfan.uniboard.error.CommonException
import com.coooolfan.uniboard.error.ProfileException
import com.coooolfan.uniboard.model.Profile
import com.coooolfan.uniboard.model.by
import com.coooolfan.uniboard.model.dto.PasswordUpdate
import com.coooolfan.uniboard.model.dto.ProfileCreate
import com.coooolfan.uniboard.model.dto.ProfileUpdate
import com.coooolfan.uniboard.service.ProfileService
import org.babyfish.jimmer.client.FetchBy
import org.babyfish.jimmer.sql.kt.fetcher.newFetcher
import org.springframework.web.bind.annotation.*
import org.springframework.web.multipart.MultipartFile

@RestController
@RequestMapping("/api/profile")
class ProfileController(private val service: ProfileService) {
    @GetMapping
    @Throws(ProfileException.SystemUninitialized::class)
    fun getProfile(): @FetchBy("PUBLIC_PROFILE") Profile {
        return service.getProfile(PUBLIC_PROFILE)
    }

    @PostMapping
    @Throws(
        ProfileException.SystemAlreadyInitialized::class,
        ProfileException.EmptyLoginName::class,
        ProfileException.EmptyName::class,
    )
    fun createProfile(
        @RequestPart create: ProfileCreate,
        @RequestPart(required = false) avatar: MultipartFile?,
        @RequestPart(required = false) banner: MultipartFile?,
        @RequestPart(required = false) font: MultipartFile?
    ) {
        service.createProfile(create, avatar, banner, font)
    }

    @PutMapping
    @SaCheckLogin
    @Throws(
        ProfileException.SystemUninitialized::class,
        ProfileException.EmptyName::class,
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
        ProfileException.EmptyLoginName::class,
        CommonException.Forbidden::class
    )
    fun updatePassword(
        update: PasswordUpdate
    ) {
        service.updatePassword(update)
    }

    companion object {
        private val PUBLIC_PROFILE = newFetcher(Profile::class).by {
            allScalarFields()
            loginName(false)
            loginPassword(false)
        }
    }
}