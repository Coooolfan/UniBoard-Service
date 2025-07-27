package com.coooolfan.uniboard.repo.probe

import com.coooolfan.uniboard.model.probe.ProbeMetricData
import org.babyfish.jimmer.spring.repo.support.AbstractKotlinRepository
import org.babyfish.jimmer.sql.kt.KSqlClient
import org.springframework.stereotype.Repository

@Repository
class ProbeMetricDataRepo(sql: KSqlClient) : AbstractKotlinRepository<ProbeMetricData, Long>(sql)
