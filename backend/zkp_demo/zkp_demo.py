from Crypto.Util import number
import secrets
from hashlib import sha256

# Function to generate a large prime and a generator efficiently using pycryptodome
def generate_prime_and_generator(bits=512):
    # Generate a large prime p
    p = number.getPrime(bits)
    
    # we get a prime p where g = 2 is a generator in most cases for a safe prime.
    g = 2 
    
    return p, g

# Helper function to generate a random challenge
def generate_random_challenge():
    return secrets.randbelow(2**256)  # A 256-bit random challenge

# Function to generate a proof
def commit_r(p, g):
    r = secrets.randbelow(p - 1)  # Generate a random nonce r
    a = pow(g, r, p)  # a = g^r mod p
    return a, r

# Function to verify a proof
def verify_proof(p, g, y, a, e, s):
    """Verify the zero-knowledge proof.
    
    Args:
        p: Prime number (public parameter).
        g: Generator (public parameter).
        y: Public key (g^x mod p).
        a: Commitment (g^r mod p).
        e: Challenge (random number from the verifier).
        s: Response (r + e * x).
    
    Returns:
        True if the proof is valid, False otherwise.
    """
    lhs = pow(g, s, p)  # g^s mod p
    rhs = (a * pow(y, e, p)) % p  # a * y^e mod p
    return lhs == rhs

# Main flow
def zkp_protocol():
    
    # Step 1: Setup public parameters using pycryptodome
    p, g = generate_prime_and_generator(512)  # Generate a large prime and generator
    
    print(f"Prime p: {p}")
    print(f"Generator g: {g}")
    
    # Step 2: Private key input
    user_input = input("Enter a secret passphrase: ")  # This is a user-supplied input
    x = int(sha256(user_input.encode()).hexdigest(), 16) % (p - 1)  # Derive secret x from the passphrase
    
    # Calculate the public key y = g^x mod p
    y = pow(g, x, p)
    print(f"Public key y = g^x mod p: {y}")
    
    # Step 3: User commits on r
    a, r = commit_r(p, g)
    print(f"Commitment a = g^r mod p: {a}")
    
    # Step 4: Gate generates a random challenge e
    e = generate_random_challenge()
    print(f"Challenge e: {e}")
    
    # Step 5: User responds with s = r + e * x
    s = (r + e * x) % (p - 1)  # Ensure s is mod (p-1)
    print(f"Response s: {s}")
    
    # Step 6: Gate verifies the proof
    if verify_proof(p, g, y, a, e, s):
        print("Proof verified successfully! User authenticated.")
    else:
        print("Proof verification failed! User not authenticated.")

# Run the protocol simulation
zkp_protocol()