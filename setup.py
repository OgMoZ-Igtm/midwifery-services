from setuptools import setup, find_packages

setup(
    name="midwifery_services",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "psycopg2-binary",
        "python-dotenv",
        "supabase",  # ✅ nom corrigé
    ],
    entry_points={
        "console_scripts": [
            "audit-init=modules.tools.inject_init_files:inject_init_files",
            "audit-imports=modules.tools.audit_imports:scan_imports",
        ]
    },
)
