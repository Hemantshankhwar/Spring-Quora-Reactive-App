package com.example.demo.services;

import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import com.example.demo.models.TargetType;
import com.example.demo.repositories.AnswerRepository;
import com.example.demo.repositories.CommentRepository;
import com.example.demo.repositories.QuestionRepository;

import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@ExtendWith(MockitoExtension.class)
class TargetValidatorTest {

    @Mock
    private QuestionRepository questionRepository;
    @Mock
    private AnswerRepository answerRepository;
    @Mock
    private CommentRepository commentRepository;

    @InjectMocks
    private TargetValidator validator;

    @Test
    void completesWhenQuestionExists() {
        when(questionRepository.existsById("q1")).thenReturn(Mono.just(true));

        StepVerifier.create(validator.ensureExists(TargetType.QUESTION, "q1")).verifyComplete();
        verifyNoInteractions(answerRepository, commentRepository);
    }

    @Test
    void checksTheRepositoryMatchingTheType() {
        when(answerRepository.existsById("a1")).thenReturn(Mono.just(true));
        when(commentRepository.existsById("c1")).thenReturn(Mono.just(true));

        StepVerifier.create(validator.ensureExists(TargetType.ANSWER, "a1")).verifyComplete();
        StepVerifier.create(validator.ensureExists(TargetType.COMMENT, "c1")).verifyComplete();
        verifyNoInteractions(questionRepository);
    }

    @Test
    void failsWith404WhenTargetMissing() {
        when(answerRepository.existsById("nope")).thenReturn(Mono.just(false));

        StepVerifier.create(validator.ensureExists(TargetType.ANSWER, "nope"))
                .expectErrorSatisfies(e -> {
                    ResponseStatusException ex = (ResponseStatusException) e;
                    org.junit.jupiter.api.Assertions.assertEquals(HttpStatus.NOT_FOUND, ex.getStatusCode());
                })
                .verify();
    }
}
