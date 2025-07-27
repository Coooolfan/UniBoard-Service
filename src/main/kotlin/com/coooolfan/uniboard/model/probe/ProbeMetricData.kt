package com.coooolfan.uniboard.model.probe

import org.babyfish.jimmer.sql.*
import java.time.LocalDateTime

@Entity
interface ProbeMetricData {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long

    val value: Double

    // 数据采集时间
    val reportTime: LocalDateTime

    @ManyToOne
    val probeMetric: ProbeMetric
}