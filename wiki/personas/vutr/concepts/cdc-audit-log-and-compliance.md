---
persona: vutr
kind: concept
sources:
- raw/change-data-capture-cdc-and-data-sourcing-additional/everything-you-need-to-know-about-741.md
last_updated: '2026-07-15'
qc: passed
slug: cdc-audit-log-and-compliance
topics:
- change-data-capture-cdc-and-data-sourcing
---

Because CDC (with the exception of query-based CDC) captures the entire history of changes rather than just current state, it doubles as a natural audit log for a database. Vu ties this directly to regulatory requirements that legally mandate detailed audit trails: HIPAA (the Health Insurance Portability and Accountability Act) requires that any access or modification to patient electronic health records be logged to protect patient privacy, while in finance, SOX (the Sarbanes-Oxley Act) requires public companies to control and audit changes to financial reporting data, and PCI DSS (the Payment Card Industry Data Security Standard) requires detailed logs of all access to cardholder data. Failure to comply with these regimes can mean legal action, which is what makes CDC's completeness a compliance feature and not just a technical nicety.

Beyond compliance, the same captured history helps with debugging and root-cause analysis. Because CDC records the exact operations that touched the data, it can reconstruct events after the fact — Vu's example is a product price that's suddenly `$0.00`: the captured log can show the exact `UPDATE` statement that caused it, something a current-state-only system could never reveal.

*See also: [[log-based-cdc]] · [[trigger-based-cdc]] · [[query-based-cdc]]*
