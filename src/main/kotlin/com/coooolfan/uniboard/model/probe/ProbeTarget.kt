package com.coooolfan.uniboard.model.probe

import org.babyfish.jimmer.sql.*

@Entity
interface ProbeTarget {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long

    val name: String

    val description: String

    // 用于上报服务鉴权
    @Key
    val key: String

    val location: ProbeTargetLocation

    @OneToMany(mappedBy = "probeTarget")
    val metrics: List<ProbeMetric> // 采集指标

}

