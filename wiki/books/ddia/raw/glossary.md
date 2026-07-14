---
book: Designing Data-Intensive Applications
author: Martin Kleppmann
source: local PDF, converted with markitdown
section: glossary
---

Glossary
Please note that the definitions in this glossary are short and sim‐
ple, intended to convey the core idea but not the full subtleties of a
term. For more detail, please follow the references into the main
text.
asynchronous up with it. Also known as flow control. See
Not waiting for something to complete “Messaging Systems” on page 441.
(e.g., sending data over the network to
batch process
another node), and not making any
A computation that takes some fixed (and
assumptions about how long it is going to
usually large) set of data as input and pro‐
take. See “Synchronous Versus Asynchro‐
duces some other data as output, without
nous Replication” on page 153, “Synchro‐
modifying the input. See Chapter 10.
nous Versus Asynchronous Networks” on
page 284, and “System Model and Reality” bounded
on page 306.
Having some known upper limit or size.
Used for example in the context of net‐
atomic
work delay (see “Timeouts and Unboun‐
1. In the context of concurrent operations:
ded Delays” on page 281) and datasets
describing an operation that appears to
(see the introduction to Chapter 11).
take effect at a single point in time, so
another concurrent process can never Byzantine fault
encounter the operation in a “half- A node that behaves incorrectly in some
finished” state. See also isolation. arbitrary way, for example by sending
contradictory or malicious messages to
2. In the context of transactions: grouping
other nodes. See “Byzantine Faults” on
together a set of writes that must either all
page 304.
be committed or all be rolled back, even if
faults occur. See “Atomicity” on page 223 cache
and “Atomic Commit and Two-Phase
A component that remembers recently
Commit (2PC)” on page 354.
used data in order to speed up future
reads of the same data. It is generally not
backpressure complete: thus, if some data is missing
Forcing the sender of some data to slow from the cache, it has to be fetched from
down because the recipient cannot keep some underlying, slower data storage
Glossary | 553

CAP theorem
system that has a complete copy of the ized view. See “Single-Object and Multi-
| data. |     |     | Object  Operations”  | on  page  | 228  and |
| ----- | --- | --- | -------------------- | --------- | -------- |
“Deriving several views from the same
CAP theorem
event log” on page 461.
A widely misunderstood theoretical result
| that is not useful in practice. See “The |     |     | derived data |     |     |
| ---------------------------------------- | --- | --- | ------------ | --- | --- |
CAP theorem” on page 336. A dataset that is created from some other
data through a repeatable process, which
causality
you could run again if necessary. Usually,
The dependency between events that ari‐
derived data is needed to speed up a par‐
| ses  when  | one  thing  “happens  | before” |     |     |     |
| ---------- | --------------------- | ------- | --- | --- | --- |
ticular kind of read access to the data.
another thing in a system. For example, a
Indexes, caches, and materialized views
later event that is in response to an earlier are  examples  of  derived  data.  See  the
| event, or builds upon an earlier event, or |     |     | introduction to Part III. |     |     |
| ------------------------------------------ | --- | --- | ------------------------- | --- | --- |
should be understood in the light of an
| earlier event. See “The “happens-before” |     |     | deterministic |     |     |
| ---------------------------------------- | --- | --- | ------------- | --- | --- |
relationship  and  concurrency”  on  page Describing a function that always pro‐
186 and “Ordering and Causality” on page duces the same output if you give it the
| 339. |     |     | same input. This means it cannot depend |     |     |
| ---- | --- | --- | --------------------------------------- | --- | --- |
on random numbers, the time of day, net‐
consensus
work communication, or other unpredict‐
| A  fundamental  | problem  | in  distributed |     |     |     |
| --------------- | -------- | --------------- | --- | --- | --- |
able things.
| computing,  | concerning  | getting  several |     |     |     |
| ----------- | ----------- | ---------------- | --- | --- | --- |
distributed
nodes to agree on something (for exam‐
ple, which node should be the leader for a Running on several nodes connected by a
database cluster). The problem is much network. Characterized by partial failures:
harder than it seems at first glance. See some part of the system may be broken
“Fault-Tolerant Consensus” on page 364. while other parts are still working, and it
is often impossible for the software to
| data warehouse |     |     | know what exactly is broken. See “Faults |     |     |
| -------------- | --- | --- | ---------------------------------------- | --- | --- |
A database in which data from several dif‐
and Partial Failures” on page 274.
ferent OLTP systems has been combined
| and prepared to be used for analytics pur‐ |     |     | durable |     |     |
| ------------------------------------------ | --- | --- | ------- | --- | --- |
poses. See “Data Warehousing” on page Storing  data  in  a  way  such  that  you
| 91. |     |     | believe it will not be lost, even if various |     |     |
| --- | --- | --- | -------------------------------------------- | --- | --- |
faults occur. See “Durability” on page 226.
declarative
| Describing the properties that something |     |     | ETL |     |     |
| ---------------------------------------- | --- | --- | --- | --- | --- |
should have, but not the exact steps for Extract–Transform–Load. The process of
how to achieve it. In the context of quer‐ extracting data from a source database,
ies, a query optimizer takes a declarative transforming it into a form that is more
query and decides how it should best be suitable for analytic queries, and loading it
executed. See “Query Languages for Data” into a data warehouse or batch processing
| on page 42. |     |     | system. See “Data Warehousing” on page |     |     |
| ----------- | --- | --- | -------------------------------------- | --- | --- |
91.
denormalize
| To  introduce  | some  amount  | of  redun‐ | failover |     |     |
| -------------- | ------------- | ---------- | -------- | --- | --- |
dancy  or  duplication  in  a  normalized In systems that have a single leader, fail‐
dataset, typically in the form of a cache or over is the process of moving the leader‐
index,  in  order  to  speed  up  reads.  A ship role from one node to another. See
denormalized value is a kind of precom‐ “Handling Node Outages” on page 156.
puted query result, similar to a material‐
554  |  Glossary

