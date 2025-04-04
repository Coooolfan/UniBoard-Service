package com.coooolfan.uniboard.error

import org.babyfish.jimmer.error.ErrorFamily

@ErrorFamily
enum class CommonErrorCode {
    NOT_FOUND,
    AUTHENTICATION_FAILED, // 登录失败
    FORBIDDEN, // 没有权限
}