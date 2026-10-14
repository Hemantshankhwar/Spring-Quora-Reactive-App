package com.example.demo.models;

import java.time.LocalDateTime;

import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "likes")
@CompoundIndex(def = "{'targetId': 1, 'targetType': 1}")
public class Like {

    @Id
    private String id;

    private String targetId;

    private TargetType targetType;

    private Boolean liked;

    @CreatedDate
    private LocalDateTime createdAt;

}

// web

// mobile 