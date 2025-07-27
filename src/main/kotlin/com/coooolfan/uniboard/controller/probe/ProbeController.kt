package com.coooolfan.uniboard.controller.probe

import cn.dev33.satoken.annotation.SaCheckLogin
import com.coooolfan.uniboard.model.probe.ProbeTarget
import com.coooolfan.uniboard.model.probe.by
import com.coooolfan.uniboard.model.probe.dto.ProbeMetricDataInsertItem
import com.coooolfan.uniboard.model.probe.dto.ProbeTargetInsert
import com.coooolfan.uniboard.model.probe.dto.ProbeTargetUpdate
import com.coooolfan.uniboard.service.probe.ProbeService
import org.babyfish.jimmer.client.FetchBy
import org.babyfish.jimmer.sql.kt.fetcher.newFetcher
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.*

/**
 * 探针相关资源控制器
 *
 * 处理探针目标的增删改查操作，包括获取所有探针目标、插入新探针目标和更新探针目标信息
 * 所有操作都需要登录验证
 */
@RestController
@RequestMapping("/api/probe-target")
@SaCheckLogin
class ProbeController(private val service: ProbeService) {
    /**
     * 获取所有探针目标列表
     *
     * 获取所有已注册的探针目标列表
     * 需要登录验证
     *
     * @return List<ProbeTarget>
     * 探针目标列表，包含所有标量字段和指标信息
     */
    @GetMapping
    fun getAllProbeTagets(): List<@FetchBy("DEFAULT_PROBE_TARGET") ProbeTarget> {
        return service.findAll(DEFAULT_PROBE_TARGET)
    }


    /**
     * 插入新的探针目标
     *
     * 添加新的探针目标到系统中
     * 需要登录验证
     *
     * @param insert ProbeTargetInsert
     * 包含要插入的探针目标信息
     * @return ProbeTarget
     * 插入后的探针目标对象，包含所有标量字段和指标信息
     */
    @PostMapping
    fun insertProbeTarget(@RequestBody insert: ProbeTargetInsert): @FetchBy("DEFAULT_PROBE_TARGET") ProbeTarget {
        return service.insert(insert, DEFAULT_PROBE_TARGET)
    }


    /**
     * 更新探针目标信息
     *
     * 根据ID更新指定的探针目标信息
     * 需要登录验证
     *
     * @param id 探针目标ID
     * @param update ProbeTargetUpdate
     * 包含要更新的探针目标信息
     */
    @PutMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    fun updateProbeTarget(@PathVariable id: Long, @RequestBody update: ProbeTargetUpdate) {
        service.update(update.toEntity { this.id = id })
    }

    /**
     * 删除探针目标
     *
     * 根据ID删除指定的探针目标
     * 需要登录验证
     *
     * @param id 探针目标ID
     */
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    fun deleteProbeTargetById(@PathVariable id: Long) {
        service.delete(id)
    }

    @PostMapping("/{id}/data")
    fun insertProbeMetricData(
        @PathVariable id: Long,
        @RequestBody data: ProbeMetricDataInsert
    ) {
        return service.insertMetricData(id, data)
    }

    companion object {
        private val DEFAULT_PROBE_TARGET = newFetcher(ProbeTarget::class).by {
            allScalarFields()
            metrics {
                allScalarFields()
            }
        }
    }

}

data class ProbeMetricDataInsert(
    val key: String,
    val datas: List<ProbeMetricDataInsertItem>
)