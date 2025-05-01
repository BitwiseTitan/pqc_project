# Post-Quantum Cryptography Flask Web App

This project is a demonstration of post-quantum encryption using [liboqs-python](https://github.com/open-quantum-safe/liboqs-python) and Flask. It showcases the use of modern quantum-resistant Key Encapsulation Mechanisms (KEMs) such as ML-KEM-512, FrodoKEM, BIKE, and McEliece.

## Features

- Key generation using selected post-quantum algorithms
- Encryption (encapsulation) and decryption (decapsulation)
- Interactive web interface with Bootstrap
- Algorithm selection via dropdown
- In-memory session storage (no persistent DB required)

## Technologies Used

- Python 3.x
- Flask
- liboqs-python (Python bindings for liboqs)
- Bootstrap 5 (CDN)

## Setup Instructions

### 1. Clone and set up the environment

```bash
git clone <your-repo-url>
cd post_quantum_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```
### 2. Setup liboqs-python
```bash
git clone --recursive https://github.com/open-quantum-safe/liboqs-python.git
cd liboqs-python
pip install .
cd ..

```
### 3. Run the flask app
```bash
python3 app.py

```

