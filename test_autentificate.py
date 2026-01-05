from modules.auth.auth_service import authenticate

user = authenticate("admin03@demo.com", "admin++2025")
print("✅ Authentifié :", user) if user else print("❌ Échec de connexion")
