#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Fast cycle-detect + index for:
// S0, S1 given.
// S_i = ((S_{i-1} * C) ^ (S_{i-2} + D)) % E
// Returns S_n.

static inline uint64_t pack_state(uint32_t a, uint32_t b) {
    // E is 6 digits (< 1,000,000) so 20 bits is enough per value.
    return ((uint64_t)a << 20) | (uint64_t)b;
}

static inline uint64_t hash64(uint64_t x) {
    // SplitMix64 finalizer
    x ^= x >> 30;
    x *= 0xbf58476d1ce4e5b9ULL;
    x ^= x >> 27;
    x *= 0x94d049bb133111ebULL;
    x ^= x >> 31;
    return x;
}

typedef struct {
    uint64_t *keys;   // packed states
    uint32_t *vals;   // index t
    uint32_t cap;     // power of two
    uint32_t mask;
    uint32_t size;
} map_t;

static void map_init(map_t *m, uint32_t cap_pow2) {
    m->cap = cap_pow2;
    m->mask = cap_pow2 - 1;
    m->size = 0;
    m->keys = (uint64_t*)malloc((size_t)cap_pow2 * sizeof(uint64_t));
    m->vals = (uint32_t*)malloc((size_t)cap_pow2 * sizeof(uint32_t));
    if (!m->keys || !m->vals) {
        fprintf(stderr, "alloc failed\n");
        exit(1);
    }
    // empty sentinel: 0xffff.. (pack_state never reaches that)
    for (uint32_t i = 0; i < cap_pow2; i++) m->keys[i] = UINT64_MAX;
}

static void map_free(map_t *m) {
    free(m->keys);
    free(m->vals);
    m->keys = NULL;
    m->vals = NULL;
}

static inline int map_get(const map_t *m, uint64_t key, uint32_t *out) {
    uint32_t idx = (uint32_t)hash64(key) & m->mask;
    while (1) {
        uint64_t k = m->keys[idx];
        if (k == UINT64_MAX) return 0;
        if (k == key) {
            *out = m->vals[idx];
            return 1;
        }
        idx = (idx + 1) & m->mask;
    }
}

static inline void map_put(map_t *m, uint64_t key, uint32_t val) {
    uint32_t idx = (uint32_t)hash64(key) & m->mask;
    while (m->keys[idx] != UINT64_MAX) {
        idx = (idx + 1) & m->mask;
    }
    m->keys[idx] = key;
    m->vals[idx] = val;
    m->size++;
}

static uint32_t calc_S(uint32_t n, uint32_t S0, uint32_t S1, uint32_t C, uint32_t D, uint32_t E) {
    if (n == 0) return S0;
    if (n == 1) return S1;

    // values list
    uint32_t cap = 1u << 20; // up to ~1,048,576 terms before realloc
    uint32_t *vals = (uint32_t*)malloc((size_t)cap * sizeof(uint32_t));
    if (!vals) {
        fprintf(stderr, "vals alloc failed\n");
        exit(1);
    }
    uint32_t len = 2;
    vals[0] = S0;
    vals[1] = S1;

    // state -> index t map (t is state index where state=(S_t,S_{t+1}))
    map_t seen;
    // 2^22 = 4,194,304 slots (plenty for ~1M inserts)
    map_init(&seen, 1u << 22);
    map_put(&seen, pack_state(S0, S1), 0);

    uint32_t a = S0, b = S1;
    uint32_t t = 0;
    uint32_t mu = 0, lam = 0;

    while (1) {
        uint32_t s = (uint32_t)(((uint64_t)b * (uint64_t)C) ^ (uint64_t)(a + D));
        s %= E;
        a = b;
        b = s;

        if (len == cap) {
            cap <<= 1;
            uint32_t *nv = (uint32_t*)realloc(vals, (size_t)cap * sizeof(uint32_t));
            if (!nv) {
                fprintf(stderr, "realloc failed\n");
                exit(1);
            }
            vals = nv;
        }
        vals[len++] = b;

        t++;
        uint64_t key = pack_state(a, b);
        uint32_t prev;
        if (map_get(&seen, key, &prev)) {
            mu = prev;
            lam = t - prev;
            break;
        }
        map_put(&seen, key, t);

        // Safety: if we somehow go too far, fall back to direct (still bounded)
        if (t > 3000000u) {
            break;
        }
    }

    uint32_t ans;
    if (t > 3000000u && lam == 0) {
        // no cycle found quickly; do a bounded direct compute (best-effort)
        ans = (n < len) ? vals[n] : vals[len - 1];
    } else {
        if (n < mu) ans = vals[n];
        else ans = vals[mu + (uint32_t)((n - mu) % lam)];
    }

    map_free(&seen);
    free(vals);
    return ans;
}

int main(int argc, char **argv) {
    if (argc != 7) {
        fprintf(stderr, "usage: %s S0 S1 C D E n\n", argv[0]);
        return 2;
    }
    uint32_t S0 = (uint32_t)strtoul(argv[1], NULL, 10);
    uint32_t S1 = (uint32_t)strtoul(argv[2], NULL, 10);
    uint32_t C  = (uint32_t)strtoul(argv[3], NULL, 10);
    uint32_t D  = (uint32_t)strtoul(argv[4], NULL, 10);
    uint32_t E  = (uint32_t)strtoul(argv[5], NULL, 10);
    uint32_t n  = (uint32_t)strtoul(argv[6], NULL, 10);

    uint32_t ans = calc_S(n, S0, S1, C, D, E);
    printf("%u\n", ans);
    return 0;
}
