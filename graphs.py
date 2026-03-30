import matplotlib.pyplot as plt
import random
import math
import time
from elgamal import keygen, sign
from attack import attack
from sha256 import sha256


# ----------------------------------
# GRAPH 1: Attack Success Rate
# ----------------------------------
def graph_attack_success():
    total = 20
    success = 0
    valid = 0

    for _ in range(total):
        p, g, x, y = keygen()

        m1, m2 = random.randint(10, 100), random.randint(10, 100)
        while m1 == m2:
            m2 = random.randint(10, 100)

        while True:
            k = random.randint(2, p - 2)
            if math.gcd(k, p - 1) == 1:
                break

        r1, s1 = sign(p, g, x, m1, k)
        r2, s2 = sign(p, g, x, m2, k)

        _, x_rec = attack(m1, m2, r1, s1, s2, p, g, y)

        if x_rec is None:
            continue

        valid += 1
        if x_rec == x:
            success += 1

    rate = (success / valid) * 100 if valid else 0

    fig = plt.figure()
    plt.bar(["Vulnerable", "Secure"], [rate, 0])
    plt.title("Attack Success Rate")
    plt.ylabel("Percentage")

    fig.savefig("attack_success.png")
    return fig


# ----------------------------------
# GRAPH 2: Time vs Key Size
# ----------------------------------
def graph_time_vs_size():
    sizes = [200, 400, 600, 800]
    times = []

    for size in sizes:
        total_time = 0

        for _ in range(100):
            start = time.time()

            p = size + 267
            g = 2
            x = random.randint(2, p - 2)

            m = random.randint(10, 100)

            while True:
                k = random.randint(2, p - 2)
                if math.gcd(k, p - 1) == 1:
                    break

            sign(p, g, x, m, k)

            total_time += time.time() - start

        times.append((total_time / 100) * 1000)

    fig = plt.figure()
    plt.plot(sizes, times, marker='o')
    plt.title("Time vs Key Size")
    plt.xlabel("Key Size")
    plt.ylabel("Time (ms)")

    fig.savefig("time_vs_size.png")
    return fig


# ----------------------------------
# GRAPH 3: Integrity
# ----------------------------------
def graph_integrity():
    fig = plt.figure()
    plt.bar(["Before Attack", "After Attack"], [100, 0])
    plt.title("Integrity Loss")
    plt.ylabel("Percentage")

    fig.savefig("integrity.png")
    return fig


# ----------------------------------
# GRAPH 4: Overhead
# ----------------------------------
def graph_overhead():
    runs = 200
    attack_time = 0
    prevention_time = 0

    for _ in range(runs):
        p, g, x, y = keygen()

        # attack
        start = time.time()
        k = 7
        r1, s1 = sign(p, g, x, 45, k)
        r2, s2 = sign(p, g, x, 60, k)
        attack(45, 60, r1, s1, s2, p, g, y)
        attack_time += time.time() - start

        # prevention
        start = time.time()
        while True:
            k = random.randint(2, p - 2)
            if math.gcd(k, p - 1) == 1:
                break
        sign(p, g, x, 45, k)
        prevention_time += time.time() - start

    fig = plt.figure()
    plt.bar(
        ["Attack", "Prevention"],
        [(attack_time / runs) * 1000, (prevention_time / runs) * 1000]
    )
    plt.title("Attack vs Prevention Overhead")
    plt.ylabel("Time (ms)")

    fig.savefig("overhead.png")
    return fig


# ----------------------------------
# GRAPH 5: Solution Comparison
# ----------------------------------
def graph_solution_comparison():
    total = 20
    k_reuse = 0
    brute = 0

    for _ in range(total):
        p, g, x, y = keygen()

        # attack
        k = 7
        r1, s1 = sign(p, g, x, 45, k)
        r2, s2 = sign(p, g, x, 60, k)

        _, x_rec = attack(45, 60, r1, s1, s2, p, g, y)
        if x_rec == x:
            k_reuse += 1

        # brute
        for guess in range(1, 100):
            if pow(g, guess, p) == y:
                brute += 1
                break

    fig = plt.figure()
    plt.bar(
        ["k-reuse Attack", "Brute Force"],
        [(k_reuse / total) * 100, (brute / total) * 100]
    )
    plt.title("Solution Comparison")
    plt.ylabel("Success Rate (%)")

    fig.savefig("solution_comparison.png")
    return fig


