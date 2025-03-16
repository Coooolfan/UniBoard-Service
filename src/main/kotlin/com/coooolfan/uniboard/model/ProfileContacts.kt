package com.coooolfan.uniboard.model

import org.babyfish.jimmer.sql.Serialized

@Serialized
data class ProfileContacts(
    val github: String,
    val weibo: String,
    val qq: String,
    val wechat: String,
    val email: String,
    val twitter: String,
    val linkedin: String,
    val facebook: String,
    val instagram: String,
    val telegram: String,
    val website: String
)
