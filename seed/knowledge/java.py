# Curated Java knowledge used to generate seed questions and answers.
# concepts: (name, definition, usage, pitfall, tags)
# pairs:    (a, b, fact about a, fact about b, rule of thumb, tags)
# howtos:   (task, solution, code, tags)
# errors:   (error, cause, fix, tags)

CONCEPTS = [
    ("HashMap", "A hash table based Map that stores key-value pairs and gives average O(1) get and put.", "Use it as the default map when you do not need ordering or thread safety.", "It is not thread-safe, and mutable keys whose hashCode changes make entries unreachable.", ["collections"]),
    ("ConcurrentHashMap", "A thread-safe hash map that uses fine-grained locking and compare-and-swap so many threads can read and write at once.", "Use it for shared caches and counters accessed by multiple threads.", "Compound actions like check-then-put are not atomic unless you use putIfAbsent or compute.", ["concurrency", "collections"]),
    ("ArrayList", "A resizable array-backed List with O(1) random access.", "Use it as the default list when you mostly read by index or append at the end.", "Inserting or removing in the middle is O(n), and removing while iterating throws ConcurrentModificationException.", ["collections"]),
    ("LinkedList", "A doubly linked list that implements both List and Deque.", "Use it when you need frequent insertions and removals at both ends through the Deque methods.", "Index access is O(n) and every node costs extra memory, so ArrayList is usually faster in practice.", ["collections"]),
    ("HashSet", "A Set backed by a HashMap that rejects duplicate elements.", "Use it for fast membership checks and de-duplication.", "Elements need correct equals and hashCode, and iteration order is not guaranteed.", ["collections"]),
    ("TreeMap", "A sorted Map implemented as a red-black tree with O(log n) operations.", "Use it when you need keys in sorted order or range queries such as floorKey and subMap.", "Keys must be comparable or you must supply a Comparator, and null keys are not allowed.", ["collections"]),
    ("Optional", "A container that may or may not hold a value, used instead of returning null.", "Use it as a return type to make absence explicit and chain map and orElse calls.", "Do not use it for fields or method parameters, and avoid calling get() without checking isPresent.", ["streams"]),
    ("the Stream API", "A pipeline of lazy operations such as filter, map and collect over a data source.", "Use it for declarative transformations of collections.", "A stream can only be consumed once, and parallel streams on small or blocking workloads often make things slower.", ["streams"]),
    ("lambda expressions", "Compact anonymous functions that implement a functional interface.", "Use them to pass behaviour to methods such as forEach, sort and CompletableFuture callbacks.", "Variables captured by a lambda must be effectively final.", ["lambda"]),
    ("functional interfaces", "Interfaces with a single abstract method, like Function, Predicate and Supplier.", "Reach for the built-in ones in java.util.function before inventing your own.", "Checked exceptions cannot be thrown from the standard ones without wrapping.", ["lambda"]),
    ("CompletableFuture", "An async computation you can compose with thenApply, thenCompose and allOf.", "Use it to run independent calls in parallel and combine their results without blocking threads.", "Without a custom executor it runs on the common ForkJoinPool, and exceptions are swallowed unless you handle them.", ["concurrency"]),
    ("ExecutorService", "A thread pool abstraction that separates task submission from execution.", "Use it instead of creating threads manually, and size the pool to the workload.", "Forgetting to call shutdown keeps the JVM alive, and unbounded queues can hide overload.", ["concurrency"]),
    ("the synchronized keyword", "A keyword that locks an object monitor so only one thread runs a block at a time.", "Use it for small critical sections that protect shared mutable state.", "Holding locks while calling slow code causes contention, and inconsistent lock ordering causes deadlocks.", ["concurrency"]),
    ("the volatile keyword", "A modifier that guarantees writes to a variable are visible to other threads.", "Use it for simple flags that one thread writes and others read.", "It does not make compound operations like count++ atomic.", ["concurrency"]),
    ("AtomicInteger", "A lock-free integer with atomic operations built on compare-and-swap.", "Use it for counters shared between threads.", "It only makes single operations atomic, so combining several atomic variables still needs coordination.", ["concurrency"]),
    ("ReentrantLock", "An explicit lock with tryLock, timeouts and fairness options.", "Use it when synchronized is too limited, for example to try acquiring a lock with a timeout.", "You must unlock in a finally block or the lock is never released.", ["concurrency"]),
    ("virtual threads", "Lightweight threads managed by the JVM, final since Java 21.", "Use them for large numbers of blocking I/O tasks with one thread per request.", "They do not speed up CPU-bound work, and pinning inside synchronized blocks can limit scalability.", ["concurrency", "java-21"]),
    ("garbage collection", "Automatic reclamation of memory held by objects that are no longer reachable.", "Pick a collector like G1 or ZGC based on your latency and throughput needs.", "Creating huge numbers of short-lived objects or holding references in static collections causes memory pressure and leaks.", ["jvm", "memory"]),
    ("the JVM heap", "The memory area where all objects live and where the garbage collector works.", "Tune it with -Xms and -Xmx and monitor it with tools like jcmd and VisualVM.", "Setting -Xmx larger than the container memory limit gets the process killed by the operating system.", ["jvm", "memory"]),
    ("classloaders", "The JVM components that load classes on demand from the classpath or modules.", "Understanding them helps with NoClassDefFoundError and plugin systems.", "Loading the same class through different classloaders creates distinct types that cannot be cast to each other.", ["jvm"]),
    ("generics", "Compile-time type parameters that make collections and methods type-safe.", "Use them to avoid casts and catch type errors early.", "Type erasure removes the type arguments at runtime, so you cannot do instanceof List<String> or create generic arrays.", ["generics"]),
    ("bounded wildcards", "Wildcards such as ? extends T and ? super T let a generic method accept a family of types.", "Use extends when you only read from a collection and super when you only write to it.", "You cannot add elements to a List<? extends T> except null.", ["generics"]),
    ("records", "Immutable data carriers that generate the constructor, accessors, equals, hashCode and toString.", "Use them for DTOs and value objects.", "Records cannot extend other classes and their fields are final, so they do not suit mutable JPA entities.", ["oop"]),
    ("sealed classes", "Classes or interfaces that restrict which types may extend them.", "Use them with pattern matching in switch to model a closed set of cases.", "Every permitted subclass must be final, sealed or non-sealed.", ["oop"]),
    ("default methods in interfaces", "Methods with a body in an interface that let you evolve APIs without breaking implementers.", "Use them to add behaviour to existing interfaces.", "Two interfaces with the same default method force the class to override it to resolve the conflict.", ["oop"]),
    ("abstract classes", "Classes that cannot be instantiated and can hold state and partial implementation.", "Use them when subclasses share fields and behaviour.", "A class can extend only one, so prefer interfaces when you need multiple inheritance of type.", ["oop"]),
    ("the equals and hashCode contract", "The rule that equal objects must return the same hashCode.", "Override both together whenever objects are used as map keys or set elements.", "Overriding only equals breaks HashMap and HashSet lookups.", ["oop", "collections"]),
    ("string immutability", "Strings never change after creation, which makes them safe to share and cache.", "Use StringBuilder when concatenating in loops.", "Using == to compare strings compares references, so use equals.", ["strings"]),
    ("the string pool", "A cache where the JVM stores string literals so identical literals share one instance.", "Use intern() sparingly to deduplicate large numbers of repeated strings.", "Relying on == for strings because literals happen to be pooled is a bug waiting to happen.", ["strings", "memory"]),
    ("checked exceptions", "Exceptions that must be declared or caught, unlike unchecked ones that extend RuntimeException.", "Use checked exceptions for recoverable conditions and unchecked ones for programming errors.", "Swallowing exceptions with an empty catch block hides failures.", ["exceptions"]),
    ("try-with-resources", "A try block that automatically closes AutoCloseable resources.", "Use it for streams, connections and readers.", "Exceptions thrown on close are added as suppressed exceptions, so check getSuppressed when debugging.", ["exceptions"]),
    ("Java serialization", "Converting an object into bytes so it can be stored or sent.", "Prefer JSON or Protobuf for data exchange between services.", "Native Java serialization is fragile and has a history of security vulnerabilities, so never deserialize untrusted data.", ["io"]),
    ("reflection", "APIs for inspecting and invoking classes, methods and fields at runtime.", "Frameworks like Spring and Hibernate use it for injection and mapping.", "It is slower than direct calls, bypasses compile-time checks and is restricted by the module system.", ["jvm"]),
    ("annotations", "Metadata attached to code that tools and frameworks can read.", "Use them with RUNTIME retention to drive behaviour through reflection.", "Annotations do nothing on their own, because something must process them.", ["oop"]),
    ("enums", "A fixed set of named constants that can have fields and methods.", "Use them instead of int or String constants.", "Prefer EnumMap and EnumSet for collections, and avoid relying on ordinal().", ["oop"]),
    ("immutable objects", "Objects whose state cannot change after construction.", "Use them for thread safety and as map keys.", "Making fields final is not enough if they hold mutable collections, so copy defensively.", ["oop", "concurrency"]),
    ("fail-fast iterators", "Iterators that throw ConcurrentModificationException when the collection is modified during iteration.", "Use iterator.remove or removeIf to modify a collection while looping.", "Removing inside a for-each loop is the classic mistake.", ["collections"]),
    ("Comparator", "An object that defines a custom ordering of elements.", "Use Comparator.comparing and thenComparing to sort by multiple fields.", "A comparator that is inconsistent can make TreeSet drop elements or make sort throw errors.", ["collections"]),
    ("memory leaks in Java", "Objects that are no longer needed but still reachable, so the garbage collector cannot free them.", "Use heap dumps and tools like Eclipse MAT to find the references that hold them.", "Common causes are static collections, unclosed resources and listeners that are never removed.", ["memory", "jvm"]),
    ("SOLID principles", "Five design guidelines: single responsibility, open-closed, Liskov substitution, interface segregation and dependency inversion.", "Use them as a review checklist to keep classes small and easy to change.", "Applying them dogmatically leads to needless abstraction.", ["oop"]),
    ("method references", "Short syntax such as String::length that points at an existing method.", "Use them when a lambda only calls one method.", "Overloaded methods can make the target ambiguous.", ["lambda"]),
    ("the var keyword", "Local variable type inference introduced in Java 10.", "Use it when the type is obvious from the right-hand side.", "It cannot be used for fields or method parameters, and overuse hurts readability.", ["oop"]),
    ("pattern matching for switch", "A switch that can match on types and deconstruct records.", "Use it to replace chains of instanceof checks.", "Cases must be exhaustive for sealed hierarchies, and dominated patterns are rejected by the compiler.", ["oop", "java-21"]),
    ("ThreadLocal", "Per-thread storage for values such as user context.", "Use it for request-scoped data in thread-per-request servers.", "Not removing values in pooled threads leaks memory and can leak data between requests.", ["concurrency"]),
    ("deadlocks", "A situation where two or more threads wait forever for locks held by each other.", "Acquire locks in a consistent order or use tryLock with timeouts.", "Thread dumps from jstack reveal the cycle, so capture one before restarting.", ["concurrency"]),
]

