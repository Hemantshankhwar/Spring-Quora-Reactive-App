# Curated knowledge for the infrastructure the project itself uses.

KAFKA = {
    "key": "kafka",
    "name": "Kafka",
    "count": 700,
    "tags": ["kafka"],
    "suffixes": ["", " in Spring Boot", " in production", " with Docker", " for microservices", " in a small team"],
    "concepts": [
        ("Kafka topics", "Named, append-only logs that producers write to and consumers read from.", "Use one topic per kind of event.", "Topic names are hard to change later, so agree on a naming convention early.", ["messaging"]),
        ("Kafka partitions", "Slices of a topic that allow parallel consumption and preserve order only within a partition.", "Choose the partition count based on the consumer parallelism you will need.", "You can add partitions later, but that changes which partition a key maps to.", ["messaging"]),
        ("consumer groups", "A set of consumers that share the partitions of a topic so each message is handled once per group.", "Run several consumers in the same group to scale reading.", "More consumers than partitions leaves some consumers idle.", ["messaging"]),
        ("Kafka offsets", "The position of a message within a partition, which consumers commit to remember progress.", "Commit offsets after processing so work is not lost.", "Committing before processing can lose messages and committing too late can reprocess them.", ["messaging"]),
        ("producer acks", "A setting that controls how many brokers must confirm a write.", "Use acks=all for data you cannot lose.", "acks=0 can silently lose messages.", ["reliability"]),
        ("idempotent producers", "Producers that avoid writing duplicates when they retry.", "Enable idempotence for safe retries.", "It only protects within a single producer session and partition.", ["reliability"]),
        ("Kafka replication", "Copies of each partition kept on several brokers.", "Use a replication factor of 3 in production.", "A single-broker development setup has no fault tolerance.", ["reliability"]),
        ("Kafka retention", "The policy that decides how long messages are kept, by time or size.", "Set it to cover the longest outage your consumers must survive.", "Consumers that fall behind the retention window lose data.", ["operations"]),
        ("consumer lag", "The difference between the latest offset and the consumer's committed offset.", "Monitor it to detect slow consumers.", "Growing lag usually means slow processing or too few consumers.", ["operations"]),
        ("consumer group rebalancing", "The redistribution of partitions among consumers when members join or leave.", "Keep processing time below max.poll.interval.ms to avoid unwanted rebalances.", "Frequent rebalances stall consumption.", ["operations"]),
        ("dead letter topics", "Topics that hold messages that could not be processed.", "Send poison messages there instead of blocking the partition.", "Without monitoring, a dead letter topic becomes a silent data graveyard.", ["reliability"]),
        ("Kafka in KRaft mode", "Kafka running without ZooKeeper, using its own Raft-based metadata quorum.", "Use KRaft for new clusters.", "Migration from ZooKeeper clusters needs planning.", ["operations"]),
    ],
    "pairs": [
        ("Kafka", "RabbitMQ", "Kafka is a distributed log that keeps messages for replay.", "RabbitMQ is a broker focused on routing and per-message acknowledgement.", "Use Kafka for event streaming and replay, and RabbitMQ for task queues with complex routing.", ["messaging"]),
        ("at-least-once", "at-most-once delivery", "At-least-once never loses messages but may deliver duplicates.", "At-most-once never duplicates but may lose messages.", "Pick at-least-once and make consumers idempotent.", ["reliability"]),
        ("topics", "partitions", "A topic is the logical stream of related events.", "A partition is one ordered slice of that topic.", "Order is guaranteed per partition, not per topic.", ["messaging"]),
        ("Kafka consumers", "Kafka Streams", "A plain consumer gives you full control over processing.", "Kafka Streams offers built-in joins, windows and state stores.", "Use Streams for stateful stream processing and plain consumers for simple handlers.", ["messaging"]),
    ],
    "howtos": [
        ("create a Kafka topic with 3 partitions", "Use the kafka-topics script with the create option.", '''kafka-topics.sh --bootstrap-server localhost:9092 \\
  --create --topic orders --partitions 3 --replication-factor 1''', ["operations"]),
        ("read a topic from the beginning", "Use the console consumer with the from-beginning flag.", '''kafka-console-consumer.sh --bootstrap-server localhost:9092 \\
  --topic orders --from-beginning''', ["operations"]),
        ("send keyed messages so related events stay in order", "Use the same key for related events, because the key decides the partition.", '''kafkaTemplate.send("orders", order.getId(), order);''', ["messaging"]),
        ("reset a consumer group to the earliest offset", "Stop the consumers and use the kafka-consumer-groups reset option.", '''kafka-consumer-groups.sh --bootstrap-server localhost:9092 \\
  --group view-count-consumer --topic orders \\
  --reset-offsets --to-earliest --execute''', ["operations"]),
        ("consume messages with Spring Kafka", "Annotate a method with @KafkaListener and set the group id.", '''@KafkaListener(topics = "orders", groupId = "billing")
public void handle(OrderEvent event) {
    // process the event
}''', ["spring-boot"]),
    ],
    "errors": [
        ("LEADER_NOT_AVAILABLE", "a topic that was just created or a broker that is still electing a leader", "retry after a moment or create the topic before producing", ["operations"]),
        ("Topic not present in metadata after 60000 ms", "the topic missing or the producer being unable to reach the brokers", "check the bootstrap servers and that auto topic creation is enabled", ["operations"]),
        ("Connection to node -1 could not be established", "advertised listeners pointing at an address the client cannot reach, which is common inside Docker", "set separate internal and external advertised listeners", ["docker"]),
        ("SerializationException when consuming", "a consumer deserializer that does not match what the producer wrote", "align the serializers and trusted packages on both sides", ["messaging"]),
        ("consumer keeps rebalancing", "slow processing exceeding max.poll.interval.ms", "reduce batch size or increase the interval", ["operations"]),
    ],
}

