package com.example.demo.dto;

import com.example.demo.models.TargetType;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LikeRequestDTO {
    
    @NotBlank(message = "Target ID is required")
    private String targetId;

    @NotNull(message = "Target Type is required")
    private TargetType targetType;

    @NotNull(message = "Is Like is required")
    private Boolean isLike;
}
