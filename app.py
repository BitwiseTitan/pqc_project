from flask import Flask, render_template, request, flash, session
import oqs
import base64

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # required for session

def to_b64(data: bytes) -> str:
    return base64.b64encode(data).decode()

def from_b64(data: str) -> bytes:
    return base64.b64decode(data.encode())

@app.route("/", methods=["GET", "POST"])
def index():
    result = {}
    message = None
    selected_alg = request.form.get("algorithm", "ML-KEM-512")

    if request.method == "POST":
        action = request.form.get("action")

        if selected_alg not in oqs.get_enabled_kem_mechanisms():
            flash(f"Algorithm {selected_alg} is not supported.", "danger")
            return render_template("index.html", result=None, selected_alg=selected_alg)

        if action == "generate":
            with oqs.KeyEncapsulation(selected_alg) as kem:
                public_key = kem.generate_keypair()
                private_key = kem.export_secret_key()

                session["public_key"] = to_b64(public_key)
                session["private_key"] = to_b64(private_key)
                session.pop("ciphertext", None)
                session.pop("shared_secret_enc", None)

                message = "Key pair generated successfully."
                result["public_key"] = session["public_key"]
                result["private_key"] = session["private_key"]

        elif action == "encrypt":
            if "public_key" not in session:
                flash("Public key not found. Please generate keys first.", "warning")
                return render_template("index.html", result=None, selected_alg=selected_alg)

            with oqs.KeyEncapsulation(selected_alg) as kem:
                public_key = from_b64(session["public_key"])
                ciphertext, shared_secret_enc = kem.encap_secret(public_key)

                session["ciphertext"] = to_b64(ciphertext)
                session["shared_secret_enc"] = shared_secret_enc.hex()

                message = "Encryption complete."
                result["ciphertext"] = session["ciphertext"]
                result["shared_secret_enc"] = session["shared_secret_enc"]
                result["public_key"] = session["public_key"]
                result["private_key"] = session.get("private_key")

        elif action == "decrypt":
            if "private_key" not in session or "ciphertext" not in session:
                flash("Missing private key or ciphertext. Generate and encrypt first.", "warning")
                return render_template("index.html", result=None, selected_alg=selected_alg)

            with oqs.KeyEncapsulation(selected_alg) as kem:
                kem.generate_keypair()  # Required to init internal buffers
                kem._secret_key = from_b64(session["private_key"])  # Undocumented workaround
                ciphertext = from_b64(session["ciphertext"])

                shared_secret_dec = kem.decap_secret(ciphertext)
                shared_secret_enc = session.get("shared_secret_enc")

                result["shared_secret_dec"] = shared_secret_dec.hex()
                result["shared_secret_enc"] = shared_secret_enc
                result["match"] = shared_secret_enc == shared_secret_dec.hex()
                result["ciphertext"] = session["ciphertext"]
                result["public_key"] = session.get("public_key")
                result["private_key"] = session.get("private_key")
                message = "Decryption complete."

        else:
            flash("Invalid action requested.", "danger")

    return render_template("index.html", result=result, selected_alg=selected_alg, message=message)

if __name__ == "__main__":
    app.run(debug=True)

