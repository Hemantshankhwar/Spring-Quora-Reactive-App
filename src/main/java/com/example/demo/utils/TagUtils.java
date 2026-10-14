package com.example.demo.utils;

import java.util.Locale;

public final class TagUtils {

    private TagUtils() {
    }

    public static String normalize(String tag) {
        return tag.trim().toLowerCase(Locale.ROOT);
    }
}
