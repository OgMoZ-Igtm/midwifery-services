import streamlit as st
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Configurer la mise en page de la page Streamlit pour qu'elle soit large
st.set_page_config(layout="wide")

# Titre principal de l'application
st.title("Hello World")
st.subheader("C'est un sous-titre")

# Titre et sous-titre de la barre latérale
st.sidebar.title("Sidebar")
st.sidebar.subheader("C'est un sous-titre de la sidebar")

# Écrire du markdown dans l'application
st.markdown("## Markdown")

# Création de trois colonnes avec des largeurs spécifiques (2:1:2)
c1, _, c2 = st.columns((2, 1, 2))

# Titres pour les colonnes 1 et 2
c1.title("Colonne 1")
c2.title("Colonne 2")

# Contenu dans la colonne 1
with c1:
    st.write("Contenu de la colonne 1")

# Contenu dans la colonne 2
with c2:
    st.write("Contenu de la colonne 2")

# Ajouter des espaces et une ligne de séparation
st.write("##")
st.divider()
st.write("##")

# Titre pour la section des widgets d'entrée
st.title("Input widgets")

# Widget pour entrer un nombre avec une valeur par défaut de 42.0
st.number_input("Nombre", value=42, min_value=0, max_value=100, step=1)

# Bouton qui affiche une notification toast lorsqu'il est cliqué
if st.button("Bouton"):
    st.toast("Vous avez cliqué sur le bouton")

# Checkbox qui renvoie un booléen
is_checked = st.checkbox("Cocher pour activer")
st.write(f"Checkbox: {is_checked}")

# Toggle switch (identique à une checkbox ici)
is_toggle = st.toggle("Toggle pour activer")
st.write(f"Toggle: {is_toggle}")

# Selectbox pour choisir une option parmi une liste
one_select = st.selectbox("Selectbox", ["Option 1", "Option 2", "Option 3"])
st.write(f"Selectbox: {one_select}")

# Multiselect pour choisir plusieurs options
multi_select = st.multiselect("Multiselect", ["Option 1", "Option 2", "Option 3"])
st.write(f"Multiselect: {multi_select}")

# Créer un formulaire avec des champs de texte
with st.form("my_form"):
    text_input = st.text_input("Text input")
    text_area = st.text_area("Text area")
    submit_button = st.form_submit_button("Submit")

# Afficher les valeurs saisies dans le formulaire
if submit_button:
    st.write(f"Text input: {text_input}")
    st.write(f"Text area: {text_area}")

# Ajouter des espaces et une ligne de séparation
st.write("##")
st.divider()
st.write("##")

# Sous-titre pour la section des graphiques
st.subheader("Graphiques")

# -------- Graphique Plotly --------
# Charger le jeu de données 'iris' avec Seaborn
df = sns.load_dataset("iris")

# Créer un graphique de dispersion interactif avec Plotly Express
fig = px.scatter(df, x="sepal_length", y="sepal_width", color="species")

# Afficher le graphique Plotly dans l'application
st.plotly_chart(fig)

# -------- Graphique Matplotlib --------
# Générer des données pour le graphique
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Créer une figure Matplotlib
figure = plt.figure()
# Tracer la courbe sinusoïdale
plt.plot(x, y)
# Afficher le graphique Matplotlib dans l'application
st.pyplot(figure)

# Ajouter des espaces et une ligne de séparation
st.write("##")
st.divider()
st.write("##")

# Sous-titre pour l'affichage de DataFrame
st.subheader("Affichage de DataFrame")

# Créer un DataFrame aléatoire avec 50 lignes et 5 colonnes
df = pd.DataFrame(np.random.randn(50, 5), columns=("colonne %d" % i for i in range(5)))

# Afficher le DataFrame de manière interactive
st.dataframe(df)  # Vous pouvez aussi utiliser st.write(df)

# Sous-titre pour la section de chargement de fichier
st.subheader("Chargement de fichier")

# Widget pour uploader un fichier CSV
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

# Si un fichier est uploadé, le lire et l'afficher
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)
else:
    st.info("Veuillez charger un fichier CSV pour afficher les données.")

