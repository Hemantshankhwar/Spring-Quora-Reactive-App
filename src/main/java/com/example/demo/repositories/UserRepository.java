package com.example.demo.repositories;

import org.springframework.data.repository.reactive.ReactiveCrudRepository;

import com.example.demo.models.User;

import reactor.core.publisher.Mono;

public interface UserRepository extends ReactiveCrudRepository<User, Long> {

    Mono<Boolean> existsByUsername(String username);

    Mono<Boolean> existsByEmail(String email);
}