DOCKER = {
    "key": "docker",
    "name": "Docker",
    "count": 500,
    "tags": ["docker", "devops"],
    "suffixes": ["", " on macOS", " in production", " with Spring Boot", " for local development", " in CI"],
    "concepts": [
        ("Dockerfiles", "Text files with the instructions for building an image.", "Order instructions from least to most frequently changing.", "Every instruction adds a layer, so careless ordering ruins the build cache.", ["images"]),
        ("Docker layer caching", "Reuse of unchanged image layers during builds.", "Copy dependency manifests before the source so dependency layers stay cached.", "Copying the whole project first invalidates the cache on every change.", ["images"]),
        ("Docker volumes", "Managed storage that persists data outside the container's lifecycle.", "Use named volumes for database data.", "Removing volumes with down -v deletes the data permanently.", ["storage"]),
        ("bind mounts", "Mounts that map a host directory into a container.", "Use them for source code during local development.", "File permissions and performance can differ across operating systems.", ["storage"]),
        ("Docker networks", "Virtual networks that let containers reach each other by service name.", "Use the compose service name as the hostname.", "Inside a container, localhost refers to the container itself and not to your machine.", ["networking"]),
        ("Docker Compose", "A tool for defining and running multi-container applications in one file.", "Use it to run the app together with its database and broker.", "The depends_on option waits for start, not for readiness, unless you add health checks.", ["compose"]),
        ("Docker health checks", "Commands that report whether a container is actually ready.", "Combine them with depends_on conditions so dependants wait.", "A health check that is too strict keeps a container unhealthy forever.", ["compose"]),
        ("multi-stage builds", "Dockerfiles with several stages so only the final artifacts end up in the image.", "Build with a full JDK and run on a small JRE image.", "Forgetting to copy a needed file into the last stage causes runtime errors.", ["images"]),
        ("environment variables in Docker", "Key-value settings passed to a container at runtime.", "Use them for configuration that differs per environment.", "Secrets in plain environment variables can leak through inspect output and logs.", ["configuration"]),
        ("port mapping", "Publishing a container port on a host port.", "Map only the ports that need to be reachable from outside.", "Two services cannot publish the same host port.", ["networking"]),
        ("dockerignore files", "Files that list paths excluded from the build context.", "Exclude build outputs, dependencies and version control folders.", "A large build context slows every build.", ["images"]),
        ("restart policies", "Settings that decide when Docker restarts a container.", "Use unless-stopped for long-running services.", "A crash loop restarts forever and can hide the underlying bug.", ["operations"]),
    ],
    "pairs": [
        ("images", "containers", "An image is a read-only template that contains the filesystem and metadata.", "A container is a running instance of an image.", "You build images and run containers.", ["basics"]),
        ("CMD", "ENTRYPOINT", "CMD provides default arguments that are easy to override.", "ENTRYPOINT defines the executable that always runs.", "Use ENTRYPOINT for the main program and CMD for its default arguments.", ["images"]),
        ("COPY", "ADD", "COPY copies files in a predictable way.", "ADD also extracts archives and fetches URLs.", "Prefer COPY unless you specifically need ADD's extras.", ["images"]),
        ("volumes", "bind mounts", "Volumes are managed by Docker and portable across hosts.", "Bind mounts expose an exact host path.", "Use volumes for data and bind mounts for code you are editing.", ["storage"]),
        ("docker stop", "docker kill", "docker stop sends SIGTERM and waits before force killing.", "docker kill sends SIGKILL immediately.", "Prefer stop so the application can shut down gracefully.", ["operations"]),
    ],
    "howtos": [
        ("persist database data between restarts", "Mount a named volume at the database data directory.", '''services:
  postgres:
    image: postgres:16
    volumes:
      - pg-data:/var/lib/postgresql/data
volumes:
  pg-data:''', ["storage"]),
        ("make an image smaller", "Use a slim base image, a multi-stage build and a .dockerignore file.", '''FROM eclipse-temurin:21-jre
COPY --from=build /app/app.jar app.jar''', ["images"]),
        ("see the logs of a container", "Use docker logs with the follow flag.", '''docker logs -f my-container''', ["operations"]),
        ("run a command inside a running container", "Use docker exec with the interactive flags.", '''docker exec -it my-container sh''', ["operations"]),
        ("remove unused images and containers", "Use the prune commands, carefully.", '''docker system prune''', ["operations"]),
        ("let two containers talk to each other", "Put them on the same network and use the service name as host.", '''services:
  api:
    environment:
      DB_HOST: postgres''', ["networking"]),
        ("limit the memory of a container", "Set a memory limit in the run command or compose file.", '''docker run -m 512m my-image''', ["operations"]),
        ("wait for the database before starting the app", "Add a health check to the database and use depends_on with service_healthy.", '''depends_on:
  postgres:
    condition: service_healthy''', ["compose"]),
    ],
    "errors": [
        ("Bind for 0.0.0.0:8080 failed: port is already allocated", "another process or container already publishing that port", "stop the other process or change the host port", ["networking"]),
        ("no space left on device", "Docker images, containers and volumes filling the disk", "prune unused resources and increase the disk size in Docker Desktop", ["operations"]),
        ("container exits immediately after starting", "the main process finishing or crashing", "read the logs with docker logs and check the entrypoint", ["operations"]),
        ("Cannot connect to the Docker daemon", "the Docker service not running or the socket not being accessible", "start Docker Desktop and check your permissions", ["operations"]),
        ("connection refused when one container calls another on localhost", "localhost pointing to the container itself", "use the compose service name instead", ["networking"]),
    ],
}

