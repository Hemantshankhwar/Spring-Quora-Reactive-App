package com.example.demo.dto;

import java.util.List;

import jakarta.validation.constraints.*;
import lombok.*;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class QuestionRequestDTO {
    
    @NotBlank(message = "Title is required")
    @Size(min = 10, max = 100, message = "Title must be between 10 and 100 characters")
    private String title;

    @NotBlank(message = "Content is required")
    @Size(min = 10, max = 1000, message = "Content must be between 10 and 1000 characters")
    private String content;

    @Size(max = 5, message = "At most 5 tags are allowed")
    private List<@NotBlank(message = "Tag must not be blank") @Size(max = 30, message = "Tag must be at most 30 characters") String> tags;

}
