# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd
import numpy as np

# --- Configuration de la Page (Optionnel) ---
st.set_page_config(
    page_title="Guide Streamlit en Français", page_icon="💡", layout="wide"
)

# --- 1. Titre et Introduction ---
st.title("🚀 Mon Guide Streamlit Interactif en Python")
st.markdown(
    """
Bienvenue dans cette introduction à Streamlit ! Cette application est conçue pour vous montrer
comment transformer rapidement un script Python en une application web interactive.
"""
)

st.header("1. Affichage de contenu")

# Affichage de texte simple et de Markdown
st.write("Ceci est un texte simple affiché avec `st.write()`.")
st.markdown("---")  # Ligne séparatrice

# Affichage d'une image
st.subheader("Visualisation ")
# Note : Pour les applications réelles, utilisez des images locales ou des URLs.
# Ici, nous utilisons un espace réservé.

# --- 2. Widgets et Entrées Utilisateur ---
st.header("2. Interaction avec les Widgets")

# Widget de barre latérale (Sidebar)
st.sidebar.header("Options de la Barre Latérale")
niveau_difficulte = st.sidebar.slider(
    "Sélectionnez le niveau de complexité",
    min_value=0,
    max_value=10,
    value=5,
    help="Utilisez `st.sidebar` pour placer des éléments ici.",
)
st.sidebar.write(f"Niveau sélectionné : **{niveau_difficulte}**")

# Widget d'entrée de texte dans le corps principal
nom_utilisateur = st.text_input(
    "Saisissez votre nom ou un mot-clé", "Utilisateur Streamlit"
)

# Widget de sélection (Selectbox)
option_choisie = st.selectbox(
    "Choisissez une option dans la liste", ("Option A", "Option B", "Option C")
)

st.info(f"Bonjour, **{nom_utilisateur}**. Vous avez choisi **{option_choisie}**.")

# --- 3. Affichage de Données (DataFrames) ---
st.header("3. Présentation des Données")

st.subheader("Aperçu des données avec Pandas")
st.write("Streamlit facilite l'affichage de DataFrames.")

# Création d'un exemple de DataFrame
data = {
    "Catégorie": ["Pomme", "Banane", "Cerise", "Datte"],
    "Quantité": np.random.randint(10, 100, 4),
    "Prix (€)": np.round(np.random.rand(4) * 10, 2),
}
df = pd.DataFrame(data)

# Affichage du DataFrame
st.dataframe(df)

# Affichage d'un graphique simple
st.subheader("Visualisation de données (Graphique)")
st.bar_chart(df.set_index("Catégorie")["Quantité"])

# --- 4. Boutons et Logique Conditionnelle ---
st.header("4. Actions et Événements")

# Bouton qui exécute une action
if st.button("Cliquez pour exécuter une action"):
    # Ceci s'exécute uniquement après le clic
    st.success(f"Action exécutée ! Merci pour le clic, {nom_utilisateur}.")

# Bouton qui affiche un message de confirmation
if st.button("Afficher un message d'alerte"):
    st.warning("Ceci est un avertissement affiché après le clic.")


st.markdown("---")
st.caption("Fin du guide de démonstration Streamlit.")