PAIRS = [
    ("ArrayList", "LinkedList", "ArrayList is backed by an array, so index access is O(1) and iteration is cache friendly.", "LinkedList stores nodes with pointers, so inserting at the ends is cheap but index access is O(n).", "Default to ArrayList and only consider LinkedList for queue-like access patterns.", ["collections"]),
    ("HashMap", "ConcurrentHashMap", "HashMap is faster but not thread-safe, so concurrent writes can corrupt it.", "ConcurrentHashMap allows safe concurrent access without locking the whole map.", "Use HashMap for single-threaded code and ConcurrentHashMap when threads share the map.", ["collections", "concurrency"]),
    ("HashMap", "Hashtable", "HashMap is unsynchronized, allows one null key and null values, and is the modern default.", "Hashtable is a legacy class where every method is synchronized and nulls are not allowed.", "Avoid Hashtable in new code and use HashMap or ConcurrentHashMap.", ["collections"]),
    ("==", "equals()", "== compares references for objects, so two equal strings can still be different objects.", "equals() compares logical content when a class overrides it properly.", "Use equals() for value comparison and == only for primitives, enums and identity checks.", ["strings"]),
    ("String", "StringBuilder", "String is immutable, so every concatenation creates a new object.", "StringBuilder is mutable and appends in place without extra allocations.", "Use StringBuilder for concatenation in loops and String everywhere else.", ["strings"]),
    ("abstract classes", "interfaces", "An abstract class can hold state and constructors, but a class can extend only one.", "An interface defines a contract that a class can implement many times, now with default methods too.", "Prefer interfaces for contracts and abstract classes when subclasses share state.", ["oop"]),
    ("checked exceptions", "unchecked exceptions", "Checked exceptions must be caught or declared, which forces callers to deal with them.", "Unchecked exceptions extend RuntimeException and signal programming errors.", "Use checked exceptions for recoverable conditions and unchecked ones for bugs.", ["exceptions"]),
    ("Comparable", "Comparator", "Comparable defines the natural ordering inside the class itself.", "Comparator defines an external ordering that you can swap per use case.", "Use Comparable for one obvious ordering and Comparator for everything else.", ["collections"]),
    ("stack memory", "heap memory", "The stack holds method frames, local variables and references, and is cleaned up automatically on return.", "The heap holds objects and is managed by the garbage collector.", "Local primitives live on the stack, while every object lives on the heap.", ["jvm", "memory"]),
    ("Thread", "Runnable", "Extending Thread ties your task to a thread and uses up your single inheritance.", "Runnable separates the task from how it runs, so you can pass it to an executor.", "Implement Runnable or Callable and let an ExecutorService run it.", ["concurrency"]),
    ("synchronized", "ReentrantLock", "synchronized is simple and releases the lock automatically.", "ReentrantLock supports tryLock, timeouts and fairness but must be unlocked manually.", "Start with synchronized and move to ReentrantLock only when you need its extra features.", ["concurrency"]),
    ("HashSet", "TreeSet", "HashSet offers O(1) lookups with no ordering.", "TreeSet keeps elements sorted with O(log n) operations.", "Use HashSet by default and TreeSet when you need sorted iteration.", ["collections"]),
    ("List", "Set", "A List keeps insertion order and allows duplicates.", "A Set rejects duplicates and models uniqueness.", "Choose List when order or duplicates matter and Set when uniqueness matters.", ["collections"]),
    ("map()", "flatMap()", "map() transforms each element into exactly one result.", "flatMap() transforms each element into a stream and flattens the results.", "Use flatMap when each element produces zero or many results.", ["streams"]),
    ("Callable", "Runnable", "Callable returns a result and can throw checked exceptions.", "Runnable returns nothing and cannot throw checked exceptions.", "Use Callable when you need a result from an async task.", ["concurrency"]),
    ("sleep()", "wait()", "sleep() pauses the current thread without releasing any locks.", "wait() releases the monitor and waits until another thread calls notify.", "Use wait and notify for coordination and sleep only for delays.", ["concurrency"]),
    ("orElse()", "orElseGet()", "orElse() always evaluates its argument, even when the Optional has a value.", "orElseGet() only calls its supplier when the Optional is empty.", "Use orElseGet when the fallback is expensive to compute.", ["streams"]),
]

