package com.example.demo.dto;

import java.time.LocalDateTime;

import com.example.demo.models.TargetType;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CommentResponseDTO {

    private String id;

    private String content;

    private String targetId;

    private TargetType targetType;

    private LocalDateTime createdAt;

    private LocalDateTime updatedAt;
}
