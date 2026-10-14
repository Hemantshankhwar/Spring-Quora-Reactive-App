package com.example.demo.services;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import com.example.demo.dto.LikeCountResponseDTO;
import com.example.demo.dto.LikeRequestDTO;
import com.example.demo.dto.LikeResponseDTO;
import com.example.demo.models.Like;
import com.example.demo.models.TargetType;
import com.example.demo.repositories.LikeRepository;

import lombok.RequiredArgsConstructor;
import reactor.core.publisher.Mono;

@Service
@RequiredArgsConstructor
public class LikeService implements ILikeService {

    private final LikeRepository likeRepository;

    private final TargetValidator targetValidator;

    @Override
    public Mono<LikeResponseDTO> createLike(LikeRequestDTO likeRequestDTO) {
        Like like = Like.builder()
                .targetId(likeRequestDTO.getTargetId())
                .targetType(likeRequestDTO.getTargetType())
                .liked(likeRequestDTO.getIsLike())
                .build();

        return targetValidator.ensureExists(likeRequestDTO.getTargetType(), likeRequestDTO.getTargetId())
                .then(Mono.defer(() -> likeRepository.save(like)))
                .map(this::mapToResponseDTO);
    }

    @Override
    public Mono<LikeCountResponseDTO> countLikesByTarget(String targetId, TargetType targetType) {
        return targetValidator.ensureExists(targetType, targetId)
                .then(Mono.defer(() -> Mono.zip(
                        likeRepository.countByTargetIdAndTargetTypeAndLiked(targetId, targetType, true),
                        likeRepository.countByTargetIdAndTargetTypeAndLiked(targetId, targetType, false))))
                .map(counts -> LikeCountResponseDTO.builder()
                        .targetId(targetId)
                        .targetType(targetType)
                        .likes(counts.getT1())
                        .dislikes(counts.getT2())
                        .build());
    }

    @Override
    public Mono<Void> deleteLike(String id) {
        return likeRepository.findById(id)
                .switchIfEmpty(Mono.error(new ResponseStatusException(
                        HttpStatus.NOT_FOUND, "Like not found with id: " + id)))
                .flatMap(like -> likeRepository.deleteById(like.getId()));
    }

    private LikeResponseDTO mapToResponseDTO(Like like) {
        return LikeResponseDTO.builder()
                .id(like.getId())
                .targetId(like.getTargetId())
                .targetType(like.getTargetType())
                .isLike(like.getLiked())
                .createdAt(like.getCreatedAt())
                .build();
    }
}