locality
| fault-tolerant |     |     | index |     |     |
| -------------- | --- | --- | ----- | --- | --- |
Able  to  recover  automatically  if  some‐ A data structure that lets you efficiently
thing  goes  wrong  (e.g.,  if  a  machine search for all records that have a particu‐
crashes or a network link fails). See “Reli‐ lar value in a particular field. See “Data
| ability” on page 6. |     |     | Structures That Power Your Database” on |     |     |
| ------------------- | --- | --- | --------------------------------------- | --- | --- |
page 70.
flow control
| See backpressure. |     |     | isolation |     |     |
| ----------------- | --- | --- | --------- | --- | --- |
In the context of transactions, describing
follower
the degree to which concurrently execut‐
A replica that does not directly accept any
ing transactions can interfere with each
| writes  from  | clients,  but  only  | processes |     |     |     |
| ------------- | -------------------- | --------- | --- | --- | --- |
other. Serializable isolation provides the
data changes that it receives from a leader. strongest guarantees, but weaker isolation
Also known as a secondary, slave, read levels are also used. See “Isolation” on
replica, or hot standby. See “Leaders and
page 225.
Followers” on page 152.
join
full-text search
To bring together records that have some‐
Searching  text  by  arbitrary  keywords, thing in common. Most commonly used
| often  with  | additional  features  | such  as |     |     |     |
| ------------ | --------------------- | -------- | --- | --- | --- |
in the case where one record has a refer‐
matching similarly spelled words or syno‐
ence to another (a foreign key, a docu‐
nyms. A full-text index is a kind of secon‐
ment reference, an edge in a graph) and a
dary index that supports such queries. See
query needs to get the record that the ref‐
“Full-text search and fuzzy indexes” on erence points to. See “Many-to-One and
| page 88.                                  |                        |              | Many-to-Many Relationships” on page 33  |     |     |
| ----------------------------------------- | ---------------------- | ------------ | --------------------------------------- | --- | --- |
| graph                                     |                        |              | and “Reduce-Side Joins and Grouping” on |     |     |
| A  data                                   | structure  consisting  | of  vertices | page 403.                               |     |     |
| (things that you can refer to, also known |                        |              | leader                                  |     |     |
as nodes or entities) and edges (connec‐ When data or a service is replicated across
tions from one vertex to another, also
several nodes, the leader is the designated
| known  | as  relationships  | or  arcs).  See |     |     |     |
| ------ | ------------------ | --------------- | --- | --- | --- |
replica that is allowed to make changes. A
“Graph-Like Data Models” on page 49.
leader may be elected through some pro‐
tocol, or manually chosen by an adminis‐
hash
|              |                  |                | trator.  Also  | known  as  | the  primary  or |
| ------------ | ---------------- | -------------- | -------------- | ---------- | ---------------- |
| A  function  | that  turns  an  | input  into  a |                |            |                  |
master. See “Leaders and Followers” on
random-looking number. The same input
| always returns the same number as out‐ |     |     | page 152. |     |     |
| -------------------------------------- | --- | --- | --------- | --- | --- |
put. Two different inputs are very likely to
linearizable
have  two  different  numbers  as  output, Behaving as if there was only a single copy
although it is possible that two different of data in the system, which is updated by
inputs produce the same output (this is
|            |                                  |     | atomic  | operations.  See  | “Linearizability” |
| ---------- | -------------------------------- | --- | ------- | ----------------- | ----------------- |
| called  a  | collision).  See  “Partitioning  | by  |         |                   |                   |
on page 324.
Hash of Key” on page 203.
locality
idempotent
A performance optimization: putting sev‐
Describing an operation that can be safely
eral pieces of data in the same place if they
retried; if it is executed more than once, it
are frequently needed at the same time.
has the same effect as if it was only exe‐
See “Data locality for queries” on page 41.
cuted once. See “Idempotence” on page
478.
Glossary  |  555

