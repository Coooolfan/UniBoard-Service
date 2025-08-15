package com.coooolfan.uniboard.controller

import com.coooolfan.uniboard.model.SimpleTargetMetricData
import com.coooolfan.uniboard.service.ProbeService
import org.springframework.web.bind.annotation.*
import java.time.Instant

@RestController
@RequestMapping("/api/probe-target/{id}")
class ProbeDataController(private val service: ProbeService) {

    @PostMapping("/data")
    fun postProbeData(@PathVariable id: Long, @RequestBody data: ProbeTargetData) {
        service.insertData(id, data)
    }

}

data class ProbeTargetData(
    val key: String,
    val timestamp: Instant,
    val data: SimpleTargetMetricData
)
