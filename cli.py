# ⚠️ import cassé : argparse
# ⚠️ import cassé : subprocess
from modules.services.email_sender import send_welcome_email, send_alert_email

send_welcome_email("etudiant@example.com", "Étudiant.e")
send_alert_email(
    "admin@example.com", "Une erreur critique a été détectée dans les logs."
)


def run_script(path):
    subprocess.run(["python", path])


def main():
    parser = argparse.ArgumentParser(description="Midwifery Audit CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Inject __init__.py dans tous les dossiers")
    subparsers.add_parser("imports", help="Scanner les imports cassés")
    subparsers.add_parser("tests", help="Générer des tests unitaires pour les forms")
    subparsers.add_parser("permissions", help="Vérifier la couverture des rôles")
    subparsers.add_parser("logs", help="Afficher les logs récents")
    subparsers.add_parser("mapping", help="Valider menus_mapping.json")
    subparsers.add_parser("dashboard", help="Lancer le dashboard Streamlit")

    args = parser.parse_args()

    if args.command == "init":
        run_script("modules/tools/inject_init_files.py")
    elif args.command == "imports":
        run_script("modules/tools/audit_imports.py")
    elif args.command == "tests":
        run_script("modules/tools/generate_tests.py")
    elif args.command == "permissions":
        run_script("modules/tools/check_role_coverage.py")
    elif args.command == "logs":
        run_script("modules/tools/full_audit.py")
    elif args.command == "mapping":
        run_script("modules/tools/validate_menu_mapping.py")
    elif args.command == "dashboard":
        subprocess.run(["streamlit", "run", "modules/dashboard/audit_dashboard.py"])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
