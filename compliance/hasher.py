import hashlib

def hash_identifier(identifier: str) -> str:
    """
    One-way hash an email or phone number for the Opt-Out Registry.
    We do not store the raw email/phone of opted-out users, only the hash.
    This ensures we don't accidentally leak strict privacy data.
    """
    clean_id = identifier.strip().lower()
    return hashlib.sha256(clean_id.encode('utf-8')).hexdigest()

if __name__ == "__main__":
    email = "ceo@example.com"
    print(f"Original: {email}")
    print(f"Hashed:   {hash_identifier(email)}")
    print("Store ONLY the hash in the DB.")
