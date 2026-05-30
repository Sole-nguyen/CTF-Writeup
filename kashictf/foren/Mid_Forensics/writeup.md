# Mid Forensics Writeup

The capture contains only ICMP echo requests from `172.16.121.134` to `8.8.8.8`.  
The suspicious field is `ip.ttl`, which alternates between only two values: `64` and `65`.

This strongly suggests a bitstream encoding:
- `64 -> 0`
- `65 -> 1`

Taking TTL values in packet order, converting bits to bytes (8 bits per byte), and decoding produces:

`kashiCTF{ttl_stego_is_evil}`

## Reproduction

Run:

```bash
python3 solve.py
```

Or explicitly:

```bash
python3 solve.py "ttl_stego.pcap?token=..."
```

## Flag

`kashiCTF{ttl_stego_is_evil}`
