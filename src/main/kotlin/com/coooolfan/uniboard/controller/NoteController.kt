package com.coooolfan.uniboard.controller

import cn.dev33.satoken.annotation.SaCheckLogin
import com.coooolfan.uniboard.error.CommonException
import com.coooolfan.uniboard.model.Note
import com.coooolfan.uniboard.model.by
import com.coooolfan.uniboard.model.dto.NoteInsert
import com.coooolfan.uniboard.model.dto.NoteUpdate
import com.coooolfan.uniboard.repo.NoteRepo
import org.babyfish.jimmer.client.FetchBy
import org.babyfish.jimmer.sql.kt.fetcher.newFetcher
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/note")
@SaCheckLogin
class NoteController(private val repo: NoteRepo) {
    @GetMapping
    fun getAllNotes(): List<@FetchBy("DEFAULT_NOTE") Note> {
        return repo.findAll(DEFAULT_NOTE)
    }

    @GetMapping("/{id}")
    @Throws(CommonException.NotFound::class)
    fun getNoteById(@PathVariable id: Long): @FetchBy("DEFAULT_NOTE") Note {
        return repo.findById(id, DEFAULT_NOTE) ?: throw CommonException.NotFound()
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    fun insertNote(@RequestBody insert: NoteInsert): @FetchBy("DEFAULT_NOTE") Note {
        return repo.insert(insert).modifiedEntity
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    fun deleteNoteById(@PathVariable id: Long) {
        repo.deleteById(id)
    }

    @PutMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    fun updateNoteById(@PathVariable id: Long, @RequestBody update: NoteUpdate) {
        repo.update(update.toEntity { this.id = id })
    }

    companion object {
        private val DEFAULT_NOTE = newFetcher(Note::class).by {
            allScalarFields()
        }
    }
}