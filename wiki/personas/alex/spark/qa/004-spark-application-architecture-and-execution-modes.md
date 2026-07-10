---
persona: alex
kind: concept
sources:
- vutr/spark-application-architecture-and-execution-modes
last_updated: '2026-07-10'
qc: passed
slug: 004-spark-application-architecture-and-execution-modes
topics:
- spark
learner: alex
source_note: spark-application-architecture-and-execution-modes
mastery: mastered
---

*What Alex understood:* Wait, so -- okay, I had this backwards. I thought "driver" and "worker" were just Spark's words for things, but you're saying the cluster manager has its *own* driver/master-and-worker idea for physical machines, and Spark's driver/executor stuff is a completely separate layer that just gets placed on top of it. Like the resource cluster is the apartment building, and the Spark cluster (driver + executors) is the specific tenants renting rooms in it -- the building manager (cluster manager) decides which rooms exist and hands out keys, but doesn't care what the tenants are doing inside.

And execution mode is really just one question: where does the driver -- the "who's in charge" process -- physically stand? In cluster mode, the driver moves into the building itself, onto one of the worker nodes, so it's inside the resource cluster the whole time. In client mode, the driver never leaves my machine -- it's like I'm managing the tenants by remote control from outside the building, and if I hang up the phone, the whole thing stops, because I AM the driver process. Local mode is just me pretending to have a building at all -- one machine, threads doing the "parallel" work.

Then the mechanism for cluster mode actually makes sense as a sequence: I write code and open a SparkSession, my client ships the JAR to the cluster manager and asks for driver resources, the cluster manager plants the driver on a worker node, THEN the driver (not me anymore) asks the cluster manager for executors, the cluster manager launches those and tells the driver where they are, the driver plans (logical plan turning into physical plan) before doing anything, THEN schedules tasks, executors report back, and when it's done the driver exits and its executors get torn down. So the driver isn't just a messenger -- it's the one actually running the show once it exists.

And Spark Connect is that same story, except the driver just... never goes home. It's a server that stays up permanently, and instead of me submitting a driver, I'm opening a session against one that's already running, and my DataFrame calls get turned into an unresolved plan and shipped over gRPC instead of being executed locally.

## Follow-up questions

**Alex:** So the driver isn't just a project manager telling executors what to do -- it's an actual process that has to physically live somewhere and stay running the whole time. That means in client mode, if my machine loses power or the network mid-job, the whole app dies even if the executors are still fine, right? Is that basically WHY cluster mode exists -- so the driver isn't stuck depending on my laptop staying on?

**vutr:** Yes on both counts, and the note backs up the mechanism directly. In client mode, the note is explicit: "the driver stays on the client machine that submitted the app. That client machine has to keep the driver process alive for the entire run." That's not a coordination detail -- the driver IS the process that owns the SparkSession, builds the execution plan, and schedules tasks; the mechanism has executors reporting task status back to the driver as they run, and the driver is what exits (successfully or not) when the app finishes. If that specific process disappears because its host machine goes down, there's no driver left to receive results, schedule remaining tasks, or exit the run cleanly -- even if individual executors out in the resource cluster are still alive and finishing their last assigned task. And yes, that dependency is exactly the gap cluster mode closes: in cluster mode the driver is launched on a worker node inside the resource cluster itself, alongside the executors, and "the cluster manager owns every process involved" -- so the driver's fate is tied to the resource cluster's reliability, not to whether your laptop stays plugged in.

**Alex:** You said a single worker node can host more than one executor -- so if I've got two totally different Spark apps running at the same time, could their executors end up crammed onto the exact same physical worker node, competing for the same CPU cores? How does the cluster manager actually decide where to place them?

**vutr:** (the wiki does not cover this — see open questions)
