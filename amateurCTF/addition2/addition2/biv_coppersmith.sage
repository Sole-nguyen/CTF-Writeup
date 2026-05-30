# ===========================
# Bivariate Coppersmith (Herrmann–May)
# ===========================

from sage.all import *
import itertools

def coppersmith_2var(f, X, Y, m=3):
    """
    Finds small (x,y) such that f(x,y) = 0 mod N.
    Parameters:
        f: polynomial in Zmod(N)[x,y]
        X,Y: bounds for |x| < X, |y| < Y
        m: lattice amplification (3–6)
    """

    R = f.base_ring()
    N = Integer(R.cardinality())

    # Convert to integer polynomial
    Rxy = PolynomialRing(ZZ, f.variables(), order='lex')
    fZ = Rxy(sum(int(c) * prod(v**e for v, e in zip(Rxy.gens(), mon))
                for mon, c in f.dict().items()))

    x, y = Rxy.gens()
    d = fZ.total_degree()

    # Build G = { N^(m-k) * f^k * x^i * y^j }
    G = []
    for k in range(m+1):
        base = (N^(m-k)) * (fZ^k)
        for i in range(d):
            for j in range(d-i):
                G.append(base * (x^i) * (y^j))

    # Collect monomials
    monos = sorted({mono for g in G for mono in g.monomials()},
                   key=lambda M: (M.degree(), M))

    # Build lattice
    B = Matrix(ZZ, len(G), len(monos))
    for r, g in enumerate(G):
        coeffs = g.dict()
        for c, mono in enumerate(monos):
            B[r,c] = coeffs.get(mono, 0)

    print("[*] Lattice size:", B.nrows(), "x", B.ncols())

    # Scale columns
    scale = []
    for mono in monos:
        ex = mono.exponents()[0]
        factor = (X^ex[0]) * (Y^ex[1])
        scale.append(factor)

    for c, factor in enumerate(scale):
        B.rescale_col(c, factor)

    B = B.LLL()

    # Unscale (rational is OK here, after LLL)
    B = B.change_ring(QQ)
    for c, factor in enumerate(scale):
        B.rescale_col(c, 1/factor)

    # Try solve each row
    Rxy_Q = Rxy.change_ring(QQ)
    for row in B.rows():
        h = Rxy_Q(sum(row[c] * monos[c] for c in range(len(monos))))
        if h == 0:
            continue

        try:
            I = ideal([fZ, h])
            sols = I.variety(ring=ZZ)
        except Exception:
            continue

        for sol in sols:
            xs = int(sol[x])
            ys = int(sol[y])
            if abs(xs) < X and abs(ys) < Y:
                # verify
                if ((ys * (2^256) + xs)^3) % N == int(f.base_ring()(C)):
                    return (xs, ys)

    return None
