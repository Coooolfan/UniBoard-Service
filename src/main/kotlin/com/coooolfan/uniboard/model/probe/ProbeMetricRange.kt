package com.coooolfan.uniboard.model.probe

import org.babyfish.jimmer.sql.Embeddable

@Embeddable
interface ProbeMetricRange {
    val min: Double // 最小值
    val max: Double // 最大值
}