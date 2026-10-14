# Curated SQL knowledge (PostgreSQL flavoured) used to generate seed questions and answers.

CONCEPTS = [
    ("INNER JOIN", "A join that returns only rows with matching values in both tables.", "Use it when you only want related rows that exist on both sides.", "A missing join condition creates a cartesian product.", ["joins"]),
    ("LEFT JOIN", "A join that returns all rows from the left table and matching rows from the right, with NULLs where there is no match.", "Use it to find rows with or without related data, such as customers with no orders.", "Putting a filter on the right table in WHERE turns it into an inner join, so put it in the ON clause instead.", ["joins"]),
    ("FULL OUTER JOIN", "A join that keeps unmatched rows from both tables.", "Use it to compare two tables and see what exists on only one side.", "Many engines do not support it for all join types, and the result can contain NULLs on either side.", ["joins"]),
    ("CROSS JOIN", "A join that produces every combination of rows from two tables.", "Use it to generate combinations such as dates times products.", "On large tables the row count explodes.", ["joins"]),
    ("self joins", "Joining a table to itself using aliases.", "Use it for hierarchies such as employees and their managers.", "Forgetting the aliases makes the query ambiguous.", ["joins"]),
    ("GROUP BY", "A clause that collapses rows with the same values into groups so aggregates can be computed.", "Use it with COUNT, SUM and AVG.", "Every non-aggregated selected column must appear in GROUP BY.", ["aggregation"]),
    ("HAVING", "A clause that filters groups after aggregation.", "Use it for conditions on aggregates such as COUNT(*) > 5.", "Conditions on plain columns belong in WHERE because it filters earlier and is cheaper.", ["aggregation"]),
    ("database indexes", "Data structures, usually B-trees, that speed up lookups on one or more columns.", "Index the columns used in WHERE, JOIN and ORDER BY.", "Each extra index slows writes and uses disk, so do not index everything.", ["indexing"]),
    ("composite indexes", "Indexes on several columns in a defined order.", "Put equality columns first and range columns last.", "A query that skips the leading column cannot use the index efficiently.", ["indexing"]),
    ("covering indexes", "Indexes that contain every column a query needs, so the table is never read.", "Use them for hot read queries.", "Wide covering indexes cost write performance and storage.", ["indexing"]),
    ("primary keys", "A column or set of columns that uniquely identifies each row and cannot be NULL.", "Give every table one.", "Random UUID keys can fragment B-tree indexes compared with sequential ids.", ["design"]),
    ("foreign keys", "Constraints that link a column to the primary key of another table.", "Use them to guarantee referential integrity.", "Cascading deletes can remove far more data than you expect.", ["design"]),
    ("database normalization", "Organizing tables to reduce redundancy through normal forms such as 1NF, 2NF and 3NF.", "Normalize transactional schemas to avoid update anomalies.", "Over-normalizing can force expensive joins on read-heavy workloads.", ["normalization"]),
    ("denormalization", "Deliberately duplicating data to avoid joins.", "Use it for read-heavy reporting tables.", "You must keep the copies in sync or they drift apart.", ["normalization"]),
    ("ACID properties", "Atomicity, Consistency, Isolation and Durability, the guarantees of a transaction.", "Rely on them for payments and inventory.", "Higher isolation levels reduce concurrency and can cause more lock waits.", ["transactions"]),
    ("transaction isolation levels", "Read uncommitted, read committed, repeatable read and serializable control what concurrent transactions can see.", "Choose the lowest level that prevents the anomalies your business logic cannot tolerate.", "PostgreSQL defaults to read committed, and serializable transactions may fail with serialization errors that you must retry.", ["transactions"]),
    ("deadlocks in SQL", "Two transactions that each hold a lock the other needs.", "Access rows in a consistent order and keep transactions short.", "The database aborts one of them, so the application must be ready to retry.", ["transactions"]),
    ("window functions", "Functions like ROW_NUMBER, RANK and SUM OVER that compute across related rows without collapsing them.", "Use them for running totals, rankings and top-N per group.", "They run after WHERE and GROUP BY, so you cannot filter on them directly without a subquery or CTE.", ["window-functions"]),
    ("CTEs", "Named temporary result sets defined with the WITH clause at the top of a query.", "Use them to break complex queries into readable steps or to write recursive queries.", "In some engines or versions a CTE acts as an optimization fence, so check the plan.", ["query-optimization"]),
    ("subqueries", "Queries nested inside another query.", "Use them for filtering with IN or EXISTS and for derived tables.", "Correlated subqueries run once per outer row and can be slow.", ["query-optimization"]),
    ("EXISTS", "A predicate that is true if a subquery returns any row.", "Use it for existence checks, since it can stop at the first match.", "NOT IN with NULLs in the subquery returns no rows, while NOT EXISTS avoids that trap.", ["query-optimization"]),
    ("NULL handling", "NULL means unknown, and comparisons with it yield unknown rather than true or false.", "Use IS NULL, COALESCE and NULLIF.", "column = NULL never matches, and aggregates like COUNT(column) ignore NULLs.", ["basics"]),
    ("EXPLAIN and query plans", "Output that shows how the database will execute a query.", "Use EXPLAIN ANALYZE to see real timings, row counts and index usage.", "A Seq Scan on a large table is not always bad, but a big gap between estimated and actual rows suggests stale statistics.", ["query-optimization"]),
    ("the N+1 query problem", "Running one query for a list and then one more query per row.", "Fix it with a join or a batched IN query.", "ORMs with lazy loading hide it, so log the SQL and count the queries.", ["query-optimization"]),
    ("pagination in SQL", "Returning results in pages using LIMIT and OFFSET or keyset conditions.", "Use keyset pagination such as WHERE id > last_id for large tables.", "Large OFFSET values make the database scan and discard rows.", ["query-optimization"]),
    ("views", "Stored queries that behave like virtual tables.", "Use them to simplify access and hide complexity.", "A plain view stores no data, so it is as slow as its underlying query.", ["design"]),
    ("materialized views", "Views whose results are stored on disk and refreshed on demand.", "Use them for expensive reports that tolerate slightly stale data.", "You must refresh them, and a plain refresh can block reads unless done concurrently.", ["design"]),
    ("stored procedures", "Programs stored in the database that run on the server.", "Use them for set-based batch work close to the data.", "Business logic split between the application and the database is harder to test and version.", ["design"]),
    ("triggers", "Functions that run automatically on INSERT, UPDATE or DELETE.", "Use them for audit logs and derived columns.", "Hidden side effects make behaviour hard to debug.", ["design"]),
    ("table partitioning", "Splitting a large table into smaller physical pieces by range, list or hash.", "Use it for time-series data so old partitions can be dropped quickly.", "Queries that do not filter on the partition key scan every partition.", ["performance"]),
    ("UNIQUE and CHECK constraints", "Rules the database enforces on column values.", "Use them to protect data integrity independent of the application.", "Application-only validation can be bypassed by other clients.", ["design"]),
    ("SQL injection", "An attack where untrusted input is concatenated into a query and executed.", "Always use parameterized queries or prepared statements.", "Escaping strings by hand is unreliable.", ["security"]),
    ("prepared statements", "Precompiled queries with placeholders for parameters.", "Use them for security and plan reuse.", "You cannot parameterize identifiers such as table names.", ["security"]),
    ("DISTINCT", "A keyword that removes duplicate rows from the result.", "Use it when duplicates are legitimate but unwanted.", "It often hides a faulty join, so fix the join instead.", ["basics"]),
    ("database connection pooling", "Reusing a fixed set of database connections instead of opening one per request.", "Use a pool like HikariCP and size it to the database rather than to the number of threads.", "Too many connections can exhaust the database's max_connections.", ["performance"]),
    ("sequences and auto-increment ids", "Generators for unique numeric ids.", "Use identity columns or sequences for surrogate keys.", "Gaps are normal after rollbacks, so never rely on gapless ids.", ["design"]),
    ("ORDER BY with LIMIT", "A pattern that sorts rows and keeps the first N.", "Use it for top-N queries, ideally backed by an index on the sort column.", "Without a deterministic tie-breaker, pages can repeat or skip rows.", ["basics"]),
    ("SELECT FOR UPDATE", "A locking read that locks the selected rows until the transaction ends.", "Use it to prevent lost updates in read-modify-write cycles.", "Long transactions holding these locks block other writers.", ["transactions"]),
    ("full-text search in SQL", "Database features such as PostgreSQL tsvector and GIN indexes for searching text.", "Use them for simple search without another system.", "For relevance ranking, typo tolerance and scale, a search engine like Elasticsearch is a better fit.", ["search"]),
]