MONGODB = {
    "key": "mongodb",
    "name": "MongoDB",
    "count": 500,
    "tags": ["mongodb", "nosql"],
    "suffixes": ["", " in Spring Boot", " in production", " with large collections", " for a reporting query", " in Docker"],
    "concepts": [
        ("the MongoDB document model", "Storing data as flexible JSON-like documents inside collections.", "Model data around how your application reads it.", "Unbounded arrays inside a document can hit the 16 MB document limit.", ["modeling"]),
        ("ObjectId", "A 12-byte identifier that MongoDB generates for _id by default.", "Use it as the primary key unless you have a natural key.", "Treating it as a string in some places and an ObjectId in others causes lookups to fail.", ["modeling"]),
        ("MongoDB indexes", "Structures that speed up queries on fields.", "Create indexes for fields you filter and sort on.", "A query that sorts on an unindexed field can fail with a memory limit error.", ["indexing"]),
        ("compound indexes in MongoDB", "Indexes on multiple fields with a defined order.", "Follow the equality, sort, range guideline when ordering fields.", "The order of fields decides which queries the index can serve.", ["indexing"]),
        ("the aggregation pipeline", "A sequence of stages such as $match, $group and $sort that transform documents.", "Put $match and $limit early to reduce the data processed.", "Large $group stages can exceed memory limits unless allowed to use disk.", ["aggregation"]),
        ("$lookup", "A pipeline stage that joins documents from another collection.", "Use it sparingly for occasional joins.", "Heavy use of $lookup suggests the data should be embedded or modelled differently.", ["aggregation"]),
        ("MongoDB replica sets", "Groups of servers that maintain the same data for high availability.", "Use at least three members in production.", "Transactions and change streams require a replica set.", ["operations"]),
        ("MongoDB sharding", "Splitting data across servers by a shard key.", "Pick a shard key with high cardinality and even distribution.", "A poor shard key creates hot shards that are hard to fix.", ["operations"]),
        ("embedding versus referencing", "A modelling choice between nesting related data and storing ids that point to it.", "Embed data that is read together and changes together.", "Embedding data that grows without bound or is shared widely leads to problems.", ["modeling"]),
        ("TTL indexes", "Indexes that automatically delete documents after a time.", "Use them for sessions and temporary data.", "Deletion runs in the background and is not exact to the second.", ["indexing"]),
    ],
    "pairs": [
        ("embedding", "referencing", "Embedding stores related data inside one document for fast reads.", "Referencing stores ids and loads related documents separately.", "Embed data that is used together and reference data that grows or is shared.", ["modeling"]),
        ("MongoDB", "PostgreSQL", "MongoDB offers flexible schemas and easy horizontal scaling.", "PostgreSQL offers strict schemas, joins and mature transactions.", "Choose based on your access patterns and consistency needs.", ["design"]),
        ("find", "aggregate", "find retrieves documents with a filter and projection.", "aggregate runs multi-stage transformations such as grouping.", "Use find for simple reads and aggregate for analytics.", ["aggregation"]),
        ("updateOne", "replaceOne", "updateOne changes only the specified fields.", "replaceOne swaps the entire document.", "Prefer updateOne so you do not overwrite fields by accident.", ["basics"]),
    ],
    "howtos": [
        ("query a nested field", "Use dot notation in the filter.", '''db.users.find({ "address.city": "Pune" })''', ["basics"]),
        ("update one element of an array", "Use the positional operator with a filter on the array element.", '''db.orders.updateOne(
  { _id: id, "items.sku": "A1" },
  { $set: { "items.$.qty": 3 } })''', ["basics"]),
        ("create a unique index", "Call createIndex with the unique option.", '''db.tags.createIndex({ name: 1 }, { unique: true })''', ["indexing"]),
        ("count documents per group", "Use $group with $sum in an aggregation pipeline.", '''db.questions.aggregate([
  { $group: { _id: "$tags", total: { $sum: 1 } } }
])''', ["aggregation"]),
        ("import and export data", "Use mongoimport and mongoexport, or mongodump and mongorestore for backups.", '''mongoimport --db quora_db --collection questions --file questions.json''', ["operations"]),
    ],
    "errors": [
        ("E11000 duplicate key error", "inserting a document that violates a unique index", "handle the duplicate or use an upsert", ["indexing"]),
        ("Sort exceeded memory limit of 33554432 bytes", "sorting a large result without a supporting index", "add an index on the sort field or use allowDiskUse", ["indexing"]),
        ("MongoServerSelectionError: connect ECONNREFUSED", "the driver being unable to reach the server", "check the host, port and that the container is running", ["docker"]),
        ("BSON document too large", "a document growing past the 16 MB limit", "split the data into separate documents or collections", ["modeling"]),
    ],
}

