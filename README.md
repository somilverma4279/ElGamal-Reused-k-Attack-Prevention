# ElGamal-Reused-k-Attack-Prevention
This project demonstrates a critical vulnerability in the ElGamal Cryptosystem when the same random value k is reused during encryption or signing.
It shows:

* How the **Reused k Attack** works
* Mathematical breakdown of the attack
* Implementation of the attack from scratch
* Prevention techniques using secure practices
* Performance and comparison analysis using graphs

---

## 🎯 Objectives

* Understand the ElGamal cryptographic scheme
* Demonstrate how reuse of `k` leads to private key leakage
* Implement attack without using crypto libraries
* Build a secure prevention mechanism
* Analyze results with visual graphs

---

## 📂 Project Structure

```
elgamal/
│
├── elgamal.py        # Core ElGamal implementation
├── attack.py         # Reused k attack implementation
├── prevent.py        # Secure implementation (fix)
├── sha256.py         # Custom SHA-256 implementation (no libraries)
├── comparison.py     # Attack vs Prevention comparison
├── graphs.py         # Graph generation scripts
├── gui.py            # Optional GUI interface
├── testcases.py      # Test cases for validation
│
├── *.png             # Graphs and result visualizations
├── xxx.docx          # Project report
```

---

## ⚙️ Technologies Used

* Python (No external crypto libraries)
* Mathematical Cryptography
* Custom SHA-256 Implementation
* Data Visualization (Matplotlib or similar)

---

## 🔍 Key Concepts

### 1. ElGamal Cryptosystem

* Based on Discrete Logarithm Problem
* Uses:

  * Public key `(p, g, y)`
  * Private key `x`

---

### 2. Reused k Attack

If the same random value `k` is used in two encryptions:

* Attacker can compute:

  * The private key `x`
  * Or recover plaintext

📌 Root cause:

```
k must be random and unique for every encryption
```

---

### 3. SHA-256 Implementation

* Fully implemented from scratch
* Used for:

  * Integrity verification
  * Secure hashing in prevention

---
## 📊 ElGamal Reused k Attack Visualization
<img width="1507" height="1030" alt="image" src="https://github.com/user-attachments/assets/fbc1dfa8-c887-4b8c-8ee8-2c1c0379ffe8" />
<p align="center"><i>Figure: Demonstration of private key leakage due to k reuse in ElGamal</i></p>

---

### 4. Prevention Strategy

* Never reuse `k`
* Use:

  * Cryptographically secure randomness
  * Hash-based validation (SHA-256)
* Ensures:

  * Confidentiality
  * Integrity
  * Resistance to attacks

---

## 📊 Results & Analysis

The project includes multiple graphs:

* Attack success rate
* Time vs input size
* Resource usage
* Comparison between insecure vs secure system

These show:

* Vulnerability severity
* Effectiveness of prevention

## 📊 Experimental Results & Visual Analysis
<img width="640" height="480" alt="attack_success" src="https://github.com/user-attachments/assets/dafb6efa-d601-4ad1-9ee3-6455fdf6b23d" />

<i>Figure: Success rate of reused k attack vs secure scenarios</i></p>


<img width="640" height="480" alt="attack_variants" src="https://github.com/user-attachments/assets/ea9ebcae-816f-4a86-84c2-ff98406650dc" />

<i>Figure: Comparison showing that attacks succeed only when the same k is reused, while different k remains secure</i></p>

<img width="640" height="480" alt="improvement" src="https://github.com/user-attachments/assets/871c7c41-b14b-4070-bce8-27b96234f06a" />

<i>Figure: Significant reduction in attack success rate after applying secure k generation techniques</i>

<img width="640" height="480" alt="integrity" src="https://github.com/user-attachments/assets/7da6bc44-7d4e-4bfb-9db4-49e97bc3d99d" />

<i>Figure: Demonstrates total loss of message integrity when the system is compromised by reused k</i>

<img width="640" height="480" alt="overhead" src="https://github.com/user-attachments/assets/350cc98c-8fa4-4ab6-a127-311ac8e54a4b" />

<i>Figure: Comparison of computational overhead showing minimal cost for implementing prevention mechanisms</i>

<img width="640" height="480" alt="prevention" src="https://github.com/user-attachments/assets/b93c17f1-3c32-45d7-ad60-80039994ef15" />

<i>Figure: Both random and deterministic k generation methods effectively eliminate the vulnerability</i>

<img width="640" height="480" alt="resource" src="https://github.com/user-attachments/assets/0d1ffaa5-bcb7-4082-bd7c-ba1710e2eafd" />

<i>Figure: Resource utilization comparison indicating slightly higher cost for secure implementations</i>

<img width="640" height="480" alt="solution_comparison" src="https://github.com/user-attachments/assets/4ab157ee-410c-45c2-8589-389c5c6a7ed3" />

<i>Figure: Reused k attack is significantly more effective than brute force, emphasizing its severity</i>

<img width="640" height="480" alt="time_vs_size" src="https://github.com/user-attachments/assets/ddad4e4f-ef91-4e89-9b9d-4143da7bde35" />

<i>Figure: Execution time analysis across different key sizes demonstrating scalability of the approach</i>


---

## ▶️ How to Run

### Step 1: Clone the repository

```
git clone https://github.com/your-username/elgamal-project.git
cd elgamal-project/elgamal
```

### Step 2: Run attack

```
python attack.py
```

### Step 3: Run prevention

```
python prevent.py
```

### Step 4: Run comparison

```
python comparison.py
```

---

## 🧪 Sample Output

* Successful key recovery when `k` is reused
* Secure system prevents leakage
* Graphs generated for analysis

---

## 🚨 Important Note

This project is for **educational purposes only**.
It demonstrates vulnerabilities to help understand secure cryptographic design.

---

## 📈 Future Improvements

* Add real-time attack simulation UI
* Integrate with network-based systems
* Extend to other cryptographic attacks

---

## 👨‍💻 Author

* Ishita Banerjee
* Somil Verma
* Arnav Shukla

---

## ⭐ Conclusion

This project clearly shows that:

> **Reusing k in ElGamal completely breaks security**

and highlights the importance of:

* Proper randomness
* Secure implementation practices

