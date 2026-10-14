package com.example.demo.controllers;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import com.example.demo.dto.TagRequestDTO;
import com.example.demo.dto.TagResponseDTO;
import com.example.demo.services.ITagService;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/api/tags")
@RequiredArgsConstructor
public class TagController {

    private final ITagService tagService;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<TagResponseDTO> createTag(@Valid @RequestBody TagRequestDTO tagRequestDTO) {
        return tagService.createTag(tagRequestDTO);
    }

    @GetMapping
    public Flux<TagResponseDTO> getAllTags() {
        return tagService.getAllTags();
    }

    @GetMapping("/{id}")
    public Mono<TagResponseDTO> getTagById(@PathVariable String id) {
        return tagService.getTagById(id);
    }
}
