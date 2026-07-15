---
persona: vutr
kind: entity
sources:
- raw/meta-data-stack-and-infrastructure/how-meta-solves-data-lineage-at-scale.md
last_updated: '2026-07-15'
qc: passed
slug: policy-zone-manager
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

The Policy Zone Manager (PZM) is Meta's lineage-powered privacy tool, part of the broader Privacy-Aware Infrastructure (PAI). It answers "where does my data come from, and where does it go?" by building on data-flow lineage graphs, letting developers identify every downstream asset reachable from a set of sources — which accelerates the rollout of privacy controls. As PAI scaled to all of Meta's apps, manually authored diagrams and spreadsheets couldn't keep up with the volume and pace of change, which is what forced Meta to automate lineage collection (see [[data-lineage-signal-collection]]); PZM is the tool that consumes the resulting lineage graphs and lets developers iteratively discover, exclude, and refine the specific data flows relevant to a privacy question, such as where a user's religious-views data actually travels.

*See also: [[data-lineage-signal-collection]]*
