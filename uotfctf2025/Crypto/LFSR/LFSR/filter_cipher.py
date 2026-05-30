import itertools

# WG-style transformation ANF on 7 variables (x0..x6).
WG_ANF_TERMS = [
    (1, 2, 3, 4, 5, 6),
    (0, 1, 2, 3, 5),
    (0, 1, 2, 4, 5),
    (0, 1, 3, 4, 5),
    (1, 2, 3, 4, 5),
    (0, 1, 2, 4, 6),
    (0, 2, 3, 4, 6),
    (1, 2, 3, 4, 6),
    (0, 1, 2, 5, 6),
    (0, 2, 3, 5, 6),
    (1, 2, 3, 5, 6),
    (0, 3, 4, 5, 6),
    (1, 3, 4, 5, 6),
    (0, 1, 2, 4),
    (0, 1, 2, 5),
    (1, 2, 3, 5),
    (0, 1, 4, 5),
    (1, 3, 4, 5),
    (2, 3, 4, 5),
    (1, 2, 3, 6),
    (0, 1, 4, 6),
    (1, 2, 4, 6),
    (0, 3, 4, 6),
    (1, 3, 4, 6),
    (1, 2, 5, 6),
    (0, 3, 5, 6),
    (1, 4, 5, 6),
    (2, 4, 5, 6),
    (3, 4, 5, 6),
    (0, 1, 2),
    (0, 1, 4),
    (0, 2, 4),
    (1, 2, 4),
    (0, 1, 5),
    (0, 3, 5),
    (1, 3, 5),
    (2, 3, 5),
    (3, 4, 5),
    (0, 1, 6),
    (0, 3, 6),
    (2, 3, 6),
    (3, 4, 6),
    (0, 5, 6),
    (2, 5, 6),
    (4, 5, 6),
    (2, 3),
    (3, 4),
    (0, 5),
    (3, 5),
    (1, 6),
    (3, 6),
    (4, 6),
    (0,),
    (3,),
    (5,),
    (6,),
]


def eval_anf(bits, terms):
    """Evaluate ANF given bits (tuple/list of 0/1) and list of monomial tuples."""
    acc = 0
    for mon in terms:
        prod = 1
        for idx in mon:
            prod &= bits[idx]
            if prod == 0:
                break
        acc ^= prod
    return acc


class NLFFilterCipher:
    """
    Bit-level LFSR with nonlinear filter function.
    state[0] is the newest bit; shift inserts feedback at position 0 and drops the last bit.
    """

    def __init__(self, feedback_taps, filter_taps, state_bits):
        self.feedback_taps = tuple(feedback_taps)
        self.filter_taps = tuple(filter_taps)
        self.L = len(state_bits)
        self.state = list(state_bits)

    def clock(self):
        """Clock once, update state, and return keystream bit."""
        taps = [self.state[i] for i in self.filter_taps]
        z = eval_anf(taps, WG_ANF_TERMS)
        fb = 0
        for idx in self.feedback_taps:
            fb ^= self.state[idx]
        self.state = [fb] + self.state[:-1]
        return z

    def keystream(self, n):
        return [self.clock() for _ in range(n)]
