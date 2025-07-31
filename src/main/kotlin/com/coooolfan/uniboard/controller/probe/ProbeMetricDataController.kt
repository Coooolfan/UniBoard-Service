package com.coooolfan.uniboard.controller.probe

import cn.dev33.satoken.annotation.SaCheckLogin
import com.coooolfan.uniboard.model.probe.ProbeTarget
import com.coooolfan.uniboard.model.probe.dto.ProbeMetricDataInsertItem
import com.coooolfan.uniboard.service.probe.ProbeService
import org.springframework.web.bind.annotation.*
import java.time.Instant


@RestController
@RequestMapping("/api/probe-target/metric/data")
class ProbeMetricDataController(private val service: ProbeService) {

    @PostMapping
    fun insertProbeMetricData(
        @RequestBody data: ProbeMetricDataInsert,
    ) {
        return service.insertMetricData(data)
    }

    @GetMapping
    @SaCheckLogin
    fun getMetricData(
        @RequestParam targetIds: List<Long>,
        @RequestParam metricIds: List<Long>,
        @RequestParam(required = false) start: Instant?,
        @RequestParam(required = false) end: Instant?
    ): List<ProbeTarget> {
        return service.getMetricData(targetIds, metricIds, start, end)
    }
}

data class ProbeMetricDataInsert(
    val targetId: Long,
    val key: String,
    val datas: List<ProbeMetricDataInsertItem>
)