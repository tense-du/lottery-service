"""Security utilities for protecting sensitive data."""

from cryptography.fernet import Fernet
from base64 import b64encode, b64decode
import os
from typing import Optional, Any, Tuple
import hashlib
from app.core.settings import settings


class SensitiveDataProtection:
    """Handles encryption, decryption and hashing of sensitive data.
    
    Provides methods for:
    - Encrypting data using Fernet (symmetric encryption)
    - Decrypting previously encrypted data
    - Creating searchable hashes of data
    - Generating encryption keys
    """
    
    def __init__(self):
        self.cipher_suite = Fernet(settings.ENCRYPTION_KEY.encode())
        self.hash_salt = settings.HASH_SALT

    def encrypt(self, data: str) -> str:
        return b64encode(self.cipher_suite.encrypt(data.encode())).decode()

    def decrypt(self, encrypted_data: str) -> str:
        try:
            return self.cipher_suite.decrypt(b64decode(encrypted_data)).decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt data: {str(e)}")

    def hash_for_search(self, data: str) -> str:
        """Create a deterministic hash of data for searching.
        
        This creates a hash that can be used to search for encrypted data
        without revealing the original value. The hash is deterministic
        (same input always produces same output) but cannot be reversed.
        """
        salted = f"{data}{self.hash_salt}"
        return hashlib.sha256(salted.encode()).hexdigest()

    @staticmethod
    def generate_key() -> str:
        """Generate a new encryption key.
        
        Returns:
            A new Fernet key as a string
            
        Note:
            This should only be used to generate the initial key.
            The key should be stored securely and reused.
        """
        return Fernet.generate_key().decode()


# Create a singleton instance
data_protection = SensitiveDataProtection()


def create_encrypted_and_hashed_versions_of_data(data: str) -> Tuple[str, str]:
    """Create encrypted and hashed versions of the input data.
    
    This function takes a string and creates two secure versions of it:
    1. An encrypted version for secure storage
    2. A hashed version for searching without revealing the original value
    """
    return (
        data_protection.encrypt(data),
        data_protection.hash_for_search(data)
    )


def decrypt_data(encrypted_data: str) -> str:
    """Decrypt any encrypted data.
    
    Args:
        encrypted_data: The encrypted data (base64-encoded string)
        
    Returns:
        The decrypted data
        
    Raises:
        ValueError: If the encrypted data is invalid
    """
    return data_protection.decrypt(encrypted_data)


def hash_for_search(data: str) -> str:
    return data_protection.hash_for_search(data) 