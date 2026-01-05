# ⚠️ import cassé : os
# ⚠️ from pathlib import Path

alias_line = 'alias start-midwifery="conda activate midwifery-env && streamlit run modules/forms/form_home.py"\n'
comment_line = "# 🚀 Alias pour lancer l’application Midwifery Services\n"

# Détection du shell
bashrc = Path.home() / ".bashrc"
zshrc = Path.home() / ".zshrc"
target_file = bashrc if bashrc.exists() else zshrc

if not target_file.exists():
    print("❌ Aucun fichier .bashrc ou .zshrc trouvé.")
else:
    with open(target_file, "r") as f:
        content = f.read()

    if "start-midwifery" in content:
        print("✅ L’alias start-midwifery existe déjà.")
    else:
        with open(target_file, "a") as f:
            f.write("\n" + comment_line + alias_line)
        print(f"✅ Alias ajouté dans {target_file}")
        print("💡 Recharge ton shell avec : source ~/.bashrc ou source ~/.zshrc")
