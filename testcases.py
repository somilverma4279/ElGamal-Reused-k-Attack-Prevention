import random
import math
from elgamal import keygen, sign
from attack import attack

def run_tests():
    success = 0
    valid_tests = 0
    total = 20

    for i in range(total):
        print("\n==============================")
        print(f"Test Case {i+1}")

        p, g, x, y = keygen()

        # Generate two different messages
        m1 = random.randint(10, 100)
        m2 = random.randint(10, 100)

        while m1 == m2:
            m2 = random.randint(10, 100)

        # Choose valid k (coprime with p-1)
        while True:
            k = random.randint(2, p-2)
            if math.gcd(k, p-1) == 1:
                break

        # Sign both messages with SAME k
        r1, s1 = sign(p, g, x, m1, k)
        r2, s2 = sign(p, g, x, m2, k)

        # Print all values
        print("p:", p)
        print("g:", g)
        print("Original private key x:", x)
        print("Public key y:", y)
        print("Message 1:", m1)
        print("Message 2:", m2)
        print("k used:", k)
        print("Signature 1 (r, s1):", r1, s1)
        print("Signature 2 (r, s2):", r2, s2)

        # Run attack
        k_rec, x_rec = attack(m1, m2, r1, s1, s2, p, g, y)

        if k_rec is None or x_rec is None:
            print("Result: SKIPPED (non-invertible case)")
            continue

        valid_tests += 1

        print("Recovered k:", k_rec)
        print("Recovered private key x:", x_rec)

        if x_rec == x:
            success += 1
            print("Result: PASS ✅")
        else:
            print("Result: FAIL ❌")

    print("\n==============================")
    print("FINAL RESULT")
    print("==============================")
    print("Total Tests Run:", total)
    print("Valid Tests:", valid_tests)

    if valid_tests > 0:
        print("Success Rate:", (success / valid_tests) * 100, "%")
    else:
        print("No valid test cases")


if __name__ == "__main__":
    run_tests()