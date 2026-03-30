import tkinter as tk
from tkinter import ttk, scrolledtext
import sv_ttk
import random
import math
import threading
from sha256 import sha256
import comparison

from elgamal import sign
from attack import attack

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# =====================================================
# VALID k GENERATOR
# =====================================================
def get_valid_k(p):
    while True:
        k = random.randint(2, p - 2)
        if math.gcd(k, p - 1) == 1:
            return k


# =====================================================
class ElGamalApp:

    def __init__(self, root):
        self.root = root
        self.root.title("🔐 ElGamal Attack Visualizer")
        self.root.geometry("1200x800")

        sv_ttk.set_theme("dark")

        self.p = self.g = self.x = self.y = None

        self.setup_ui()

    # =====================================================
    def setup_ui(self):
        main = ttk.Frame(self.root)
        main.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(main, width=250)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        right = ttk.Frame(main)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # LEFT PANEL
        ttk.Label(left, text="⚙️ Controls", font=("Arial", 14, "bold")).pack(pady=10)

        ttk.Button(left, text="Generate Keys", command=self.generate_keys).pack(fill="x", pady=5)
        ttk.Button(left, text="Run Attack (k reuse)", command=self.run_attack).pack(fill="x", pady=5)

        ttk.Label(left, text="🛡️ Prevention", font=("Arial", 12, "bold")).pack(pady=5)

        ttk.Button(left, text="Random k", command=self.prevent_random_k).pack(fill="x", pady=3)
        ttk.Button(left, text="Deterministic k", command=self.prevent_deterministic_k).pack(fill="x", pady=3)
        ttk.Button(left, text="Reuse Detection", command=self.prevent_detection).pack(fill="x", pady=3)

        ttk.Button(left, text="Run Testcases", command=self.run_tests_thread).pack(fill="x", pady=5)

        ttk.Button(left, text="📊 Show Graphs", command=self.show_graphs).pack(fill="x", pady=5)
        ttk.Button(left, text="📈 Comparative Analysis", command=self.run_comparison).pack(fill="x", pady=5)
        ttk.Button(left, text="🧠 Show Diagram", command=self.show_diagram).pack(fill="x", pady=5)

        ttk.Button(left, text="Clear Log", command=self.clear_log).pack(fill="x", pady=5)

        self.status = ttk.Label(left, text="Status: Idle", font=("Arial", 11, "bold"))
        self.status.pack(pady=20)

        # RIGHT PANEL

        # BIG LOG BOX
        self.logbox = scrolledtext.ScrolledText(right, height=20, font=("Consolas", 10))
        self.logbox.pack(fill=tk.BOTH, expand=True)

        # SMALL GRAPH PANEL
        self.graph_container = ttk.Frame(right, height=300)
        self.graph_container.pack(fill=tk.BOTH, expand=False)

        self.canvas = tk.Canvas(self.graph_container)
        self.scrollbar = ttk.Scrollbar(self.graph_container, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )   

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    # =====================================================
    # COLORED LOGGING
    def log(self, msg, tag=None):
        self.root.after(0, lambda: self._log(msg, tag))

    def _log(self, msg, tag):
        if tag:
            self.logbox.insert(tk.END, msg + "\n", tag)
        else:
            self.logbox.insert(tk.END, msg + "\n")

        self.logbox.tag_config("red", foreground="red")
        self.logbox.tag_config("green", foreground="lightgreen")
        self.logbox.tag_config("yellow", foreground="yellow")
        self.logbox.tag_config("blue", foreground="cyan")

        self.logbox.see(tk.END)

    # =====================================================
    def generate_keys(self):
        self.p = random.randint(200, 500)
        self.g = random.randint(2, self.p - 2)
        self.x = random.randint(2, self.p - 2)
        self.y = pow(self.g, self.x, self.p)

        self.log("\n=== KEY GENERATION ===", "blue")
        self.log(f"p = {self.p}")
        self.log(f"g = {self.g}")
        self.log(f"Private key x = {self.x}", "yellow")

    # =====================================================
    def run_attack(self):
        if self.p is None:
            self.log("Generate keys first", "red")
            return

        self.log("\n=== ATTACK: k REUSE ===", "blue")

        # 🔥 retry until attack works
        while True:
            k = get_valid_k(self.p)

            r1, s1 = sign(self.p, self.g, self.x, 45, k)
            r2, s2 = sign(self.p, self.g, self.x, 60, k)

            _, x_rec = attack(45, 60, r1, s1, s2, self.p, self.g, self.y)

            if x_rec is not None:
                break

        self.log(f"Using SAME k = {k}", "yellow")
        self.log(f"Signature1: (r={r1}, s={s1})")
        self.log(f"Signature2: (r={r2}, s={s2})")

        self.log(f"Recovered key = {x_rec}", "red")

        if x_rec == self.x:
            self.log("ATTACK SUCCESS ❌ System Vulnerable", "red")
            self.status.config(text="VULNERABLE ❌", foreground="red")

    # =====================================================
    def prevent_random_k(self):
        if self.p is None:
            self.log("Generate keys first", "red")
            return

        self.log("\n=== PREVENTION: RANDOM k ===", "blue")

        k1 = get_valid_k(self.p)
        k2 = get_valid_k(self.p)

        self.log(f"k1={k1}, k2={k2}", "yellow")

        r1, s1 = sign(self.p, self.g, self.x, 45, k1)
        r2, s2 = sign(self.p, self.g, self.x, 60, k2)

        _, x_rec = attack(45, 60, r1, s1, s2, self.p, self.g, self.y)

        if x_rec != self.x:
            self.log("SECURE ✅ Attack Failed", "green")
            self.status.config(text="SECURE ✅", foreground="green")

    # =====================================================
    def prevent_deterministic_k(self):
        if self.p is None:
            self.log("Generate keys first", "red")
            return

        self.log("\n=== PREVENTION: DETERMINISTIC k ===", "blue")

        k1 = int(sha256(f"{self.x}45"), 16) % (self.p - 1)
        k2 = int(sha256(f"{self.x}60"), 16) % (self.p - 1)

        while math.gcd(k1, self.p - 1) != 1:
            k1 = (k1 + 1) % (self.p - 1)
        while math.gcd(k2, self.p - 1) != 1:
            k2 = (k2 + 1) % (self.p - 1)

        self.log(f"k1={k1}, k2={k2}", "yellow")

        r1, s1 = sign(self.p, self.g, self.x, 45, k1)
        r2, s2 = sign(self.p, self.g, self.x, 60, k2)

        _, x_rec = attack(45, 60, r1, s1, s2, self.p, self.g, self.y)

        if x_rec != self.x:
            self.log("SECURE ✅ Deterministic Protection Works", "green")
            self.status.config(text="SECURE ✅", foreground="green")

    # =====================================================
    def prevent_detection(self):
        if self.p is None:
            self.log("Generate keys first", "red")
            return

        self.log("\n=== PREVENTION: REUSE DETECTION ===", "blue")

        k = get_valid_k(self.p)

        r1, _ = sign(self.p, self.g, self.x, 45, k)
        r2, _ = sign(self.p, self.g, self.x, 60, k)

        self.log(f"r1 = {r1}, r2 = {r2}", "yellow")

        # 🔥 CORRECT CHECK
        if r1 == r2:
            self.log("Reuse detected → Attack Prevented ✅", "green")
            self.status.config(text="SECURE ✅", foreground="green")
        else:
            self.log("No reuse detected", "yellow")

    # =====================================================
    def show_graphs(self):
        import graphs

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        figs = graphs.run_all_graphs()

        for fig in figs:
            canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)

        self.log("\nGraphs displayed successfully", "green")

    # =====================================================
    def show_diagram(self):
    # clear old content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    # 🔥 BIGGER canvas + visible background
        diagram_canvas = tk.Canvas(
            self.scrollable_frame,
            width=1000,
            height=400,
            bg="#1e1e1e",
            highlightthickness=0
        )
        diagram_canvas.pack(fill="both", expand=True, pady=10)

    # ---- DRAW DIAGRAM ----

    # User
        diagram_canvas.create_text(150, 200, text="User", fill="white", font=("Arial", 14, "bold"))

    # Signing box
        diagram_canvas.create_rectangle(300, 120, 500, 280, outline="yellow", width=2)
        diagram_canvas.create_text(400, 200, text="Sign(m, k)", fill="yellow", font=("Arial", 12))

    # Attacker
        diagram_canvas.create_text(750, 200, text="Attacker\n(recovers x)", fill="red", font=("Arial", 12, "bold"))

    # Arrows
        diagram_canvas.create_line(200, 200, 300, 200, arrow=tk.LAST, fill="white", width=2)
        diagram_canvas.create_line(500, 200, 650, 200, arrow=tk.LAST, fill="white", width=2)

    # Vulnerability note
        diagram_canvas.create_text(
            500, 330,
            text="k reuse → vulnerability → private key leak",
            fill="orange",
            font=("Arial", 12, "italic")
        )

    # 🔥 FORCE UPDATE SCROLL REGION
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.log("\nDiagram displayed successfully ✅", "green")

    # =====================================================
    def run_tests_thread(self):
        threading.Thread(target=self.run_tests, daemon=True).start()

    def run_tests(self):
        success = 0
        self.log("\n=== RUNNING TEST CASES ===", "blue")

        for i in range(10):
            p = random.randint(200, 500)
            g = 2
            x = random.randint(2, p-2)
            y = pow(g, x, p)

            k = get_valid_k(p)

            r1, s1 = sign(p, g, x, 45, k)
            r2, s2 = sign(p, g, x, 60, k)

            _, x_rec = attack(45, 60, r1, s1, s2, p, g, y)

            if x_rec == x:
                success += 1
                self.log(f"Test {i+1}: PASS", "green")
            else:
                self.log(f"Test {i+1}: FAIL", "red")

        self.log(f"\nFinal Success Rate: {success*10}%", "yellow")

    # =====================================================
    def run_comparison(self):
        self.log("\n=== COMPARATIVE ANALYSIS ===", "blue")
        comparison.compare_attacks(self.log)
        comparison.compare_prevention(self.log)

    # =====================================================
    def clear_log(self):
        self.logbox.delete(1.0, tk.END)


# =====================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = ElGamalApp(root)
    root.mainloop()