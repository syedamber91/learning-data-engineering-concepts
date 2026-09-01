---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 1
chapter_title: Trade-Offs in Data Systems Architecture
type: topic
tags: [ddia2, oltp, olap, analytics, data-warehouse]
sources:
  - raw/ch01.md
---
# Operational Versus Analytical Systems
The split the whole book is organised around, and the book introduces it through *people* rather than technology. Three groups touch an organisation's data: backend engineers, who build services that read and modify data on behalf of users; business analysts, who produce reports that help management decide what to do; and data scientists, who hunt for novel insights or build data-driven product features. The last two share two habits — they *analyse* data that users and backend services generated, and they do not modify it — and that shared shape is enough to justify giving them their own systems. So **operational systems** are where data is created and changed, and **analytical systems** hold a read-only copy optimised for a completely different kind of query. Two newer roles sit on the seam: data engineers, who own the integration between the two sides and the wider data infrastructure, and analytics engineers, who model and transform data to make it useful downstream.

## Subtopics
- [[Characterizing Transaction Processing and Analytics (2e)]] — point queries versus aggregating scans; where the names OLTP and OLAP came from and what real-time analytics does to the boundary.
- [[Data Warehousing (2e)]] — why analysts get a separate database, how ETL fills it, and the drift from warehouse to lake to streams to reverse ETL.
- [[Systems of Record and Derived Data (2e)]] — a second, orthogonal cut: which data is authoritative and which can be rebuilt.

## Key Takeaways
- The distinction is about *access pattern and audience*, not about a product category. The same database engine can serve either role.
- Operational systems read and write; analytical systems only read (though they create derived datasets of their own).
- The separation exists for four practical reasons — data silos across many operational systems, schemas that suit OLTP badly suiting analytics, expensive queries hurting production performance, and network/compliance isolation — not merely for tidiness.
- The rise of specialised systems is a general trend: general-purpose tools cope fine at small scale, and the larger the scale, the more specialised systems become.
- HTAP (hybrid transactional/analytical processing) tries to erase the boundary, but most HTAP systems are an OLTP engine and an analytical engine behind one interface — so the distinction still explains how they work.

## Since the 1st Edition
The 1st edition made this same comparison, but buried it inside its storage chapter as [[Transaction Processing or Analytics]] — a detour taken to motivate column stores. The 2nd edition promotes it to the book's opening argument and reframes it around roles (backend engineer / analyst / data scientist / data engineer / analytics engineer) rather than around query shapes alone. HTAP, product/real-time analytics engines, and the analytics-engineer role are all new here.

## Related
- chapter: [[Ch 01 - Trade-Offs in Data Systems Architecture (2e)]]
- [[Data Storage for Analytics (2e)]] — the physical consequence of this split, two chapters later
- [[Batch Use Cases (2e)]] — ETL, analytics, and ML as the jobs that cross the divide
- 1st edition: [[Transaction Processing or Analytics]] — the same comparison in its old home