lock
lock records. See “Transaction Processing or
A mechanism to ensure that only one Analytics?” on page 90.
thread, node, or transaction can access
OLTP
something, and anyone else who wants to
Online transaction processing. Access
access the same thing must wait until the
pattern characterized by fast queries that
lock is released. See “Two-Phase Locking
read or write a small number of records,
(2PL)” on page 257 and “The leader and
usually indexed by key. See “Transaction
the lock” on page 301.
Processing or Analytics?” on page 90.
log
partitioning
An append-only file for storing data. A
Splitting up a large dataset or computa‐
write-ahead log is used to make a storage
tion that is too big for a single machine
engine resilient against crashes (see “Mak‐
into smaller parts and spreading them
ing B-trees reliable” on page 82), a log-
across several machines. Also known as
structured storage engine uses logs as its
sharding. See Chapter 6.
primary storage format (see “SSTables
and LSM-Trees” on page 76), a replication percentile
log is used to copy writes from a leader to
A way of measuring the distribution of
followers (see “Leaders and Followers” on
values by counting how many values are
page 152), and an event log can represent
above or below some threshold. For
a data stream (see “Partitioned Logs” on
example, the 95th percentile response
page 446).
time during some period is the time t such
that 95% of requests in that period com‐
materialize
plete in less than t, and 5% take longer
To perform a computation eagerly and
than t. See “Describing Performance” on
write out its result, as opposed to calculat‐
page 13.
ing it on demand when requested. See
“Aggregation: Data Cubes and Material‐ primary key
ized Views” on page 101 and “Materializa‐
A value (typically a number or a string)
tion of Intermediate State” on page 419.
that uniquely identifies a record. In many
applications, primary keys are generated
node
by the system when a record is created
An instance of some software running on
(e.g., sequentially or randomly); they are
a computer, which communicates with
not usually set by users. See also secondary
other nodes via a network in order to
index.
accomplish some task.
quorum
normalized
The minimum number of nodes that need
Structured in such a way that there is no
to vote on an operation before it can be
redundancy or duplication. In a normal‐
considered successful. See “Quorums for
ized database, when some piece of data
reading and writing” on page 179.
changes, you only need to change it in one
place, not many copies in many different rebalance
places. See “Many-to-One and Many-to-
To move data or services from one node
Many Relationships” on page 33.
to another in order to spread the load
fairly. See “Rebalancing Partitions” on
OLAP
page 209.
Online analytic processing. Access pattern
characterized by aggregating (e.g., count, replication
sum, average) over a large number of
Keeping a copy of the same data on sev‐
eral nodes (replicas) so that it remains
556 | Glossary