ELASTICSEARCH = {
    "key": "elasticsearch",
    "name": "Elasticsearch",
    "count": 300,
    "tags": ["elasticsearch", "search"],
    "suffixes": ["", " in Spring Boot", " in production", " for a Q and A site", " with Docker", " for autocomplete"],
    "concepts": [
        ("the inverted index", "A structure that maps each term to the documents that contain it.", "It is what makes full-text search fast.", "Fields must be analyzed into the same terms at index and query time to match.", ["indexing"]),
        ("Elasticsearch analyzers", "Components made of a tokenizer and filters that turn text into terms.", "Choose a language analyzer for stemming and stop words.", "Changing an analyzer requires reindexing existing documents.", ["indexing"]),
        ("text versus keyword fields", "text fields are analyzed for full-text search, while keyword fields are stored as exact values.", "Use keyword for filtering, sorting and aggregations.", "Sorting on a text field fails unless you use a keyword sub-field.", ["mapping"]),
        ("relevance scoring with BM25", "A ranking function that scores documents by term frequency and rarity.", "Boost important fields such as the title.", "Scores are not comparable across different queries.", ["search"]),
        ("multi_match queries", "Queries that search the same text across several fields.", "Use them with field boosts like title^2.", "Without a clear type, results can surprise you when terms are spread across fields.", ["search"]),
        ("fuzzy matching", "A search that tolerates typos by allowing a small edit distance.", "Enable fuzziness AUTO on user-facing search boxes.", "High fuzziness on short terms produces noisy matches.", ["search"]),
        ("shards and replicas", "Shards split an index across nodes and replicas copy them for resilience.", "Size shards to tens of gigabytes rather than creating many tiny ones.", "The primary shard count cannot be changed without reindexing.", ["operations"]),
        ("the bulk API", "An endpoint for indexing or updating many documents in one request.", "Use it for loading data in chunks of a few thousand documents.", "Always check the errors flag in the response, because failures are reported per item.", ["indexing"]),
        ("the refresh interval", "The delay before newly indexed documents become searchable.", "Increase it during bulk loads for better throughput.", "Documents are not searchable until a refresh happens.", ["operations"]),
    ],
    "pairs": [
        ("text", "keyword", "A text field is analyzed into terms for full-text matching.", "A keyword field keeps the exact value for filters and sorting.", "Index a field as both when you need search and sorting.", ["mapping"]),
        ("match", "term queries", "A match query analyzes the input like the field does.", "A term query looks for the exact term without analysis.", "Use match for full-text and term for keywords.", ["search"]),
        ("query context", "filter context", "Query context calculates relevance scores.", "Filter context only asks yes or no and can be cached.", "Use filters for conditions that should not affect ranking.", ["search"]),
        ("Elasticsearch", "a relational database", "Elasticsearch is built for search, relevance and analytics over text.", "A relational database is built for transactions and consistency.", "Keep the database as the source of truth and index a copy into Elasticsearch.", ["design"]),
    ],
    "howtos": [
        ("search across several fields", "Use a multi_match query listing the fields.", '''{ "multi_match": { "query": "spring boot", "fields": ["title", "content"] } }''', ["search"]),
        ("boost the title over the body", "Add a caret and a factor to the field name.", '''{ "multi_match": { "query": "kafka", "fields": ["title^2", "content"] } }''', ["search"]),
        ("tolerate typos in the query", "Set fuzziness to AUTO.", '''{ "multi_match": { "query": "hasmap", "fields": ["title"], "fuzziness": "AUTO" } }''', ["search"]),
        ("load many documents quickly", "Send newline-delimited JSON to the bulk endpoint.", '''curl -XPOST localhost:9200/_bulk -H 'Content-Type: application/x-ndjson' --data-binary @docs.ndjson''', ["indexing"]),
        ("check cluster health", "Call the cluster health endpoint.", '''curl localhost:9200/_cluster/health''', ["operations"]),
    ],
    "errors": [
        ("cluster health is yellow", "replica shards that cannot be assigned, which is normal on a single node", "set replicas to 0 on a single-node cluster or add nodes", ["operations"]),
        ("mapper_parsing_exception", "a document field that does not fit the existing mapping", "fix the value type or create a new index with the right mapping", ["mapping"]),
        ("index_not_found_exception", "querying an index that does not exist yet", "create the index first or check the name", ["indexing"]),
        ("max virtual memory areas vm.max_map_count is too low", "the host limit for memory maps being too small for Elasticsearch", "raise vm.max_map_count on the Docker host", ["docker", "operations"]),
    ],
}

TOPICS = [KAFKA, DOCKER, MONGODB, ELASTICSEARCH]