PAIRS = [
    ("WHERE", "HAVING", "WHERE filters individual rows before grouping.", "HAVING filters groups after aggregation.", "Use WHERE for row conditions and HAVING only for conditions on aggregates.", ["aggregation"]),
    ("INNER JOIN", "LEFT JOIN", "INNER JOIN returns only rows that match on both sides.", "LEFT JOIN keeps every row from the left table and fills missing matches with NULL.", "Use LEFT JOIN when you must keep rows that have no match.", ["joins"]),
    ("UNION", "UNION ALL", "UNION removes duplicates, which requires a sort or hash step.", "UNION ALL keeps every row and is faster.", "Use UNION ALL unless you really need de-duplication.", ["basics"]),
    ("DELETE", "TRUNCATE", "DELETE removes rows one by one, can use WHERE and fires row triggers.", "TRUNCATE empties the whole table quickly and cannot filter rows.", "Use DELETE for selective removal and TRUNCATE to reset a table.", ["basics"]),
    ("IN", "EXISTS", "IN compares a value against a list or subquery result.", "EXISTS checks whether a correlated subquery returns any row.", "Prefer EXISTS for large subqueries and for NOT checks that involve NULLs.", ["query-optimization"]),
    ("CHAR", "VARCHAR", "CHAR pads values to a fixed length.", "VARCHAR stores only the characters you give it, up to a limit.", "Use VARCHAR unless values are truly fixed length.", ["design"]),
    ("clustered indexes", "non-clustered indexes", "A clustered index defines the physical order of the table rows, so there is one per table.", "A non-clustered index is a separate structure that points back to the rows.", "Pick the clustered key for the most common range access and add non-clustered indexes for other lookups.", ["indexing"]),
    ("RANK()", "DENSE_RANK()", "RANK leaves gaps after ties.", "DENSE_RANK numbers ties without gaps.", "Use DENSE_RANK when you want consecutive rank numbers.", ["window-functions"]),
    ("ROW_NUMBER()", "RANK()", "ROW_NUMBER gives every row a unique number even for ties.", "RANK gives tied rows the same number.", "Use ROW_NUMBER to pick exactly one row per group.", ["window-functions"]),
    ("primary keys", "unique keys", "A table has one primary key and it cannot be NULL.", "A table can have several unique constraints and they may allow NULL.", "Use the primary key as the row identity and unique constraints for other natural keys.", ["design"]),
    ("SQL", "NoSQL", "SQL databases give strong schemas, joins and ACID transactions.", "NoSQL databases favour flexible schemas and horizontal scaling.", "Start with SQL unless your access pattern clearly fits a document or key-value model.", ["design"]),
    ("views", "materialized views", "A view runs its query every time it is used.", "A materialized view stores the result and has to be refreshed.", "Use a materialized view when the query is expensive and slightly stale data is fine.", ["design"]),
    ("COUNT(*)", "COUNT(column)", "COUNT(*) counts all rows.", "COUNT(column) counts only rows where the column is not NULL.", "Use COUNT(*) for row counts and COUNT(column) when NULLs should be ignored.", ["aggregation"]),
    ("temporary tables", "CTEs", "A temporary table is materialized, can be indexed and persists for the session.", "A CTE is part of one statement and is mainly for readability and recursion.", "Use a temp table to reuse a large intermediate result and a CTE for readability.", ["query-optimization"]),
    ("optimistic locking", "pessimistic locking", "Optimistic locking checks a version column at update time and retries on conflict.", "Pessimistic locking locks the rows up front with SELECT FOR UPDATE.", "Use optimistic locking when conflicts are rare and pessimistic when they are common.", ["transactions"]),
    ("B-tree indexes", "hash indexes", "B-tree indexes support equality, ranges and ordering.", "Hash indexes only support equality lookups.", "Use B-tree unless you have measured a reason to use hash.", ["indexing"]),
]

