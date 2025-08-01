package com.coooolfan.uniboard.service.probe

import com.coooolfan.uniboard.controller.probe.ProbeMetricDataInsert
import com.coooolfan.uniboard.error.CommonException
import com.coooolfan.uniboard.model.probe.ProbeTarget
import com.coooolfan.uniboard.model.probe.dto.ProbeTargetInsert
import com.coooolfan.uniboard.repo.probe.ProbeMetricDataRepo
import com.coooolfan.uniboard.repo.probe.ProbeTargetRepo
import org.babyfish.jimmer.sql.ast.mutation.SaveMode
import org.babyfish.jimmer.sql.fetcher.Fetcher
import org.springframework.stereotype.Service
import java.time.Duration
import java.time.Instant
import java.util.*

@Service
class ProbeService(private val repo: ProbeTargetRepo, private val datasource: ProbeMetricDataRepo) {
    fun findAll(fetcher: Fetcher<ProbeTarget>) = repo.findAll(fetcher)

    fun insert(insert: ProbeTargetInsert, fetcher: Fetcher<ProbeTarget>) =
        repo.saveCommand(insert.toEntity { this.key = UUID.randomUUID().toString() }, SaveMode.INSERT_ONLY)
            .execute(fetcher).modifiedEntity

    fun update(entity: ProbeTarget) {
        repo.saveCommand(entity, SaveMode.UPDATE_ONLY).execute()
    }

    fun delete(id: Long) = repo.deleteById(id)

    fun insertMetricData(insert: ProbeMetricDataInsert) {
        if (!repo.checkKeyValid(insert.targetId, insert.key)) throw CommonException.forbidden()

        datasource.saveInputsCommand(
            insert.datas,
            SaveMode.INSERT_ONLY
        ).execute()
    }

    fun getMetricData(targetIds: List<Long>, metricIds: List<Long>, start: Instant?, end: Instant?): List<ProbeTarget> {
        val startTime = start ?: Instant.now().minus(Duration.ofDays(1))
        val endTime = end ?: Instant.now()
        return repo.getMetricData(targetIds, metricIds, startTime, endTime)
    }
}