---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 6
chapter_title: Replication
topic: Multi-Leader Replication
type: subtopic
tags: [ddia2, sync-engine, offline-first, local-first, collaboration, crdt, netcode]
sources:
  - raw/ch06.md
---
# Sync Engines and Local-First Software
> Every device is a leader and the network between them is extremely unreliable. That's not a degenerate case of multi-leader replication — it's the architecture behind Google Docs, Figma, and your calendar app.

## The Idea
Multi-leader replication also suits applications that must **keep working while disconnected from the internet**. Consider the calendar apps on your phone, laptop, and other devices: you need to see meetings (reads) and enter new ones (writes) at any time, regardless of connectivity, and changes made offline must sync with a server and your other devices when you're next online.

Here **every device has a local database replica that acts as a leader**, and there is an asynchronous multi-leader replication process — **sync** — between all your devices' replicas. The replication lag may be **hours or even days**, depending on when you have internet access. Architecturally this is **multi-leader replication between regions taken to the extreme**: each device is a "region," and the network between them is extremely unreliable.

## How It Works
**Real-time collaboration, offline-first, and local-first apps.** Many modern web apps offer real-time collaboration — **Google Docs and Sheets** for documents and spreadsheets, **Figma** for graphics, **Linear** for project management. What makes them responsive is that **user input is immediately reflected in the UI without waiting for a network round-trip**, and edits by one user reach collaborators with low latency.

**This is again a multi-leader architecture**: each browser tab with the shared file open is a replica, and updates are asynchronously replicated to the other users' devices. **Even if the app does not allow editing while offline, the fact that multiple users can make edits without waiting for a server response already makes it multi-leader.**

Both offline editing and real-time collaboration need similar infrastructure: capture the user's changes and either send them immediately (online) or store them locally for later (offline); receive collaborators' changes, merge them into the local copy, and update the UI. **If multiple users changed the file concurrently, conflict resolution logic may be needed.**

The vocabulary:
- A software library supporting this process is a **sync engine**. The idea has existed a long time but the term has recently gained attention.
- An application that lets a user keep editing while offline is **offline-first**.
- **Local-first software** refers to collaborative apps that are **not only offline-first but also designed to keep working even if the developer who made the software shuts down all their online services.** This is achieved by using a sync engine with an **open standard sync protocol for which multiple service providers are available**. **Git is a local-first collaboration system** — albeit one without real-time collaboration — since you can sync via GitHub, GitLab, or any other hosting service.

**Pros of sync engines.** The dominant way of building web apps today keeps **very little persistent state on the client** and makes requests to a server whenever data must be displayed or updated. With a sync engine you have **persistent state on the client and communication with the server moved into a background process**:
- **Speed.** Local data means the UI responds much faster than waiting for a service call. Some apps aim to respond in the **next frame of the graphics system — rendering within 16 ms on a 60 Hz display**.
- **Offline.** Valuable especially on mobile with intermittent connectivity. With a sync engine **an app doesn't need a separate offline mode: being offline is the same as having a very large network delay.**
- **A simpler programming model.** Every explicit service call requires error handling — if a request to update data fails, the UI must somehow reflect that. **A sync engine lets the app read and write local data, operations that almost never fail**, leading to a more declarative programming style.
- **Reactivity.** To display others' edits in real time you need notifications and efficient UI updates; **a sync engine combined with a reactive programming model is a good way to implement this.**

## Trade-offs & Pitfalls
- **Sync engines work best when all the data the user may need is downloaded in advance and stored persistently on the client.** That makes it available offline, but also means **sync engines are not suitable if the user has access to a very large amount of data**. Downloading all the files a user created is probably fine — one user doesn't generate that much — but **downloading an entire ecommerce catalog probably doesn't make sense**.
- **The idea is old.** The sync engine was pioneered by **Lotus Notes in the 1980s** (without the term), and app-specific sync, such as for calendars, has existed a long time. Today there are numerous general-purpose engines: some with a **proprietary backend** (Google Firestore, Realm, Ditto), others with an **open source backend**, making them suitable for local-first software (**PouchDB/CouchDB, Automerge, Yjs**).
- **Multiplayer video games have the same need** — respond immediately to local actions, reconcile with other players' actions received asynchronously. In game development the equivalent of a sync engine is called **netcode**, but its techniques are quite specific to games' requirements and don't directly carry over.

## Examples & Systems
Google Docs/Sheets, Figma, Linear (real-time collaboration); Git (local-first without real-time); Firestore, Realm, Ditto (proprietary backends); PouchDB/CouchDB, Automerge, Yjs (open source); Lotus Notes as the ancestor.

## Since the 1st Edition
Substantially new. The 1st edition had two short use-case sections — "clients with offline operation" (with the calendar example) and "collaborative editing" (mentioning Etherpad and Google Docs) — totalling perhaps a page. The 2nd edition expands this into a full subtopic with the **sync engine / offline-first / local-first vocabulary**, the four-way argument for sync engines as an application architecture, the data-volume limitation, the modern engine roster, and the netcode aside. This is one of the clearest additions reflecting Kleppmann's own research direction since 2017.

## Related
- up: [[Multi-Leader Replication (2e)]] · chapter: [[Ch 06 - Replication (2e)]]
- [[Dealing with Conflicting Writes (2e)]] — CRDTs and OT, which sync engines depend on
- [[Geographically Distributed Operation (2e)]] — the same architecture at server scale
- [[Distributed Versus Single-Node Systems (2e)]] — inherent distribution as a reason to distribute
