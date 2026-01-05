from modules.auth.auth_service import hash_password

# ⚠️ from modules.backend.supabase_client import supabase

url = "https://dfkoznevqrkhsqptfhfy.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRma296bmV2cXJraHNxcHRmaGZ5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1OTA4NDk5MiwiZXhwIjoyMDc0NjYwOTkyfQ.Xv5wflzdKBvaLjL6JWwxNBUE_RS99OOcE33_LppNB8M"
supabase = create_client(url, key)

email = "admin03@demo.com"
username = "admin03"
role = "admin"
password = "admin++2025"

hashed = hash_password(password)

supabase.table("users").upsert(
    {"username": username, "email": email, "password_hash": hashed, "role": role},
    on_conflict=["email"],
).execute()

print("✅ admin03 réinséré avec mot de passe haché")
