package com.example.demo.services;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ResponseStatusException;

import com.example.demo.models.TargetType;
import com.example.demo.repositories.AnswerRepository;
import com.example.demo.repositories.CommentRepository;
import com.example.demo.repositories.QuestionRepository;

import lombok.RequiredArgsConstructor;
import reactor.core.publisher.Mono;

@Component
@RequiredArgsConstructor
public class TargetValidator {

    private final QuestionRepository questionRepository;

    private final AnswerRepository answerRepository;

    private final CommentRepository commentRepository;

    public Mono<Void> ensureExists(TargetType targetType, String targetId) {
        Mono<Boolean> exists = switch (targetType) {
            case QUESTION -> questionRepository.existsById(targetId);
            case ANSWER -> answerRepository.existsById(targetId);
            case COMMENT -> commentRepository.existsById(targetId);
        };

        return exists
                .filter(Boolean::booleanValue)
                .switchIfEmpty(Mono.error(new ResponseStatusException(
                        HttpStatus.NOT_FOUND, targetType + " not found with id: " + targetId)))
                .then();
    }
}
