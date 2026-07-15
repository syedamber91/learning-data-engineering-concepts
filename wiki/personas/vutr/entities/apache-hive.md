---
persona: vutr
kind: entity
sources:
- raw/history-of-data-engineering-and-hadoop-ecosystem/what-is-apache-hive.md
- raw/history-of-data-engineering-and-hadoop-ecosystem/the-history-of-data-engineering.md
last_updated: '2026-07-15'
qc: passed
slug: apache-hive
topics:
- history-of-data-engineering
---

Meta released a paper in 2009 officially introducing Hive as an open-source data warehousing solution built on top of Hadoop, though Meta had been working with Hive before that, as Hadoop was gaining its place in the big-data world. Facebook developed Apache Hive in 2010 (the history-of-data-engineering timeline dates its public arrival there) to add a SQL abstraction over [[hadoop-mapreduce|MapReduce]]. In Hadoop's prime, MapReduce was the obvious choice for data processing, but the model is low-level and requires users to explicitly define Map and Reduce tasks. Hive's pitch was to let users express that logic in a SQL-like declarative language — HiveQL — which Hive translates into MapReduce jobs, and to give that SQL something to run against by providing a simple table abstraction on top of the files sitting in HDFS. Later, Netflix also used Hive for its data warehouse architecture. Because it was open-source, Hive gained wide attention and ended up supported by most query engines, but it eventually showed real limitations and was gradually replaced by newer table formats (see [[hive-object-storage-mismatch]]).

**Architecture.** Hive has several primary components. Users interact with it through Interfaces — the CLI, a web UI, JDBC, or ODBC. The Hive Thrift Server exposes a client API for executing HiveQL statements; Thrift clients generated in different languages build the standard JDBC (Java) and ODBC (C++) drivers, plus scripting drivers such as a Python one. The Metastore is the system catalog, providing the metadata every other component needs. The Driver manages a HiveQL statement's entire lifecycle from compilation through optimization to execution, communicating with the Compiler to translate the statement into a DAG of MapReduce jobs; the Driver then submits that DAG's jobs, in topological order, to the Execution Engine — Hadoop, in Hive's original design.

**Data model.** Hive organizes data into folders: each table maps to an HDFS directory, and each partition of a table maps to a subdirectory of it — a `sales` table partitioned by `date` produces subdirectories like `sales/date=2025-01-01`, `sales/date=2025-01-02`, and so on. Within a partition, data can additionally be split into buckets, distributed by the hash value of a column, with each bucket stored as its own file in the partition directory. Hive supports common column types (int, float, strings, dates, bool) plus complex types like array and map, and users can define their own custom types programmatically.

**Query language.** HiveQL supports select, join, aggregate, union, and subqueries, plus DDL statements for creating tables with serialization formats, partitioning schemes, and bucketing columns. Users load data from external sources and insert query results into Hive tables via DML statements — but data modification can only happen at the partition level, so even a small change requires replacing an entire partition (see [[hive-object-storage-mismatch]] for why). Users can also define UDFs in Java to extend Hive's processing.

**The Metastore.** Like a database catalog, the Hive Metastore records metadata whenever users create Hive tables and serves it to any component that needs it. It stores Database objects (a table's namespace, defaulting to 'default'), Table objects (column list and types, owner, SerDe serializer/deserializer information, and storage information including physical data location, data formats, and bucketing), and Partition objects (which can themselves carry columns, SerDe, and storage information). The Metastore itself is backed by a traditional relational database such as MySQL or PostgreSQL.

Hive doesn't have the adoption it once did — by 2025, an organization is unlikely to still be running it — but its role in the lakehouse lineage is foundational rather than incidental: it pioneered the table abstraction on top of a pile of files in the lake, and without it we might not see the growth of Delta Lake, Iceberg, and Hudi, which took the same goal and re-engineered it for object storage (see [[open-table-formats]]).

*See also: [[hadoop-mapreduce]] · [[hive-object-storage-mismatch]] · [[presto]] · [[kimball-vs-inmon]]*

## Related in the other wiki
- [[Beyond MapReduce]] — DDIA names Hive explicitly among the high-level, increasingly declarative APIs (with Pig, Cascading, Crunch) that emerged to spare users from writing raw MapReduce jobs, the same motivation this note traces through Hive's SQL-to-MapReduce compiler.
- [[MapReduce Querying]] — DDIA's account of using a declarative query language over a MapReduce-executed join is the general pattern HiveQL's compilation into a DAG of MapReduce jobs instantiates concretely.
