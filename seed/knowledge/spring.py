# Curated Spring knowledge used to generate seed questions and answers.

CONCEPTS = [
    ("dependency injection", "A pattern where Spring creates objects and supplies their dependencies instead of you calling new.", "Use constructor injection so dependencies are explicit and final.", "Field injection hides dependencies and makes unit testing harder.", ["dependency-injection"]),
    ("the @Autowired annotation", "An annotation that asks Spring to inject a matching bean.", "Prefer constructor injection, where @Autowired is optional with a single constructor.", "If several beans match the type, startup fails until you add @Primary or @Qualifier.", ["dependency-injection"]),
    ("stereotype annotations", "Annotations such as @Component, @Service and @Repository that register classes as Spring beans.", "Use @Service for business logic and @Repository for data access.", "Classes outside the scanned packages are never registered.", ["dependency-injection"]),
    ("bean scopes", "Settings that decide how many instances Spring creates: singleton by default, plus prototype, request and session.", "Keep beans stateless so singletons are safe.", "Injecting a prototype bean into a singleton gives you the same instance every time unless you use a provider.", ["dependency-injection"]),
    ("@Configuration and @Bean", "Java-based configuration that declares beans explicitly.", "Use it for third-party classes that you cannot annotate.", "Calling a @Bean method directly outside a configuration proxy creates a new instance each time.", ["dependency-injection"]),
    ("Spring Boot auto-configuration", "A mechanism that configures beans automatically based on the classpath and properties.", "Override it with your own beans or exclude specific auto-configurations.", "Run with the debug flag to see which auto-configurations were applied and why.", ["spring-boot"]),
    ("application.yml and profiles", "Externalized configuration with environment-specific profiles such as dev and prod.", "Keep secrets in environment variables and switch settings per profile.", "Committing secrets in application.yml leaks them.", ["spring-boot", "configuration"]),
    ("@RestController", "An annotation that combines @Controller and @ResponseBody so return values are written as JSON.", "Use it for REST APIs.", "Returning entities directly can leak internal fields, so return DTOs.", ["rest"]),
    ("@RequestBody and @PathVariable", "Annotations that bind JSON bodies and URL segments to method parameters.", "Add @Valid to trigger bean validation.", "Missing or malformed bodies produce 400 errors, so handle them in an exception handler.", ["rest"]),
    ("@ControllerAdvice", "A component for global exception handling shared across controllers.", "Use it with @ExceptionHandler to return consistent error responses.", "Without it, internal exception details can leak to clients.", ["rest"]),
    ("bean validation", "Annotations such as @NotBlank and @Size that validate input.", "Put them on DTOs and trigger them with @Valid.", "Validation on a nested object needs @Valid on the field as well.", ["rest", "validation"]),
    ("Spring Data JPA", "A repository abstraction that generates queries from method names.", "Use it to avoid boilerplate DAO code.", "Long derived method names get unreadable, so switch to @Query.", ["jpa", "spring-data"]),
    ("@Transactional", "An annotation that runs a method inside a database transaction.", "Put it on service methods rather than controllers.", "Self-invocation within the same class bypasses the proxy, and by default it only rolls back on unchecked exceptions.", ["transactions", "jpa"]),
    ("lazy and eager loading", "Lazy loading fetches associations on first access, while eager loading fetches them immediately.", "Prefer lazy and fetch what you need with JOIN FETCH or entity graphs.", "Touching a lazy association after the session closes throws LazyInitializationException.", ["jpa", "hibernate"]),
    ("the N+1 problem in JPA", "A pattern where one query loads a list and one extra query runs per element for its association.", "Use JOIN FETCH, @EntityGraph or batch fetching to fix it.", "Enable SQL logging to spot it, because it hides well in small test data.", ["jpa", "hibernate"]),
    ("JPA entity relationships", "Mappings such as @OneToMany and @ManyToOne that connect entities.", "Keep the owning side in sync and use mappedBy on the inverse side.", "Bidirectional relationships can cause infinite recursion during JSON serialization.", ["jpa", "hibernate"]),
    ("Spring Security", "A framework for authentication and authorization.", "Use it to protect endpoints with roles and JWT or session login.", "Disabling CSRF is only safe for stateless APIs that do not rely on cookies.", ["spring-security"]),
    ("JWT authentication", "Signed tokens that carry claims so the server can stay stateless.", "Send them in the Authorization header and verify the signature on each request.", "Tokens cannot be revoked easily, so keep them short-lived and use refresh tokens.", ["spring-security"]),
    ("password hashing with BCrypt", "A slow, salted hashing algorithm designed for passwords.", "Use BCryptPasswordEncoder and never store plain text.", "Fast hashes like MD5 or plain SHA-256 are unsuitable for passwords.", ["spring-security"]),
    ("Spring WebFlux", "A reactive web stack built on Project Reactor with non-blocking I/O.", "Use it for high-concurrency, I/O-bound services.", "Blocking calls such as JDBC or Thread.sleep inside a handler stall the event loop.", ["webflux", "reactive"]),
    ("Mono and Flux", "Reactor publishers for zero or one element (Mono) and zero to many elements (Flux).", "Return them from controllers and compose with map and flatMap.", "Nothing happens until something subscribes, and calling block() inside a reactive chain defeats the purpose.", ["webflux", "reactive"]),
    ("WebClient", "The non-blocking HTTP client in Spring.", "Use it instead of RestTemplate in reactive applications.", "Always set timeouts and handle errors with onStatus or onErrorResume.", ["webflux", "rest"]),
    ("RestTemplate", "The classic synchronous HTTP client.", "It is fine for simple blocking applications.", "It is in maintenance mode, so prefer RestClient or WebClient for new code.", ["rest"]),
    ("Spring Boot Actuator", "Production-ready endpoints for health, metrics and info.", "Expose health and metrics for monitoring and Kubernetes probes.", "Exposing all endpoints publicly leaks sensitive details.", ["spring-boot", "monitoring"]),
    ("Spring AOP", "Aspect-oriented programming for cross-cutting concerns such as logging and transactions.", "Use @Aspect with pointcuts for logging and timing.", "AOP works through proxies, so internal calls and private methods are not intercepted.", ["aop"]),
    ("@Scheduled tasks", "An annotation that runs methods on a fixed rate, fixed delay or cron schedule.", "Enable it with @EnableScheduling.", "With several instances the job runs on every node unless you add a distributed lock.", ["scheduling"]),
    ("@Async methods", "An annotation that runs a method on a separate thread pool.", "Use it for fire-and-forget work, together with @EnableAsync.", "Calling it from within the same class bypasses the proxy and runs synchronously.", ["async"]),
    ("Spring Cache", "Annotations such as @Cacheable that cache method results.", "Use it for expensive, read-mostly calls.", "Without eviction or a TTL you serve stale data.", ["caching"]),
    ("Spring Boot test slices", "Annotations like @WebMvcTest and @DataJpaTest that load only part of the context, unlike the full @SpringBootTest.", "Prefer slice tests and mocks for speed.", "Overusing @SpringBootTest makes the test suite slow.", ["testing"]),
    ("@MockBean", "An annotation that replaces a bean with a Mockito mock in the test context.", "Use it to isolate the class under test.", "Each different set of mock beans creates a new application context and slows the suite.", ["testing"]),
    ("Testcontainers", "A library that runs real databases and brokers in Docker during tests.", "Use it for integration tests that match production.", "Tests need Docker available and are slower than mocks.", ["testing"]),
    ("Spring Kafka", "Integration for producing and consuming Kafka messages with KafkaTemplate and @KafkaListener.", "Use it for event-driven communication between services.", "Deserialization errors can block a partition unless you configure an error handler.", ["kafka"]),
    ("Spring Data MongoDB", "Repository support for MongoDB documents.", "Use it for flexible, document-shaped data.", "There are no joins or multi-document constraints by default, so model the data around your queries.", ["mongodb", "spring-data"]),
    ("reactive repositories", "Repositories that return Mono and Flux.", "Use them with WebFlux together with R2DBC or reactive MongoDB.", "Mixing a blocking JDBC repository into a reactive chain blocks the event loop.", ["webflux", "reactive"]),
    ("R2DBC", "A reactive driver API for relational databases.", "Use it with WebFlux to stay non-blocking end to end.", "It has no lazy loading or relationship mapping like JPA, so joins are manual.", ["reactive", "postgresql"]),
    ("CORS configuration", "A browser rule that restricts cross-origin requests.", "Configure allowed origins with @CrossOrigin or a CorsConfigurationSource.", "Allowing all origins together with credentials is unsafe.", ["rest", "spring-security"]),
    ("circular dependencies", "Beans that depend on each other in a cycle.", "Refactor to break the cycle, for example with an event or a third bean.", "Using @Lazy hides the design problem rather than fixing it.", ["dependency-injection"]),
    ("@ConfigurationProperties", "An annotation that binds groups of properties into a typed class.", "Prefer it over many @Value fields for related settings.", "Missing required properties fail at startup unless you give defaults.", ["configuration"]),
    ("pagination with Spring Data", "Pageable and Page support for paging and sorting.", "Return Page or Slice from repositories.", "Large page numbers with OFFSET get slower, and unsorted pages may repeat rows.", ["spring-data"]),
    ("optimistic locking with @Version", "A version column that detects concurrent updates.", "Use it for entities that are rarely edited concurrently.", "Callers must handle OptimisticLockingFailureException and retry.", ["jpa", "transactions"]),
    ("SLF4J logging", "A logging facade, usually backed by Logback.", "Use parameterized messages and set log levels per package.", "Logging sensitive data such as passwords is a security issue.", ["logging"]),
]

