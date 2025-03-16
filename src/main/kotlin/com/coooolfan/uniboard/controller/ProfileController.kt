package com.coooolfan.uniboard.controller

import com.coooolfan.uniboard.model.Profile
import com.coooolfan.uniboard.model.dto.ProfileUpdate
import com.coooolfan.uniboard.service.ProfileService
import org.springframework.web.bind.annotation.*
import org.springframework.web.multipart.MultipartFile

@RestController
@RequestMapping("/api/profile")
class ProfileController(private val service: ProfileService) {
    @GetMapping
    fun getProfile(): Profile {
        return service.getProfile()
    }

    @PostMapping
    fun createProfile(
        @RequestPart update: ProfileUpdate,
        @RequestPart(required = false) avatar: MultipartFile?,
        @RequestPart(required = false) banner: MultipartFile?,
        @RequestPart(required = false) font: MultipartFile?
    ) {
        service.createProfile(update, avatar, banner, font)
    }

    @PutMapping
    fun updateProfile(
        @RequestPart update: ProfileUpdate,
        @RequestPart(required = false) avatar: MultipartFile?,
        @RequestPart(required = false) banner: MultipartFile?,
        @RequestPart(required = false) font: MultipartFile?
    ) {
        service.updateProfile(update, avatar, banner, font)
    }
}