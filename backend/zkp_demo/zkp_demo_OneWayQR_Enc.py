from Crypto.Util import number
from hashlib import sha256
import secrets
import qrcode
from PIL import Image
import cv2
import numpy as np
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key

# Generating prime and generator
def generate_prime_and_generator(bits=512):
    """Generate a large prime and a generator."""
    p = number.getPrime(bits)
    g = 2  # We assume g = 2 as the generator for simplicity
    return p, g

# Deriving the private key from passphrase
def derive_private_key(passphrase, p):
    """Derive the private key from the passphrase."""
    x = int(sha256(passphrase.encode()).hexdigest(), 16) % (p - 1)
    return x

# Compute public key from private key
def compute_public_key(x, g, p):
    """Compute the public key y = g^x mod p."""
    y = pow(g, x, p)
    return y

# Generate a commitment for r
def commit_r(p, g):
    """Generate commitment a = g^r mod p and return r."""
    r = secrets.randbelow(p - 1)
    a = pow(g, r, p)
    return a, r

# Fiat-Shamir Heuristic to derive challenge e
def derive_challenge(a, y, p):
    """Derive a challenge using Fiat-Shamir heuristic."""
    e = int(sha256(f"{a}{y}".encode()).hexdigest(), 16) % (p - 1)
    return e

# User computes response s = r + e * x mod (p-1)
def compute_response(r, e, x, p):
    """Compute response s = r + e * x mod (p-1)."""
    s = (r + e * x) % (p - 1)
    return s

# Verify proof on the Gate
def verify_proof(p, g, y, a, e, s):
    """Verify the proof on the gate."""
    lhs = pow(g, s, p)  # g^s mod p
    rhs = (a * pow(y, e, p)) % p  # a * y^e mod p
    return lhs == rhs

# Encrypt proof data with AES
def encrypt_proof_data_with_symmetric_key(proof_data, aes_key):
    """Encrypt the proof data using AES GCM."""
    aesgcm = AESGCM(aes_key)
    nonce = secrets.token_bytes(12)  # 12 bytes nonce for AES GCM
    ciphertext = aesgcm.encrypt(nonce, proof_data.encode(), None)
    return ciphertext, nonce