PAIRS = [
    ("@Component", "@Bean", "@Component marks a class for component scanning.", "@Bean declares a bean from a method inside a configuration class.", "Use @Component for your own classes and @Bean for third-party types.", ["dependency-injection"]),
    ("@Controller", "@RestController", "@Controller returns view names by default.", "@RestController writes return values straight to the response body.", "Use @RestController for JSON APIs and @Controller for server-rendered pages.", ["rest"]),
    ("constructor injection", "field injection", "Constructor injection makes dependencies explicit, final and easy to test.", "Field injection is shorter but hides dependencies and needs reflection in tests.", "Prefer constructor injection almost always.", ["dependency-injection"]),
    ("@Qualifier", "@Primary", "@Qualifier selects a specific bean by name at the injection point.", "@Primary marks one bean as the default choice among several.", "Use @Primary for the common case and @Qualifier for the exceptions.", ["dependency-injection"]),
    ("JPA", "JdbcTemplate", "JPA maps objects to tables and generates SQL for you.", "JdbcTemplate runs hand-written SQL with less magic.", "Use JPA for CRUD-heavy domains and JdbcTemplate for reporting or bulk SQL.", ["jpa", "spring-data"]),
    ("Spring MVC", "WebFlux", "Spring MVC uses a thread per request and blocking I/O.", "WebFlux uses an event loop and non-blocking I/O.", "Use MVC for typical CRUD apps and WebFlux when you need high concurrency with non-blocking libraries.", ["webflux"]),
    ("RestTemplate", "WebClient", "RestTemplate is synchronous and in maintenance mode.", "WebClient is non-blocking and supports streaming.", "Use WebClient or RestClient in new code.", ["rest"]),
    ("@MockBean", "@Mock", "@MockBean puts a Mockito mock into the Spring context.", "@Mock creates a plain Mockito mock outside Spring.", "Use @Mock in unit tests and @MockBean only when the Spring context is needed.", ["testing"]),
    ("CrudRepository", "JpaRepository", "CrudRepository offers basic create, read, update and delete methods.", "JpaRepository adds paging, sorting and JPA-specific operations such as flush.", "Use JpaRepository when you need paging or batch operations.", ["spring-data"]),
    ("session authentication", "JWT authentication", "Sessions keep state on the server and rely on a cookie.", "JWTs are self-contained tokens that the client sends with every request.", "Use sessions for server-rendered apps and JWTs for stateless APIs.", ["spring-security"]),
    ("@RequestParam", "@PathVariable", "@RequestParam reads query string values.", "@PathVariable reads values from the URL path.", "Use path variables for identifiers and request parameters for filters.", ["rest"]),
    ("Hibernate", "JPA", "JPA is a specification.", "Hibernate is the most common implementation of that specification.", "Code against JPA and let Hibernate do the work, using its extras only when needed.", ["jpa", "hibernate"]),
    ("Spring", "Spring Boot", "Spring is the core framework for dependency injection and the rest of the ecosystem.", "Spring Boot adds auto-configuration, starters and an embedded server on top of it.", "Use Spring Boot unless you have a reason to configure everything by hand.", ["spring-boot"]),
    ("map", "flatMap in Reactor", "map transforms each element synchronously into another value.", "flatMap transforms each element into a publisher and merges the results.", "Use flatMap whenever the transformation itself is asynchronous.", ["webflux", "reactive"]),
    ("@Transactional(readOnly = true)", "a default @Transactional", "A read-only transaction lets the framework and database skip some work such as dirty checking.", "A default transaction allows writes and flushes changes.", "Use readOnly for query methods.", ["transactions"]),
    ("eager fetching", "lazy fetching", "Eager fetching loads associations immediately with the parent.", "Lazy fetching loads them only when accessed.", "Default to lazy and fetch specific graphs when a use case needs them.", ["jpa"]),
]

