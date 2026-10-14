package com.example.demo.dto;

import com.example.demo.models.TargetType;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CommentRequestDTO {

    @NotBlank(message = "Content is required")
    @Size(max = 500, message = "Content must be at most 500 characters")
    private String content;

    @NotBlank(message = "Target ID is required")
    private String targetId;

    @NotNull(message = "Target Type is required")
    private TargetType targetType;
}
