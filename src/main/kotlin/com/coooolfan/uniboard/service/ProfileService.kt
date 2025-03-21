package com.coooolfan.uniboard.service

import com.coooolfan.uniboard.error.ProfileException
import com.coooolfan.uniboard.model.Profile
import com.coooolfan.uniboard.model.dto.ProfileUpdate
import com.coooolfan.uniboard.repo.ProfileRepo
import org.springframework.stereotype.Service
import org.springframework.web.multipart.MultipartFile
import java.nio.file.Paths

@Service
class ProfileService(private val repo: ProfileRepo) {
    fun getProfile(): Profile {
        return repo.findById(0) ?: throw ProfileException.SystemUninitialized()
    }

    fun createProfile(update: ProfileUpdate, avatar: MultipartFile?, banner: MultipartFile?, font: MultipartFile?) {
        if (repo.count() > 0) throw ProfileException.SystemAlreadyInitialized()

        repo.save(update.toEntity {
            id = 0
            saveProfileFile(avatar, "avatar")?.let { path -> avatar { filepath = path } }
            saveProfileFile(banner, "banner")?.let { path -> banner { filepath = path } }
            saveProfileFile(font, "font")?.let { path -> customFont { filepath = path } }
        })
    }

    private fun saveProfileFile(file: MultipartFile?, category: String): String? {
        if (file?.isEmpty != false) return null

        val fileFormat = file.originalFilename?.substringAfterLast('.') ?: "jpg"
        val relativePath = Paths.get("service/profile/${category}.$fileFormat")
        val filePath = Paths.get(System.getProperty("user.dir")).resolve(relativePath)
        filePath.parent.toFile().mkdirs()
        file.transferTo(filePath)
        return relativePath.toString()
    }

    fun updateProfile(update: ProfileUpdate, avatar: MultipartFile?, banner: MultipartFile?, font: MultipartFile?) =
        createProfile(update, avatar, banner, font)

}