HOWTOS = [
    ("find duplicate rows in a table", "Group by the columns that define a duplicate and keep groups with more than one row.", '''SELECT email, COUNT(*)
FROM users
GROUP BY email
HAVING COUNT(*) > 1;''', ["aggregation"]),
    ("get the second highest salary", "Order the distinct salaries descending and skip the first one, or use DENSE_RANK.", '''SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 1;''', ["basics"]),
    ("get the top 3 rows per group", "Use ROW_NUMBER partitioned by the group and filter in an outer query.", '''SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
  FROM employees
) t
WHERE rn <= 3;''', ["window-functions"]),
    ("delete duplicate rows but keep one", "Delete rows whose id is larger than the smallest id in the same duplicate group.", '''DELETE FROM users u
USING users v
WHERE u.email = v.email AND u.id > v.id;''', ["basics"]),
    ("calculate a running total", "Use SUM as a window function ordered by the date column.", '''SELECT day, SUM(amount) OVER (ORDER BY day) AS running_total
FROM sales;''', ["window-functions"]),
    ("find rows in one table that have no match in another", "LEFT JOIN and filter for NULL on the right side, or use NOT EXISTS.", '''SELECT c.*
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.id IS NULL;''', ["joins"]),
    ("update a table using values from another table", "Use UPDATE with a FROM clause (or a join in MySQL).", '''UPDATE orders o
SET status = s.status
FROM shipments s
WHERE s.order_id = o.id;''', ["basics"]),
    ("pivot rows into columns", "Use conditional aggregation with CASE inside SUM.", '''SELECT year,
  SUM(CASE WHEN q = 1 THEN amount END) AS q1,
  SUM(CASE WHEN q = 2 THEN amount END) AS q2
FROM sales
GROUP BY year;''', ["aggregation"]),
    ("count rows per day for the last 7 days", "Cast the timestamp to a date, filter on the last 7 days and group by it.", '''SELECT created_at::date AS day, COUNT(*)
FROM events
WHERE created_at >= now() - interval '7 days'
GROUP BY 1
ORDER BY 1;''', ["aggregation"]),
    ("add an index without locking the table", "In PostgreSQL use CREATE INDEX CONCURRENTLY, which avoids blocking writes.", '''CREATE INDEX CONCURRENTLY idx_orders_customer
ON orders (customer_id);''', ["indexing"]),
    ("speed up a slow query", "Run EXPLAIN ANALYZE, add the missing index, avoid functions on indexed columns and select only the columns you need.", '''EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 42;''', ["query-optimization"]),
    ("paginate results efficiently", "Use keyset pagination: remember the last id and ask for rows after it.", '''SELECT * FROM posts
WHERE id < :last_id
ORDER BY id DESC
LIMIT 20;''', ["query-optimization"]),
    ("concatenate values from several rows into one string", "Use STRING_AGG in PostgreSQL or GROUP_CONCAT in MySQL.", '''SELECT dept, STRING_AGG(name, ', ')
FROM employees
GROUP BY dept;''', ["aggregation"]),
    ("store JSON and query it", "Use a jsonb column with a GIN index and the arrow operators.", '''SELECT * FROM events
WHERE payload->>'type' = 'click';''', ["postgresql"]),
    ("safely add a NOT NULL column to a large table", "Add it as nullable, backfill in batches, then set NOT NULL.", '''ALTER TABLE users ADD COLUMN age int;
-- backfill in batches, then:
ALTER TABLE users ALTER COLUMN age SET NOT NULL;''', ["design"]),
    ("compare two tables for differences", "Use EXCEPT in both directions, or a FULL OUTER JOIN on the key.", '''SELECT * FROM a
EXCEPT
SELECT * FROM b;''', ["joins"]),
    ("get the latest row per user", "In PostgreSQL use DISTINCT ON ordered by the timestamp descending.", '''SELECT DISTINCT ON (user_id) *
FROM logins
ORDER BY user_id, created_at DESC;''', ["postgresql"]),
    ("back up and restore a PostgreSQL database", "Use pg_dump to export and psql or pg_restore to import.", '''pg_dump -U app mydb > mydb.sql
psql -U app mydb < mydb.sql''', ["postgresql"]),
]

