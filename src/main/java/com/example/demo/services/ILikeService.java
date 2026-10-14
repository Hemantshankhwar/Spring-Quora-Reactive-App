package com.example.demo.services;

import com.example.demo.dto.LikeCountResponseDTO;
import com.example.demo.dto.LikeRequestDTO;
import com.example.demo.dto.LikeResponseDTO;
import com.example.demo.models.TargetType;

import reactor.core.publisher.Mono;

public interface ILikeService {

    Mono<LikeResponseDTO> createLike(LikeRequestDTO likeRequestDTO);

    Mono<LikeCountResponseDTO> countLikesByTarget(String targetId, TargetType targetType);

    Mono<Void> deleteLike(String id);
}
