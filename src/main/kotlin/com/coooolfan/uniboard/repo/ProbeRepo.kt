package com.coooolfan.uniboard.repo

import com.coooolfan.uniboard.model.probe.ProbeTarget
import org.babyfish.jimmer.spring.repo.support.AbstractKotlinRepository
import org.babyfish.jimmer.sql.kt.KSqlClient
import org.springframework.stereotype.Repository

@Repository
class ProbeTargetRepo(sql: KSqlClient) : AbstractKotlinRepository<ProbeTarget, Long>(sql)

//@Repository
//class ProbeMetricRepo(sql: KSqlClient) : AbstractKotlinRepository<ProbeMetric, Long>(sql)

//@Repository
//class ProbeMetricDataRepo(sql: KSqlClient) : AbstractKotlinRepository<ProbeMetricData, Long>(sql)