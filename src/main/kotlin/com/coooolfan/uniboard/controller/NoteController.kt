package com.coooolfan.uniboard.controller

import cn.dev33.satoken.annotation.SaCheckLogin
import com.coooolfan.uniboard.model.Note
import com.coooolfan.uniboard.model.dto.NoteInsert
import com.coooolfan.uniboard.model.dto.NoteUpdate
import com.coooolfan.uniboard.repo.NoteRepo
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/note")
@SaCheckLogin
class NoteController(private val repo: NoteRepo) {
    @GetMapping
    fun getAllNotes(): List<Note> {
        return repo.findAll()
    }

    @GetMapping("/{id}")
    fun getNoteById(@PathVariable id: Long): Note {
        return repo.findById(id) ?: throw IllegalArgumentException("Note not found")
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    fun insertNote(@RequestBody insert: NoteInsert) {
        repo.insert(insert)
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

}