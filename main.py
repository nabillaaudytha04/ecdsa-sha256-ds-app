from cryptography.hazmat.primitives.asymmetric.ec import ECDSA, generate_private_key, SECP256R1
from cryptography.hazmat.primitives.hashes import SHA256 
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
    Encoding,
    PrivateFormat,
    PublicFormat,
    NoEncryption,
)

def generate_keys():
    private_key = generate_private_key(SECP256R1())
    public_key = private_key.public_key()
    return private_key, public_key

def save_keys(private_key, public_key, private_key_file, public_key_file):
    with open(private_key_file, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=Encoding.PEM,
                format=PrivateFormat.PKCS8,
                encryption_algorithm=NoEncryption(),
            )
        )

    with open(public_key_file, "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo
            )
        )

def load_public_key(public_key_file):
    with open(public_key_file, "rb") as f:
        try:
            public_key = load_pem_public_key(f.read())
        except:
            return False

    return public_key

def load_private_key(private_key_file):
    with open(private_key_file, "rb") as f:
        try:
            private_key = load_pem_private_key(f.read(), password=None)
        except:
            return False

    return private_key

def sign_document(file_path):
    with open("private_key.pem", "rb") as f:
        private_key = load_pem_private_key(f.read(), password=None)
        
    with open(file_path, "rb") as f:
        document_data = f.read()
        
    signature = private_key.sign(
        document_data, ECDSA(SHA256())
    )
    
    with open("signature.sig", "wb") as f:
        f.write(signature)
        
    return "Document berhasil di tanda tangan"

def verify_document(file_path):
        with open("public_key.pem", "rb") as f:
            public_key = load_pem_public_key(f.read())
        with open(file_path, 'rb') as f:
            file_data = f.read()
        with open("signature.sig", "rb") as f:
            signature = f.read()
        try:
            public_key.verify(
                signature,
                file_data,
                ECDSA(SHA256())
            )
            return "Valid"
        except:
            return "Tidak Valid"