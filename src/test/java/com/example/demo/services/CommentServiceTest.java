package com.example.demo.services;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import com.example.demo.dto.CommentRequestDTO;
import com.example.demo.dto.CommentUpdateRequestDTO;
import com.example.demo.models.Comment;
import com.example.demo.models.TargetType;
import com.example.demo.repositories.CommentRepository;

import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@ExtendWith(MockitoExtension.class)
class CommentServiceTest {

    @Mock
    private CommentRepository commentRepository;
    @Mock
    private TargetValidator targetValidator;

    @InjectMocks
    private CommentService commentService;

    private CommentRequestDTO request(TargetType type) {
        CommentRequestDTO dto = new CommentRequestDTO();
        dto.setContent("nice");
        dto.setTargetId("t1");
        dto.setTargetType(type);
        return dto;
    }

    @Test
    void commentOnQuestionIsRejectedWith400() {
        StepVerifier.create(commentService.createComment(request(TargetType.QUESTION)))
                .expectErrorSatisfies(e -> assertEquals(HttpStatus.BAD_REQUEST,
                        ((ResponseStatusException) e).getStatusCode()))
                .verify();
        verify(commentRepository, never()).save(any());
    }

    @Test
    void commentOnAnswerIsSaved() {
        when(targetValidator.ensureExists(TargetType.ANSWER, "t1")).thenReturn(Mono.empty());
        when(commentRepository.save(any(Comment.class))).thenAnswer(inv -> {
            Comment c = inv.getArgument(0);
            c.setId("c1");
            return Mono.just(c);
        });

        StepVerifier.create(commentService.createComment(request(TargetType.ANSWER)))
                .assertNext(dto -> {
                    assertEquals("c1", dto.getId());
                    assertEquals(TargetType.ANSWER, dto.getTargetType());
                })
                .verifyComplete();
    }

    @Test
    void replyToMissingCommentFails() {
        when(targetValidator.ensureExists(TargetType.COMMENT, "t1"))
                .thenReturn(Mono.error(new ResponseStatusException(HttpStatus.NOT_FOUND)));

        StepVerifier.create(commentService.createComment(request(TargetType.COMMENT)))
                .expectError(ResponseStatusException.class)
                .verify();
        verify(commentRepository, never()).save(any());
    }

    @Test
    void updateChangesOnlyTheText() {
        Comment existing = Comment.builder().id("c1").content("old").targetId("a1")
                .targetType(TargetType.ANSWER).build();
        when(commentRepository.findById("c1")).thenReturn(Mono.just(existing));
        when(commentRepository.save(existing)).thenReturn(Mono.just(existing));
        CommentUpdateRequestDTO update = new CommentUpdateRequestDTO();
        update.setContent("edited");

        StepVerifier.create(commentService.updateComment("c1", update))
                .assertNext(dto -> {
                    assertEquals("edited", dto.getContent());
                    assertEquals("a1", dto.getTargetId());
                })
                .verifyComplete();
    }

    @Test
    void getMissingCommentReturns404() {
        when(commentRepository.findById("x")).thenReturn(Mono.empty());

        StepVerifier.create(commentService.getCommentById("x"))
                .expectErrorSatisfies(e -> assertEquals(HttpStatus.NOT_FOUND,
                        ((ResponseStatusException) e).getStatusCode()))
                .verify();
    }

    @Test
    void deleteRemovesRepliesBeforeTheParent() {
        Comment parent = Comment.builder().id("c1").build();
        Comment reply = Comment.builder().id("c2").build();
        when(commentRepository.findById("c1")).thenReturn(Mono.just(parent));
        when(commentRepository.findByTargetIdAndTargetTypeOrderByCreatedAtAsc("c1", TargetType.COMMENT))
                .thenReturn(Flux.just(reply));
        when(commentRepository.findByTargetIdAndTargetTypeOrderByCreatedAtAsc("c2", TargetType.COMMENT))
                .thenReturn(Flux.empty());
        List<String> deleted = new ArrayList<>();
        when(commentRepository.deleteById("c1")).thenReturn(Mono.fromRunnable(() -> deleted.add("c1")));
        when(commentRepository.deleteById("c2")).thenReturn(Mono.fromRunnable(() -> deleted.add("c2")));

        StepVerifier.create(commentService.deleteComment("c1")).verifyComplete();

        assertEquals(List.of("c2", "c1"), deleted);
    }
}
