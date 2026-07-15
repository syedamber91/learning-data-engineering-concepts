---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 12
chapter_title: The Future of Data Systems
topic: Doing the Right Thing
type: subtopic
tags: [ddia, algorithmic-bias, accountability, feedback-loops]
sources:
  - raw/ch12.md
---
# Predictive Analytics

> Predicting the weather is one thing; predicting whether a person will reoffend, default, or cost too much is a decision about their life — made by an opaque model that learned from a biased past.

## The Idea
Predictive analytics sits at the heart of "Big Data" hype, but there's a moral gulf between forecasting weather or disease spread and scoring individuals: will this convict reoffend, this borrower default, this customer file expensive claims? Organizations rationally prefer false "no"s — a missed opportunity is cheap, a bad loan expensive. Kleppmann's chain of concern: as algorithmic gatekeeping spreads, a person labeled risky (accurately or not) accumulates exclusions — from work, flights, insurance, housing, credit — an "algorithmic prison" that constrains freedom without proof of guilt or meaningful appeal, inverting the presumption of innocence that justice systems maintain.

## How It Works (and fails)
- **Bias in, bias out.** Algorithmic decisions aren't inherently worse than human ones — data could even correct instinctive prejudice — but with ML we no longer write the rules; we let them be inferred, and the learned patterns are opaque. Systematic bias in inputs is learned and *amplified* in outputs. Anti-discrimination law protects traits like ethnicity, age, gender, sexuality, disability, belief — yet proxies leak: in segregated neighborhoods, postal code or IP address effectively encodes race. Hoping biased data yields impartial output earned the satire "machine learning is like money laundering for bias." Models extrapolate the past; a discriminatory past becomes codified discrimination. A better future requires moral imagination, which only humans supply — data and models should be tools, not masters.
- **Accountability evaporates.** A human decision-maker can be held responsible; an appeal exists. Who answers when a self-driving car crashes, or a credit model systematically discriminates — and can you explain its decision to a judge? Old-style credit scores at least use one's *own* borrowing history and support error correction; ML scoring uses far wider, opaque inputs and stereotypes by similarity: "how did people like you behave?" Mis-bucketed individuals have almost no recourse. Statistical outputs are wrong in individual cases even when the distribution is right (average life expectancy of 80 predicts no one's death date) — blind faith in data-driven decisions is, in Kleppmann's word, dangerous. Analytics can target aid at the needy — or help predators find the desperate to sell them high-cost loans and worthless degrees.
- **Feedback loops.** Recommenders optimizing engagement create echo chambers that breed misinformation and polarization (already visible in elections). Worse, self-reinforcing spirals: employers screening by credit score push someone hit by misfortune into missed payments → worse score → no job → poverty → worse score. Poisonous assumptions camouflaged as mathematical rigor. Systems thinking — analyzing the whole sociotechnical loop, not just the code — can anticipate some of these: does the system amplify existing differences or counteract them?

## Examples & Systems
Recidivism, loan-default, and insurance scoring; hiring filters using credit scores; postal-code/IP as race proxies; social-media echo chambers; predatory lending discovered via analytics.

## Related
- up: [[Doing the Right Thing]] · chapter: [[Ch 12 - The Future of Data Systems]]
- [[Privacy and Tracking]] — the data collection that feeds these models
- [[Designing Applications Around Dataflow]] — ML models as derivation functions in the pipeline
- [[Batch and Stream Processing]] — the machinery that trains and applies them at scale