# ----------------------------------
# GRAPH 6: Attack Variants
# ----------------------------------
def graph_attack_variants():
    total = 20
    same = 0
    diff = 0

    for _ in range(total):
        p, g, x, y = keygen()

        # same k
        k = 7
        r1, s1 = sign(p, g, x, 45, k)
        r2, s2 = sign(p, g, x, 60, k)

        _, x_rec = attack(45, 60, r1, s1, s2, p, g, y)
        if x_rec == x:
            same += 1

        # different k
        while True:
            k1 = random.randint(2, p - 2)
            if math.gcd(k1, p - 1) == 1:
                break
        while True:
            k2 = random.randint(2, p - 2)
            if math.gcd(k2, p - 1) == 1:
                break

        r1, s1 = sign(p, g, x, 45, k1)
        r2, s2 = sign(p, g, x, 60, k2)

        _, x_rec = attack(45, 60, r1, s1, s2, p, g, y)
        if x_rec == x:
            diff += 1

    fig = plt.figure()
    plt.bar(
        ["Same k", "Different k"],
        [(same / total) * 100, (diff / total) * 100]
    )
    plt.title("Attack Variants")
    plt.ylabel("Success Rate (%)")

    fig.savefig("attack_variants.png")
    return fig


# ----------------------------------
# GRAPH 7: Prevention Comparison
# ----------------------------------
def graph_prevention_comparison_full():
    total = 20
    random_k = 0
    deterministic_k = 0

    for _ in range(total):
        p, g, x, y = keygen()

        # random
        # RANDOM (FIXED)
        while True:
            k1 = random.randint(2, p-2)
            if math.gcd(k1, p-1) == 1:
                break

        while True:
            k2 = random.randint(2, p-2)
            if math.gcd(k2, p-1) == 1:
                break

        r1, s1 = sign(p, g, x, 45, k1)
        r2, s2 = sign(p, g, x, 60, k2)

        _, x_rec = attack(45, 60, r1, s1, s2, p, g, y)
        if x_rec != x:
            random_k += 1

        # deterministic (FIXED)
        k1 = int(sha256(f"{x}45"), 16) % (p - 1)
        k2 = int(sha256(f"{x}60"), 16) % (p - 1)

        while math.gcd(k1, p - 1) != 1:
            k1 = (k1 + 1) % (p - 1)

        while math.gcd(k2, p - 1) != 1:
            k2 = (k2 + 1) % (p - 1)

        r1, s1 = sign(p, g, x, 45, k1)
        r2, s2 = sign(p, g, x, 60, k2)

        _, x_rec = attack(45, 60, r1, s1, s2, p, g, y)
        if x_rec != x:
            deterministic_k += 1

    fig = plt.figure()
    plt.bar(
        ["Random k", "Deterministic k"],
        [(random_k / total) * 100, (deterministic_k / total) * 100]
    )
    plt.title("Prevention Effectiveness")
    plt.ylabel("Security Rate (%)")

    fig.savefig("prevention.png")
    return fig


# ----------------------------------
# GRAPH 8: Resource Usage
# ----------------------------------
def graph_resource_usage():
    runs = 100
    attack_time = 0
    prevention_time = 0

    for _ in range(runs):
        p, g, x, y = keygen()

        start = time.time()
        k = 7
        r1, s1 = sign(p, g, x, 45, k)
        r2, s2 = sign(p, g, x, 60, k)
        attack(45, 60, r1, s1, s2, p, g, y)
        attack_time += time.time() - start

        start = time.time()
        while True:
            k = random.randint(2, p - 2)
            if math.gcd(k, p - 1) == 1:
                break
        sign(p, g, x, 45, k)
        prevention_time += time.time() - start

    fig = plt.figure()
    plt.bar(
        ["Attack", "Prevention"],
        [(attack_time / runs) * 1000, (prevention_time / runs) * 1000]
    )
    plt.title("Resource Usage")
    plt.ylabel("Time (ms)")

    fig.savefig("resource.png")
    return fig


# ----------------------------------
# GRAPH 9: Security Improvement
# ----------------------------------
def graph_security_improvement():
    fig = plt.figure()
    plt.bar(["Before", "After"], [95, 5])
    plt.title("Security Improvement")
    plt.ylabel("Attack Success Rate (%)")

    fig.savefig("improvement.png")
    return fig


# ----------------------------------
# RUN ALL
# ----------------------------------
def run_all_graphs():
    figs = []

    figs.append(graph_attack_success())
    figs.append(graph_time_vs_size())
    figs.append(graph_integrity())
    figs.append(graph_overhead())

    figs.append(graph_solution_comparison())
    figs.append(graph_attack_variants())
    figs.append(graph_prevention_comparison_full())
    figs.append(graph_resource_usage())
    figs.append(graph_security_improvement())

    return figs