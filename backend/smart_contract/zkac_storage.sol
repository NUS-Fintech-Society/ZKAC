// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;

contract ZKACStorage {

    // Manager address (can add/edit/delete commitments)
    address public manager;

    // Mapping to track smart gates (whether an address is a smart gate)
    mapping(address => bool) public smartGates;

    // Mapping to store commitments (public keys `y`) and their validity state
    mapping(uint256 => bool) public publicKeyValid;

    // Event for when a public key is registered or updated
    event PublicKeyUpdated(uint256 newPublicKey);

    // Event for when a public key is invalidated
    event PublicKeyInvalidated(uint256 publicKey, address smartGate);

    // Event for communication of invalidation ID to the manager
    event InvalidationIDSent(address smartGate, bytes invalidationID);

    // Constructor to set the manager
    constructor() {
        manager = msg.sender;  // Set the contract deployer as the manager
    }

    // Modifier to restrict actions to the manager
    modifier onlyManager() {
        require(msg.sender == manager, "Only the manager can perform this action");
        _;
    }

    // Modifier to restrict actions to smart gates
    modifier onlySmartGate() {
        require(smartGates[msg.sender], "Only an authorized smart gate can perform this action");
        _;
    }

    // Function to add or update a commitment (public key `y`)
    function updatePublicKey(uint256 _newPublicKey) external onlyManager {
        require(!publicKeyValid[_newPublicKey], "New public key must not be already valid"); // New key must not already be in use
        
        // Add the new public key
        publicKeyValid[_newPublicKey] = true;

        emit PublicKeyUpdated( _newPublicKey);  // Log the event for the update
    }

    // Function to invalidate a public key (called by authorized smart gates)
    function invalidatePublicKey(uint256 _publicKey) external onlySmartGate {
        require(publicKeyValid[_publicKey], "The public key is not valid or already invalidated");
        
        publicKeyValid[_publicKey] = false;  // Mark the public key as invalid

        emit PublicKeyInvalidated(_publicKey, msg.sender);  // Emit event for the invalidation
    }

    // Function for a smart gate to send an encrypted invalidation ID to the manager (assumed to be encrypted off-chain)
    function sendInvalidationID(bytes calldata enc_invalidationID) external onlySmartGate {
        emit InvalidationIDSent(msg.sender, enc_invalidationID);
    }

    // Function for the manager to add or remove a smart gate address
    function manageSmartGate(address _smartGate, bool _add) external onlyManager {
        smartGates[_smartGate] = _add;
    }

    // Function to check if a public key is valid
    function isPublicKeyValid(uint256 _publicKey) external view returns (bool) {
        return publicKeyValid[_publicKey];
    }

    // Batch function to add or update multiple public keys
    function updatePublicKeyBatch(uint256[] calldata _newPublicKeys) external onlyManager {
        for (uint i = 0; i < _newPublicKeys.length; i++) {
            require(!publicKeyValid[_newPublicKeys[i]], "One or more public keys are already valid");
            publicKeyValid[_newPublicKeys[i]] = true;
            emit PublicKeyUpdated(_newPublicKeys[i]);  // Emit event for each key
        }
    }

    // Batch function to invalidate multiple public keys
    function invalidatePublicKeyBatch(uint256[] calldata _publicKeys) external onlySmartGate {
        for (uint i = 0; i < _publicKeys.length; i++) {
            require(publicKeyValid[_publicKeys[i]], "One or more public keys are not valid or already invalidated");
            publicKeyValid[_publicKeys[i]] = false;
            emit PublicKeyInvalidated(_publicKeys[i], msg.sender);  // Emit event for each invalidated key
        }
    }

    // Batch function for smart gates to send multiple encrypted invalidation IDs
    function sendInvalidationIDBatch(bytes[] calldata enc_invalidationIDs) external onlySmartGate {
        for (uint i = 0; i < enc_invalidationIDs.length; i++) {
            emit InvalidationIDSent(msg.sender, enc_invalidationIDs[i]);  // Emit event for each invalidation ID
        }
    }

    // Batch function to add or remove multiple smart gate addresses
    function manageSmartGateBatch(address[] calldata _smartGates, bool _add) external onlyManager {
        for (uint i = 0; i < _smartGates.length; i++) {
            smartGates[_smartGates[i]] = _add;
        }
    }
    
}