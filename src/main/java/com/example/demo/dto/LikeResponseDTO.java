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
public class LikeResponseDTO {
    
    private String id;

    private String targetId;

    private TargetType targetType;

    private Boolean isLike;

    private LocalDateTime createdAt;
}
