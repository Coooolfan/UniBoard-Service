package com.coooolfan.uniboard.repo.probe

import com.coooolfan.uniboard.model.probe.ProbeMetric
import org.babyfish.jimmer.spring.repo.support.AbstractKotlinRepository
import org.babyfish.jimmer.sql.kt.KSqlClient
import org.springframework.stereotype.Repository

@Repository
class ProbeMetricRepo(sql: KSqlClient) : AbstractKotlinRepository<ProbeMetric, Long>(sql)