package com.example.demo.services;

import java.util.List;

import com.example.demo.dto.TagRequestDTO;
import com.example.demo.dto.TagResponseDTO;

import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

public interface ITagService {

    Mono<TagResponseDTO> createTag(TagRequestDTO tagRequestDTO);

    Mono<TagResponseDTO> getTagById(String id);

    Flux<TagResponseDTO> getAllTags();

    // Creates missing tags and returns the normalized, de-duplicated names
    Mono<List<String>> ensureTags(List<String> names);
}