HOWTOS = [
    ("read a file line by line", "Use Files.lines or Files.newBufferedReader inside try-with-resources so the file is closed automatically.", '''try (Stream<String> lines = Files.lines(Path.of("data.txt"))) {
    lines.forEach(System.out::println);
}''', ["io"]),
    ("convert a List to a Map", "Collect with Collectors.toMap and pass a merge function if keys can repeat.", '''Map<Long, User> byId = users.stream()
    .collect(Collectors.toMap(User::getId, u -> u, (a, b) -> a));''', ["streams"]),
    ("sort a list of objects by multiple fields", "Chain comparators with thenComparing.", '''list.sort(Comparator.comparing(Person::getLastName)
    .thenComparing(Person::getAge));''', ["collections"]),
    ("remove elements from a list while iterating", "Use removeIf or an explicit Iterator instead of removing inside a for-each loop.", '''list.removeIf(x -> x < 0);''', ["collections"]),
    ("run tasks in parallel and wait for all of them", "Start each task with CompletableFuture.supplyAsync on a custom executor, then combine with allOf.", '''CompletableFuture<Void> all = CompletableFuture.allOf(f1, f2, f3);
all.join();''', ["concurrency"]),
    ("make a class immutable", "Make the class final, keep all fields private final, avoid setters and copy mutable inputs. A record does most of this for you.", '''public record Point(int x, int y) {}''', ["oop"]),
    ("implement a thread-safe singleton", "Use an enum singleton or the initialization-on-demand holder idiom.", '''public enum Config {
    INSTANCE;
}''', ["concurrency", "oop"]),
    ("convert a String to int safely", "Call Integer.parseInt inside a try-catch for NumberFormatException, after trimming the input.", '''try {
    int n = Integer.parseInt(s.trim());
} catch (NumberFormatException e) {
    // handle invalid input
}''', ["strings"]),
    ("group a list by a field and count the groups", "Use Collectors.groupingBy together with Collectors.counting.", '''Map<String, Long> counts = people.stream()
    .collect(Collectors.groupingBy(Person::getCity, Collectors.counting()));''', ["streams"]),
    ("handle null safely in a chain of calls", "Wrap the first value in Optional, chain map calls and finish with orElse.", '''String city = Optional.ofNullable(user)
    .map(User::getAddress)
    .map(Address::getCity)
    .orElse("unknown");''', ["streams"]),
    ("create a thread pool with a fixed size", "Use Executors.newFixedThreadPool, submit your tasks and shut the pool down when finished.", '''ExecutorService pool = Executors.newFixedThreadPool(4);
pool.submit(() -> doWork());
pool.shutdown();''', ["concurrency"]),
    ("measure the execution time of a method", "Use System.nanoTime around the call, or JMH when you need trustworthy benchmark numbers.", '''long start = System.nanoTime();
run();
long ms = (System.nanoTime() - start) / 1_000_000;''', ["jvm"]),
    ("deep copy an object", "Use a copy constructor or copy factory, or map through JSON for complex graphs, and avoid clone().", '''public Order(Order other) {
    this.items = new ArrayList<>(other.items);
}''', ["oop"]),
    ("parse JSON into an object", "Use Jackson's ObjectMapper and readValue with the target class.", '''ObjectMapper mapper = new ObjectMapper();
User user = mapper.readValue(json, User.class);''', ["json"]),
    ("format a date with a specific pattern", "Use DateTimeFormatter with LocalDate or LocalDateTime instead of the legacy SimpleDateFormat.", '''String s = LocalDate.now()
    .format(DateTimeFormatter.ofPattern("dd-MM-yyyy"));''', ["datetime"]),
    ("find duplicates in a list", "Add elements to a HashSet and collect the ones that fail to add.", '''Set<String> seen = new HashSet<>();
Set<String> dupes = list.stream()
    .filter(s -> !seen.add(s))
    .collect(Collectors.toSet());''', ["collections"]),
    ("stop a running thread safely", "Use interruption: call interrupt on the thread and check isInterrupted or handle InterruptedException in the loop.", '''while (!Thread.currentThread().isInterrupted()) {
    // do work
}''', ["concurrency"]),
    ("generate a random number in a range", "Use ThreadLocalRandom, where the upper bound is exclusive.", '''int n = ThreadLocalRandom.current().nextInt(1, 7);''', ["java"]),
    ("reverse a string", "Wrap it in a StringBuilder and call reverse.", '''String r = new StringBuilder(s).reverse().toString();''', ["strings"]),
    ("write a custom exception", "Extend RuntimeException or Exception and add constructors that accept a message and a cause.", '''public class OrderNotFoundException extends RuntimeException {
    public OrderNotFoundException(String message) {
        super(message);
    }
}''', ["exceptions"]),
]

