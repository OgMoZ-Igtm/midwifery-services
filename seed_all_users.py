# ⚠️ from modules.backend.supabase_client import supabase
from modules.auth.auth_service import hash_password

url = "https://dfkoznevqrkhsqptfhfy.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRma296bmV2cXJraHNxcHRmaGZ5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1OTA4NDk5MiwiZXhwIjoyMDc0NjYwOTkyfQ.Xv5wflzdKBvaLjL6JWwxNBUE_RS99OOcE33_LppNB8M"
supabase = create_client(url, key)

users = [
    # 🌸 15 sages-femmes
    ("midwife01", "midwife01@demo.com", "mwf2025!", "midwife"),
    ("midwife02", "midwife02@demo.com", "mwf2025!", "midwife"),
    ("midwife03", "midwife03@demo.com", "mwf2025!", "midwife"),
    ("midwife04", "midwife04@demo.com", "mwf2025!", "midwife"),
    ("midwife05", "midwife05@demo.com", "mwf2025!", "midwife"),
    ("midwife06", "midwife06@demo.com", "mwf2025!", "midwife"),
    ("midwife07", "midwife07@demo.com", "mwf2025!", "midwife"),
    ("midwife08", "midwife08@demo.com", "mwf2025!", "midwife"),
    ("midwife09", "midwife09@demo.com", "mwf2025!", "midwife"),
    ("midwife10", "midwife10@demo.com", "mwf2025!", "midwife"),
    ("midwife11", "midwife11@demo.com", "mwf2025!", "midwife"),
    ("midwife12", "midwife12@demo.com", "mwf2025!", "midwife"),
    ("midwife13", "midwife13@demo.com", "mwf2025!", "midwife"),
    ("midwife14", "midwife14@demo.com", "mwf2025!", "midwife"),
    ("midwife15", "midwife15@demo.com", "mwf2025!", "midwife"),
    # 🔐 3 administrateurs
    ("admin01", "admin01@demo.com", "admin++2025", "admin"),
    ("admin02", "admin02@demo.com", "admin++2025", "admin"),
    ("admin03", "admin03@demo.com", "admin++2025", "admin"),
    # 🩺 3 médecins
    ("doctor01", "doctor01@demo.com", "docSecure!", "doctor"),
    ("doctor02", "doctor02@demo.com", "docSecure!", "doctor"),
    ("doctor03", "doctor03@demo.com", "docSecure!", "doctor"),
    # 💊 5 patientes
    ("patient01", "patient01@demo.com", "myBaby2025", "patient"),
    ("patient02", "patient02@demo.com", "myBaby2025", "patient"),
    ("patient03", "patient03@demo.com", "myBaby2025", "patient"),
    ("patient04", "patient04@demo.com", "myBaby2025", "patient"),
    ("patient05", "patient05@demo.com", "myBaby2025", "patient"),
    # 📚 5 étudiants
    ("student01", "student01@demo.com", "learnFast!", "student"),
    ("student02", "student02@demo.com", "learnFast!", "student"),
    ("student03", "student03@demo.com", "learnFast!", "student"),
    ("student04", "student04@demo.com", "learnFast!", "student"),
    ("student05", "student05@demo.com", "learnFast!", "student"),
    # 🧠 5 chercheurs
    ("doctoral01", "doctoral01@demo.com", "research++", "doctoral"),
    ("doctoral02", "doctoral02@demo.com", "research++", "doctoral"),
    ("doctoral03", "doctoral03@demo.com", "research++", "doctoral"),
    ("doctoral04", "doctoral04@demo.com", "research++", "doctoral"),
    ("doctoral05", "doctoral05@demo.com", "research++", "doctoral"),
    # 💉 5 infirmier·ères
    ("nurse01", "nurse01@demo.com", "care4all!", "nurse"),
    ("nurse02", "nurse02@demo.com", "care4all!", "nurse"),
    ("nurse03", "nurse03@demo.com", "care4all!", "nurse"),
    ("nurse04", "nurse04@demo.com", "care4all!", "nurse"),
    ("nurse05", "nurse05@demo.com", "care4all!", "nurse"),
    # 👀 5 invité·es
    ("guest01", "guest01@demo.com", "tempAccess!", "guest"),
    ("guest02", "guest02@demo.com", "tempAccess!", "guest"),
    ("guest03", "guest03@demo.com", "tempAccess!", "guest"),
    ("guest04", "guest04@demo.com", "tempAccess!", "guest"),
    ("guest05", "guest05@demo.com", "tempAccess!", "guest"),
    # 🧪 5 internes
    ("intern01", "intern01@demo.com", "stage2025", "intern"),
    ("intern02", "intern02@demo.com", "stage2025", "intern"),
    ("intern03", "intern03@demo.com", "stage2025", "intern"),
    ("intern04", "intern04@demo.com", "stage2025", "intern"),
    ("intern05", "intern05@demo.com", "stage2025", "intern"),
]

for username, email, password, role in users:
    hashed = hash_password(password)
    supabase.table("users").upsert(
        {"username": username, "email": email, "password_hash": hashed, "role": role},
        on_conflict=["email"],
    ).execute()

print("✅ Tous les comptes ont été réinsérés avec hachage sécurisé")
