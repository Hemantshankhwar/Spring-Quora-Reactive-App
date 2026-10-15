package com.example.demo.services;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.verify;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import com.example.demo.models.Question;
import com.example.demo.models.QuestionElasticDocument;
import com.example.demo.repositories.QuestionDocumentRepository;

@ExtendWith(MockitoExtension.class)
class QuestionIndexServiceTest {

    @Mock
    private QuestionDocumentRepository repository;

    @InjectMocks
    private QuestionIndexService indexService;

    @Test
    void indexesOnlyIdTitleAndContent() {
        Question question = Question.builder().id("q1").title("A searchable title").content("Body text here")
                .tags(java.util.List.of("java")).views(5).build();

        indexService.createQuestionIndex(question);

        ArgumentCaptor<QuestionElasticDocument> saved = ArgumentCaptor.forClass(QuestionElasticDocument.class);
        verify(repository).save(saved.capture());
        assertEquals("q1", saved.getValue().getId());
        assertEquals("A searchable title", saved.getValue().getTitle());
        assertEquals("Body text here", saved.getValue().getContent());
    }
}
