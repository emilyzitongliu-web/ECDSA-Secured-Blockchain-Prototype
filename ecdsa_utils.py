from ecdsa import SigningKey, VerifyingKey, SECP256k1


def generate_keys():
    #generate a new ECDSA signing and verifying key pair
    #uses the SECP256k1 curve.
  
    sign_key = SigningKey.generate(curve=SECP256k1)
    verify_key = sign_key.get_verifying_key()
    return sign_key, verify_key


def sign_data(data, private_key):
    #Sign a string using the given private key.
    #Returns the signature as a hex string.

    data_bytes = data.encode("utf-8")
    signature = private_key.sign(data_bytes)
    return signature.hex()


def verify_signature(data, signature, public_key):
    #Verify that `signature` is a valid ECDSA signature of `data`
    #under the given public key.
 
    try:
        signature_bytes = bytes.fromhex(signature)
        data_bytes = data.encode("utf-8")
        public_key.verify(signature_bytes, data_bytes)
        return True
    except Exception:
        return False
