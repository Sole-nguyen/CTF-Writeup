#define _POSIX_C_SOURCE 200809L
#include <arpa/inet.h>
#include <errno.h>
#include <netdb.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

static const uint64_t MOD = 1000000007ULL;

static int connect_tcp(const char *host, const char *port) {
  struct addrinfo hints;
  memset(&hints, 0, sizeof(hints));
  hints.ai_family = AF_UNSPEC;
  hints.ai_socktype = SOCK_STREAM;

  struct addrinfo *res = NULL;
  int rc = getaddrinfo(host, port, &hints, &res);
  if (rc != 0) {
    fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rc));
    return -1;
  }

  int sock = -1;
  for (struct addrinfo *p = res; p; p = p->ai_next) {
    sock = socket(p->ai_family, p->ai_socktype, p->ai_protocol);
    if (sock < 0)
      continue;
    if (connect(sock, p->ai_addr, p->ai_addrlen) == 0)
      break;
    close(sock);
    sock = -1;
  }
  freeaddrinfo(res);
  return sock;
}

static inline uint64_t reduce_once(uint64_t v) {
  if (v >= MOD)
    v -= MOD;
  return v;
}

static inline uint64_t op_add101(uint64_t v) {
  v += 101ULL;
  if (v >= MOD)
    v -= MOD;
  return v;
}

static inline uint64_t op_mul3(uint64_t v) {
  v = reduce_once(v);
  v = v * 3ULL;
  if (v >= MOD)
    v -= MOD;
  if (v >= MOD)
    v -= MOD;
  return v;
}

static inline uint64_t op_collatz(uint64_t v) {
  if ((v & 1ULL) == 0ULL) {
    v = v / 2ULL;
    // With our value range, v < MOD holds here.
    if (v >= MOD)
      v %= MOD;
    return v;
  }
  v = reduce_once(v);
  v = v * 3ULL + 1ULL;
  if (v >= MOD)
    v -= MOD;
  if (v >= MOD)
    v -= MOD;
  if (v >= MOD)
    v -= MOD;
  return v;
}

int main(void) {
  const char *HOST = "34.131.216.230";
  const char *PORT = "1339";

  int sock = connect_tcp(HOST, PORT);
  if (sock < 0) {
    perror("connect");
    return 1;
  }

  enum { MODE_HEADER = 0, MODE_STREAM = 1, MODE_AFTER = 2 } mode = MODE_HEADER;
  uint64_t V = 0;
  int have_start = 0;
  int saw_stream_marker = 0;

  char line[4096];
  size_t linelen = 0;

  uint8_t buf[1 << 16];
  ssize_t n;
  while ((n = recv(sock, buf, sizeof(buf), 0)) > 0) {
    size_t i = 0;
    while (i < (size_t)n) {
      if (mode == MODE_HEADER) {
        uint8_t c = buf[i++];
        if (linelen + 1 < sizeof(line))
          line[linelen++] = (char)c;

        if (c == '\n') {
          line[linelen] = '\0';

          if (!have_start) {
            const char *p = strstr(line, "Starting Value (V) = ");
            if (p) {
              V = strtoull(p + strlen("Starting Value (V) = "), NULL, 10);
              have_start = 1;
            }
          }

          if (strstr(line, "[INCOMING STREAM]"))
            saw_stream_marker = 1;

          linelen = 0;

          if (saw_stream_marker) {
            // The next bytes (after this newline) are the stream itself.
            mode = MODE_STREAM;
          }
        }
      } else if (mode == MODE_STREAM) {
        // Process operation bytes until newline ends the stream.
        for (; i < (size_t)n; i++) {
          uint8_t c = buf[i];
          if (c == '\n' || c == '\r') {
            i++; // consume newline
            mode = MODE_AFTER;

            if (!have_start) {
              fprintf(stderr, "Did not parse starting V.\n");
              close(sock);
              return 2;
            }

            char out[64];
            int outlen = snprintf(out, sizeof(out), "%llu\n", (unsigned long long)V);
            if (send(sock, out, (size_t)outlen, 0) < 0) {
              perror("send");
              close(sock);
              return 3;
            }
            break;
          }

          switch (c) {
          case '@':
            V = op_add101(V);
            break;
          case '#':
            V = op_mul3(V);
            break;
          case '$':
            V = V ^ 4242ULL;
            break;
          case '%':
            V = op_collatz(V);
            break;
          case '&':
            V = (~V) & 0xFFFFFULL;
            break;
          default:
            // Ignore anything unexpected (shouldn't happen).
            break;
          }
        }
      } else {
        // MODE_AFTER: just print the remaining server output.
        fwrite(buf + i, 1, (size_t)n - i, stdout);
        fflush(stdout);
        i = (size_t)n;
      }
    }
  }

  if (n < 0) {
    perror("recv");
    close(sock);
    return 4;
  }

  close(sock);
  return 0;
}
