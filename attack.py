import math

# Recover k
def recover_k(m1, m2, s1, s2, p):
    mod = p - 1
    numerator = (m1 - m2) % mod
    denominator = (s1 - s2) % mod

    # Check if inverse exists
    if math.gcd(denominator, mod) != 1:
        return None  # not solvable

    k = (numerator * pow(denominator, -1, mod)) % mod
    return k


# Recover private key x
def recover_x(m1, s1, k, r, p, g, y):
    mod = p - 1
    rhs = (m1 - s1 * k) % mod

    g_val = math.gcd(r, mod)

    if rhs % g_val != 0:
        return None

    # Reduce equation
    r1 = r // g_val
    rhs1 = rhs // g_val
    mod1 = mod // g_val

    inv = pow(r1, -1, mod1)
    x0 = (rhs1 * inv) % mod1

    # Try all possible solutions
    for i in range(g_val):
        x_candidate = x0 + i * mod1
        if pow(g, x_candidate, p) == y:
            return x_candidate

    return None


# Full attack
def attack(m1, m2, r, s1, s2, p, g, y):
    k = recover_k(m1, m2, s1, s2, p)

    if k is None:
        return None, None

    x = recover_x(m1, s1, k, r, p, g, y)

    return k, x