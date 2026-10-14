package com.example.demo.services;

import java.util.List;

import org.springframework.dao.DuplicateKeyException;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import com.example.demo.dto.TagRequestDTO;
import com.example.demo.dto.TagResponseDTO;
import com.example.demo.models.Tag;
import com.example.demo.repositories.TagRepository;
import com.example.demo.utils.TagUtils;

import lombok.RequiredArgsConstructor;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Service
@RequiredArgsConstructor
public class TagService implements ITagService {

    private final TagRepository tagRepository;

    @Override
    public Mono<TagResponseDTO> createTag(TagRequestDTO tagRequestDTO) {
        String name = TagUtils.normalize(tagRequestDTO.getName());

        return tagRepository.findByName(name)
                .flatMap(existing -> Mono.<Tag>error(
                        new ResponseStatusException(HttpStatus.CONFLICT, "Tag already exists: " + name)))
                .switchIfEmpty(Mono.defer(() -> tagRepository.save(Tag.builder().name(name).build())))
                .map(this::mapToResponseDTO);
    }

    @Override
    public Mono<TagResponseDTO> getTagById(String id) {
        return tagRepository.findById(id)
                .map(this::mapToResponseDTO)
                .switchIfEmpty(Mono.error(
                        new ResponseStatusException(HttpStatus.NOT_FOUND, "Tag not found with id: " + id)));
    }

    @Override
    public Flux<TagResponseDTO> getAllTags() {
        return tagRepository.findAll().map(this::mapToResponseDTO);
    }

    @Override
    public Mono<List<String>> ensureTags(List<String> names) {
        if (names == null || names.isEmpty()) {
            return Mono.just(List.of());
        }

        return Flux.fromIterable(names)
                .map(TagUtils::normalize)
                .filter(name -> !name.isEmpty())
                .distinct()
                .concatMap(this::findOrCreate)
                .map(Tag::getName)
                .collectList();
    }

    private Mono<Tag> findOrCreate(String name) {
        return tagRepository.findByName(name)
                .switchIfEmpty(Mono.defer(() -> tagRepository.save(Tag.builder().name(name).build())
                        // a concurrent request may have created the same tag first
                        .onErrorResume(DuplicateKeyException.class, e -> tagRepository.findByName(name))));
    }

    private TagResponseDTO mapToResponseDTO(Tag tag) {
        return TagResponseDTO.builder()
                .id(tag.getId())
                .name(tag.getName())
                .createdAt(tag.getCreatedAt())
                .build();
    }
}
