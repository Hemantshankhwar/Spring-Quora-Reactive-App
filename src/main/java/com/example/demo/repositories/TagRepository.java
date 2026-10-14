package com.example.demo.repositories;

import org.springframework.data.mongodb.repository.ReactiveMongoRepository;
import org.springframework.stereotype.Repository;

import com.example.demo.models.Tag;

import reactor.core.publisher.Mono;

@Repository
public interface TagRepository extends ReactiveMongoRepository<Tag, String> {

    Mono<Tag> findByName(String name);
}
