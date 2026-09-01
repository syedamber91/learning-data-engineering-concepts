---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 1
chapter_title: Trade-Offs in Data Systems Architecture
type: topic
tags: [ddia2, cloud, self-hosting, build-vs-buy, iaas, saas]
sources:
  - raw/ch01.md
---
# Cloud Versus Self-Hosting
Underneath the cloud debate is the oldest question an organisation asks about anything it needs done: in-house or outsourced — build or buy? The book's answer is that this is ultimately a question about business priorities, with a common rule of thumb: things that are a core competency or competitive advantage should be done in-house; things that are non-core, routine, or commonplace should be left to a vendor. The extreme illustration is that almost no company fabricates its own CPUs, because buying them from semiconductor manufacturers is cheaper.

For software, two separate decisions are hiding inside "cloud": **who builds the software** and **who deploys it**. At one extreme sits bespoke software you write and run yourself; at the other, widely used cloud services or SaaS products built and operated by a vendor and reached only through a web interface or API. The middle ground is off-the-shelf software — open source or commercial — that you **self-host**: download MySQL and install it on a server you control, either on your own hardware (often called *on premises*, even when the server is in a rented datacenter rack) or on a cloud VM (**infrastructure as a service**, IaaS). There are further points along the spectrum, such as running a modified build of an open source system. Deployment tooling — whether you use an orchestration framework like Kubernetes — is deliberately out of scope, because other factors influence data-system architecture more.

## Subtopics
- [[Pros and Cons of Cloud Services (2e)]] — where the cost argument actually lands, and the six concrete ways loss of control bites.
- [[Cloud Native System Architecture (2e)]] — how the cloud changed system *design*, not just system *procurement*: layered services, separated storage and compute, multitenancy.
- [[Operations in the Cloud Era (2e)]] — DBAs to DevOps/SRE, and what operations becomes when the machines are hidden behind an API.

## Key Takeaways
- Cloud versus self-hosting is two questions (who builds, who operates) presented as one, and the interesting position is usually the middle: off-the-shelf software you deploy yourself.
- The economic argument is genuinely situation-dependent — predictable load plus existing skills favours owning; spiky load or unfamiliar systems favour renting.
- The bigger consequence is technical, not financial: **cloud native** designs perform better on the same hardware, recover faster, scale to load faster, and support larger datasets than lifted-and-shifted self-hosted systems.
- Cloud will not subsume everything. Many systems predate it, and specialist requirements — the example given is high-frequency trading needing full hardware control — keep in-house systems necessary.

## Since the 1st Edition
Entirely new. The 1st edition (2017) had essentially nothing on cloud-versus-self-hosting as an architectural axis, no treatment of cloud native design, and no serverless. This topic, plus [[Cloud Native System Architecture (2e)]], is one of the largest genuinely new bodies of material in the 2nd edition.

## Related
- chapter: [[Ch 01 - Trade-Offs in Data Systems Architecture (2e)]]
- [[Distributed Versus Single-Node Systems (2e)]] — cloud systems are intrinsically distributed, so this topic feeds directly into the next
- [[Cloud Data Warehouses (2e)]] — the clearest worked example of a cloud native data system
