from Crypto.Util import number
from hashlib import sha256
import secrets
import qrcode
from io import BytesIO
from PIL import Image
import cv2  # For decoding QR
import numpy as np

# Step 1: Generating prime and generator
def generate_prime_and_generator(bits=512):
    """Generate a large prime and a generator."""
    p = number.getPrime(bits)
    g = 2  # We assume g = 2 as the generator for simplicity
    return p, g

# Step 2: Deriving the private key from passphrase
def derive_private_key(passphrase, p):
    """Derive the private key from the passphrase."""
    x = int(sha256(passphrase.encode()).hexdigest(), 16) % (p - 1)
    return x

# Step 3: Compute public key from private key
def compute_public_key(x, g, p):
    """Compute the public key y = g^x mod p."""
    y = pow(g, x, p)
    return y

# Step 4: Generate a commitment for r
def commit_r(p, g):
    """Generate commitment a = g^r mod p and return r."""
    r = secrets.randbelow(p - 1)
    a = pow(g, r, p)
    return a, r

# Step 5: Fiat-Shamir Heuristic to derive challenge e
def derive_challenge(a, y, p):
    """Derive a challenge using Fiat-Shamir heuristic."""
    e = int(sha256(f"{a}{y}".encode()).hexdigest(), 16) % (p - 1)
    return e

# Step 6: User computes response s = r + e * x mod (p-1)
def compute_response(r, e, x, p):
    """Compute response s = r + e * x mod (p-1)."""
    s = (r + e * x) % (p - 1)
    return s

# Step 7: Verify proof on the Gate
def verify_proof(p, g, y, a, e, s):
    """Verify the proof on the gate."""
    lhs = pow(g, s, p)  # g^s mod p
    rhs = (a * pow(y, e, p)) % p  # a * y^e mod p
    return lhs == rhs

# Step 8: Generate QR code with proof data
def generate_qr_code(a, s, y, invalidation_id):
    """Generate a QR code containing the proof data and invalidation ID."""
    proof_data = f"{a},{s},{y},{invalidation_id}"
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(proof_data)
    qr.make(fit=True)

    # Create image of QR code
    img = qr.make_image(fill='black', back_color='white')
    
    # Save QR code to a BytesIO object
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    return img_bytes

# Step 9: Decode QR code and extract proof data
def decode_qr_code(img_bytes):
    """Decode the QR code and extract proof data."""
    
    file_name="QR_Proof.png"
    img_bytes.seek(0)
    img = Image.open(img_bytes)
    img.save(file_name)

    # Use OpenCV's QRCodeDetector to decode the QR code
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(cv2.imread(file_name))

    if not data:
        raise ValueError("Failed to decode QR code")

    # Extract a, s, y, and invalidation ID from the decoded data
    a_str, s_str, y_str, id_str = data.split(',')
    return int(a_str), int(s_str), int(y_str), id_str

# Step 10: Main ZKP Protocol flow with QR code for proof transmission
def zkp_protocol():
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
    invalidation_id = secrets.token_hex(16)  # Generate a random invalidation ID
    print(f"Invalidation ID: {invalidation_id}")

    # Step 8: Bundle proof data and generate QR code
    qr_img_bytes = generate_qr_code(a, s, y, invalidation_id)
    
    # Display the QR code for scanning (optional, as PIL image)
    qr_img = Image.open(qr_img_bytes)
    qr_img.show()

    # Simulate scanning the QR code and extracting the proof and invalidation ID
    try:
        a_decoded, s_decoded, y_decoded, id_decoded = decode_qr_code(qr_img_bytes)
        print(f"Decoded values: a={a_decoded}, s={s_decoded}, y={y_decoded}, ID={id_decoded}")
    except ValueError as e:
        print(f"Error decoding QR code: {e}")
        return

    # Step 9: The Gate verifies the proof
    if verify_proof(p, g, y_decoded, a_decoded, e, s_decoded):
        print("Proof verified successfully! User authenticated.")
        print(f"Invalidation ID to be sent to the school: {id_decoded}")
    else:
        print("Proof verification failed! User not authenticated.")

# Run the protocol simulation
zkp_protocol()