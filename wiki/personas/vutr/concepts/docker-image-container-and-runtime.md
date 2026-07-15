---
persona: vutr
kind: concept
sources:
- raw/cloud-kubernetes-docker-infrastructure-tooling/i-spent-3-hours-to-understand-more.md
last_updated: '2026-07-15'
qc: passed
slug: docker-image-container-and-runtime
topics:
- cloud-kubernetes-docker-infrastructure-tooling
---

Vu's analogy for the image/container relationship: building a house needs an architect's blueprint first — the **image** is that blueprint, and the running application is the house. An image is obtained one of two ways: pulled as-is from a public or private registry, or built from a **Dockerfile** — a simple-syntax file declaring the steps to construct it, either from scratch or as customization on top of an existing image (his example: building a Python image by layering a Python installation onto a base Ubuntu image). Behind the scenes, an image is not one flat artifact but a stack of **layers**, each one roughly corresponding to a single Dockerfile instruction. That layering is also the caching mechanism: editing a Dockerfile and rebuilding only rebuilds the layers that actually changed, which is what keeps iterative image development fast.

A **container**, by the same analogy, is a runnable instance of an image — just as multiple houses can be built from one blueprint, multiple containers can be created from one image, managed via the Docker API or CLI. Underneath, containers are handled by a two-level runtime split: **containerd**, the high-level, long-running runtime responsible for the entire container lifecycle — including pulling images and managing instances of the lower-level runtime — and **runc**, the low-level runtime and reference implementation of the Open Container Initiative (OCI) spec, whose only job is to actually start a container by talking to the OS kernel; a `runc` process exits as soon as its container has started, unlike `containerd`, which keeps running.

Vu traces the concrete flow behind a single `docker run hello-world`: the Docker CLI converts the command into an API payload and POSTs it to the **Docker daemon** (`dockerd`); the daemon contacts `containerd`; `containerd` converts the target Docker image into an **OCI bundle** and instructs `runc` to build a new container from it; `runc` communicates with the OS kernel to assemble everything the container needs, and exits the moment the container has actually started. Every container is created by its own `runc` instance, but ongoing lifecycle management (not startup) stays with `containerd`.

Beyond single containers, **docker-compose** manages an entire multi-container application stack declared in one YAML compose file, rather than requiring separate commands per container. Vu's own example: deploying an Airflow environment, which in practice requires several coordinated components — scheduler, webserver, metadata database, worker, and a Redis instance — each needing its own container; docker-compose lets the whole stack be brought up and managed together instead of juggling individual container commands.

*See also: [[docker]] · [[kubernetes-workload-abstractions]]*
