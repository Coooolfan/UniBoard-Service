package com.coooolfan.uniboard.model

import org.babyfish.jimmer.sql.EnumType

@EnumType(EnumType.Strategy.NAME)
enum class FileRecordVisibility {
    OPEN,
    PASSWORD,
    PRIVATE
}