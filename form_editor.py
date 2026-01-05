# Module: modules/form_editor.py
# Formulaire: Éditeur de Formulaires Dynamique (ADMIN ONLY)

import json
from typing import List, Dict, Any


class FormField:
    """Représente un champ unique dans un formulaire (ex: zone de texte, liste déroulante)."""

    def __init__(
        self,
        field_id: str,
        field_type: str,
        label_fr: str,
        is_required: bool = True,
        options: List[str] = None,
    ):
        self.field_id = field_id  # Clé unique pour la base de données
        self.field_type = field_type  # Ex: "text", "number", "select", "date"
        self.label_fr = label_fr  # Texte affiché à l'utilisateur
        self.is_required = is_required  # Vrai si le champ est obligatoire
        self.options = (
            options if options is not None else []
        )  # Options pour les listes déroulantes

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


class FormConfig:
    """Structure complète de la configuration d'un formulaire modifiable."""

    def __init__(
        self, form_name: str, form_id: str, theme_icon: str, fields: List[FormField]
    ):
        self.form_name = form_name
        self.form_id = form_id
        self.theme_icon = theme_icon  # Icône thématique associée (comme dans les formulaires précédents)
        self.fields = [f.to_dict() for f in fields]

    def to_json(self) -> str:
        """Sérialise la configuration complète du formulaire."""
        return json.dumps(self.__dict__, indent=4)


def render_form_editor_admin():
    """
    Simule le rendu de l'interface d'édition de formulaires, réservée aux administrateurs.
    Icône Thématique: Clé et marteau.
    """
    print(
        "--- Rendu du Formulaire Éditeur de Formulaires (ADMINISTRATION SEULEMENT) ---"
    )
    print("Icône Thématique: ")

    # Étape 1: Sélection du formulaire à éditer
    print("\n[Section 1: Sélection du Formulaire]")
    print(
        "Champ (Select): Choisir un formulaire existant (Ex: 'form_agenda', 'form_profile')"
    )
    print("Bouton: 'Créer un Nouveau Formulaire'")

    # Étape 2: Modification de la configuration du formulaire
    print("\n[Section 2: Propriétés Générales du Formulaire]")
    print("Champ (Text): Nom du Formulaire (Ex: Formulaire de Suivi Postnatal)")
    print("Champ (Text): ID unique du Formulaire (Ex: f_postnatal_01)")
    print("Champ (Text): Icône Thématique (Ex: 'bébé et coeur')")

    # Étape 3: Gestion des champs
    print("\n[Section 3: Gestion des Champs du Formulaire]")
    print("Tableau d'édition interactif des champs:")
    print(
        "  - Ligne 1: Champ 1 | Étiquette (Fr) | ID de champ | Type | Obligatoire? | Options"
    )
    print("  - Bouton: 'Ajouter un nouveau Champ'")
    print("  - Bouton: 'Supprimer le Champ sélectionné'")

    # Exemple de configuration
    example_fields = [
        FormField("p_name", "text", "Nom du Patient"),
        FormField(
            "p_vitals",
            "select",
            "Statut des Signes Vitaux",
            options=["Stable", "Alerte", "Critique"],
        ),
    ]
    example_config = FormConfig(
        "Exemple de Suivi", "f_test_01", "cercle de la vie", example_fields
    )

    print("\n--- Aperçu de la Configuration JSON ---")
    print(example_config.to_json())

    # Boutons d'Action (pour l'enregistrement)
    print("\n--- Commandes du Formulaire ---")
    print(
        "Bouton: 'Sauvegarder la Configuration' -> Enregistre les changements dans la base de données (Firestore)."
    )
    print("Bouton: 'Aperçu du Formulaire' -> Affiche la version rendue pour test.")
    print("Bouton: 'Annuler les Modifications'")


if __name__ == "__main.main":
    render_form_editor_admin()
