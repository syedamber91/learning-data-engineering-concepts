---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 5
chapter_title: Encoding and Evolution
topic: Modes of Dataflow
type: subtopic
tags: [ddia2, rest, rpc, grpc, openapi, service-discovery, service-mesh, load-balancing]
sources:
  - raw/ch05.md
---
# Dataflow Through Services: REST and RPC
> RPC's promise was that a remote call could look like a local one. It cannot, for six specific reasons — and part of REST's appeal is that it never pretends otherwise.

## The Idea
The most common arrangement for processes communicating over a network is **clients and servers**: servers expose an API over the network — that API is a **service** — and clients connect to make requests. The web works this way: browsers make `GET` requests for HTML, CSS, JavaScript, and images, and `POST` requests to submit data, with the API being a standardized set of protocols and formats (HTTP, URLs, SSL/TLS, HTML). Because browsers, servers, and site authors mostly agree on these standards, any browser can access any website — at least in theory.

Browsers aren't the only clients: native mobile and desktop apps talk to servers, and client-side JavaScript in browsers makes HTTP requests. There the server's response is typically **not HTML for a human but data in an encoding convenient for client-side processing, most often JSON**. HTTP may be the transport, but the API on top is application-specific and both sides must agree on its details.

Services resemble databases in that they let clients submit and query data — but **while databases allow arbitrary queries in a query language, services expose an application-specific API allowing only inputs and outputs predetermined by the service's business logic**. That restriction provides **encapsulation**: services can impose fine-grained restrictions on what clients can and cannot do.

A key design goal of service-oriented/microservices architecture is making the application easier to change and maintain by making services **independently deployable and evolvable** — each owned by one team able to release frequently without coordinating with others. So old and new versions of servers and clients will run at the same time, and **the encoding must be compatible across versions of the service API**. As long as APIs remain compatible, teams can modify their systems however they like, which makes internal migrations of data, services, or even entire systems far easier.

## How It Works
**Web services.** When HTTP is the underlying protocol, the service is a **web service** — a slight misnomer, since they are used in several contexts: a client application on a user's device making requests over the public internet; one service calling another owned by the same organisation, often inside a private network; and one service calling another organisation's service over the internet, for backend data exchange, public APIs such as credit card processing, or OAuth for shared access to user data.

**REST** is the most popular design philosophy, building on HTTP's principles: simple data formats, URLs identifying resources, and HTTP features for cache control, authentication, and content type negotiation. An API following those principles is **RESTful**.

**IDLs and frameworks.** Code invoking a web service API must know which HTTP endpoint to query and what data format to send and expect — and even a RESTful service must communicate those details somehow. Developers use an **interface definition language** to define, document, and evolve endpoints and data models. The two most popular are **OpenAPI** (also known as **Swagger**), for web services sending and receiving JSON, and **Protocol Buffers**, for gRPC services. OpenAPI definitions are written in JSON or YAML and define endpoints, documentation, versions, and data models.

Developers must still implement the calls, and a **service framework** — **Spring Boot, FastAPI, gRPC** — is often adopted so they can focus on business logic while the framework handles routing, metrics, caching, and authentication. Many frameworks couple definition and server code: with **FastAPI** servers are written in code and an IDL is **generated automatically**; with **gRPC** the definition is written first and **server scaffolding is generated**. Both directions allow generating client libraries and SDKs in many languages, and IDL tools such as Swagger's can also **generate documentation, verify schema change compatibility, and provide a GUI for querying and testing services**.

**The problems with remote procedure calls.** Web services are the latest in a long line of network-API technologies, many much-hyped with serious problems: **EJB and Java RMI** are Java-only; **DCOM** is Microsoft-only; **CORBA** is excessively complex and provides neither backward nor forward compatibility; **SOAP and the WS-\* framework** aim for cross-vendor interoperability but are plagued by complexity and compatibility problems. All are based on **remote procedure calls (RPC)**, introduced in the 1970s, whose model tries to make a request to a remote service look like calling a local function — an abstraction called **location transparency**. Convenient-seeming, but **fundamentally flawed**, because a network request differs from a local call in six ways:
- A local call is **predictable**, succeeding or failing on parameters under your control. A network request is unpredictable for reasons entirely outside your control — the request or response may be lost, or the remote machine may be slow or unavailable — so applications must anticipate this, for example by retrying.
- A local call returns, throws, or never returns. A network request has **another outcome: returning without a result because of a timeout**, where you simply don't know what happened — you have no way of knowing whether the request got through.
- **Retrying may duplicate the action**, if the previous request got through and only the response was lost, unless you build deduplication (**idempotence**) into the protocol. Local calls don't have this problem.
- A local call takes about the same time each time. A network request is **much slower and wildly variable in latency** — under a millisecond at good times, many seconds when the network is congested or the service overloaded, for exactly the same work.
- Local calls can pass **references (pointers)** to objects in memory efficiently. A network request must encode all parameters into bytes — fine for immutable primitives, quickly problematic for larger amounts of data and mutable objects.
- Client and service may be in **different programming languages**, so the framework must translate datatypes between them, which gets ugly since not all languages have the same types — recall JavaScript's problems with numbers above 2⁵³.

