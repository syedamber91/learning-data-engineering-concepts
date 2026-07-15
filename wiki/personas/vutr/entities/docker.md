---
persona: vutr
kind: entity
sources:
- raw/cloud-kubernetes-docker-infrastructure-tooling/i-spent-3-hours-to-understand-more.md
last_updated: '2026-07-15'
qc: passed
slug: docker
topics:
- cloud-kubernetes-docker-infrastructure-tooling
---

Vu frames this post as the note he wishes he'd had on his first day as a data engineer, when Docker — a technology he'd never heard of — became his first assignment before he ever touched Spark, Hadoop, or Kafka; he calls his biggest early mistake "not researching which problem Docker solves" before jumping straight to implementation. That problem traces back to the virtual machine. VMs let multiple applications run securely and in isolation on one server, which was a genuine breakthrough over dedicating a physical server per application — but every VM still needs its own full OS, and that OS consumes CPU/RAM that could otherwise run applications, plus it needs patching, monitoring, and sometimes a license fee. Containers are the lighter-weight answer: they bundle an application with everything it needs to run (code, libraries, environment variables) but, unlike VMs, share the host's OS rather than each carrying their own — no per-container OS resource tax, no per-container patching, no license fee. Container technology existed before Docker but stayed complex and unfriendly; Docker, Inc. (a 2013 rebrand of dotCloud, built from tooling in the open-source Moby project) is what made containers usable enough to democratize.

Docker's own architecture is client-server. Users issue commands (`docker run`, etc.) through the Docker client, which talks to the **Docker daemon** (`dockerd`) — the process actually responsible for building, running, and managing containers. Client and daemon can live on the same machine or be split across separate ones, communicating via a REST API over either a UNIX socket or a network interface. When an image or a pull target isn't already local, Docker resolves it against a configured **registry** — the storage layer for Docker images. The best-known registry is the public Docker Hub, but private registries are common too; any `docker run` or `docker pull` looks up the image in whichever registry the client is pointed at.

The deeper mechanics of what happens once an image needs to become a running container — the image-as-blueprint/container-as-house analogy, the layered image format, and the containerd/runc split that actually creates a container — are covered in [[docker-image-container-and-runtime]], along with docker-compose, Docker's tool for managing a whole multi-container application stack (Vu's example: standing up an entire Airflow deployment — scheduler, webserver, metadata database, worker, Redis — from one YAML file instead of separate commands per container).

Vu's own next-step suggestions for someone past their first `docker run hello-world`: build a custom image from a Dockerfile rather than only ever pulling existing ones; stand up a complete Airflow environment via docker-compose; and dig into Docker networking specifically, which he says accounts for 77% of the Docker bugs he's personally hit (containers failing to see each other) — followed naturally by Docker volumes and then a first look at Kubernetes.

*See also: [[docker-image-container-and-runtime]] · [[kubernetes]] · [[cloud-compute-abstraction-spectrum]]*
