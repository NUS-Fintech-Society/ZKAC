import { zkContract } from "@/constants/contracts";

export function verifyProof(p: number, g: number, y: number, a: number, e: number, s: number): boolean {
    // Calculate the left-hand side: g^s mod p
    const lhs = BigInt(g) ** BigInt(s) % BigInt(p);

    // Calculate the right-hand side: (a * y^e) mod p
    const rhs = (BigInt(a) * (BigInt(y) ** BigInt(e) % BigInt(p))) % BigInt(p);

    // Return whether lhs and rhs are equal
    return lhs === rhs;
}

export async function verifyPublicKey(publicKey: number) {
    await zkContract.isPublicKeyValid(publicKey);
}

export async function invalidatePublicKey(publicKey: number) {
    await zkContract.invalidatePublicKey(publicKey);
}