package com.example.demo.controllers;

import static org.mockito.Mockito.when;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.test.web.reactive.server.WebTestClient;
import org.springframework.web.server.ResponseStatusException;

import com.example.demo.dto.TagRequestDTO;
import com.example.demo.dto.TagResponseDTO;
import com.example.demo.services.ITagService;

import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@ExtendWith(MockitoExtension.class)
class TagControllerTest {

    @Mock
    private ITagService tagService;

    private WebTestClient client;

    @BeforeEach
    void setUp() {
        client = WebTestClient.bindToController(new TagController(tagService)).build();
    }

    @Test
    void postReturns201WithBody() {
        when(tagService.createTag(new TagRequestDTO("kafka")))
                .thenReturn(Mono.just(TagResponseDTO.builder().id("t1").name("kafka").build()));

        client.post().uri("/api/tags").bodyValue(new TagRequestDTO("kafka"))
                .exchange()
                .expectStatus().isCreated()
                .expectBody()
                .jsonPath("$.id").isEqualTo("t1")
                .jsonPath("$.name").isEqualTo("kafka");
    }

    @Test
    void getAllReturnsList() {
        when(tagService.getAllTags()).thenReturn(Flux.just(
                TagResponseDTO.builder().id("1").name("java").build(),
                TagResponseDTO.builder().id("2").name("sql").build()));

        client.get().uri("/api/tags")
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.length()").isEqualTo(2)
                .jsonPath("$[1].name").isEqualTo("sql");
    }

    @Test
    void unknownIdMapsTo404() {
        when(tagService.getTagById("x"))
                .thenReturn(Mono.error(new ResponseStatusException(HttpStatus.NOT_FOUND, "Tag not found")));

        client.get().uri("/api/tags/x").exchange().expectStatus().isNotFound();
    }

    @Test
    void blankNameIsRejectedBeforeReachingTheService() {
        client.post().uri("/api/tags").bodyValue(new TagRequestDTO(" "))
                .exchange()
                .expectStatus().isBadRequest();
    }
}
