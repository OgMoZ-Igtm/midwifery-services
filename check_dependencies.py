# ⚠️ import cassé : importlib

core = ["streamlit", "PIL", "pandas", "numpy", "plotly", "requests"]
dev = ["faker", "git", "matplotlib", "markdownlit", "rich"]

print("📦 Dépendances principales :")
for pkg in core:
    try:
        importlib.import_module(pkg)
        print(f"✅ {pkg}")
    except ImportError:
        print(f"❌ {pkg} manquant")

print("\n🧪 Dépendances développeur :")
for pkg in dev:
    try:
        importlib.import_module(pkg)
        print(f"✅ {pkg}")
    except ImportError:
        print(f"❌ {pkg} manquant")
