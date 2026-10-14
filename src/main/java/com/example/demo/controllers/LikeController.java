package com.example.demo.controllers;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import com.example.demo.dto.LikeCountResponseDTO;
import com.example.demo.dto.LikeRequestDTO;
import com.example.demo.dto.LikeResponseDTO;
import com.example.demo.models.TargetType;
import com.example.demo.services.ILikeService;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/api/likes")
@RequiredArgsConstructor
public class LikeController {

    private final ILikeService likeService;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<LikeResponseDTO> createLike(@Valid @RequestBody LikeRequestDTO likeRequestDTO) {
        return likeService.createLike(likeRequestDTO);
    }

    @GetMapping("/count")
    public Mono<LikeCountResponseDTO> countLikes(@RequestParam String targetId,
            @RequestParam TargetType targetType) {
        return likeService.countLikesByTarget(targetId, targetType);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> deleteLike(@PathVariable String id) {
        return likeService.deleteLike(id);
    }
}
