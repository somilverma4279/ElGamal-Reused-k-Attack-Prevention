import random
import math
from sha256 import sha256
from elgamal import keygen, sign
from attack import attack

def generate_k(x, m, p):
    mod = p - 1
    k = int(sha256(f"{x}{m}"), 16) % mod

    # ensure k is valid (invertible)
    while math.gcd(k, mod) != 1:
        k = (k + 1) % mod

    return k

def demo():
    p, g, x, y = keygen()

    m1 = 45
    m2 = 60

    print("\n==============================")
    print("Original Private Key x:", x)
    print("==============================")

    # =====================================================
    # ❌ CASE 1: VULNERABLE (same k)
    # =====================================================
    print("\n[1] Vulnerable Case (Same k)")

    k = 7

    r1, s1 = sign(p, g, x, m1, k)
    r2, s2 = sign(p, g, x, m2, k)

    k_rec, x_rec = attack(m1, m2, r1, s1, s2, p, g, y)

    print("k used:", k)
    print("Recovered x:", x_rec)
    print("Attack Success?", x == x_rec)

    # =====================================================
    # 🛡️ CASE 2: Fresh Random k
    # =====================================================
    print("\n[2] Prevention: Fresh Random k")

    while True:
        k1 = random.randint(2, p-2)
        if math.gcd(k1, p-1) == 1:
            break

    while True:
        k2 = random.randint(2, p-2)
        if math.gcd(k2, p-1) == 1 and k2 != k1:
            break

    r1, s1 = sign(p, g, x, m1, k1)
    r2, s2 = sign(p, g, x, m2, k2)

    k_rec, x_rec = attack(m1, m2, r1, s1, s2, p, g, y)

    print("k1:", k1, "k2:", k2)
    print("Attack result:", x_rec)
    print("Attack Failed?", x_rec != x)

    # =====================================================
    # 🔒 CASE 3: Deterministic k
    # =====================================================
    print("\n[3] Prevention: Deterministic k")

    k1 = generate_k(x, m1, p)
    k2 = generate_k(x, m2, p)

    r1, s1 = sign(p, g, x, m1, k1)
    r2, s2 = sign(p, g, x, m2, k2)

    k_rec, x_rec = attack(m1, m2, r1, s1, s2, p, g, y)

    print("k1:", k1, "k2:", k2)
    print("Attack result:", x_rec)
    print("Attack Failed?", x_rec != x)

    # =====================================================
    # 🚨 CASE 4: Reuse Detection
    # =====================================================
    print("\n[4] Prevention: Reuse Detection")

    used_r = set()

    k = 7
    r1, s1 = sign(p, g, x, m1, k)
    r2, s2 = sign(p, g, x, m2, k)

    if r1 in used_r:
        print("Reuse detected! ❌")
    else:
        used_r.add(r1)

    if r2 in used_r:
        print("Reuse detected! Attack prevented ✅")
    else:
        used_r.add(r2)


if __name__ == "__main__":
    demo()