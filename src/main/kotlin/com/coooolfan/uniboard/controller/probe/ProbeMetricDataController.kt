package com.coooolfan.uniboard.controller.probe

import cn.dev33.satoken.annotation.SaCheckLogin
import com.coooolfan.uniboard.model.probe.ProbeTarget
import com.coooolfan.uniboard.model.probe.dto.ProbeMetricDataInsertItem
import com.coooolfan.uniboard.model.probe.fetchBy
import com.coooolfan.uniboard.model.probe.id
import com.coooolfan.uniboard.model.probe.reportTime
import com.coooolfan.uniboard.service.probe.ProbeService
import org.babyfish.jimmer.sql.kt.KSqlClient
import org.babyfish.jimmer.sql.kt.ast.expression.`ge?`
import org.babyfish.jimmer.sql.kt.ast.expression.`le?`
import org.babyfish.jimmer.sql.kt.ast.expression.valueIn
import org.springframework.web.bind.annotation.*
import java.time.Instant


@RestController
@RequestMapping("/api/probe-target/metric/data")
class ProbeMetricDataController(private val service: ProbeService, private val sql: KSqlClient) {

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
        return sql.executeQuery(ProbeTarget::class) {
            where(table.id valueIn targetIds)
            select(table.fetchBy {
                allScalarFields()
                metrics({
                    filter { where(table.id valueIn metricIds) }
                }) {
                    allScalarFields()
                    datas({
                        filter {
                            where(table.reportTime `ge?` start)
                            where(table.reportTime `le?` end)
                        }
                    }) {
                        allScalarFields()
                    }
                }
            })
        }
    }
}

data class ProbeMetricDataInsert(
    val targetId: Long,
    val key: String,
    val datas: List<ProbeMetricDataInsertItem>
)