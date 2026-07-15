---
persona: vutr
kind: concept
sources:
- raw/airbnb-data-infrastructure/groupby-40-data-infrastructure-at.md
last_updated: '2026-07-15'
qc: passed
slug: airbnb-infrastructure-philosophy
topics:
- airbnb-data-infrastructure
---

Reading Airbnb's 2016 infrastructure writeup, Vu distills its data infrastructure decisions down to four stated philosophies: prefer open source (adopt open-source systems, and contribute back anything Airbnb builds that others would find useful — Airflow itself is the proof point, built internally and open-sourced later); prefer standard components and methods (the skill is knowing when a unique solution is actually warranted versus when an existing one will do); design for scalability (infrastructure has to keep pace with data growth, not just handle today's volume); and solve real problems by listening to colleagues (empathizing with internal data users drives what gets built, rather than building what's technically interesting).

These aren't abstract values — they show up directly in the choices [[airbnb-gold-silver-hadoop-clusters]] describes: Hive, Presto, and Spark are adopted open-source components rather than bespoke builds, while Airflow is the opposite case — a bespoke Airbnb build (open-sourced only afterward) rather than something adopted from outside; the Gold/Silver split and the later Cloudera partnership are "standard components" bets (paying for Cloudera's expertise rather than reinventing cluster monitoring); the Mesos-to-dedicated-instances migration and the EC2-instance-type-per-workload change are scalability fixes; and Airpal — a purpose-built web query tool on top of Presto — is a direct answer to what internal users needed to run SQL day to day.

*See also: [[airbnb-gold-silver-hadoop-clusters]] · [[minerva]]*
