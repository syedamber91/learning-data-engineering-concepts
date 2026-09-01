---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 9
chapter_title: The Trouble with Distributed Systems
topic: Unreliable Networks
type: subtopic
tags: [ddia2, tcp, quic, congestion-control, backpressure, udp]
sources:
  - raw/ch09.md
---
# The Limitations of TCP
> TCP is "reliable" in a specific, narrow sense. It will not tell you whether the application on the other side actually processed your data.

## The Idea
Network packets have a **maximum size, generally a few kilobytes**, but many applications send messages too big for one packet. They most often use **TCP** to establish a connection that **breaks large data streams into packets and reassembles them on the receiving side.** (*Most of this applies also to **QUIC**, to **SCTP** used in WebRTC, to BitTorrent's uTP, and to other transport protocols.*)

**TCP is often described as providing "reliable" delivery**: it detects and retransmits dropped packets, detects reordered packets and puts them back in order, and detects corruption with a simple checksum. It also works out how fast it can send data so the transfer is as quick as possible without overloading the network or receiver — **congestion control, flow control, or backpressure.**

## How It Works
**Writing to a socket doesn't send data immediately** — it goes into a buffer managed by your operating system. **When the congestion control algorithm decides it has capacity**, it takes the next packet's worth from the buffer and passes it to the network interface. **The packet passes through several switches and routers**, and eventually the receiving OS places its data in a receive buffer and **sends an acknowledgment back. Only then does the receiving OS notify the application that more data has arrived.**

## Trade-offs & Pitfalls
**So does TCP's reliability mean we no longer need to worry? Unfortunately not.**
- **TCP decides a packet must have been lost if no acknowledgment arrives within a timeout, but it can't tell whether the outbound packet or the acknowledgment was lost.** It can resend, **but can't guarantee the new packet gets through** — if the network cable is unplugged, **TCP can't plug it back in for you.** Eventually, after a configurable timeout, **it gives up and signals an error to the application.**
- **TCP's deduplication and retransmission apply to only a single connection**, so **if the application reconnects and retransmits, data could be duplicated.**
- **If a connection is closed with an error** — the remote node crashed, or the network was interrupted — **you have no way of knowing how much data was actually processed by the remote node.**
- **Even an acknowledgment that a packet was delivered means only that the operating system kernel on the remote node received it; the application may have crashed before handling that data.** **If you want to be sure a request was successful, you need a positive response from the application itself.**

**Nevertheless TCP is very useful**, providing a convenient way of sending and receiving messages too big for one packet, and once established a connection can carry multiple requests and responses — **usually by sending a header indicating the following message's length in bytes, then the message.** HTTP and many RPC protocols work like this.

## Examples & Systems
TCP, QUIC, SCTP (WebRTC), BitTorrent uTP; HTTP and RPC protocols using length-prefixed framing.

## Since the 1st Edition
**New as a subtopic.** The 1st edition mentioned TCP's retransmission and congestion control in passing within [[Unreliable Networks]] and [[Timeouts and Unbounded Delays]], but did not systematically separate **what TCP guarantees (bytes in order, on one connection) from what it cannot guarantee (that the application processed them)** — the distinction that motivates application-level acknowledgments and idempotence throughout the book. QUIC is also new.

## Related
- up: [[Unreliable Networks (2e)]] · chapter: [[Ch 09 - The Trouble with Distributed Systems (2e)]]
- [[Timeouts and Unbounded Delays (2e)]] — where TCP's queueing shows up as latency
- [[Backpressure (2e)]] — the cross-cutting concept note
- [[Exactly-Once Message Processing Revisited (2e)]] — why application-level acknowledgment matters
