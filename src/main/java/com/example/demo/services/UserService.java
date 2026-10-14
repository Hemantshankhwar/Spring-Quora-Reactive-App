package com.example.demo.services;

import java.time.LocalDateTime;

import org.springframework.dao.DuplicateKeyException;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import com.example.demo.dto.UserRequestDTO;
import com.example.demo.dto.UserResponseDTO;
import com.example.demo.models.User;
import com.example.demo.repositories.UserRepository;

import lombok.RequiredArgsConstructor;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Service
@RequiredArgsConstructor
public class UserService implements IUserService {

    private final UserRepository userRepository;

    @Override
    public Mono<UserResponseDTO> createUser(UserRequestDTO userRequestDTO) {
        String username = userRequestDTO.getUsername().trim();
        String email = userRequestDTO.getEmail().trim().toLowerCase();

        User user = User.builder()
                .username(username)
                .email(email)
                .displayName(userRequestDTO.getDisplayName())
                .createdAt(LocalDateTime.now())
                .build();

        return userRepository.existsByUsername(username)
                .flatMap(exists -> exists
                        ? Mono.<Boolean>error(conflict("Username already taken: " + username))
                        : userRepository.existsByEmail(email))
                .flatMap(exists -> exists
                        ? Mono.<User>error(conflict("Email already registered: " + email))
                        : userRepository.save(user))
                // the unique constraints are the real guard against concurrent signups
                .onErrorMap(DuplicateKeyException.class, e -> conflict("Username or email already in use"))
                .map(this::mapToResponseDTO);
    }

    @Override
    public Mono<UserResponseDTO> getUserById(Long id) {
        return userRepository.findById(id)
                .map(this::mapToResponseDTO)
                .switchIfEmpty(Mono.error(
                        new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found with id: " + id)));
    }

    @Override
    public Flux<UserResponseDTO> getAllUsers() {
        return userRepository.findAll().map(this::mapToResponseDTO);
    }

    private ResponseStatusException conflict(String message) {
        return new ResponseStatusException(HttpStatus.CONFLICT, message);
    }

    private UserResponseDTO mapToResponseDTO(User user) {
        return UserResponseDTO.builder()
                .id(user.getId())
                .username(user.getUsername())
                .email(user.getEmail())
                .displayName(user.getDisplayName())
                .createdAt(user.getCreatedAt())
                .build();
    }
}
