package com.coooolfan.uniboard.error

import org.babyfish.jimmer.error.ErrorFamily

@ErrorFamily
enum class CommonErrorCode {
    NOT_FOUND,
    AUTHENTICATION_FAILED, // 登录失败
    FORBIDDEN, // 没有权限
}

@ErrorFamily
enum class FileRecordErrorCode {
    EMPTY_PASSWORD,
}

@ErrorFamily
enum class ProfileErrorCode {
    SYSTEM_UNINITIALIZED,
    SYSTEM_ALREADY_INITIALIZED,
    PASSWORD_NOT_MATCH,
    EMPTY_LOGIN_NAME,
    EMPTY_NAME,
}

@ErrorFamily
enum class HyperLinkErrorCode {
    FETCH_SNAPSHOT_FAILED,
}