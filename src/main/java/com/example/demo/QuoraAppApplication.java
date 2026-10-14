package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.mongodb.config.EnableReactiveMongoAuditing;

@SpringBootApplication
@EnableReactiveMongoAuditing
public class QuoraAppApplication {

	public static void main(String[] args) {
		SpringApplication.run(QuoraAppApplication.class, args);
	}

}