total order
accessible if a node becomes unreachable. skew in “Timestamps for ordering events”
See Chapter 5. on page 291.
schema
split brain
A description of the structure of some
data, including its fields and datatypes. A scenario in which two nodes simultane‐
Whether some data conforms to a schema ously believe themselves to be the leader,
can be checked at various points in the and which may cause system guarantees
data’s lifetime (see “Schema flexibility in to be violated. See “Handling Node Out‐
the document model” on page 39), and a ages” on page 156 and “The Truth Is
schema can change over time (see Chap‐ Defined by the Majority” on page 300.
ter 4).
stored procedure
secondary index A way of encoding the logic of a transac‐
An additional data structure that is main‐ tion such that it can be entirely executed
tained alongside the primary data storage on a database server, without communi‐
and which allows you to efficiently search cating back and forth with a client during
for records that match a certain kind of the transaction. See “Actual Serial Execu‐
condition. See “Other Indexing Struc‐ tion” on page 252.
tures” on page 85 and “Partitioning and
stream process
Secondary Indexes” on page 206.
A continually running computation that
serializable consumes a never-ending stream of events
A guarantee that if several transactions as input, and derives some output from it.
execute concurrently, they behave the See Chapter 11.
same as if they had executed one at a time,
synchronous
in some serial order. See “Serializability”
The opposite of asynchronous.
on page 251.
system of record
shared-nothing
A system that holds the primary, authori‐
An architecture in which independent
tative version of some data, also known as
nodes—each with their own CPUs, mem‐
the source of truth. Changes are first writ‐
ory, and disks—are connected via a con‐
ten here, and other datasets may be
ventional network, in contrast to shared-
derived from the system of record. See the
memory or shared-disk architectures. See
introduction to Part III.
the introduction to Part II.
timeout
skew
One of the simplest ways of detecting a
1. Imbalanced load across partitions, such
fault, namely by observing the lack of a
that some partitions have lots of requests response within some amount of time.
or data, and others have much less. Also However, it is impossible to know
known as hot spots. See “Skewed Work‐ whether a timeout is due to a problem
loads and Relieving Hot Spots” on page with the remote node, or an issue in the
205 and “Handling skew” on page 407. network. See “Timeouts and Unbounded
2. A timing anomaly that causes events to Delays” on page 281.
appear in an unexpected, nonsequential
total order
order. See the discussions of read skew in
A way of comparing things (e.g., time‐
“Snapshot Isolation and Repeatable Read”
stamps) that allows you to always say
on page 237, write skew in “Write Skew
which one of two things is greater and
and Phantoms” on page 246, and clock
which one is lesser. An ordering in which
Glossary | 557

transaction
some things are incomparable (you can‐ transaction.  See  “Atomic  Commit  and
not say which is greater or smaller) is Two-Phase Commit (2PC)” on page 354.
| called  a  partial  | order.  See  “The  | causal |     |     |     |
| ------------------- | ------------------ | ------ | --- | --- | --- |
two-phase locking (2PL)
order is not a total order” on page 341.
|             |     |     | An  algorithm  | for  achieving   | serializable   |
| ----------- | --- | --- | -------------- | ---------------- | -------------- |
| transaction |     |     | isolation      | that  works  by  | a  transaction |
Grouping  together  several  reads  and acquiring a lock on all data it reads or
writes into a logical unit, in order to sim‐ writes, and holding the lock until the end
plify  error  handling  and  concurrency of the transaction. See “Two-Phase Lock‐
| issues. See Chapter 7. |     |     | ing (2PL)” on page 257. |     |     |
| ---------------------- | --- | --- | ----------------------- | --- | --- |
| two-phase commit (2PC) |     |     | unbounded               |     |     |
An algorithm to ensure that several data‐ Not having any known upper limit or size.
base nodes either all commit or all abort a The opposite of bounded.
558  |  Glossary