# Encrypt the AES symmetric key with the gate's RSA public key
def encrypt_symmetric_key_with_rsa_public_key(aes_key, gate_public_bytes):
    """Encrypt the AES key using the gate's RSA public key."""
    gate_public_key = serialization.load_pem_public_key(gate_public_bytes)
    encrypted_aes_key = gate_public_key.encrypt(
        aes_key,
        OAEP(
            mgf=MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_aes_key

# Decrypt the AES symmetric key with the gate's RSA private key
def decrypt_symmetric_key_with_rsa_private_key(encrypted_aes_key, gate_private_bytes):
    """Decrypt the AES key using the gate's RSA private key."""
    gate_private_key = serialization.load_pem_private_key(gate_private_bytes, password=None)
    aes_key = gate_private_key.decrypt(
        encrypted_aes_key,
        OAEP(
            mgf=MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return aes_key

# Decrypt proof data with AES
def decrypt_proof_data_with_symmetric_key(ciphertext, nonce, aes_key):
    """Decrypt the proof data using AES GCM."""
    aesgcm = AESGCM(aes_key)
    decrypted_data = aesgcm.decrypt(nonce, ciphertext, None)
    return decrypted_data.decode()

# Generate RSA key pair for the gate
def generate_rsa_keypair():
    gate_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=1024,
    )
    gate_public_key = gate_private_key.public_key()
    # Serialize the keys
    private_bytes = gate_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())
    public_bytes = gate_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
    return private_bytes, public_bytes

# Generate QR code with encrypted data
def generate_qr_code(encrypted_aes_key, ciphertext, nonce, file_name):
    import base64
    # Convert data to base64
    encrypted_aes_key_b64 = base64.b64encode(encrypted_aes_key).decode('utf-8')
    ciphertext_b64 = base64.b64encode(ciphertext).decode('utf-8')
    nonce_b64 = base64.b64encode(nonce).decode('utf-8')
    
    # Combine the data
    qr_data = f"{encrypted_aes_key_b64},{ciphertext_b64},{nonce_b64}"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Save the QR code directly to a file
    img = qr.make_image(fill_color='black', back_color='white')
    img.save(file_name)
    
    print(f"QR code saved to {file_name}")

# Decode QR code and extract encrypted data
def decode_qr_code(file_name):
    import base64
    
    # Use OpenCV's QRCodeDetector to decode the QR code
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(cv2.imread(file_name))
    
    if not data:
        raise ValueError("Failed to decode QR code")
    
    # Extract data from the decoded QR code
    encrypted_aes_key_b64, ciphertext_b64, nonce_b64 = data.split(',')
    
    # Convert from base64 to bytes
    encrypted_aes_key = base64.b64decode(encrypted_aes_key_b64)
    ciphertext = base64.b64decode(ciphertext_b64)
    nonce = base64.b64decode(nonce_b64)
    
    return encrypted_aes_key, ciphertext, nonce

def zkp_protocol():
    # Define the consistent filename for the QR code
    qr_file_name = "QR_Encrypted.png"

    # Gate generates RSA key pair (this would be done once in practice)
    gate_private_bytes, gate_public_bytes = generate_rsa_keypair()
    
    # Step 1: Setup public parameters
    p, g = generate_prime_and_generator()
    print(f"Prime p: {p}")
    print(f"Generator g: {g}")

    # Step 2: Derive private key from user input
    user_input = input("Enter a secret passphrase: ")
    x = derive_private_key(user_input, p)
    print(f"Private key x: {x}")

    # Step 3: Compute public key
    y = compute_public_key(x, g, p)
    print(f"Public key y = g^x mod p: {y}")

    # Step 4: User generates commitment
    a, r = commit_r(p, g)
    print(f"Commitment a = g^r mod p: {a}")

    # Step 5: Derive challenge using Fiat-Shamir Heuristic
    e = derive_challenge(a, y, p)
    print(f"Challenge e: {e}")

    # Step 6: User computes response
    s = compute_response(r, e, x, p)
    print(f"Response s: {s}")

    # Step 7: User generates invalidation ID
    invalidation_id = secrets.token_hex(16)
    print(f"Invalidation ID: {invalidation_id}")

    # Step 8: Create proof data
    proof_data = f"{a},{s},{y},{invalidation_id}"

    # Step 9: User generates a symmetric key for AES encryption
    aes_key = AESGCM.generate_key(bit_length=128)

    # Step 10: Encrypt the proof data with the symmetric key
    ciphertext, nonce = encrypt_proof_data_with_symmetric_key(proof_data, aes_key)

    # Step 11: Encrypt the AES key with the gate's RSA public key
    encrypted_aes_key = encrypt_symmetric_key_with_rsa_public_key(aes_key, gate_public_bytes)

    # Step 12: Combine the encrypted AES key, ciphertext, and nonce into the QR code
    generate_qr_code(encrypted_aes_key, ciphertext, nonce, qr_file_name)

    # Display the QR code for scanning (you can skip this for automation)
    qr_img = Image.open(qr_file_name)
    qr_img.show()

    # Simulate scanning the QR code
    try:
        encrypted_aes_key_decoded, ciphertext_decoded, nonce_decoded = decode_qr_code(qr_file_name)
    except ValueError as e:
        print(f"Error decoding QR code: {e}")
        return

    # Step 13: Gate decrypts the AES key using its RSA private key
    aes_key_gate = decrypt_symmetric_key_with_rsa_private_key(encrypted_aes_key_decoded, gate_private_bytes)

    # Step 14: Gate decrypts proof data using the decrypted AES key
    decrypted_proof_data = decrypt_proof_data_with_symmetric_key(ciphertext_decoded, nonce_decoded, aes_key_gate)
    print(f"Decrypted proof data: {decrypted_proof_data}")

    # Step 15: Parse and verify the decrypted proof data
    a_decoded, s_decoded, y_decoded, id_decoded = decrypted_proof_data.split(',')
    a_decoded, s_decoded, y_decoded = int(a_decoded), int(s_decoded), int(y_decoded)

    # Step 16: Gate verifies the proof
    if verify_proof(p, g, y_decoded, a_decoded, e, s_decoded):
        print("Proof verified successfully! User authenticated.")
        print(f"Invalidation ID to be sent to the school: {id_decoded}")
    else:
        print("Proof verification failed! User not authenticated.")

# Run the protocol simulation
zkp_protocol()
