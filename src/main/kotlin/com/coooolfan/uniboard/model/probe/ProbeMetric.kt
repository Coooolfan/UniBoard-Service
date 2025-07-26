package com.coooolfan.uniboard.model.probe

import org.babyfish.jimmer.sql.*


@Entity
interface ProbeMetric {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long

    @Key
    val name: String

    val unit: String

    val range: ProbeMetricRange

    @Key
    @ManyToOne
    val probeTarget: ProbeTarget

    @OneToMany(mappedBy = "probeMetric")
    val datas: List<ProbeMetricData> // 采集指标


}
