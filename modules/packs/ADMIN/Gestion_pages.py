# Fonction à ajouter à votre page d'administration (ex: admin.py)
def delete_page_from_pack(pack_name: str, page_id: str):
    """
    Supprime une page de la configuration et du système de fichiers.
    Cette fonction doit être utilisée avec précaution.
    """
    user_name = st.session_state.get("full_name", "Inconnu")

    # Charger la configuration actuelle du menu
    try:
        menu_mapping_path = os.path.join(utils_dir, "menu_mapping.json")
        with open(menu_mapping_path, "r", encoding="utf-8") as f:
            menu_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        log_audit_event(
            user_name,
            "Admin Error",
            f"Failed to load menu_mapping.json for deletion: {e}",
        )
        st.error("Erreur de chargement de la configuration du menu.")
        return

    pages = menu_data.get(pack_name, [])

    # Trouver la page à supprimer
    page_to_delete = next((p for p in pages if p["id"] == page_id), None)

    if not page_to_delete:
        st.warning("La page sélectionnée n'a pas été trouvée dans le pack.")
        return

    # Mettre à jour la configuration
    menu_data[pack_name] = [p for p in pages if p["id"] != page_id]

    # Sauvegarder la nouvelle configuration
    with open(menu_mapping_path, "w", encoding="utf-8") as f:
        json.dump(menu_data, f, indent=4)

    # Supprimer physiquement le fichier
    page_file_path = os.path.join(script_dir, "modules", page_to_delete["file"])
    if os.path.exists(page_file_path):
        os.remove(page_file_path)
        log_audit_event(
            user_name,
            "Admin Action",
            f"Successfully deleted page file: {page_file_path}",
        )
        st.success(f"La page '{page_to_delete['name']}' a été supprimée avec succès.")
    else:
        st.warning(
            f"Le fichier de la page '{page_to_delete['name']}' n'a pas été trouvé, mais la référence a été retirée du menu."
        )
        log_audit_event(
            user_name,
            "Admin Warning",
            f"File not found during deletion, but menu reference removed: {page_file_path}",
        )

    # Forcer la mise à jour de l'état de la session
    st.session_state["MENU_MAPPING"] = menu_data
    st.rerun()
