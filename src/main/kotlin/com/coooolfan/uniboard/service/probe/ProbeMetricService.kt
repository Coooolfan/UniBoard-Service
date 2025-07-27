package com.coooolfan.uniboard.service.probe

import com.coooolfan.uniboard.model.probe.ProbeMetric
import com.coooolfan.uniboard.repo.probe.ProbeMetricRepo
import org.babyfish.jimmer.sql.ast.mutation.SaveMode
import org.babyfish.jimmer.sql.fetcher.Fetcher
import org.springframework.stereotype.Service

@Service
class ProbeMetricService(private val repo: ProbeMetricRepo) {
    fun insert(insert: ProbeMetric, fetcher: Fetcher<ProbeMetric>) =
        repo.saveCommand(insert, SaveMode.INSERT_ONLY).execute(fetcher).modifiedEntity

    fun update(entity: ProbeMetric, fetcher: Fetcher<ProbeMetric>) =
        repo.saveCommand(entity, SaveMode.UPDATE_ONLY).execute(fetcher).modifiedEntity

    fun delete(metricId: Long) = repo.deleteById(metricId)

}