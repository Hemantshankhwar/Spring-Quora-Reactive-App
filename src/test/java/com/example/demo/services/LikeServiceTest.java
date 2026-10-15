package com.example.demo.services;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
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

import com.example.demo.dto.LikeRequestDTO;
import com.example.demo.models.Like;
import com.example.demo.models.TargetType;
import com.example.demo.repositories.LikeRepository;

import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@ExtendWith(MockitoExtension.class)
class LikeServiceTest {

    @Mock
    private LikeRepository likeRepository;
    @Mock
    private TargetValidator targetValidator;

    @InjectMocks
    private LikeService likeService;

    @Test
    void createLikeSavesWhenTargetExists() {
        LikeRequestDTO request = new LikeRequestDTO();
        request.setTargetId("a1");
        request.setTargetType(TargetType.ANSWER);
        request.setIsLike(true);
        when(targetValidator.ensureExists(TargetType.ANSWER, "a1")).thenReturn(Mono.empty());
        when(likeRepository.save(any(Like.class))).thenAnswer(inv -> {
            Like l = inv.getArgument(0);
            l.setId("l1");
            return Mono.just(l);
        });

        StepVerifier.create(likeService.createLike(request))
                .assertNext(dto -> {
                    assertEquals("l1", dto.getId());
                    assertTrue(dto.getIsLike());
                    assertEquals(TargetType.ANSWER, dto.getTargetType());
                })
                .verifyComplete();
    }

    @Test
    void createLikeFailsWhenTargetMissing() {
        LikeRequestDTO request = new LikeRequestDTO();
        request.setTargetId("q9");
        request.setTargetType(TargetType.QUESTION);
        request.setIsLike(false);
        when(targetValidator.ensureExists(TargetType.QUESTION, "q9"))
                .thenReturn(Mono.error(new ResponseStatusException(HttpStatus.NOT_FOUND)));

        StepVerifier.create(likeService.createLike(request)).expectError(ResponseStatusException.class).verify();
        verify(likeRepository, never()).save(any());
    }

    @Test
    void countReturnsLikesAndDislikesSeparately() {
        when(targetValidator.ensureExists(TargetType.COMMENT, "c1")).thenReturn(Mono.empty());
        when(likeRepository.countByTargetIdAndTargetTypeAndLiked("c1", TargetType.COMMENT, true))
                .thenReturn(Mono.just(7L));
        when(likeRepository.countByTargetIdAndTargetTypeAndLiked("c1", TargetType.COMMENT, false))
                .thenReturn(Mono.just(2L));

        StepVerifier.create(likeService.countLikesByTarget("c1", TargetType.COMMENT))
                .assertNext(dto -> {
                    assertEquals(7L, dto.getLikes());
                    assertEquals(2L, dto.getDislikes());
                })
                .verifyComplete();
    }

    @Test
    void deleteLikeReturns404WhenMissing() {
        when(likeRepository.findById("x")).thenReturn(Mono.empty());

        StepVerifier.create(likeService.deleteLike("x"))
                .expectErrorSatisfies(e -> assertEquals(HttpStatus.NOT_FOUND,
                        ((ResponseStatusException) e).getStatusCode()))
                .verify();
    }
}
