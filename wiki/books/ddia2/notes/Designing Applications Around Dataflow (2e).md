---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 13
chapter_title: A Philosophy of Streaming Systems
topic: Unbundling Databases
type: subtopic
tags: [ddia2, dataflow, spreadsheet, derivation-function, microservices, observer-pattern]
sources:
  - raw/ch13.md
---
# Designing Applications Around Dataflow
> VisiCalc had it in 1979: change a cell, and everything derived from it updates automatically. Most data systems still don't.

## The Idea
**Spreadsheets have powerful dataflow programming capabilities: put a formula in one cell — the sum of another column — and whenever any input changes, the result is automatically recalculated.** **This is exactly what we want at a data system level.** **When a record changes, any index for it should be automatically updated and any cached views or aggregations depending on it automatically refreshed** — **we should not have to worry about the technical details of how the refresh happens, and should be able to simply trust that it works correctly.**

**Most data systems still have something to learn from features VisiCalc already had in 1979.** **The difference is that today's systems need to be fault-tolerant, scalable, and capable of storing data durably** — **and need to integrate disparate technologies written by different groups of people over time, making use of existing libraries and services.** **It is unrealistic to expect all software to be developed using one particular language, framework, or tool.**

## How It Works
**Application code as a derivation function.** **When one dataset is derived from another it goes through some transformation function:**
- **A secondary index** has a straightforward one: **for each row, pick out the values in the indexed columns and sort by them.**
- **A full-text search index** applies **language detection, word segmentation, stemming or lemmatization, spelling correction, and synonym identification**, then builds an inverted index.
- **In an ML system, the model is derived from training data by feature extraction and statistical analysis functions**, and its output on new input is derived from that input and its learned parameters.
- **A cache** often contains **an aggregation of data in the form it will be displayed in a UI** — **so populating it requires knowledge of what fields the UI references, and UI changes may require updating the cache definition and rebuilding it.**

**The secondary-index derivation is so commonly required that it is built into databases as a core feature, invoked by `CREATE INDEX`.** **For full-text indexing, basic linguistic features may be built in, but sophisticated features often require domain-specific tuning.** **In machine learning, feature engineering is notoriously application-specific.**

**When the derivation function is not a standard cookie-cutter function, custom code is required — and this is where many databases struggle.** **Although relational databases support triggers, stored procedures, and user-defined functions, these have been somewhat of an afterthought in database design.**

**Separation of application code and state.** **In theory databases could be deployment environments for arbitrary application code, like an operating system. In practice they have turned out to be poorly suited**: **they do not fit well with modern application development requirements such as dependency and package management, version control, rolling upgrades, evolvability, monitoring, metrics, calls to network services, and integration with external systems.**

**Deployment and cluster management tools such as Kubernetes, Docker, Mesos, and YARN are designed specifically for running application code, and by focusing on doing one thing well they do it much better than a database that provides user-defined function execution as one of many features.**

**Most web applications are deployed as stateless services**, where any request can go to any server and the server forgets everything after responding. **Servers can then be added and removed at will — but the state has to go somewhere, typically a database.** **The trend has been to keep stateless application logic separate from state management: not putting application logic in the database and not putting persistent state in the application.** As functional programmers joke, **"We believe in the separation of Church and state."** (*Church is Alonzo Church, creator of the lambda calculus, which has no mutable state.*)

**In this model the database acts as a kind of mutable shared variable accessed synchronously over the network.** **The application reads and updates it, and the database provides durability, concurrency control, and fault tolerance.** **However, in most programming languages you cannot subscribe to changes in a mutable variable — you can only read it periodically.** **Unlike a spreadsheet, readers don't get notified when the value changes.** (You can implement notifications yourself — **the observer pattern** — **but most languages don't have it built in.**) **Databases have inherited this passive approach: if you want to know whether the content changed, often your only option is to poll. Subscribing to changes is only just beginning to emerge as a feature.**

