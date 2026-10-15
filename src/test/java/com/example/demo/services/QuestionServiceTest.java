package com.example.demo.services;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.time.LocalDateTime;
import java.util.List;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.core.FindAndModifyOptions;
import org.springframework.data.mongodb.core.ReactiveMongoTemplate;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.UpdateDefinition;

import com.example.demo.dto.QuestionRequestDTO;
import com.example.demo.models.Question;
import com.example.demo.models.QuestionElasticDocument;
import com.example.demo.repositories.QuestionDocumentRepository;
import com.example.demo.repositories.QuestionRepository;

import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@ExtendWith(MockitoExtension.class)
class QuestionServiceTest {

    @Mock
    private QuestionRepository questionRepository;
    @Mock
    private ReactiveMongoTemplate mongoTemplate;
    @Mock
    private IQuestionIndexService questionIndexService;
    @Mock
    private QuestionDocumentRepository questionDocumentRepository;
    @Mock
    private ITagService tagService;

    @InjectMocks
    private QuestionService questionService;

    private Question question(String id, String title) {
        return Question.builder().id(id).title(title).content("some content here")
                .tags(List.of("java")).views(0).createdAt(LocalDateTime.now()).build();
    }

    @Test
    void createQuestionSavesWithNormalizedTagsAndIndexesIt() {
        QuestionRequestDTO request = new QuestionRequestDTO();
        request.setTitle("How does WebFlux work?");
        request.setContent("Explain the event loop");
        request.setTags(List.of("Java", "Spring"));
        when(tagService.ensureTags(request.getTags())).thenReturn(Mono.just(List.of("java", "spring")));
        when(questionRepository.save(any(Question.class))).thenAnswer(inv -> {
            Question q = inv.getArgument(0);
            q.setId("q1");
            return Mono.just(q);
        });

        StepVerifier.create(questionService.createQuestion(request))
                .assertNext(dto -> {
                    assertEquals("q1", dto.getId());
                    assertEquals(List.of("java", "spring"), dto.getTags());
                })
                .verifyComplete();

        ArgumentCaptor<Question> indexed = ArgumentCaptor.forClass(Question.class);
        verify(questionIndexService).createQuestionIndex(indexed.capture());
        assertEquals("q1", indexed.getValue().getId());
    }

    @Test
    void getQuestionByIdIncrementsViewsAtomically() {
        when(mongoTemplate.findAndModify(any(Query.class), any(UpdateDefinition.class),
                any(FindAndModifyOptions.class), eq(Question.class)))
                .thenReturn(Mono.just(question("q1", "A reasonably long title")));

        StepVerifier.create(questionService.getQuestionById("q1"))
                .assertNext(dto -> assertEquals("q1", dto.getId()))
                .verifyComplete();

        ArgumentCaptor<UpdateDefinition> update = ArgumentCaptor.forClass(UpdateDefinition.class);
        ArgumentCaptor<FindAndModifyOptions> options = ArgumentCaptor.forClass(FindAndModifyOptions.class);
        verify(mongoTemplate).findAndModify(any(Query.class), update.capture(), options.capture(),
                eq(Question.class));
        assertEquals(1, update.getValue().getUpdateObject().get("$inc", org.bson.Document.class).get("views"));
        assertEquals(true, options.getValue().isReturnNew());
    }

    @Test
    void getQuestionByIdCompletesEmptyForUnknownId() {
        when(mongoTemplate.findAndModify(any(Query.class), any(UpdateDefinition.class),
                any(FindAndModifyOptions.class), eq(Question.class)))
                .thenReturn(Mono.empty());

        StepVerifier.create(questionService.getQuestionById("missing")).verifyComplete();
    }

    @Test
    void feedWithoutCursorUsesFirstPageQueryAndHonoursSize() {
        when(questionRepository.findTop10ByOrderByCreatedAtAsc())
                .thenReturn(Flux.just(question("q1", "First question title"),
                        question("q2", "Second question title"), question("q3", "Third question title")));

        StepVerifier.create(questionService.getAllQuestions(null, 2)).expectNextCount(2).verifyComplete();
    }

    @Test
    void feedWithCursorPagesAfterThatTimestamp() {
        LocalDateTime cursor = LocalDateTime.of(2026, 1, 1, 10, 0);
        when(questionRepository.findByCreatedAtGreaterThanOrderByCreatedAtAsc(eq(cursor), any(Pageable.class)))
                .thenReturn(Flux.just(question("q9", "Later question title")));

        StepVerifier.create(questionService.getAllQuestions(cursor.toString(), 5))
                .assertNext(dto -> assertEquals("q9", dto.getId()))
                .verifyComplete();
    }

    @Test
    void tagLookupIsCaseInsensitive() {
        when(questionRepository.findByTags(eq("java"), any(Pageable.class)))
                .thenReturn(Flux.just(question("q1", "Tagged question title")));

        StepVerifier.create(questionService.getQuestionsByTag("  JAVA ", 0, 10))
                .expectNextCount(1)
                .verifyComplete();
    }

    @Test
    void elasticsearchSearchIsCappedAtTwentyHits() {
        List<QuestionElasticDocument> hits = List.of(
                QuestionElasticDocument.builder().id("q1").title("t").content("c").build());
        when(questionDocumentRepository.search("hashmap", PageRequest.of(0, 20))).thenReturn(hits);

        assertEquals(hits, questionService.searchQuestionsByElasticsearch("hashmap"));
    }
}
