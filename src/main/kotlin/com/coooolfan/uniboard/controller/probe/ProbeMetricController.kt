package com.coooolfan.uniboard.controller.probe

import cn.dev33.satoken.annotation.SaCheckLogin
import com.coooolfan.uniboard.model.probe.ProbeMetric
import com.coooolfan.uniboard.model.probe.by
import com.coooolfan.uniboard.model.probe.dto.ProbeMetricInsert
import com.coooolfan.uniboard.model.probe.dto.ProbeMetricUpdate
import com.coooolfan.uniboard.service.probe.ProbeMetricService
import org.babyfish.jimmer.sql.kt.fetcher.newFetcher
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.*

/**
 * 探针指标控制器
 *
 * 处理探针目标下的指标管理操作，包括添加、更新和删除指标
 * 所有操作都需要登录验证
 */
@RestController
@RequestMapping("/api/probe-target/{targetId}/metric")
@SaCheckLogin
class ProbeMetricController(private val service: ProbeMetricService) {

    /**
     * 为指定探针目标添加新指标
     *
     * 为指定的探针目标添加一个新的监控指标，用于定义需要采集的数据类型
     * 需要登录验证
     *
     * @param targetId 探针目标ID
     * @param insert ProbeMetricInsert 包含指标信息的DTO对象
     * @return ProbeMetric 创建后的指标对象，包含所有标量字段
     */
    @PostMapping
    fun insertProbeMetric(@PathVariable targetId: Long, @RequestBody insert: ProbeMetricInsert): ProbeMetric {
        return service.insert(insert.toEntity { probeTargetId = targetId }, DEFAULT_PROBE_TARGET_METRIC)
    }

    /**
     * 更新指定的探针指标
     *
     * 更新指定探针目标下的特定指标的配置信息，如指标名称、单位、范围等
     * 需要登录验证
     *
     * @param targetId 探针目标ID
     * @param metricId 指标ID
     * @param insert ProbeMetricUpdate 包含要更新的指标信息
     * @return ProbeMetric 更新后的指标对象，包含所有标量字段
     */
    @PutMapping("/{metricId}")
    fun updateProbeMetric(
        @PathVariable targetId: Long, @PathVariable metricId: Long, @RequestBody insert: ProbeMetricUpdate
    ): ProbeMetric {
        return service.update(insert.toEntity {
            probeTargetId = targetId
            id = metricId
        }, DEFAULT_PROBE_TARGET_METRIC)
    }

    /**
     * 删除指定的探针指标
     *
     * 删除指定探针目标下的特定指标，删除后该指标的所有历史数据也将被清理
     * 需要登录验证
     *
     * @param targetId 探针目标ID
     * @param metricId 指标ID
     */
    @DeleteMapping("/{metricId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
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