ERRORS = [
    ("column must appear in the GROUP BY clause or be used in an aggregate function", "selecting a non-aggregated column that is not part of the grouping", "add the column to GROUP BY or wrap it in an aggregate function", ["aggregation"]),
    ("deadlock detected", "two transactions locking the same rows in opposite order", "lock rows in a consistent order, keep transactions short and retry the failed one", ["transactions"]),
    ("duplicate key value violates unique constraint", "inserting a value that already exists in a unique column", "use INSERT with ON CONFLICT or check for existence first", ["design"]),
    ("violates foreign key constraint", "referencing a parent row that does not exist or deleting a parent that is still referenced", "insert the parent first or use ON DELETE CASCADE carefully", ["design"]),
    ("relation does not exist", "a wrong table name, a table in another schema, or a mixed-case name that needs quoting", "check the search_path and use the schema-qualified, correctly quoted name", ["postgresql"]),
    ("operator does not exist: integer = character varying", "comparing different data types without a cast", "cast explicitly or fix the column type", ["postgresql"]),
    ("more than one row returned by a subquery used as an expression", "using = with a subquery that returns several rows", "use IN or ANY, or limit and aggregate the subquery", ["query-optimization"]),
    ("too many connections", "the application opening more connections than max_connections allows", "use a connection pool and lower the pool size", ["performance"]),
    ("division by zero", "dividing by a column that can be zero", "wrap the denominator in NULLIF(denominator, 0)", ["basics"]),
    ("ambiguous column name", "the same column name existing in several joined tables", "qualify the column with a table alias", ["joins"]),
    ("could not serialize access due to concurrent update", "a serialization conflict under repeatable read or serializable isolation", "retry the whole transaction", ["transactions"]),
    ("query suddenly became slow after loading more data", "stale planner statistics or a missing index", "run ANALYZE and check the plan with EXPLAIN ANALYZE", ["query-optimization"]),
]

TOPICS = [
    {
        "key": "sql",
        "name": "SQL",
        "count": 2200,
        "tags": ["sql"],
        "suffixes": ["", " in PostgreSQL", " in MySQL", " on a large table", " in a reporting query", " in production"],
        "concepts": CONCEPTS,
        "pairs": PAIRS,
        "howtos": HOWTOS,
        "errors": ERRORS,
    }
]
