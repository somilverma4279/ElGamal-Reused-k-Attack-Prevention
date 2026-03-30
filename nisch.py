import tkinter as tk
from tkinter import scrolledtext, ttk
import random
import time
import matplotlib.pyplot as plt
import threading

# ============================================================
# ---------- PRIMALITY (Miller–Rabin) ----------
# ============================================================
def is_prime(n, k=5):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_safe_prime(bits):
    while True:
        q = random.getrandbits(bits - 1)
        q |= (1 << (bits - 2)) | 1
        if not is_prime(q):
            continue
        p = 2 * q + 1
        if is_prime(p):
            return p, q


def find_generator(p, q):
    for g in range(2, 100):
        if pow(g, 2, p) != 1 and pow(g, q, p) != 1:
            return g
    raise ValueError("No generator found")


# ============================================================
# ---------------- GUI APPLICATION ----------------
# ============================================================
class DHApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Diffie-Hellman MITM Visualizer")
        self.root.geometry("1100x650")

        self.p = None
        self.g = None
        self.bits = 256
        self.mitm_enabled = False
        self.times = []
        self.multi_results = {}

        self.setup_ui()

    # ========================================================
    def setup_ui(self):

        left = tk.Frame(self.root)
        left.pack(side=tk.LEFT, padx=10, pady=10)

        right = tk.Frame(self.root)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(left, text="Key Size").pack()

        self.size_combo = ttk.Combobox(
            left,
            values=[256, 512, 768],
            width=10
        )
        self.size_combo.set(256)
        self.size_combo.pack(pady=5)

        tk.Button(left, text="Generate Parameters",
                  width=24, command=self.generate_params).pack(pady=4)

        tk.Button(left, text="Generate Public Keys",
                  width=24, command=self.generate_public).pack(pady=4)

        tk.Button(left, text="Send Alice → Bob",
                  width=24, command=self.send_keys).pack(pady=4)

        tk.Button(left, text="Toggle MITM (Nischay)",
                  width=24, command=self.toggle_mitm).pack(pady=4)

        tk.Button(left, text="Run 10 Test Cases",
                  width=24, command=self.run_tests_thread).pack(pady=4)

        tk.Button(left, text="Show Graphs",
                  width=24, command=self.show_graphs).pack(pady=4)

        self.status = tk.Label(left, text="Status: Idle",
                               font=("Arial", 12, "bold"))
        self.status.pack(pady=20)

        self.logbox = scrolledtext.ScrolledText(
            right, width=80, height=22)
        self.logbox.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(right, width=750, height=300, bg="white")
        self.canvas.pack(pady=5)

        self.draw_network()

    # ========================================================
    def log(self, msg):
        self.logbox.insert(tk.END, msg + "\n")
        self.logbox.see(tk.END)
        self.root.update_idletasks()

    # ========================================================
    def draw_network(self):
        self.canvas.delete("all")

        ax, ay = 120, 120
        bx, by = 620, 120
        nx, ny = 370, 240

        self.canvas.create_oval(ax-40, ay-40, ax+40, ay+40, fill="#d0e6ff")
        self.canvas.create_text(ax, ay, text="Alice", font=("Arial", 11, "bold"))

        self.canvas.create_oval(bx-40, by-40, bx+40, by+40, fill="#d0e6ff")
        self.canvas.create_text(bx, by, text="Bob", font=("Arial", 11, "bold"))

        self.canvas.create_oval(nx-40, ny-40, nx+40, ny+40, fill="#ffd0d0")
        self.canvas.create_text(nx, ny, text="Nischay", font=("Arial", 11, "bold"))

        if self.mitm_enabled:
            self.canvas.create_line(ax+40, ay, nx-40, ny,
                                    arrow=tk.LAST, width=3, fill="red")
            self.canvas.create_line(nx+40, ny, bx-40, by,
                                    arrow=tk.LAST, width=3, fill="red")
        else:
            self.canvas.create_line(ax+40, ay, bx-40, by,
                                    arrow=tk.LAST, width=3, fill="green")

    # ========================================================
    def generate_params(self):
        self.bits = int(self.size_combo.get())
        self.log(f"\n[+] Generating parameters ({self.bits}-bit)...")

        self.p, q = generate_safe_prime(self.bits)
        self.g = find_generator(self.p, q)

        self.log(f"p = {self.p}")
        self.log(f"g = {self.g}")

        self.status.config(text="Parameters Ready", fg="blue")

    # ========================================================
    def generate_public(self):
        if not self.p:
            self.log("❌ Generate parameters first")
            return

        self.a = random.getrandbits(self.bits - 2)
        self.b = random.getrandbits(self.bits - 2)

        self.A = pow(self.g, self.a, self.p)
        self.B = pow(self.g, self.b, self.p)

        self.log("\n[ALICE]")
        self.log(f"a = {self.a}")
        self.log(f"A = {self.A}")

        self.log("\n[BOB]")
        self.log(f"b = {self.b}")
        self.log(f"B = {self.B}")

    # ========================================================
    def toggle_mitm(self):
        self.mitm_enabled = not self.mitm_enabled

        if self.mitm_enabled:
            self.status.config(text="MITM ENABLED", fg="red")
            self.log("\n⚠️ MITM attacker Nischay ACTIVE")
        else:
            self.status.config(text="MITM DISABLED", fg="green")
            self.log("\n✅ MITM disabled")

        self.draw_network()

    # ========================================================
    def send_keys(self):
        if not hasattr(self, 'A'):
            self.log("❌ Generate public keys first")
            return

        self.log("\n--- KEY EXCHANGE ---")

        if self.mitm_enabled:
            e1 = random.getrandbits(self.bits - 2)
            e2 = random.getrandbits(self.bits - 2)

            fake_A = pow(self.g, e1, self.p)
            fake_B = pow(self.g, e2, self.p)

            alice_key = pow(fake_B, self.a, self.p)
            bob_key = pow(fake_A, self.b, self.p)
            darthA = pow(self.A, e2, self.p)
            darthB = pow(self.B, e1, self.p)

            success = (alice_key == darthA and bob_key == darthB)

            self.log(f"Alice key = {alice_key}")
            self.log(f"Bob key = {bob_key}")
            self.log(f"Nischay with Alice = {darthA}")
            self.log(f"Nischay with Bob = {darthB}")
            self.log(f"\nMITM SUCCESS = {success}")

            self.status.config(text="VULNERABLE", fg="red")

        else:
            alice_key = pow(self.B, self.a, self.p)
            bob_key = pow(self.A, self.b, self.p)

            self.log(f"Alice key = {alice_key}")
            self.log(f"Bob key = {bob_key}")
            self.log("\n✅ Secure DH exchange")

            self.status.config(text="SECURE", fg="green")

        self.draw_network()

    # ========================================================
    # THREAD WRAPPER (prevents freeze)
    # ========================================================
    def run_tests_thread(self):
        t = threading.Thread(target=self.run_tests)
        t.daemon = True
        t.start()

    # ========================================================
    def run_tests(self):
        if not self.p:
            self.log("Generate parameters first")
            return

        self.times.clear()
        self.multi_results.clear()
        successes = 0

        key_sizes = [256, 512, 768]

        for bits in key_sizes:
            self.log(f"\n######## KEY SIZE = {bits} ##########")

            start_param = time.time()
            p, q = generate_safe_prime(bits)
            g = find_generator(p, q)
            end_param = time.time()

            self.multi_results[bits] = end_param - start_param

            for i in range(10):
                self.log("\n" + "="*65)
                self.log(f"TEST CASE {i+1}")
                self.log("="*65)

                a = random.getrandbits(bits-2)
                b = random.getrandbits(bits-2)
                A = pow(g, a, p)
                B = pow(g, b, p)

                e1 = random.getrandbits(bits-2)
                e2 = random.getrandbits(bits-2)

                fake_A = pow(g, e1, p)
                fake_B = pow(g, e2, p)

                alice_key = pow(fake_B, a, p)
                bob_key = pow(fake_A, b, p)
                darthA = pow(A, e2, p)
                darthB = pow(B, e1, p)

                success = (alice_key == darthA and bob_key == darthB)
                if success:
                    successes += 1

                self.log(f"p = {p}")
                self.log(f"g = {g}")
                self.log(f"a = {a}")
                self.log(f"b = {b}")
                self.log(f"A = {A}")
                self.log(f"B = {B}")
                self.log(f"Nischay-Alice = {darthA}")
                self.log(f"Nischay-Bob = {darthB}")
                self.log(f"MITM SUCCESS = {success}")

        rate = (successes / (len(key_sizes)*10)) * 100
        self.log(f"\nSuccess Rate = {rate:.2f}%")

    # ========================================================
    def show_graphs(self):
        if not self.multi_results:
            self.log("Run tests first")
            return

        # Graph 1
        plt.figure()
        plt.bar(["Before Attack"], [100])
        plt.title("MITM Success Rate (Attack Only)")

        # Graph 2 (multi key size)
        plt.figure()
        sizes = list(self.multi_results.keys())
        times = list(self.multi_results.values())
        plt.plot(sizes, times, marker='o')
        plt.title("Time vs Key Size")
        plt.xlabel("Key Size (bits)")
        plt.ylabel("Time (s)")

        # Graph 3 (no auth implemented)
        plt.figure()
        plt.bar(["Without Auth"], [0])
        plt.title("Authentication Rate (Not Implemented)")

        # Graph 4 (no overhead since no auth)
        plt.figure()
        plt.bar(["Attack Only"], [sum(times)/len(times)])
        plt.title("Latency Overhead (Attack Only)")

        plt.show()


# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = DHApp(root)
    root.mainloop()