# Sous-titre pour la section de prédiction avec un modèle de Machine Learning
st.subheader("Prédiction avec un modèle de Machine Learning")

# -------- Chargement et entraînement du modèle --------
# Charger le jeu de données Iris
iris = load_iris()
X = iris.data  # Les caractéristiques
Y = iris.target  # Les étiquettes

# Créer un classifieur Random Forest
clf = RandomForestClassifier()

# Entraîner le modèle sur l'ensemble des données
clf.fit(X, Y)

# -------- Interface utilisateur pour les entrées du modèle --------
# Séparateur et sous-titre dans la barre latérale
st.sidebar.divider()
st.sidebar.subheader("Paramètres d'entrée du modèle de Machine Learning")

# Sliders pour saisir les caractéristiques du modèle
sepal_length = st.sidebar.slider(
    "Longueur du sépale",
    float(X[:, 0].min()),
    float(X[:, 0].max()),
    float(X[:, 0].mean()),
)
sepal_width = st.sidebar.slider(
    "Largeur du sépale",
    float(X[:, 1].min()),
    float(X[:, 1].max()),
    float(X[:, 1].mean()),
)
petal_length = st.sidebar.slider(
    "Longueur du pétale",
    float(X[:, 2].min()),
    float(X[:, 2].max()),
    float(X[:, 2].mean()),
)
petal_width = st.sidebar.slider(
    "Largeur du pétale",
    float(X[:, 3].min()),
    float(X[:, 3].max()),
    float(X[:, 3].mean()),
)

# Bouton pour lancer la prédiction
start_prediction = st.sidebar.button("Prédire")

# Ajouter un espace avant la section des résultats
st.write("##")
st.subheader("Utilisation de modèle de Machine Learning")

# -------- Effectuer la prédiction --------
if start_prediction:
    # Créer un tableau avec les valeurs d'entrée
    input_data = [[sepal_length, sepal_width, petal_length, petal_width]]

    # Prédire la classe de la fleur
    prediction = clf.predict(input_data)

    # Obtenir les probabilités pour chaque classe
    prediction_proba = clf.predict_proba(input_data)

    # Afficher le résultat de la prédiction
    st.write("### Classe prédite : ", iris.target_names[prediction][0])
    st.write("### Probabilités :")
    st.write(prediction_proba)

# Ajouter des espaces et une ligne de séparation
st.write("##")
st.divider()
st.write("##")

# Sous-titre pour la section HTML et CSS
st.subheader("Utiliser html et css")

# Injecter du CSS personnalisé pour augmenter la taille du texte
st.markdown(
    """
    <style>
    .grand-texte {
        font-size:70px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Utiliser une balise HTML avec la classe CSS définie
st.markdown('<p class="grand-texte">Texte en grand</p>', unsafe_allow_html=True)

# Ajouter un espace avant la section suivante
st.write("##")
st.subheader("Utiliser le cache")


# -------- Utilisation du cache avec st.cache_data --------
@st.cache_data(ttl=60)  # Le cache expire après 60 secondes
def charger_donnees():
    # Simulation d'un chargement de données coûteux
    data = {"valeurs": [1, 2, 3, 4, 5]}
    return data


# Appeler la fonction pour charger les données
data = charger_donnees()
st.write(data)


# -------- Mise en cache d'un modèle de Machine Learning --------
@st.cache_data
def train_model():
    # Simuler un entraînement de modèle coûteux
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X, Y)
    return clf


# Appeler la fonction pour entraîner le modèle (sera mis en cache)
clf = train_model()

# Ajouter un espace avant la section suivante
st.write("##")
st.subheader("Utiliser la session")

# -------- Gestion de l'état avec st.session_state --------
# Initialiser un compteur dans la session si ce n'est pas déjà fait
if "compteur" not in st.session_state:
    st.session_state.compteur = 0

# Bouton pour incrémenter le compteur
if st.button("Incrémenter"):
    st.session_state.compteur += 1

# Afficher la valeur actuelle du compteur
st.write("Valeur du compteur : ", st.session_state.compteur)
