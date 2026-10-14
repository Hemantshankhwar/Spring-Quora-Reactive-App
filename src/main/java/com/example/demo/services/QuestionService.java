package com.example.demo.services;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.core.FindAndModifyOptions;
import org.springframework.data.mongodb.core.ReactiveMongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Service;

import com.example.demo.adapter.QuestionAdapter;
import com.example.demo.dto.QuestionRequestDTO;
import com.example.demo.dto.QuestionResponseDTO;
import com.example.demo.models.Question;
import com.example.demo.models.QuestionElasticDocument;
import com.example.demo.repositories.QuestionDocumentRepository;
import com.example.demo.repositories.QuestionRepository;
import com.example.demo.utils.CursorUtils;
import com.example.demo.utils.TagUtils;

import lombok.RequiredArgsConstructor;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Service
@RequiredArgsConstructor
public class QuestionService implements IQuestionService {

    private final QuestionRepository questionRepository;

    private final ReactiveMongoTemplate mongoTemplate;

    private final IQuestionIndexService questionIndexService;

    private final QuestionDocumentRepository questionDocumentRepository;

    private final ITagService tagService;
    
    @Override
    public Mono<QuestionResponseDTO> createQuestion(QuestionRequestDTO questionRequestDTO) {

        return tagService.ensureTags(questionRequestDTO.getTags())
        .flatMap(tagNames -> {
            Question question = Question.builder()
                .title(questionRequestDTO.getTitle())
                .content(questionRequestDTO.getContent())
                .tags(tagNames)
                .createdAt(LocalDateTime.now())
                .updatedAt(LocalDateTime.now())
                .build();
            return questionRepository.save(question);
        })
        .map(savedQuestion -> {
            questionIndexService.createQuestionIndex(savedQuestion); // dumping the question to elasticsearch
            return QuestionAdapter.toQuestionResponseDTO(savedQuestion);
        })
        .doOnSuccess(response -> System.out.println("Question created successfully: " + response))
        .doOnError(error -> System.out.println("Error creating question: " + error));
    }

    @Override
    public Flux<QuestionResponseDTO> searchQuestions(String searchTerm, int offset, int page) {
        return questionRepository.findByTitleOrContentContainingIgnoreCase(searchTerm, PageRequest.of(offset, page))
        .map(QuestionAdapter::toQuestionResponseDTO)
        .doOnError(error -> System.out.println("Error searching questions: " + error))
        .doOnComplete(() -> System.out.println("Questions searched successfully"));
    }

    @Override
    public Flux<QuestionResponseDTO> getAllQuestions(String cursor, int size) {
        Pageable pageable = PageRequest.of(0, size);

        if(!CursorUtils.isValidCursor(cursor)) {
            return questionRepository.findTop10ByOrderByCreatedAtAsc()
            .take(size)
            .map(QuestionAdapter::toQuestionResponseDTO)
            .doOnError(error -> System.out.println("Error fetching questions: " + error))
            .doOnComplete(() -> System.out.println("Questions fetched successfully"));
        } else {
            LocalDateTime cursorTimeStamp = CursorUtils.parseCursor(cursor);
            return questionRepository.findByCreatedAtGreaterThanOrderByCreatedAtAsc(cursorTimeStamp, pageable)
            .map(QuestionAdapter::toQuestionResponseDTO)
            .doOnError(error -> System.out.println("Error fetching questions: " + error))
            .doOnComplete(() -> System.out.println("Questions fetched successfully"));
        }

    }

    @Override
    public Mono<QuestionResponseDTO> getQuestionById(String id) {
        // $inc is atomic, so concurrent readers cannot lose a view
        return mongoTemplate.findAndModify(
            Query.query(Criteria.where("_id").is(id)),
            new Update().inc("views", 1),
            FindAndModifyOptions.options().returnNew(true),
            Question.class)
        .map(QuestionAdapter::toQuestionResponseDTO)
        .doOnError(error -> System.out.println("Error fetching question: " + error))
        .doOnSuccess(response -> System.out.println("Question fetched successfully: " + response));
    }

    @Override
    public Flux<QuestionResponseDTO> getQuestionsByTag(String tag, int page, int size) {
        return questionRepository.findByTags(TagUtils.normalize(tag), PageRequest.of(page, size))
        .map(QuestionAdapter::toQuestionResponseDTO);
    }

    public List<QuestionElasticDocument> searchQuestionsByElasticsearch(String query) {
        return questionDocumentRepository.search(query, PageRequest.of(0, 20));
    }
}