ERRORS = [
    ("NullPointerException", "calling a method or reading a field on a reference that is null", "check where the value is assigned, use Optional or Objects.requireNonNull, and read the line number in the stack trace", ["exceptions"]),
    ("ConcurrentModificationException", "structurally modifying a collection while iterating over it", "use Iterator.remove, removeIf, or iterate over a copy", ["collections"]),
    ("ClassCastException", "casting an object to a type it is not an instance of", "check with instanceof or fix the generic types so the cast is not needed", ["generics"]),
    ("java.lang.OutOfMemoryError: Java heap space", "a heap full of objects that are still reachable", "take a heap dump, look for leaks, and raise -Xmx only after that", ["memory", "jvm"]),
    ("StackOverflowError", "recursion without a base case or a call stack that is simply too deep", "add a proper termination condition or convert the recursion to a loop", ["jvm"]),
    ("NoClassDefFoundError", "a class that was present at compile time missing at runtime", "check the runtime classpath and dependency versions", ["jvm"]),
    ("UnsupportedOperationException when modifying a list", "modifying a collection returned by List.of or Arrays.asList", "copy it into a new ArrayList before changing it", ["collections"]),
    ("NumberFormatException", "parsing a string that is not a valid number", "trim and validate the input before parsing", ["strings"]),
    ("ArrayIndexOutOfBoundsException", "accessing an index outside the range 0 to length minus one", "check loop bounds and off-by-one errors", ["java"]),
    ("UnsupportedClassVersionError", "running a class compiled with a newer Java version than the runtime", "run with the same or a newer JDK, or compile with the release flag", ["jvm"]),
    ("unchecked cast warning", "casting to a generic type the compiler cannot verify", "use proper generics, or suppress the warning only where you can prove it is safe", ["generics"]),
    ("incompatible types: possible lossy conversion from double to int", "assigning a wider numeric type to a narrower one", "cast explicitly or use Math.round when you really want a rounded int", ["java"]),
]

TOPICS = [
    {
        "key": "java",
        "name": "Java",
        "count": 3000,
        "tags": ["java"],
        "suffixes": ["", " in Java 17", " in Java 21", " in a multi-threaded app", " in a REST API", " in production"],
        "concepts": CONCEPTS,
        "pairs": PAIRS,
        "howtos": HOWTOS,
        "errors": ERRORS,
    }
]