HOWTOS = [
    ("return a custom error response for validation failures", "Add a @RestControllerAdvice with an @ExceptionHandler for MethodArgumentNotValidException.", '''@RestControllerAdvice
public class ApiErrors {
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<String> onInvalid(MethodArgumentNotValidException e) {
        return ResponseEntity.badRequest().body("Validation failed");
    }
}''', ["rest", "validation"]),
    ("read a value from application.yml", "Use @Value for a single property or @ConfigurationProperties for groups.", '''@Value("${app.name}")
private String name;''', ["configuration"]),
    ("enable CORS for a React frontend", "Register a CORS mapping that allows your frontend origin.", '''@Bean
WebMvcConfigurer cors() {
    return registry -> registry.addMapping("/api/**")
        .allowedOrigins("http://localhost:3000");
}''', ["rest"]),
    ("connect Spring Boot to PostgreSQL", "Add the PostgreSQL driver and set the datasource properties.", '''spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/app
    username: app
    password: secret''', ["postgresql", "spring-data"]),
    ("write a custom query in Spring Data JPA", "Annotate a repository method with @Query and bind parameters by name.", '''@Query("select u from User u where u.email = :email")
Optional<User> findByEmailAddress(@Param("email") String email);''', ["jpa", "spring-data"]),
    ("paginate a repository result", "Pass a PageRequest to the repository and return a Page.", '''Page<Order> page = orderRepository.findAll(
    PageRequest.of(0, 20, Sort.by("createdAt").descending()));''', ["spring-data"]),
    ("secure an endpoint with JWT", "Add a filter that validates the token and sets the security context before the authentication filter.", '''http.addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class);''', ["spring-security"]),
    ("run a task every night at midnight", "Annotate a method with @Scheduled and a cron expression, and enable scheduling.", '''@Scheduled(cron = "0 0 0 * * *")
public void nightlyCleanup() {
    // cleanup work
}''', ["scheduling"]),
    ("call another service with WebClient", "Build a WebClient, call retrieve and convert the body to a Mono.", '''webClient.get()
    .uri("/users/{id}", id)
    .retrieve()
    .bodyToMono(User.class);''', ["webflux", "rest"]),
    ("write a unit test for a service with Mockito", "Use MockitoExtension, mock the repository and inject it into the service under test.", '''@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
    @Mock OrderRepository repo;
    @InjectMocks OrderService service;
}''', ["testing"]),
    ("log all incoming requests", "Add a OncePerRequestFilter that logs the method and URI, then continues the chain.", '''@Component
public class RequestLogFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res, FilterChain chain)
            throws ServletException, IOException {
        log.info("{} {}", req.getMethod(), req.getRequestURI());
        chain.doFilter(req, res);
    }
}''', ["logging"]),
    ("handle file uploads", "Accept a MultipartFile with @RequestParam and configure the size limits.", '''@PostMapping("/upload")
public String upload(@RequestParam("file") MultipartFile file) {
    return file.getOriginalFilename();
}''', ["rest"]),
    ("configure different settings per environment", "Create application-dev.yml and application-prod.yml and activate one with the profiles property.", '''java -jar app.jar --spring.profiles.active=prod''', ["configuration"]),
    ("return 404 when an entity is not found", "Throw a ResponseStatusException with NOT_FOUND.", '''throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Order not found");''', ["rest"]),
    ("send a Kafka message from a service", "Inject KafkaTemplate and call send with a topic, key and payload.", '''kafkaTemplate.send("orders", order.getId(), order);''', ["kafka"]),
    ("add Swagger or OpenAPI docs", "Add the springdoc starter and open the generated UI.", '''implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.6.0\'''', ["rest"]),
    ("dockerize a Spring Boot application", "Build the jar, then copy it into a slim JRE image.", '''FROM eclipse-temurin:21-jre
COPY build/libs/app.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]''', ["docker", "spring-boot"]),
    ("retry a failed call automatically", "Add spring-retry and annotate the method with @Retryable.", '''@Retryable(maxAttempts = 3)
public String callRemote() {
    return client.fetch();
}''', ["resilience"]),
    ("set the database connection pool size", "Set the Hikari maximum pool size in the properties.", '''spring.datasource.hikari.maximum-pool-size=10''', ["configuration", "spring-data"]),
    ("return a 201 status from a controller", "Annotate the handler with @ResponseStatus or return a ResponseEntity.", '''@PostMapping
@ResponseStatus(HttpStatus.CREATED)
public Order create(@Valid @RequestBody OrderRequest request) {
    return service.create(request);
}''', ["rest"]),
]

