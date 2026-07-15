---
persona: vutr
kind: entity
sources:
- raw/lakehouse-architecture-and-practical-builds/the-data-lake-warehouse-and-lakehouse.md
- raw/lakehouse-architecture-and-practical-builds/data-architecture-101.md
- raw/lakehouse-architecture-and-practical-builds/do-we-need-the-lakehouse-architecture.md
last_updated: '2026-07-15'
qc: passed
slug: data-lake
topics:
- data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa
---

Vu traces the data lake to the Big Data era: companies like Yahoo, Google, and Amazon kept hitting the limits of the relational [[data-warehouse]] as data volume and format diversity grew, and Yahoo's response was Apache Hadoop — MapReduce for processing, HDFS for storage, based on Google's MapReduce and GFS papers. The data lake is the storage half of that response: it stores vast amounts of data in its native format (first on HDFS, later on cloud object storage) without requiring a schema definition in advance, so unstructured data like video, audio, and text documents can land there without concern for format. That's the schema-on-read trade Vu contrasts against the warehouse's schema-on-write.

The lake's early ambition was bigger than storage, though: people tried to replace the data warehouse outright by running processing directly on top of the lake. Vu is blunt about how that went — the approach had serious drawbacks, and the data lake soon became a "data swamp" for lack of the management features a warehouse provides: data discovery, data quality and integrity guarantees, ACID constraints, and DML support. The industry's actual answer was not to replace the warehouse but to combine the two: ingest raw data into the lake, then move a transformed subset into the warehouse via ETL for reporting, while advanced use cases like machine learning could still read the raw lake data directly. Vu says this two-tier lake-plus-warehouse pattern is what dominated from the mid-2000s through the 2020s — until the same "swamp" problem, now solved with real transactional metadata layers instead of bare files, resurfaced as the pitch for the [[lakehouse]].

*See also: [[data-warehouse]] · [[kappa-architecture]] · [[lambda-architecture]] · [[data-mesh]] · [[medallion-architecture]] · [[lakehouse]]*

## Open questions
- **source gap**: the posts name Apache Hadoop/HDFS as the origin of the data lake and object storage (S3/GCS) as the later replacement, but don't spell out why object storage displaced HDFS specifically (durability/availability numbers, cost, or the coupling of HDFS's NameNode to a single machine are not discussed in these posts).
