package com.coooolfan.uniboard.model

import org.babyfish.jimmer.sql.Entity
import org.babyfish.jimmer.sql.GeneratedValue
import org.babyfish.jimmer.sql.GenerationType
import org.babyfish.jimmer.sql.Id

@Entity
interface FileRecord {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long

    val file: BaseSimpleFile

    val shareCode:String

    val description:String

    val visibility: FileRecordVisibility

    val password:String

    val downloadCount : Long
}