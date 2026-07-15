---
persona: vutr
kind: entity
sources:
- raw/lakehouse-architecture-and-practical-builds/bauplan-operate-your-lakehouse-with.md
last_updated: '2026-07-15'
qc: passed
slug: bauplan
topics:
- data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa
---

Bauplan is a Function-as-a-Service (FaaS) platform, built by a New York/San Francisco team, that Vu frames as an attempt to answer a question he'd had since using AWS Lambda in 2021: could a data pipeline get the same "define logic, forget infrastructure" simplicity as a Lambda function? Vu's diagnosis of why *existing* FaaS platforms fail at this job for data pipelines names three specific failure modes: scaling (generic FaaS runtimes reuse the same instance size for a 10GB and a 1TB input, so out-of-memory errors are common), large intermediate I/O (chaining functions into a DAG means passing dataframes through object storage between every step, which is slow and expensive to serialize), and a slow feedback loop (data-science work needs rapid iteration, but AWS Lambda's only real observability is CloudWatch).

Bauplan's answer is to spin up new, independent instances for every run rather than reusing warm instances, letting the same pipeline scale from a 10GB run to a 100GB run without carrying over stale sizing assumptions. Architecturally it splits into a Control Plane (CP), which lives in Bauplan's own VPC and only handles metadata across tenants, and a Data Plane (DP), a fleet of cloud VMs per customer — deployable inside the customer's own VPC (BYOC) — running a Golang worker binary that is the only Bauplan component that ever touches customer data. When a user submits a run, the CP parses the Python/SQL code, reconstructs the DAG topology into a logical plan, and — notably — refuses to run DAGs referencing nonexistent tables, wrong snapshots, or malformed Python, unlike dbt. The CP then compiles that logical plan into a physical plan (containerized runtime instructions plus a mapping of dataframes to physical object-storage tables) and dispatches it to workers. A bidirectional gRPC connection between customer and worker gives users live `print`/`logging` output even though the code runs inside Bauplan's cloud VMs.

**Caching.** Because instances are stateless and thrown away after each run, Bauplan caches at two levels to keep re-runs fast: it avoids re-installing Python packages across runs, and it tracks changes in both code and data to decide whether an intermediate dataframe produced by an upstream function can be reused rather than recomputed. It goes further with column-level reuse — if a first run reads four columns and a second run needs those four plus one more, Bauplan reuses the cached four and fetches only the new column from source. Cache invalidation works because Bauplan's data is stored in immutable Iceberg files: dataframe changes are identified via data commits, so the cache knows precisely when an underlying table has actually changed.

**Data exchange via Arrow.** Bauplan represents intermediate dataframes as Apache Arrow tables rather than moving them exclusively through object storage the way generic FaaS platforms do. Depending on where the producing and consuming functions run, Bauplan picks the fastest available sharing mechanism: shared memory or local disk for functions on the same worker (no copy at all — Vu's example: 10GB of intermediate data read by four functions on one worker costs 10GB of RAM, not 10GB × 4), or Arrow Flight (gRPC-based streaming) across workers. Vu's claim is that this makes inter-function data movement "hundreds of times faster" than S3-backed exchange alone.

**Storage.** Beyond the pipeline runtime, Bauplan offers a full lakehouse storage layer built on Iceberg plus [[project-nessie]] — Nessie specifically to add cross-table atomic commits on top of Iceberg's table-level-only ACID guarantees, giving users a Git-like branch/commit/merge workflow over their data.

*See also: [[trino]] · [[project-nessie]] · [[lakehouse]] · [[apache-arrow]]*

## Open questions
- **source gap**: the post names Bauplan's per-run resource elasticity (new instances scale from 10GB to 100GB runs) but doesn't explain the provisioning mechanism — how instance sizing is actually determined or requested per run.