**All of this means there is no point trying to make a remote service look too much like a local object, because it is a fundamentally different thing.** Part of REST's appeal is that it **treats state transfer over a network as a process distinct from a function call**.

**Load balancers, service discovery, and service meshes.** A client must know the address of the service it connects to — **service discovery**. The simplest approach, configuring an IP and port, works until the server goes offline, moves, or becomes overloaded, at which point the client needs manual reconfiguration. For availability and scalability, multiple instances usually run across machines, and spreading requests across them is **load balancing**. The options:
- **Hardware load balancers** — specialized datacenter equipment letting clients connect to a single host and port, routing connections to one of the servers and shifting traffic away from servers that fail.
- **Software load balancers** (**NGINX**, **HAProxy**) — the same behaviour as applications on standard machines.
- **DNS** — multiple IP addresses per domain name, with the client's network layer picking one. The drawback is that **DNS is designed to propagate changes slowly and to cache entries**, so with servers starting, stopping, or moving frequently, clients may see stale IPs.
- **Service discovery systems** — a centralized registry such as **etcd** or **Apache ZooKeeper** rather than DNS. A new instance registers its host and port plus metadata such as shard ownership and datacenter location, then sends periodic **heartbeats**. A client queries the registry for available endpoints, then connects directly. Compared to DNS this supports a **much more dynamic environment**, and the extra metadata **enables smarter load-balancing decisions**.
- **Service meshes** — combining software load balancing and service discovery. Unlike traditional software load balancers running on a separate machine, a mesh load balancer is deployed as an **in-process client library or a "sidecar" process/container on both client and server**. Clients connect to their own local load balancer, which connects to the server's, which routes to the local server process. Complicated, but: because everything is routed through local connections, **connection encryption can be handled entirely at the load balancer level**, shielding applications from SSL certificates and TLS; and meshes provide sophisticated **observability**, tracking which services call each other in real time, detecting failures, and tracking traffic load.

Which to use depends on the organisation: very dynamic environments with an orchestrator such as Kubernetes often run **Istio** or **Linkerd**; specialised infrastructure such as databases or messaging systems might need purpose-built load balancers; simpler deployments are best served by software load balancers.

## Trade-offs & Pitfalls
**Data encoding and evolution for RPC.** For evolvability, clients and servers must be changeable and deployable independently. Compared to databases, services allow a simplifying assumption: **it is reasonable to assume all servers are updated first and all clients second**, so you need **backward compatibility only on requests and forward compatibility on responses**.

Compatibility properties are inherited from the encoding: **gRPC (Protocol Buffers) and Avro RPC** evolve according to their format's rules; **RESTful APIs** most commonly use JSON for responses and JSON or URI/form-encoded parameters for requests, where adding optional request parameters and adding new response fields are usually compatible changes.

**The hard part is organisational.** RPC is often used across organisational boundaries, so a service provider **often has no control over its clients and cannot force them to upgrade** — compatibility must be maintained for a long time, perhaps indefinitely. When a breaking change is required, the provider frequently ends up **maintaining multiple versions of the API side by side**. And **there is no agreement on how API versioning should work**: for RESTful APIs, common approaches put a version number in the URL or the HTTP `Accept` header; for services using API keys, another option is storing a client's requested version on the server, updatable through a separate administrative interface.

## Examples & Systems
OpenAPI/Swagger and Protocol Buffers as service IDLs; Spring Boot, FastAPI, gRPC as frameworks; NGINX, HAProxy, etcd, ZooKeeper, Istio, Linkerd for load balancing and discovery; EJB, RMI, DCOM, CORBA, SOAP/WS-\* as the cautionary history.

## Since the 1st Edition
The 1st edition's [[Dataflow Through Services - REST and RPC]] covered web services, REST versus SOAP, the six problems with RPC, and RPC compatibility, all of which survive. **Substantially new:** the whole **IDL and service framework** section (OpenAPI/Swagger, FastAPI, Spring Boot, gRPC, code generation in both directions, compatibility verification tooling), and the entire **load balancing, service discovery, and service mesh** section (hardware/software load balancers, DNS's staleness problem, etcd/ZooKeeper registries with heartbeats and metadata, sidecar meshes handling TLS and observability, Istio and Linkerd). Neither appeared in the 1st edition, which discussed service communication almost purely as an encoding problem.

## Related
- up: [[Modes of Dataflow (2e)]] · chapter: [[Ch 05 - Encoding and Evolution (2e)]]
- [[Microservices and Serverless (2e)]] — the architecture these services compose
- [[Durable Execution and Workflows (2e)]] — what you build on top when a sequence of calls must be reliable
- [[Coordination Services (2e)]] — etcd and ZooKeeper examined properly
- 1st edition: [[Dataflow Through Services - REST and RPC]] — the same subtopic, half the scope
