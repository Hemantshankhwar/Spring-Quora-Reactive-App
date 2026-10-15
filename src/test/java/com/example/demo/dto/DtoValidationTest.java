package com.example.demo.dto;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

import jakarta.validation.Validation;
import jakarta.validation.Validator;

class DtoValidationTest {

    private final Validator validator = Validation.buildDefaultValidatorFactory().getValidator();

    @Test
    void validAnswerPasses() {
        assertTrue(validator.validate(new AnswerRequestDTO("Long enough answer", "q1")).isEmpty());
    }

    @Test
    void answerTooShortOrWithoutQuestionFails() {
        assertEquals(1, validator.validate(new AnswerRequestDTO("short", "q1")).size());
        assertEquals(1, validator.validate(new AnswerRequestDTO("Long enough answer", " ")).size());
    }

    @Test
    void answerLongerThan1000CharsFails() {
        assertEquals(1, validator.validate(new AnswerRequestDTO("x".repeat(1001), "q1")).size());
    }

    @Test
    void tagNameLimits() {
        assertTrue(validator.validate(new TagRequestDTO("java")).isEmpty());
        assertFalse(validator.validate(new TagRequestDTO("")).isEmpty());
        assertEquals(1, validator.validate(new TagRequestDTO("t".repeat(31))).size());
    }
}
