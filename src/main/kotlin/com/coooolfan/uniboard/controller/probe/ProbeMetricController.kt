package com.coooolfan.uniboard.controller.probe

import cn.dev33.satoken.annotation.SaCheckLogin
import com.coooolfan.uniboard.model.probe.ProbeMetric
import com.coooolfan.uniboard.model.probe.by
import com.coooolfan.uniboard.model.probe.dto.ProbeMetricInsert
import com.coooolfan.uniboard.model.probe.dto.ProbeMetricUpdate
import com.coooolfan.uniboard.service.probe.ProbeMetricService
import org.babyfish.jimmer.sql.kt.fetcher.newFetcher
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/probe-target/{targetId}/metric")
@SaCheckLogin
class ProbeMetricController(private val service: ProbeMetricService) {

    @PostMapping
    fun insertProbeMetric(@PathVariable targetId: Long, @RequestBody insert: ProbeMetricInsert): ProbeMetric {
        return service.insert(insert.toEntity { probeTargetId = targetId }, DEFAULT_PROBE_TARGET_METRIC)
    }

    @PutMapping("/{metricId}")
    fun updateProbeMetric(
        @PathVariable targetId: Long, @PathVariable metricId: Long, @RequestBody insert: ProbeMetricUpdate
    ): ProbeMetric {
        return service.update(insert.toEntity {
            probeTargetId = targetId
            id = metricId
        }, DEFAULT_PROBE_TARGET_METRIC)
    }

    @DeleteMapping("/{metricId}")
    fun deleteProbeMetric(
        @PathVariable targetId: Long, @PathVariable metricId: Long
    ) {
        service.delete(metricId)
    }

    companion object {
        private val DEFAULT_PROBE_TARGET_METRIC = newFetcher(ProbeMetric::class).by {
            allScalarFields()
        }
    }

}
