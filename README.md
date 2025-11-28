# MiniChain: ECDSA-Secured Blockchain Prototype

This repository contains the coding work for my Gold CREST Award project: a simplified blockchain prototype written in Python that demonstrates how SHA-256 hashing and ECDSA digital signatures can be used to secure medical records against tampering.

The project also includes a small HTML/CSS/JavaScript demo interface which visually demonstrates how changing ("tampering") a record produces a completely different hash.

---

## Project Overview

### **1. Blockchain**

• The Python implementation demonstrates the core elements of a blockchain
• New blocks link back to the previous block  
• Changing any block changes its hash, breaking the chain  
• The chain can be validated by recomputing all hashes  
• Blocks contain:  
  – index  
  – data  
  – previous hash  
  – timestamp  
  – SHA-256 hash of all fields 

### **2. ECDSA Digital Signatures**
The program randomly tampers records to demonstrate that signatures fail once data changes
Each medical record is:
1. Converted to a deterministic JSON string  
2. Hashed using SHA-256  
3. Signed using **ECDSA (SECP256k1)**  
4. Verified using the doctor’s public key
5. The Python implementation demonstrates the core elements of a blockchain
• New blocks link back to the previous block  
• Changing any block changes its hash, breaking the chain  
• The chain can be validated by recomputing all hashes  
• Blocks contain:  
  – index  
  – data  
  – previous hash  
  – timestamp  
  – SHA-256 hash of all fields 

---

##  This project explores:
• Cryptographic hashing  
• Digital signatures  
• Linking blocks using hashes  
• Detecting tampering  
• Basic attack simulation  
• Use of real Python libraries (`ecdsa`, `hashlib`)  
• Clean, readable implementation  
• A simple UI that illustrates hashing visually  

---


