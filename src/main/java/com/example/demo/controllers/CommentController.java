package com.example.demo.controllers;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import com.example.demo.dto.CommentRequestDTO;
import com.example.demo.dto.CommentResponseDTO;
import com.example.demo.dto.CommentUpdateRequestDTO;
import com.example.demo.models.TargetType;
import com.example.demo.services.ICommentService;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/api/comments")
@RequiredArgsConstructor
public class CommentController {

    private final ICommentService commentService;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<CommentResponseDTO> createComment(@Valid @RequestBody CommentRequestDTO commentRequestDTO) {
        return commentService.createComment(commentRequestDTO);
    }

    @GetMapping("/{id}")
    public Mono<CommentResponseDTO> getCommentById(@PathVariable String id) {
        return commentService.getCommentById(id);
    }

    @PutMapping("/{id}")
    public Mono<CommentResponseDTO> updateComment(@PathVariable String id,
            @Valid @RequestBody CommentUpdateRequestDTO commentUpdateRequestDTO) {
        return commentService.updateComment(id, commentUpdateRequestDTO);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> deleteComment(@PathVariable String id) {
        return commentService.deleteComment(id);
    }

    @GetMapping
    public Flux<CommentResponseDTO> getCommentsByTarget(@RequestParam String targetId,
            @RequestParam TargetType targetType) {
        return commentService.getCommentsByTarget(targetId, targetType);
    }

    @GetMapping("/count")
    public Mono<Long> countCommentsByTarget(@RequestParam String targetId,
            @RequestParam TargetType targetType) {
        return commentService.countCommentsByTarget(targetId, targetType);
    }
}
