---
persona: vutr
kind: entity
sources:
- raw/history-of-data-engineering-and-hadoop-ecosystem/the-history-of-data-engineering.md
- raw/history-of-data-engineering-and-hadoop-ecosystem/what-is-apache-hive.md
last_updated: '2026-07-15'
qc: passed
slug: hadoop-mapreduce
topics:
- history-of-data-engineering
---

Hadoop MapReduce traces to two Google papers: a 2003 paper introducing the Google File System, followed by a 2004 paper describing the MapReduce programming model for processing large amounts of data. Doug Cutting and Mike Cafarella built Hadoop MapReduce and HDFS based on those two papers — both were first developed under the Nutch web-crawler project before moving to the new Hadoop subproject in January 2006. Yahoo! adopted Apache Hadoop for its WebMap application that same year. Cloudera, founded in 2008, and Hortonworks, started in 2011, became the first companies to offer managed Hadoop services. The birth of Hadoop — especially HDFS — alongside this big-tech practice fueled the broader trend of gathering data in raw format in a central repository without pre-transformation, the idea that would later get the name "data lake."

MapReduce is a low-level programming model: it requires users to explicitly define Map and Reduce tasks, which is exactly the gap Apache Hive was built to close by letting people express that logic in a SQL-like language that Hive compiles down to MapReduce jobs (see [[apache-hive]]).

Despite its dominance, Hadoop's market cratered in the 2010s. Many enterprises invested heavily in Hadoop clusters but could not all benefit from them, because developers always had to tailor their processing logic to the MapReduce paradigm — this left the three leading Hadoop vendors (Cloudera, Hortonworks, and MapR) without a viable product to sell. Their responses diverged in a telling way: Cloudera rebranded "Hadoop" to mean the whole stack (application, Hadoop, HDFS) and built an RDBMS called Impala directly on top of HDFS without leveraging MapReduce; MapR built Drill directly on HDFS; and Meta created Presto to replace Hive (see [[presto]]). None of the three replacement engines was backed by MapReduce. Google itself moved its crawl processing from MapReduce to BigTable and announced in 2014 that MapReduce was no longer used anywhere in its technology stack. At the same time, the rise of cloud object storage — S3 (2006), Google Cloud Storage (2010) — with pay-as-you-go pricing and built-in scalability, availability, and durability made people question why they needed to buy servers and install, manage, and operate HDFS themselves at all.

*See also: [[apache-hive]] · [[presto]] · [[hive-object-storage-mismatch]] · [[kimball-vs-inmon]]*

## Related in the other wiki
- [[MapReduce and Distributed Filesystems]] — DDIA's mechanical account of the map/shuffle/reduce job pattern and HDFS substrate behind the system this note says enterprises struggled to tailor logic to.
- [[Comparing Hadoop to Distributed Databases]] — DDIA frames Hadoop's real novelty as being a general-purpose "distributed Unix" tolerant of any data format or processing model, a lens this note's account of vendors bolting SQL engines (Impala, Presto) directly onto HDFS fits neatly into.
- [[Beyond MapReduce]] — DDIA's survey of what came after raw MapReduce (higher-level APIs, Hive named explicitly) is the same shift this note traces at the vendor level: Hive, then Impala/Drill/Presto, then MapReduce's abandonment altogether.
