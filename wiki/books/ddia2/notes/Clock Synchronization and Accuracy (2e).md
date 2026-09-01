---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 9
chapter_title: The Trouble with Distributed Systems
topic: Unreliable Clocks
type: subtopic
tags: [ddia2, ntp, clock-drift, leap-second, ptp, gps, mifid]
sources:
  - raw/ch09.md
---
# Clock Synchronization and Accuracy
> Monotonic clocks need no synchronization. Time-of-day clocks do — and our methods for getting a clock to tell the correct time aren't nearly as reliable or accurate as you might hope.

## The Idea
**Hardware clocks and NTP can be fickle beasts.** The book's catalogue of why:

## How It Works
- **Quartz drift.** The quartz clock in a typical computer **runs faster or slower than it should, varying with temperature.** **Google assumes clock drift of up to 200 ppm** for its servers — **6 ms of drift for a clock resynchronized every 30 seconds, or 17 seconds for one resynchronized once a day.** **This limits the best accuracy achievable even when everything is working correctly.**
- **Forcible resets.** If a computer's clock **differs too much from an NTP server, it may refuse to synchronize or be forcibly reset** — and applications observing the time before and after **may see time go backward or suddenly jump forward.**
- **Silent misconfiguration.** **If a node is accidentally firewalled off from NTP servers, the misconfiguration may go unnoticed for some time**, during which drift adds up to large discrepancies. **Anecdotal evidence suggests this does happen in practice.**
- **Network delay bounds accuracy.** **NTP synchronization can be only as good as the network delay**, so accuracy is limited on a congested network. **One experiment showed a minimum error of 35 ms is achievable over the internet**, though **occasional spikes can lead to errors of around a second.** Large delays can cause the NTP client to give up entirely.
- **Wrong servers.** **Some NTP servers are wrong or misconfigured, reporting time off by hours.** Clients mitigate this by querying several and ignoring outliers — **nevertheless, it's somewhat worrying to bet the correctness of your systems on the time you were told by a stranger on the internet.**
- **Leap seconds** produce a minute that is 59 or 61 seconds long, **messing up timing assumptions in systems not designed for them.** **The fact that leap seconds have crashed many large systems shows how easy it is for incorrect assumptions about clocks to sneak in.** The best handling may be to **make NTP servers "lie" by performing the adjustment gradually over a day — smearing** — although actual server behaviour varies. **Leap seconds will no longer be used from 2035, so this problem will fortunately go away.**
- **Virtual machines.** **The hardware clock is virtualized**, and when a core is shared, **each VM is paused for tens of milliseconds while another runs** — which from the application's point of view **manifests as the clock suddenly jumping forward.** **An NTP client inside the VM doesn't know when a pause occurs, so it may report clock accuracy incorrectly.**
- **Untrusted devices.** On devices you don't fully control — mobile or embedded — **you probably cannot trust their hardware clocks at all.** **Some users deliberately set an incorrect date and time, for example to cheat in games.**

## Trade-offs & Pitfalls
- **Very good accuracy is achievable if you care enough to invest significant resources.** **The MiFID II European regulation requires high-frequency trading funds to synchronize clocks to within 100 microseconds of UTC**, to help debug market anomalies such as flash crashes and detect market manipulation. **This needs special hardware (GPS receivers and/or atomic clocks), the Precision Time Protocol (PTP), and careful deployment and monitoring.**
- **Relying on GPS alone can be risky, because GPS signals can easily be jammed** — **in some locations, such as close to military facilities, this happens frequently.**
- **Some cloud providers have begun offering high-accuracy clock synchronization for their VMs**, but **clock synchronization still requires a lot of care**: a misconfigured NTP daemon or a firewall blocking NTP traffic means **clock error due to drift can quickly become large.**

## Examples & Systems
Google's 200 ppm drift assumption; MiFID II's 100-microsecond requirement; PTP, GPS receivers, atomic clocks; leap-second smearing.

## Since the 1st Edition
Very close to the 1st edition's [[Clock Synchronization and Accuracy]] — the same eight-item catalogue, the same Google drift figures, the same MiFID II example, and the same smearing recommendation. **Updated:** the note that **leap seconds will be abolished from 2035**, **GPS jamming near military facilities**, and **cloud providers now offering high-accuracy clock synchronization** — three genuinely post-2017 developments.

## Related
- up: [[Unreliable Clocks (2e)]] · chapter: [[Ch 09 - The Trouble with Distributed Systems (2e)]]
- [[Relying on Synchronized Clocks (2e)]] — what goes wrong when software trusts these clocks
- [[Monotonic Versus Time-of-Day Clocks (2e)]] — the clock that doesn't need any of this
- 1st edition: [[Clock Synchronization and Accuracy]] — the same subtopic
