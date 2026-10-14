package com.example.demo.services;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import com.example.demo.dto.CommentRequestDTO;
import com.example.demo.dto.CommentResponseDTO;
import com.example.demo.dto.CommentUpdateRequestDTO;
import com.example.demo.models.Comment;
import com.example.demo.models.TargetType;
import com.example.demo.repositories.CommentRepository;

import lombok.RequiredArgsConstructor;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Service
@RequiredArgsConstructor
public class CommentService implements ICommentService {

    private final CommentRepository commentRepository;

    private final TargetValidator targetValidator;

    @Override
    public Mono<CommentResponseDTO> createComment(CommentRequestDTO commentRequestDTO) {
        TargetType targetType = commentRequestDTO.getTargetType();

        if (targetType != TargetType.ANSWER && targetType != TargetType.COMMENT) {
            return Mono.error(new ResponseStatusException(
                    HttpStatus.BAD_REQUEST, "Comments can only be added to an ANSWER or a COMMENT"));
        }

        Comment comment = Comment.builder()
                .content(commentRequestDTO.getContent())
                .targetId(commentRequestDTO.getTargetId())
                .targetType(targetType)
                .build();

        return targetValidator.ensureExists(targetType, commentRequestDTO.getTargetId())
                .then(Mono.defer(() -> commentRepository.save(comment)))
                .map(this::mapToResponseDTO);
    }

    @Override
    public Mono<CommentResponseDTO> getCommentById(String id) {
        return findOrNotFound(id).map(this::mapToResponseDTO);
    }

    @Override
    public Mono<CommentResponseDTO> updateComment(String id, CommentUpdateRequestDTO commentUpdateRequestDTO) {
        return findOrNotFound(id)
                .flatMap(comment -> {
                    comment.setContent(commentUpdateRequestDTO.getContent());
                    return commentRepository.save(comment);
                })
                .map(this::mapToResponseDTO);
    }

    @Override
    public Mono<Void> deleteComment(String id) {
        return findOrNotFound(id).flatMap(comment -> deleteTree(comment.getId()));
    }

    @Override
    public Flux<CommentResponseDTO> getCommentsByTarget(String targetId, TargetType targetType) {
        return commentRepository.findByTargetIdAndTargetTypeOrderByCreatedAtAsc(targetId, targetType)
                .map(this::mapToResponseDTO);
    }

    @Override
    public Mono<Long> countCommentsByTarget(String targetId, TargetType targetType) {
        return commentRepository.countByTargetIdAndTargetType(targetId, targetType);
    }

    private Mono<Void> deleteTree(String commentId) {
        return commentRepository.findByTargetIdAndTargetTypeOrderByCreatedAtAsc(commentId, TargetType.COMMENT)
                .concatMap(reply -> deleteTree(reply.getId()))
                .then(commentRepository.deleteById(commentId));
    }

    private Mono<Comment> findOrNotFound(String id) {
        return commentRepository.findById(id)
                .switchIfEmpty(Mono.error(new ResponseStatusException(
                        HttpStatus.NOT_FOUND, "Comment not found with id: " + id)));
    }

    private CommentResponseDTO mapToResponseDTO(Comment comment) {
        return CommentResponseDTO.builder()
                .id(comment.getId())
                .content(comment.getContent())
                .targetId(comment.getTargetId())
                .targetType(comment.getTargetType())
                .createdAt(comment.getCreatedAt())
                .updatedAt(comment.getUpdatedAt())
                .build();
    }
}
