package com.coooolfan.uniboard.utils

import java.security.MessageDigest

 fun getHashedString(str: String): String {
    val strRand = str + System.currentTimeMillis().toString()
    val digest = MessageDigest.getInstance("SHA3-224")
    val hashBytes = digest.digest(strRand.toByteArray(Charsets.UTF_8))

    val charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    val result = StringBuilder()

    // 将哈希值转换为一个整数
    val hashInt = hashBytes.fold(0) { acc, byte -> (acc shl 8) + (byte.toInt() and 0xFF) }

    // 生成4个字符
    repeat(4) { i ->
        // 分布均匀
        val index = (hashInt shr (i * 6)) and 0x3F // 使用6位(0-63)来索引字符集
        val charIndex = index % charset.length
        result.append(charset[charIndex])
    }

    return result.toString()
}