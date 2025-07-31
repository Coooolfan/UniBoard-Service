package com.coooolfan.uniboard.repo.probe

import com.coooolfan.uniboard.model.probe.*
import org.babyfish.jimmer.spring.repo.support.AbstractKotlinRepository
import org.babyfish.jimmer.sql.kt.KSqlClient
import org.babyfish.jimmer.sql.kt.ast.expression.eq
import org.babyfish.jimmer.sql.kt.ast.expression.`ge?`
import org.babyfish.jimmer.sql.kt.ast.expression.`le?`
import org.babyfish.jimmer.sql.kt.ast.expression.valueIn
import org.springframework.stereotype.Repository
import java.time.Instant

@Repository
class ProbeTargetRepo(sql: KSqlClient) : AbstractKotlinRepository<ProbeTarget, Long>(sql) {
    fun checkKeyValid(id: Long, key: String): Boolean {
        return sql.createQuery(ProbeTarget::class) {
            where(table.id eq id)
            where(table.key eq key)
            selectCount()
        }.execute()[0] == 1L
    }

    fun getMetricData(targetIds: List<Long>, metricIds: List<Long>, start: Instant?, end: Instant?): List<ProbeTarget> {
        return sql.executeQuery(ProbeTarget::class) {
            where(table.id valueIn targetIds)
            select(table.fetchBy {
                allScalarFields()
                metrics({
                    filter { where(table.id valueIn metricIds) }
                }) {
                    allScalarFields()
                    datas({
                        filter {
                            where(table.reportTime `ge?` start)
                            where(table.reportTime `le?` end)
                        }
                    }) {
                        allScalarFields()
                    }
                }
            })
        }
    }
}
