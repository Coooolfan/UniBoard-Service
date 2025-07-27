package com.coooolfan.uniboard.config

import com.fasterxml.jackson.core.JsonParser
import com.fasterxml.jackson.databind.DeserializationContext
import com.fasterxml.jackson.databind.JsonDeserializer
import org.springframework.boot.jackson.JsonComponent
import java.io.IOException
import java.time.Instant
import java.time.LocalDateTime
import java.time.ZoneOffset.UTC
import java.time.format.DateTimeFormatter


@JsonComponent
class LocalDateTimeDeserializer : JsonDeserializer<LocalDateTime?>() {
    @Throws(IOException::class)
    override fun deserialize(p: JsonParser, ctxt: DeserializationContext?): LocalDateTime {
        val value: String = p.valueAsString

        // 检查是否为时间戳格式
        if (value.matches("\\d+".toRegex())) {
            val timestamp = value.toLong()
            return LocalDateTime.ofInstant(
                Instant.ofEpochMilli(timestamp),
                UTC
            )
        }

        // 如果不是时间戳，按标准格式解析
        return LocalDateTime.parse(value, DateTimeFormatter.ISO_LOCAL_DATE_TIME)
    }
}