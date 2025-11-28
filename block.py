
import hashlib
import json
import time
import random

from ecdsa_utils import generate_keys, sign_data, verify_signature


class Block:
    #a singlular block in the blockchain
    #stores an index, data payload, previous hash, timestamp and its own hash value

    def __init__(self, index, data, previous_hash, nonce=0):
        self.index = index
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.timestamp = time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        #calculates the SHA-256 hash of this block’s contents 
        
        block_string = f"{self.index}{self.data}{self.previous_hash}{self.nonce}{self.timestamp}"
        return hashlib.sha256(block_string.encode("utf-8")).hexdigest()

    
    def __str__(self):
        return (
            f"Block #{self.index}\n"
            f"Timestamp: {self.timestamp}\n"
            f"Data: {self.data}\n"
            f"Previous Hash: {self.previous_hash}\n"
            f"Nonce: {self.nonce}\n"
            f"Hash: {self.hash}\n"
        )


class Blockchain:
    #simplified blockchain implementation which holds a list of block objects

    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        #Create the first block in the chain.
 
        return Block(0, "Genesis Block - PATIENT RECORD HASH", "0")

    def get_latest_block(self):
        #Return the most recently added block.

        return self.chain[-1]

    def add_block(self, data):
         #Create a new block with the given data and add it to the chain.

        previous_block = self.get_latest_block()
        new_index = previous_block.index + 1
        new_block = Block(new_index, data, previous_block.hash)
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
  
        #Verify that the chain is internally consistent:
        #each block’s stored hash matches its contents
        #each block’s previous_hash matches the previous block’s hash
 
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True


def demo_blockchain_with_signatures():

    #Demo:
    #create a blockchain
    #hash and sign sample patient records
    #add them to the chain
    #tamper some records and check signatures

    my_chain = Blockchain()

    # generate keys for doctor
    doctor_private_key, doctor_public_key = generate_keys()

    # sample patient records
    patient_records = [
        {
            "patient_id": "654321",
            "name": "Bobby Mahoney",
            "age": 40,
            "medical_history": "None",
            "prescription": "Ibuprofen 200mg",
            "lab_results": "Blood test normal",
            "timestamp": "2025-07-20",
        },
        {
            "patient_id": "635221",
            "name": "Gertruda Gray",
            "age": 30,
            "medical_history": "Asthma",
            "prescription": "Albuterol Inhaler",
            "lab_results": "Blood test normal",
            "timestamp": "2025-07-21",
        },
        {
            "patient_id": "789012",
            "name": "Fatima Forrow",
            "age": 50,
            "medical_history": "Diabetes",
            "prescription": "Metformin",
            "lab_results": "Blood sugar normal",
            "timestamp": "2025-07-22",
        },
        {
            "patient_id": "890123",
            "name": "Larry Lawrence",
            "age": 45,
            "medical_history": "Hypertension",
            "prescription": "Lisinopril",
            "lab_results": "Blood pressure normal",
            "timestamp": "2025-07-23",
        },
        {
            "patient_id": "901234",
            "name": "Samuel Chadwick",
            "age": 35,
            "medical_history": "Allergies",
            "prescription": "Cetirizine",
            "lab_results": "Allergy test positive",
            "timestamp": "2025-07-24",
        },
    ]

    signatures = []

    #signs each record, verifies it and adds it to the chain
    for record in patient_records:
        record_json = json.dumps(record, sort_keys=True)
        record_hash = hashlib.sha256(record_json.encode("utf-8")).hexdigest()

        signature = sign_data(record_hash, doctor_private_key)
        signatures.append(signature)

        valid = verify_signature(record_hash, signature, doctor_public_key)

        print("Original Record:", record)
        print("Record Hash:", record_hash)
        print("Signature:", signature)
        print("Signature Valid?", valid)
        print()

        data_to_store = {
            "record_hash": record_hash,
            "signature": signature,
            "signer_public_key": doctor_public_key.to_string().hex(),
        }
        my_chain.add_block(json.dumps(data_to_store))

    #randomly tamper some records and test signatures
    num_records = len(patient_records)
    num_to_tamper = random.randint(1, num_records)
    tamper_indices = random.sample(range(num_records), num_to_tamper)

    for i, record in enumerate(patient_records):
        tampered = record.copy()

        if i in tamper_indices:
            tampered["prescription"] = f"Tampered Prescription #{i + 1}"

        tampered_str = json.dumps(tampered, sort_keys=True)
        tampered_hash = hashlib.sha256(tampered_str.encode("utf-8")).hexdigest()

        original_signature = signatures[i]
        tampered_valid = verify_signature(tampered_hash, original_signature, doctor_public_key)

        print(f"--- Patient Record #{i + 1} ---")
        print("Record:", tampered)
        print("Record Hash:", tampered_hash)
        print("Signature:", original_signature)
        print("Is the doctor signature still valid?", tampered_valid)
        print()

    print("Is blockchain valid?", my_chain.is_chain_valid())


if __name__ == "__main__":
    demo_blockchain_with_signatures()
