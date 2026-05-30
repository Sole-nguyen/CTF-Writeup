# Midnight Relay

A fallback relay was brought online during a midnight outage.

## Protocol Spec
- Transport: raw TCP stream.
- Banner: `midnight-relay\n`.
- Packet format:
  - `op` (`u8`)
  - `key` (`u8`)
  - `len` (`u16`, little-endian)
  - `payload` (`len` bytes)
- Integrity:
  - `key` is a 1-byte checksum of payload with an internal rolling epoch.
  - Invalid key packets are dropped silently.

## Operations
- `0x11` forge:
  - payload: `idx|size(u16)|tag_len|tag`
- `0x22` tune:
  - payload: `idx|off(u16)|n(u16)|blob`
- `0x33` observe:
  - payload: `idx|off(u16)|n(u16)`
  - returns `n` bytes from shard memory
- `0x44` shred:
  - payload: `idx`
- `0x55` sync:
  - payload: `idx|token(u32)`
- `0x66` fire:
  - payload: `idx`
