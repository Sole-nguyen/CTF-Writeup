#!/usr/bin/env python3
import re
import socket
import sys

HOST = "142.93.12.237"
PORT = 1337

RULE_RE = re.compile(r"'(.?)'\s*=>\s*([A-Z]+)")
FLAG_RE = re.compile(r"novruzctf\{[^\n\r}]*\}")

DEFAULT_OPS = {
    "+": "ADD",
    "-": "SUB",
    "*": "MUL",
    "/": "DIV",
    "%": "MOD",
    "^": "XOR",
    "$": "ADD",
    "@": "MOD",
}

PRECEDENCE = {
    "^": 1,
    "+": 2,
    "-": 2,
    "$": 2,
    "*": 3,
    "/": 3,
    "%": 3,
    "@": 3,
}


def apply_op(sym: str, a: int, b: int, rules: dict[str, str]) -> int:
    op = rules.get(sym, DEFAULT_OPS.get(sym))
    if op == "ADD":
        return a + b
    if op == "SUB":
        return a - b
    if op == "MUL":
        return a * b
    if op == "DIV":
        if b == 0:
            raise ZeroDivisionError("division by zero")
        return a // b
    if op == "MOD":
        if b == 0:
            raise ZeroDivisionError("modulo by zero")
        return a % b
    if op == "XOR":
        return a ^ b
    raise ValueError(f"Unsupported operator mapping: {sym!r} => {op!r}")


def tokenize(expr: str):
    i = 0
    n = len(expr)
    while i < n:
        c = expr[i]
        if c.isspace():
            i += 1
            continue
        if c.isdigit():
            j = i + 1
            while j < n and expr[j].isdigit():
                j += 1
            yield ("NUM", int(expr[i:j]))
            i = j
            continue
        if c in "()":
            yield (c, c)
            i += 1
            continue
        yield ("OP", c)
        i += 1


class Parser:
    def __init__(self, expr: str, rules: dict[str, str]):
        self.tokens = list(tokenize(expr))
        self.i = 0
        self.rules = rules

    def peek(self):
        if self.i >= len(self.tokens):
            return None
        return self.tokens[self.i]

    def pop(self):
        t = self.peek()
        if t is None:
            return None
        self.i += 1
        return t

    def parse_primary(self) -> int:
        t = self.pop()
        if t is None:
            raise ValueError("Unexpected end of expression")
        kind, value = t
        if kind == "NUM":
            return value
        if kind == "(":
            v = self.parse_expr(0)
            t2 = self.pop()
            if t2 is None or t2[0] != ")":
                raise ValueError("Missing closing parenthesis")
            return v
        if kind == "OP" and value == "-":
            return -self.parse_primary()
        raise ValueError(f"Unexpected token: {t}")

    def parse_expr(self, min_prec: int) -> int:
        left = self.parse_primary()
        while True:
            t = self.peek()
            if t is None or t[0] != "OP":
                break
            op = t[1]
            prec = PRECEDENCE.get(op, 2)
            if prec < min_prec:
                break
            self.pop()
            right = self.parse_expr(prec + 1)
            left = apply_op(op, left, right, self.rules)
        return left


def evaluate(expr: str, rules: dict[str, str]) -> int:
    p = Parser(expr, rules)
    v = p.parse_expr(0)
    if p.peek() is not None:
        raise ValueError(f"Trailing tokens in expression: {expr!r}")
    return v


def main():
    host = HOST
    port = PORT
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    rules: dict[str, str] = {}
    buf = ""

    with socket.create_connection((host, port), timeout=5) as s:
        # Minimize delayed small-packet latency on interactive round trips.
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.settimeout(2.0)
        while True:
            try:
                chunk = s.recv(8192)
            except socket.timeout:
                continue
            if not chunk:
                break
            text = chunk.decode("utf-8", errors="ignore")
            m = FLAG_RE.search(text)
            if m:
                print(m.group(0))
                return
            buf += text

            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                line = line.strip()
                if not line:
                    continue

                fm = FLAG_RE.search(line)
                if fm:
                    print(fm.group(0))
                    return

                if "RULES:" in line:
                    rules.clear()
                    for sym, opname in RULE_RE.findall(line):
                        rules[sym] = opname
                    continue

                if "Calculate:" in line:
                    expr = line.split("Calculate:", 1)[1].strip()
                    ans = evaluate(expr, rules)
                    s.sendall(f"{ans}\n".encode())

    fm = FLAG_RE.search(buf)
    if fm:
        print(fm.group(0))
        return


if __name__ == "__main__":
    main()
