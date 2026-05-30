# insider-info (misc) - UMDCTF

## Idea

Server logic:

1. It creates a random `secret` of length `819`.
2. If queried with `<index>.inside.info` (TXT), it returns `secret[index]`.
3. If queried with `<secret split into 63-char labels>.inside.info` (TXT), it returns the flag.

So the solve is a 2-query attack:

1. Send one DNS packet containing 819 TXT questions (`0.inside.info` ... `818.inside.info`) to leak all chars.
2. Rebuild the expected giant subdomain and query it.

## Gotchas

### 1) Truncated first response

The first answer is large. Without EDNS, DNS payload can be truncated and dnslib parsing fails.

Fix: add OPT record with large UDP size:

```python
req.add_ar(EDNS0(udp_len=65535))
```

### 2) Domain too long when building second query

The final domain is ~844 bytes on wire (>253 normal DNS name limit), so `dnslib` refuses to pack it as `DNSRecord`.

Fix: build raw DNS bytes manually for query #2 (header + QNAME + QTYPE/QCLASS), then send it through the challenge's 2-byte length-prefixed wrapper.

## Exploit

`solve.py` now:

1. Uses exact-length reads with `recvn`.
2. Uses EDNS for the leak query.
3. Crafts the oversized second DNS query manually as raw bytes.
4. Prints the flag from returned TXT record.

## Flag

`UMDCTF{5Ur31Y_N0_0N3_W111_N071C3_MY_1N51D3r_7r4D1N6}`
