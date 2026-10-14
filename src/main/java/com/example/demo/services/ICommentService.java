package com.example.demo.services;

import com.example.demo.dto.CommentRequestDTO;
import com.example.demo.dto.CommentResponseDTO;
import com.example.demo.dto.CommentUpdateRequestDTO;
import com.example.demo.models.TargetType;

import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

public interface ICommentService {

    // Comments can only target an ANSWER or another COMMENT
    Mono<CommentResponseDTO> createComment(CommentRequestDTO commentRequestDTO);

    Mono<CommentResponseDTO> getCommentById(String id);

    Mono<CommentResponseDTO> updateComment(String id, CommentUpdateRequestDTO commentUpdateRequestDTO);

    // Also deletes every reply nested under the comment
    Mono<Void> deleteComment(String id);

    Flux<CommentResponseDTO> getCommentsByTarget(String targetId, TargetType targetType);

    Mono<Long> countCommentsByTarget(String targetId, TargetType targetType);
}
