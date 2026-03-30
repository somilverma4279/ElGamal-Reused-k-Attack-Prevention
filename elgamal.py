import random
from attack import attack

# Key generation
def keygen():
    p = 467   # small prime for testing
    g = 2
    x = random.randint(2, p-2)   # private key
    y = pow(g, x, p)             # public key
    return p, g, x, y

def modInverse(a, m):
    return pow(a, -1, m)

def sign(p, g, x, m, k):
    r = pow(g, k, p)
    k_inv = modInverse(k, p-1)
    s = (k_inv * (m - x * r)) % (p-1)
    return r, s

def verify(p, g, y, m, r, s):
    v1 = (pow(y, r, p) * pow(r, s, p)) % p
    v2 = pow(g, m, p)
    return v1 == v2

if __name__ == "__main__":
    p, g, x, y = keygen()

    # Two different messages
    m1 = 45
    m2 = 60

    k = 7  # SAME k (this is the vulnerability)

    # Generate two signatures
    r1, s1 = sign(p, g, x, m1, k)
    r2, s2 = sign(p, g, x, m2, k)

    print("Original private key x:", x)

    # Attack
    k_rec, x_rec = attack(m1, m2, r1, s1, s2, p, g, y)

    print("Recovered k:", k_rec)
    print("Recovered private key x:", x_rec)

    # Check success
    print("Attack successful?", x == x_rec)