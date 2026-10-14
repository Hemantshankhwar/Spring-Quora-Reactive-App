package com.example.demo.repositories;

import org.springframework.data.mongodb.repository.ReactiveMongoRepository;
import org.springframework.stereotype.Repository;

import com.example.demo.models.Like;
import com.example.demo.models.TargetType;

import reactor.core.publisher.Mono;

@Repository
public interface LikeRepository extends ReactiveMongoRepository<Like, String> {

    Mono<Long> countByTargetIdAndTargetTypeAndLiked(String targetId, TargetType targetType, Boolean liked);
}
