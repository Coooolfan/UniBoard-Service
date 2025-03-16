package com.coooolfan.uniboard.error

import org.babyfish.jimmer.error.ErrorFamily

@ErrorFamily
enum class ProfileErrorCode {
    SYSTEM_UNINITIALIZED,
    SYSTEM_ALREADY_INITIALIZED,
    PASSWORD_NOT_MATCH,
}