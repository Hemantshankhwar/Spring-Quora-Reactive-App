package com.example.demo.services;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import com.example.demo.dto.TagRequestDTO;
import com.example.demo.models.Tag;
import com.example.demo.repositories.TagRepository;

import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@ExtendWith(MockitoExtension.class)
class TagServiceTest {

    @Mock
    private TagRepository tagRepository;

    @InjectMocks
    private TagService tagService;

    @Test
    void createTagStoresTheLowercasedName() {
        when(tagRepository.findByName("kafka")).thenReturn(Mono.empty());
        when(tagRepository.save(any(Tag.class)))
                .thenAnswer(inv -> {
                    Tag t = inv.getArgument(0);
                    t.setId("t1");
                    return Mono.just(t);
                });

        StepVerifier.create(tagService.createTag(new TagRequestDTO("  Kafka ")))
                .assertNext(dto -> {
                    assertEquals("t1", dto.getId());
                    assertEquals("kafka", dto.getName());
                })
                .verifyComplete();
    }

    @Test
    void createTagRejectsDuplicateWith409() {
        when(tagRepository.findByName("java")).thenReturn(Mono.just(Tag.builder().id("t1").name("java").build()));

        StepVerifier.create(tagService.createTag(new TagRequestDTO("Java")))
                .expectErrorSatisfies(e -> assertEquals(HttpStatus.CONFLICT,
                        ((ResponseStatusException) e).getStatusCode()))
                .verify();
        verify(tagRepository, never()).save(any());
    }

    @Test
    void getTagByIdReturns404WhenMissing() {
        when(tagRepository.findById("x")).thenReturn(Mono.empty());

        StepVerifier.create(tagService.getTagById("x"))
                .expectErrorSatisfies(e -> assertEquals(HttpStatus.NOT_FOUND,
                        ((ResponseStatusException) e).getStatusCode()))
                .verify();
    }

    @Test
    void ensureTagsReturnsEmptyListForNullOrEmpty() {
        StepVerifier.create(tagService.ensureTags(null)).expectNext(List.of()).verifyComplete();
        StepVerifier.create(tagService.ensureTags(List.of())).expectNext(List.of()).verifyComplete();
    }

    @Test
    void ensureTagsNormalizesDedupesAndCreatesOnlyMissingTags() {
        when(tagRepository.findByName("java")).thenReturn(Mono.just(Tag.builder().name("java").build()));
        when(tagRepository.findByName("spring")).thenReturn(Mono.empty());
        when(tagRepository.save(any(Tag.class))).thenAnswer(inv -> Mono.just(inv.getArgument(0)));

        StepVerifier.create(tagService.ensureTags(List.of("Java", " java ", "SPRING", "  ")))
                .expectNext(List.of("java", "spring"))
                .verifyComplete();

        verify(tagRepository, times(1)).save(any(Tag.class));
    }

    @Test
    void ensureTagsRecoversFromConcurrentCreate() {
        Tag existing = Tag.builder().name("docker").build();
        when(tagRepository.findByName("docker")).thenReturn(Mono.empty(), Mono.just(existing));
        when(tagRepository.save(any(Tag.class))).thenReturn(Mono.error(new DuplicateKeyException("dup")));

        StepVerifier.create(tagService.ensureTags(List.of("docker")))
                .expectNext(List.of("docker"))
                .verifyComplete();
    }
}
