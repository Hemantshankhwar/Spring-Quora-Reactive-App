package com.example.demo.dto;

import java.time.LocalDateTime;
import java.util.List;

import lombok.*;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class QuestionResponseDTO {

    private String id;

    private String title;

    private String content;

    private List<String> tags;

    private Integer views;

    private LocalDateTime createdAt;    
}
