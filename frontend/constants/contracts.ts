import { ethers } from "ethers";

const providerUrl = "http://localhost:8545";
const provider = new ethers.providers.JsonRpcProvider(providerUrl);

const zkContractAddress = "0x1234567890123456789012345678901234567890";

const abi = [
    "function isPublicKeyValid(uint256 _publicKey) external view returns (bool)",
    "function invalidatePublicKey(uint256 _publicKey) external",
];

export const zkContract = new ethers.Contract(zkContractAddress, abi, provider);

export const g = 2;
export const p = 23;