ERRORS = [
    ("NoSuchBeanDefinitionException", "Spring not finding a bean of the requested type, usually because the class is not annotated or sits outside the scanned packages", "add the stereotype annotation or fix the component scan", ["dependency-injection"]),
    ("circular dependency between beans", "two beans that need each other during construction", "break the cycle by extracting a third bean or using events", ["dependency-injection"]),
    ("LazyInitializationException: could not initialize proxy", "accessing a lazy association after the Hibernate session is closed", "fetch the data inside the transaction with JOIN FETCH or map to a DTO before returning", ["jpa", "hibernate"]),
    ("Whitelabel Error Page", "no handler mapped for the URL or an unhandled exception", "check the request mapping and read the server log for the real cause", ["spring-boot"]),
    ("Web server failed to start. Port 8080 was already in use", "another process already listening on the same port", "stop that process or set server.port to a free port", ["spring-boot"]),
    ("HttpMessageNotReadableException: JSON parse error", "a request body that is malformed or does not match the target type", "validate the JSON and the DTO field types", ["rest"]),
    ("TransactionRequiredException: no EntityManager with actual transaction available", "running a modifying query outside a transaction", "add @Transactional on the service method", ["transactions", "jpa"]),
    ("Failed to configure a DataSource: 'url' attribute is not specified", "having a database driver on the classpath but no datasource properties", "set spring.datasource.url or exclude the datasource auto-configuration", ["spring-boot", "spring-data"]),
    ("415 Unsupported Media Type", "sending a request without the Content-Type: application/json header", "set the header on the client", ["rest"]),
    ("403 Forbidden after adding Spring Security", "CSRF protection or missing authorization rules blocking the request", "disable CSRF for stateless APIs or send the token, and define authorizeHttpRequests rules", ["spring-security"]),
    ("expected single matching bean but found 2", "two beans of the same type being eligible for injection", "mark one @Primary or select one with @Qualifier", ["dependency-injection"]),
    ("block()/blockFirst()/blockLast() are blocking, which is not supported in thread reactor-http-nio", "calling block inside a non-blocking reactor thread", "compose the calls with flatMap instead of blocking", ["webflux", "reactive"]),
]

TOPICS = [
    {
        "key": "spring",
        "name": "Spring Boot",
        "count": 2800,
        "tags": ["spring", "spring-boot"],
        "suffixes": ["", " in Spring Boot 3", " in a REST API", " in a microservice", " in production", " in tests"],
        "concepts": CONCEPTS,
        "pairs": PAIRS,
        "howtos": HOWTOS,
        "errors": ERRORS,
    }
]
