from modules.backend.supabase_client import supabase
from datetime import datetime

def create_test_account(role="testeur"):
    email = f"test_{secrets.token_hex(4)}@example.com"
    password = generate_secure_password()
    hashed = hash_password(password)

    supabase.table("users").insert({
        "email": email,
        "password_hash": hashed,
        "role": role,
        "created_at": datetime.now().isoformat(),
        "is_test": True
    }).execute()

    return email, password