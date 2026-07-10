---
persona: alex
kind: concept
sources:
- vutr/consumer-groups-and-partition-assignment
last_updated: '2026-07-10'
qc: passed
slug: consumer-groups-and-partition-assignment
topics:
- kafka
learner: alex
source_note: consumer-groups-and-partition-assignment
mastery: mastered
---

Okay let me try to say this back like it actually makes sense to me. So the whole thing is basically a group project. If one worker can't keep up with the pile of work, you don't send that one worker to the gym to get buff — you just add more workers to the team, and everyone on the team wears the same team name tag, which is the group ID.

But here's the twist I almost missed: the work doesn't get sliced up message-by-message. It gets sliced up by *partition* — like the topic is already pre-cut into a fixed number of drawers, and each drawer can only be opened by one teammate at a time inside your team. So if there are 4 drawers and I bring 5 teammates, the 5th guy just stands around doing nothing, because there's no free drawer for him. More people than drawers = wasted people. And if a totally *different* team walks in, they get their own full set of the same drawers — the "one person per drawer" rule is only about people wearing the *same* team tag.

Then there's the management side, and this is where I'd mix things up. The **Coordinator** is a broker — like the HR person of the team — it doesn't do the assigning itself, it just tracks who's on the team and notices when someone quits or dies. The **leader** is actually one of the consumers, specifically whoever showed up to join *first*, and *that* person is the one who hands out the drawer assignments to everybody. And the way HR knows you didn't just vanish is you keep sending a little "still here!" ping — a heartbeat — on a side thread. Stop pinging and after a few seconds they assume you're dead and reshuffle the drawers, but during those few seconds your drawers are just frozen. If you quit politely and say "I'm leaving," they reshuffle right away instead of waiting.

And the leader can hand out drawers a few different ways — Range packs consecutive drawers per topic and dumps leftovers on the first people, Round Robin spreads them out evenly but reshuffles a lot, and Sticky tries not to disturb people who are already settled.

*Source: [[consumer-groups-and-partition-assignment]] (vutr)*
