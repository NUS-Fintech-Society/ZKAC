# ZKAC DAM: Zero-Knowledge Access Control for Dynamic and Anonymous Memberships

## Introduction

ZKAC DAM (Zero-Knowledge Access Control for Dynamic and Anonymous Memberships) is a blockchain-based access control system that leverages **Zero-Knowledge Proofs (ZKPs)** and **ElGamal encryption** to provide secure, dynamic, and privacy-preserving access to facilities (e.g., campus buildings, libraries, etc.). Our system allows users to authenticate themselves as members of a group without revealing their identity, while dynamically updating their keys after each use.

This project is still in its early stages, and we aim to provide a secure, scalable, and privacy-enhancing solution for access control in various environments such as academic institutions, corporate settings, and other organizations requiring group-based access control.

## Problem Statement

Traditional access control solutions compromise user privacy by exposing identifiable credentials, making them vulnerable to breaches. Additionally, they struggle to effectively manage group memberships, especially when keys need to be revoked or updated without affecting the entire group.

Our solution addresses these challenges by creating a dynamic, anonymous, and unlinkable access control system using blockchain technology and cryptographic protocols, ensuring security and privacy throughout the authentication process.

## Key Features

- **Privacy-Preserving Access Control**: Users can authenticate using **Zero-Knowledge Proofs** without revealing their identity or secret key.
- **Dynamic Key Updates**: After each authentication, the user’s key is invalidated and replaced with a new one, preventing key reuse and ensuring that compromised keys are obsolete.
- **Group Membership Authentication**: Users can prove their membership in a group without disclosing individual identity, preserving anonymity.
- **Unlinkability**: The system ensures that no party can link a user’s past and future sessions, preserving privacy across multiple authentications.
- **Resilience to Attacks**: Designed to resist common attacks such as relay attacks, replay attacks, impersonation, and man-in-the-middle (MitM) attacks.
- **Tamper-Proof Key Management**: By leveraging blockchain technology, key management is immutable and auditable.

## Project Structure

- **Frontend**: React (To be implemented)
- **Backend**: Node.js and Python (To be implemented)
- **Blockchain**: Ethereum (Solidity-based smart contracts)
- **Cryptography**: ElGamal for digital signatures and Zero-Knowledge Proofs