**Dataflow: interplay between state changes and application code.** **Thinking in terms of dataflow implies renegotiating the relationship between application code and state management.** **Instead of treating a database as a passive variable manipulated by the application, we think about the interplay and collaboration between state, state changes, and the code that processes them: application code responds to state changes in one place by triggering state changes in another.**

**We have already seen this in CDC, the actor model, triggers, and incremental view maintenance.** **Unbundling the database means applying it to creating derived datasets outside the primary database** — caches, search indexes, machine learning, analytical systems — **using stream processing and messaging systems.**

**Maintaining derived data requires two properties log-based brokers provide:** **the order of state changes is often important**, since several views derived from one log must process events in the same order to remain consistent; **and fault tolerance is essential**, since losing a single message puts the derived dataset permanently out of sync. **Stable ordering and fault-tolerant processing are stringent demands, but much less expensive and more operationally robust than distributed transactions.** **Modern stream processors provide these guarantees at scale and allow application code to run as stream operators** — **doing the arbitrary processing that built-in derivation functions generally don't provide.** **Like Unix tools chained by pipes, stream operators can be composed to build large systems around dataflow, each taking streams of state changes as input and producing others as output.**

## Trade-offs & Pitfalls
**Stream processors and services.** **The dominant style breaks functionality into services communicating via synchronous requests such as REST APIs.** **The advantage over a monolith is primarily organizational scalability through loose coupling** — different teams work on different services, reducing coordination as long as they deploy independently.

**Composing stream operators has similar characteristics to microservices, but the underlying communication mechanism is very different: one-directional asynchronous message streams rather than synchronous request/response.**

**Besides better fault tolerance, dataflow systems can achieve better performance.** The book's example: **a customer purchasing an item priced in one currency but paid in another, requiring the current exchange rate.**
- **In the microservices approach, the purchase-processing code queries an exchange rate service or database for the current rate.**
- **In the dataflow approach, it subscribes to a stream of exchange rate updates ahead of time and records the current rate in a local database whenever it changes** — **so when processing the purchase it queries that local database.**

**The second replaces a synchronous network request with a query to a local database, possibly on the same machine or even in the same process.** **In the microservices approach you could cache the rate locally — but to keep the cache fresh you'd need to poll periodically or subscribe to changes, which is exactly the dataflow approach.**

**Not only is dataflow faster, it is also more robust to the failure of another service. The fastest and most reliable network request is no network request at all.** **Instead of RPC we now have a stream join between purchase events and exchange rate update events.**

**The join is time-dependent**: **if purchase events are reprocessed later, the exchange rate will have changed, so reconstructing the original output requires the historical rate at the original time of purchase.** **Whether you query a service or subscribe to a stream, you must handle this time dependence.**

**Subscribing to a stream of changes rather than querying current state brings us closer to a spreadsheet-like model of computation**: **when a piece of data changes, any derived data depending on it can swiftly be updated.** **Many open questions remain — around time-dependent joins, for instance — but building applications around dataflow ideas is a promising direction to explore.**

## Examples & Systems
VisiCalc (1979) as the precedent; Kubernetes, Docker, Mesos, YARN for running application code; the currency conversion example as microservices-versus-dataflow.

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Designing Applications Around Dataflow]] — the same spreadsheet analogy, the same derivation-function examples, the same separation-of-Church-and-state joke and its explanation, and the same currency-conversion comparison. Another very stable section, since the argument is about programming models rather than products.

## Related
- up: [[Unbundling Databases (2e)]] · chapter: [[Ch 13 - A Philosophy of Streaming Systems (2e)]]
- [[Uses of Stream Processing (2e)]] — incremental view maintenance as the spreadsheet model realised
- [[Microservices and Serverless (2e)]] — the architecture being compared
- [[Stream Joins (2e)]] — the time dependence this inherits
- 1st edition: [[Designing Applications Around Dataflow]] — the same subtopic
