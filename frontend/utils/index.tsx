import { zkContract } from "@/constants/contracts";
import CryptoJS from 'crypto-js';
import { g, p } from '@/constants/contracts';

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

export function generateProofData(x: number, r: number) {
    const a = BigInt(g) ** BigInt(r) % BigInt(p);
    const y = BigInt(g) ** BigInt(x) % BigInt(p);
    const e = parseInt(CryptoJS.SHA256(a.toString() + y.toString()).toString(), 16) % (p - 1);
    const s = (r + e * x) % (p - 1);
    return { a: a.toString(), y: y.toString(), e, s };
}

export function createInvalidationID() {
    return CryptoJS.SHA256(Math.random().toString()).toString();
}