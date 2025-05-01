import oqs
import os

def save_binary(filename, data: bytes):
    with open(filename, 'wb') as f:
        f.write(data)

def load_binary(filename) -> bytes:
    with open(filename, 'rb') as f:
        return f.read()

def run_pqc_demo():
    kem_alg = "ML-KEM-512"

    with oqs.KeyEncapsulation(kem_alg) as kem:
        print(f"\n Using PQC Algorithm: {kem_alg}")

        # Key Generation
        public_key = kem.generate_keypair()
        private_key = kem.export_secret_key()

        # Save keys
        save_binary("public_key.bin", public_key)
        save_binary("private_key.bin", private_key)

        # Encapsulate
        ciphertext, shared_secret_enc = kem.encap_secret(public_key)
        save_binary("ciphertext.bin", ciphertext)
        save_binary("shared_secret_enc.bin", shared_secret_enc)

        # Decapsulate immediately using same kem instance
        shared_secret_dec = kem.decap_secret(ciphertext)
        save_binary("shared_secret_dec.bin", shared_secret_dec)

        print(" Encapsulation + Decapsulation complete.")
        print("   ➤ Ciphertext saved to ciphertext.bin")
        print("   ➤ Shared secret (enc) saved to shared_secret_enc.bin")
        print("   ➤ Shared secret (dec) saved to shared_secret_dec.bin")

        if shared_secret_enc == shared_secret_dec:
            print(" Success! Shared secrets match.")
        else:
            print(" Error: Shared secrets do not match.")

if __name__ == "__main__":
    run_pqc_demo()

