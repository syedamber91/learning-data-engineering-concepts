---
persona: alex
kind: concept
sources:
- vutr/spark-application-architecture-and-execution-modes
last_updated: '2026-07-10'
qc: passed
slug: spark-application-architecture-and-execution-modes
topics:
- spark
learner: alex
source_note: spark-application-architecture-and-execution-modes
mastery: mastered
---

Wait, so -- okay, I had this backwards. I thought "driver" and "worker" were just Spark's words for things, but you're saying the cluster manager has its *own* driver/master-and-worker idea for physical machines, and Spark's driver/executor stuff is a completely separate layer that just gets placed on top of it. Like the resource cluster is the apartment building, and the Spark cluster (driver + executors) is the specific tenants renting rooms in it -- the building manager (cluster manager) decides which rooms exist and hands out keys, but doesn't care what the tenants are doing inside.

And execution mode is really just one question: where does the driver -- the "who's in charge" process -- physically stand? In cluster mode, the driver moves into the building itself, onto one of the worker nodes, so it's inside the resource cluster the whole time. In client mode, the driver never leaves my machine -- it's like I'm managing the tenants by remote control from outside the building, and if I hang up the phone, the whole thing stops, because I AM the driver process. Local mode is just me pretending to have a building at all -- one machine, threads doing the "parallel" work.

Then the mechanism for cluster mode actually makes sense as a sequence: I write code and open a SparkSession, my client ships the JAR to the cluster manager and asks for driver resources, the cluster manager plants the driver on a worker node, THEN the driver (not me anymore) asks the cluster manager for executors, the cluster manager launches those and tells the driver where they are, the driver plans (logical plan turning into physical plan) before doing anything, THEN schedules tasks, executors report back, and when it's done the driver exits and its executors get torn down. So the driver isn't just a messenger -- it's the one actually running the show once it exists.

And Spark Connect is that same story, except the driver just... never goes home. It's a server that stays up permanently, and instead of me submitting a driver, I'm opening a session against one that's already running, and my DataFrame calls get turned into an unresolved plan and shipped over gRPC instead of being executed locally.

*Source: [[spark-application-architecture-and-execution-modes]] (vutr)*
