---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 1
chapter_title: Trade-Offs in Data Systems Architecture
type: topic
tags: [ddia2, gdpr, privacy, data-minimization, compliance, ethics]
sources:
  - raw/ch01.md
---
# Data Systems, Law, and Society
The architecture of data systems is shaped not only by technical goals but by the human needs of the organisations they support — and increasingly by obligations to people outside those organisations entirely. Since 2018 the GDPR has given residents of many European countries greater control and legal rights over their personal data, with similar regulations adopted elsewhere (the CCPA, for instance), and AI-specific rules such as the EU AI Act placing further restrictions on how personal data may be used. Even outside regulated areas, there is growing recognition of the effects computer systems have on people: social media changed how individuals consume news, which influences political opinions and may affect election outcomes, and automated systems increasingly make consequential decisions about who gets a loan or insurance, who is invited to interview, and who is suspected of a crime.

The book's position is that everyone working on such systems shares responsibility for considering ethical impact and legal compliance. Not everyone must become an expert in law and ethics, but a basic awareness is **just as important as foundational knowledge in distributed systems**.

## Key Takeaways
- **Legal requirements reach into system design.** The GDPR grants a right to erasure — sometimes called the right to be forgotten — but many data systems rely on immutable constructs such as append-only logs. How do you delete data in the middle of a file that is supposed to be immutable? How do you handle deletion of data already absorbed into derived datasets, such as ML training data? These are genuine new engineering problems, and the book poses them as open.
- **There is no compliance checklist.** No clear guidance exists on which technologies or architectures count as GDPR-compliant. The regulation deliberately avoids mandating technologies, because they change faster than law; the legal texts set out high-level principles subject to interpretation. So there is no simple answer, only a lens to apply.
- **Storage cost is not the storage bill.** We store data when we think its value exceeds the cost of storing it — but the cost extends beyond the S3 invoice to the risk of liability and reputational damage from a leak, and the risk of legal costs and fines for non-compliant storage or processing.
- **Some data is a safety risk to hold.** Governments or police may compel companies to hand over data. Where data could reveal criminalized behaviour — the book names homosexuality in several Middle Eastern and African countries, and seeking an abortion in several US states — storing it creates real safety risks for users. Travel to a clinic could be revealed by location data, or even by a log of the user's IP addresses over time.
- **Data minimization** (the German term *Datensparsamkeit*) is the resulting principle: once risks are counted, some data is simply not worth storing and should be deleted. This runs directly counter to the "big data" philosophy of storing everything speculatively — and it fits GDPR, which mandates that personal data may be collected only for a specified, explicit purpose, cannot later be used for another, and must not be kept longer than necessary.
- **Business pressure reinforces it.** Credit card companies require payment processors to meet PCI standards with frequent independent audits; many software buyers now require vendors to comply with SOC Type 2, also verified by third-party audit.

## Since the 1st Edition
New as an opening-chapter topic, and its placement is the point. The 1st edition confined ethics to the very last section of its final chapter, where it read as an afterword. The 2nd edition states the obligation in Chapter 1, treats legal requirements as design inputs on the same footing as latency or durability, and then gives them a full chapter of their own at the end ([[Ch 14 - Doing the Right Thing (2e)]]). GDPR, CCPA, and the EU AI Act are all post-2017 and could not have appeared in the 1st edition.

## Related
- chapter: [[Ch 01 - Trade-Offs in Data Systems Architecture (2e)]]
- [[Ch 14 - Doing the Right Thing (2e)]] — the deep treatment of ethics, bias, privacy, and surveillance
- [[Privacy and Use of Data (2e)]] — the specific question of what data may legitimately be used for
- [[Systems of Record and Derived Data (2e)]] — why erasure is hard once data has been derived
