package com.example.demo.repositories;

import java.util.List;

import org.springframework.data.domain.Pageable;
import org.springframework.data.elasticsearch.annotations.Query;
import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;

import com.example.demo.models.QuestionElasticDocument;

public interface QuestionDocumentRepository extends ElasticsearchRepository<QuestionElasticDocument, String> {
    
    // title matches count double; fuzziness tolerates typos and simple plurals
    @Query("""
        {"multi_match": {"query": "?0", "fields": ["title^2", "content"], "fuzziness": "AUTO"}}
        """)
    List<QuestionElasticDocument> search(String text, Pageable pageable);
}
