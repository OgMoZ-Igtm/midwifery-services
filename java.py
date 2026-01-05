import streamlit as st
import streamlit.components.v1 as components
import os

# Configuration de la page
st.set_page_config(layout="wide", page_title="Système de Santé Multi-Rôles")

st.title("Système de Gestion de Santé (Simulé)")
st.caption("Application React intégrée via Streamlit HTML Component")

# Lisez le contenu de votre code HTML/JS/CSS ici.
# Puisque le code est en React/JSX, nous allons le simuler avec un HTML simple qui pourrait être
# le résultat de la compilation de votre application front-end.
#
# REMARQUE IMPORTANTE : La compilation du JSX en HTML/JS est une étape manuelle qui
# doit être effectuée avec des outils comme Webpack ou Vite.
# Pour l'exemple, nous allons injecter un HTML contenant les scripts de base.

html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Application Santé</title>
    <!-- Chargement de Tailwind CSS pour le style -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Vous devriez charger ici le fichier JS de votre application React compilée.
         Ici, nous simulons juste un message. -->
    <style>
        body { margin: 0; padding: 0; font-family: 'Inter', sans-serif; background-color: #f3f4f6; }
        #root { padding: 30px; }
    </style>
</head>
<body>
    <div id="root">
        <div class="bg-white p-8 rounded-xl shadow-xl max-w-2xl mx-auto">
            <h1 class="text-3xl font-bold text-indigo-700">Interface Web Intégrée</h1>
            <p class="mt-4 text-gray-700">
                Ceci est la zone où votre application React (JSX) compilée s'exécuterait.
                Pour voir l'application React complète, compilez le fichier JSX en
                JavaScript standard et injectez-le ici dans une balise `&lt;script&gt;`.
            </p>
            <div class="mt-6 p-4 bg-yellow-100 rounded-lg border-l-4 border-yellow-500">
                <p class="font-semibold text-yellow-800">État actuel :</p>
                <p class="text-sm text-yellow-700">
                    L'environnement Streamlit ne peut pas exécuter le JSX directement. 
                    Veuillez compiler `HealthSystemSupabase.jsx` en JS/HTML et insérer le code ici.
                </p>
            </div>
        </div>
    </div>
</body>
</html>
"""

# Affichez le contenu HTML/JS dans Streamlit
components.html(
    html_content,
    height=600,  # Hauteur pour l'iframe
    scrolling=True,
)
