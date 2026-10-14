package com.example.demo.dto;

import com.example.demo.models.TargetType;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LikeCountResponseDTO {

    private String targetId;

    private TargetType targetType;

    private Long likes;

    private Long dislikes;
}
