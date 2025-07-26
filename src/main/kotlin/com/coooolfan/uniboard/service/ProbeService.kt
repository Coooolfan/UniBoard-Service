package com.coooolfan.uniboard.service

import com.coooolfan.uniboard.model.probe.ProbeTarget
import com.coooolfan.uniboard.model.probe.dto.ProbeTargetInsert
import com.coooolfan.uniboard.repo.ProbeTargetRepo
import org.babyfish.jimmer.sql.ast.mutation.SaveMode
import org.babyfish.jimmer.sql.fetcher.Fetcher
import org.springframework.stereotype.Service
import java.util.*

@Service
class ProbeService(private val repo: ProbeTargetRepo) {
    fun findAll(fetcher: Fetcher<ProbeTarget>): List<ProbeTarget> = repo.findAll(fetcher)

    fun insert(insert: ProbeTargetInsert, fetcher: Fetcher<ProbeTarget>) =
        repo.saveCommand(insert.toEntity { this.key = UUID.randomUUID().toString() }, SaveMode.INSERT_ONLY)
            .execute(fetcher).modifiedEntity

    fun update(entity: ProbeTarget) {
        repo.saveCommand(entity, SaveMode.UPDATE_ONLY).execute()
    }

}