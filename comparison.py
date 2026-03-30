import random
import math
import time
from elgamal import keygen, sign
from attack import attack
from sha256 import sha256

# =====================================================
# HELPER
# =====================================================
def get_valid_k(p):
    while True:
        k = random.randint(2, p-2)
        if math.gcd(k, p-1) == 1:
            return k


# =====================================================
# ATTACK COMPARISON
# =====================================================
def compare_attacks(log):
    total = 20

    k_reuse_success = 0
    brute_force_success = 0

    k_reuse_time = 0
    brute_force_time = 0

    for _ in range(total):
        p, g, x, y = keygen()
        m1, m2 = 45, 60

        # -------- k reuse attack --------
        k = 7
        start = time.time()

        r1, s1 = sign(p, g, x, m1, k)
        r2, s2 = sign(p, g, x, m2, k)

        _, x_rec = attack(m1, m2, r1, s1, s2, p, g, y)

        k_reuse_time += (time.time() - start)

        if x_rec == x:
            k_reuse_success += 1

        # -------- brute force (baseline) --------
        start = time.time()

        found = False
        for guess in range(1, 100):   # limited brute (simulate)
            if pow(g, guess, p) == y:
                found = True
                break

        brute_force_time += (time.time() - start)

        if found:
            brute_force_success += 1

    log("\n=== ATTACK COMPARISON ===")
    log(f"k-reuse attack success: {k_reuse_success}/{total}")
    log(f"Brute force success: {brute_force_success}/{total}")

    log(f"k-reuse avg time: {(k_reuse_time/total)*1000:.4f} ms")
    log(f"Brute force avg time: {(brute_force_time/total)*1000:.4f} ms")


# =====================================================
# PREVENTION COMPARISON
# =====================================================
def compare_prevention(log):
    total = 20

    random_secure = 0
    deterministic_secure = 0
    detection_secure = 0

    for _ in range(total):
        p, g, x, y = keygen()
        m1, m2 = 45, 60

        # -------- RANDOM k --------
        k1 = get_valid_k(p)
        k2 = get_valid_k(p)

        r1, s1 = sign(p, g, x, m1, k1)
        r2, s2 = sign(p, g, x, m2, k2)

        _, x_rec = attack(m1, m2, r1, s1, s2, p, g, y)

        if x_rec != x:
            random_secure += 1

        # -------- DETERMINISTIC k --------
        k1 = int(sha256(f"{x}{m1}"),16) % (p-1)
        k2 = int(sha256(f"{x}{m2}"),16) % (p-1)

        while math.gcd(k1, p-1) != 1:
            k1 = (k1 + 1) % (p-1)

        while math.gcd(k2, p-1) != 1:
            k2 = (k2 + 1) % (p-1)

        r1, s1 = sign(p, g, x, m1, k1)
        r2, s2 = sign(p, g, x, m2, k2)

        _, x_rec = attack(m1, m2, r1, s1, s2, p, g, y)

        if x_rec != x:
            deterministic_secure += 1

        # -------- DETECTION --------
        used_r = set()
        k = 7

        r1, s1 = sign(p, g, x, m1, k)
        r2, s2 = sign(p, g, x, m2, k)

        if r2 in used_r:
            detection_secure += 1
        else:
            used_r.add(r1)
            if r2 in used_r:
                detection_secure += 1

    log("\n=== PREVENTION COMPARISON ===")
    log(f"Random k secure: {random_secure}/{total}")
    log(f"Deterministic k secure: {deterministic_secure}/{total}")
    log(f"Reuse detection secure: {detection_secure}/{total}")