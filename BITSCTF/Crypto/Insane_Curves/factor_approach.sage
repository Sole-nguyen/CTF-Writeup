#!/usr/bin/env sage

# Maybe the format is different - let me try to work backwards from what a valid point should look like
# Since f factors, the Jacobian splits. Let me use that fact.

p = 129403459552990578380563458675806698255602319995627987262273876063027199999999
f_coeffs = [87455262955769204408909693706467098277950190590892613056321965035180446006909, 12974562908961912291194866717212639606874236186841895510497190838007409517645, 11783716142539985302405554361639449205645147839326353007313482278494373873961, 55538572054380843320095276970494894739360361643073391911629387500799664701622, 124693689608554093001160935345506274464356592648782752624438608741195842443294, 52421364818382902628746436339763596377408277031987489475057857088827865195813, 50724784947260982182351215897978953782056750224573008740629192419901238915128]

Fp = GF(p)
R.<x> = PolynomialRing(Fp)
f = R(f_coeffs)

# Factor f
factors = f.factor()
print(f"[+] f factors as: {factors}")

# Get the leading coefficient
c = factors.unit()
print(f"[+] Leading coeff: {c}")

# Get the three degree-2 factors
f1 = factors[0][0]
f2 = factors[1][0]
f3 = factors[2][0]

print(f"\n[+] f1 = {f1}")
print(f"[+] f2 = {f2}")
print(f"[+] f3 = {f3}")

# Create elliptic curves from each factor
# For y^2 = ax^2 + bx + c, we can convert to Weierstrass form

def quadratic_to_elliptic(quad_poly, field):
    """Convert y^2 = ax^2 + bx + c to Weierstrass form"""
    coeffs_dict = {i: quad_poly[i] for i in range(quad_poly.degree() + 1)}
    c0 = coeffs_dict.get(0, 0)
    c1 = coeffs_dict.get(1, 0)
    c2 = coeffs_dict.get(2, 0)
    
    # For y^2 = c2*x^2 + c1*x + c0
    # Substitute X = x, Y = y to get Y^2 = c2*X^2 + c1*X + c0
    # This isn't a complete cubic, so we need to embed it
    
    # Actually, y^2 = f(x) with deg(f) = 2 gives us genus 0 (rational curve)
    # So each factor gives us a genus 0 component
    
    return None

# Actually, the splitting means the Jacobian is isogenous to a product
# Let me try a different approach - maybe the challenge implementation has bugs
# and we should just try to work with what we have

# Perhaps G_u and Q_u are meant to be roots rather than coefficients?
# Or maybe they're using a different library convention

# Let me try: maybe the values are meant to be the roots of u?
# If u(x) = (x - r1)(x - r2) = x^2 - (r1+r2)*x + r1*r2
# Then [r1, r2] -> u = x^2 - (r1+r2)*x + r1*r2

print("\n[+] Trying interpretation: G_u = [r1, r2] are roots of u")
G_u = [95640493847532285274015733349271558012724241405617918614689663966283911276425, 1]
G_v_val = 23400917335266251424562394829509514520732985938931801439527671091919836508525

# u(x) = (x - G_u[0])(x - G_u[1])
u_from_roots = (x - Fp(G_u[0])) * (x - Fp(G_u[1]))
print(f"u = {u_from_roots}")

v_const = R(Fp(G_v_val))
print(f"v = {v_const}")
print(f"v^2 mod u = {(v_const^2) % u_from_roots}")
print(f"f mod u = {f % u_from_roots}")
print(f"Valid? {((v_const^2) % u_from_roots) == (f % u_from_roots)}")

# Maybe they use a different normalization?
# Let's also try with leading coefficient
u_non_monic = Fp(G_u[1]) * (x - Fp(G_u[0]))
print(f"\n[+] Non-monic version: u = {u_non_monic}")
print(f"f mod u = {f % u_non_monic}")
print(f"v^2 mod u = {(v_const^2) % u_non_monic}")

# Or maybe it's weighted projective where [a:b:c] means something special for genus 2?
