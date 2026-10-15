package com.example.demo.services;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import com.example.demo.dto.AnswerRequestDTO;
import com.example.demo.models.Answer;
import com.example.demo.models.TargetType;
import com.example.demo.repositories.AnswerRepository;

import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@ExtendWith(MockitoExtension.class)
class AnswerServiceTest {

    @Mock
    private AnswerRepository answerRepository;
    @Mock
    private TargetValidator targetValidator;

    @InjectMocks
    private AnswerService answerService;

    private final AnswerRequestDTO request = new AnswerRequestDTO("A long enough answer", "q1");

    @Test
    void createAnswerSavesWhenQuestionExists() {
        when(targetValidator.ensureExists(TargetType.QUESTION, "q1")).thenReturn(Mono.empty());
        when(answerRepository.save(any(Answer.class))).thenAnswer(inv -> {
            Answer a = inv.getArgument(0);
            a.setId("a1");
            return Mono.just(a);
        });

        StepVerifier.create(answerService.createAnswer(request))
                .assertNext(dto -> {
                    assertEquals("a1", dto.getId());
                    assertEquals("q1", dto.getQuestionId());
                    assertEquals("A long enough answer", dto.getContent());
                })
                .verifyComplete();
    }

    @Test
    void createAnswerDoesNotSaveWhenQuestionMissing() {
        when(targetValidator.ensureExists(TargetType.QUESTION, "q1"))
                .thenReturn(Mono.error(new ResponseStatusException(HttpStatus.NOT_FOUND)));

        StepVerifier.create(answerService.createAnswer(request))
                .expectError(ResponseStatusException.class)
                .verify();
        verify(answerRepository, never()).save(any());
    }

    @Test
    void getAnswerByIdFailsWhenMissing() {
        when(answerRepository.findById("x")).thenReturn(Mono.empty());

        StepVerifier.create(answerService.getAnswerById("x")).expectError(RuntimeException.class).verify();
    }

    @Test
    void updateAnswerReplacesContent() {
        Answer existing = Answer.builder().id("a1").content("old content here").questionId("q1").build();
        when(answerRepository.findById("a1")).thenReturn(Mono.just(existing));
        when(answerRepository.save(existing)).thenReturn(Mono.just(existing));

        StepVerifier.create(answerService.updateAnswer("a1", request))
                .assertNext(dto -> assertEquals("A long enough answer", dto.getContent()))
                .verifyComplete();
    }

    @Test
    void deleteAnswerFailsWhenMissing() {
        when(answerRepository.findById("x")).thenReturn(Mono.empty());

        StepVerifier.create(answerService.deleteAnswer("x")).expectError(RuntimeException.class).verify();
        verify(answerRepository, never()).deleteById(any(String.class));
    }

    @Test
    void getAnswersByQuestionIdMapsEveryAnswer() {
        when(answerRepository.findByQuestionId("q1")).thenReturn(Flux.just(
                Answer.builder().id("a1").questionId("q1").content("one").build(),
                Answer.builder().id("a2").questionId("q1").content("two").build()));

        StepVerifier.create(answerService.getAnswersByQuestionId("q1"))
                .expectNextCount(2)
                .verifyComplete();
    }

    @Test
    void countDelegatesToRepository() {
        when(answerRepository.countByQuestionId("q1")).thenReturn(Mono.just(3L));

        StepVerifier.create(answerService.getAnswerCountByQuestionId("q1")).expectNext(3L).verifyComplete();
    }
}
