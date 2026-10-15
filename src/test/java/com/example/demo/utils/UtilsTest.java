package com.example.demo.utils;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.LocalDateTime;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.NullAndEmptySource;
import org.junit.jupiter.params.provider.ValueSource;

class UtilsTest {

    @Test
    void cursorAcceptsIsoDateTime() {
        assertTrue(CursorUtils.isValidCursor("2026-10-14T11:53:06.075"));
        assertEquals(LocalDateTime.of(2026, 10, 14, 11, 53, 6, 75_000_000),
                CursorUtils.parseCursor("2026-10-14T11:53:06.075"));
    }

    @ParameterizedTest
    @NullAndEmptySource
    @ValueSource(strings = { "yesterday", "2026-13-45T00:00:00", "12345" })
    void cursorRejectsBadValues(String cursor) {
        assertFalse(CursorUtils.isValidCursor(cursor));
    }

    @Test
    void parseCursorThrowsOnInvalidInput() {
        assertThrows(IllegalArgumentException.class, () -> CursorUtils.parseCursor("nope"));
    }

    @Test
    void tagsAreTrimmedAndLowercased() {
        assertEquals("spring boot", TagUtils.normalize("  Spring Boot "));
        assertEquals("java", TagUtils.normalize("JAVA"));
    }
}
