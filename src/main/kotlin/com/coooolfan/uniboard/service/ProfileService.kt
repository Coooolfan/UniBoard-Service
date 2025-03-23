package com.coooolfan.uniboard.service

import cn.dev33.satoken.stp.StpUtil
import com.coooolfan.uniboard.error.CommonException
import com.coooolfan.uniboard.error.ProfileException
import com.coooolfan.uniboard.model.Profile
import com.coooolfan.uniboard.model.ProfileDraft
import com.coooolfan.uniboard.model.dto.PasswordUpdate
import com.coooolfan.uniboard.model.dto.ProfileCreate
import com.coooolfan.uniboard.model.dto.ProfileLogin
import com.coooolfan.uniboard.model.dto.ProfileUpdate
import com.coooolfan.uniboard.repo.ProfileRepo
import org.babyfish.jimmer.sql.fetcher.Fetcher
import org.springframework.stereotype.Service
import org.springframework.web.multipart.MultipartFile
import java.nio.file.Paths
import java.security.MessageDigest

@Service
class ProfileService(private val repo: ProfileRepo) {
    fun getProfile(fetcher: Fetcher<Profile>): Profile {
        return repo.findById(0, fetcher) ?: throw ProfileException.SystemUninitialized()
    }

    fun createProfile(create: ProfileCreate, avatar: MultipartFile?, banner: MultipartFile?, font: MultipartFile?) {
        if (repo.count() > 0) throw ProfileException.SystemAlreadyInitialized()
        repo.save(create.toEntity {
            id = 0
            applyProfileFiles(this, avatar, banner, font)
            loginPassword = hashPassword(create.loginPassword)
        })
    }

    fun updateProfile(update: ProfileUpdate, avatar: MultipartFile?, banner: MultipartFile?, font: MultipartFile?) {
        if (repo.count() == 0.toLong()) throw ProfileException.SystemUninitialized()
        repo.save(update.toEntity {
            id = 0
            applyProfileFiles(this, avatar, banner, font)
        })
    }

    fun checkLogin(login: ProfileLogin) {
        val profile = repo.findById(0) ?: throw CommonException.AuthenticationFailed()
        if (profile.loginName == login.loginName && profile.loginPassword == hashPassword(login.loginPassword)) StpUtil.login(
            profile.id
        )
        else throw CommonException.AuthenticationFailed()
    }

    fun updatePassword(update: PasswordUpdate) {
        val profile = repo.findById(0) ?: throw CommonException.AuthenticationFailed()
        if (profile.loginPassword != hashPassword(update.oldPassword)) throw CommonException.AuthenticationFailed()
        repo.save(Profile {
            id = 0
            loginPassword = hashPassword(update.newPassword)
        })
    }

    private fun hashPassword(password: String): String {
        val digest = MessageDigest.getInstance("SHA3-384")
        val hashBytes = digest.digest(password.toByteArray(Charsets.UTF_8))

        return hashBytes.joinToString("") {
            "%02x".format(it.toInt() and 0xFF)
        }
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

    private fun applyProfileFiles(
        profile: ProfileDraft, avatar: MultipartFile?, banner: MultipartFile?, font: MultipartFile?
    ) {
        saveProfileFile(avatar, "avatar")?.let { path ->
            profile.avatar {
                filepath = path
                filename = "avatar"
            }
        }
        saveProfileFile(banner, "banner")?.let { path ->
            profile.banner {
                filepath = path
                filename = "banner"
            }
        }
        saveProfileFile(font, "font")?.let { path ->
            profile.customFont {
                filepath = path
                filename = "font"
            }
        }
    }

}