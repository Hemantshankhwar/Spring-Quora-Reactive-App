package com.example.demo.repositories;

import org.springframework.data.mongodb.repository.ReactiveMongoRepository;
import org.springframework.stereotype.Repository;

import com.example.demo.models.Comment;
import com.example.demo.models.TargetType;

import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface CommentRepository extends ReactiveMongoRepository<Comment, String> {

    Flux<Comment> findByTargetIdAndTargetTypeOrderByCreatedAtAsc(String targetId, TargetType targetType);

    Mono<Long> countByTargetIdAndTargetType(String targetId, TargetType targetType);
}
