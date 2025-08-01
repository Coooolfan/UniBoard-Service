package com.coooolfan.uniboard.controller.probe

import cn.dev33.satoken.annotation.SaCheckLogin
import com.coooolfan.uniboard.model.probe.ProbeTarget
import com.coooolfan.uniboard.model.probe.dto.ProbeMetricDataInsertItem
import com.coooolfan.uniboard.service.probe.ProbeService
import org.springframework.web.bind.annotation.*
import java.time.Instant

/**
 * 探针指标数据控制器
 *
 * 处理探针指标数据的上报和查询操作
 * 数据上报无需登录验证（通过key进行鉴权），数据查询需要登录验证
 */
@RestController
@RequestMapping("/api/probe-target/metric/data")
class ProbeMetricDataController(private val service: ProbeService) {

    /**
     * 上报探针指标数据
     *
     * 接收探针客户端上报的监控数据，通过探针目标的key进行身份验证
     * 无需登录验证，但需要提供正确的探针目标key
     *
     * @param data ProbeMetricDataInsert 包含目标ID、验证key和指标数据列表
     */
    @PostMapping
    fun insertProbeMetricData(
        @RequestBody data: ProbeMetricDataInsert,
    ) {
        return service.insertMetricData(data)
    }

    /**
     * 查询探针指标数据
     *
     * 根据指定的探针目标和指标，查询指定时间范围内的监控数据
     * 需要登录验证
     *
     * @param targetIds 探针目标ID列表，指定要查询的探针目标
     * @param metricIds 指标ID列表，指定要查询的指标
     * @param start 查询开始时间，可选参数，默认为1天前
     * @param end 查询结束时间，可选参数，默认为当前时间
     * @return List<ProbeTarget> 包含指标数据的探针目标列表
     */
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

/**
 * 探针指标数据上报请求体
 *
 * 用于接收探针客户端上报的监控数据
 *
 * @property targetId 探针目标ID
 * @property key 探针目标的验证密钥，用于身份验证
 * @property datas 要上报的指标数据列表
 */
data class ProbeMetricDataInsert(
    val targetId: Long,
    val key: String,
    val datas: List<ProbeMetricDataInsertItem>
)