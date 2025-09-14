import streamlit as st
import bcrypt


def render():
    """
    Page : Hashing et Sécurité
    Rôle : ADMIN
    Objectif : Permettre à l’admin de tester le hachage des mots de passe.
    """

    st.title("🔐 Outils de Hashing & Sécurité")
    st.info(
        "Cette page permet de **tester le hachage** des mots de passe et leur vérification avant de les utiliser dans la base de données."
    )

    st.subheader("Générer un hash")
    mdp = st.text_input("🔑 Entrez un mot de passe à hasher", type="password")

    if st.button("Générer le hash"):
        if mdp:
            hashed = bcrypt.hashpw(mdp.encode("utf-8"), bcrypt.gensalt())
            st.success("✅ Mot de passe hashé avec succès :")
            st.code(hashed.decode("utf-8"), language="python")
        else:
            st.warning("⚠️ Veuillez entrer un mot de passe d'abord.")

    st.markdown("---")
    st.subheader("Vérifier un mot de passe")

    with st.form("verify_form"):
        mdp_a_verifier = st.text_input(
            "🔑 Entrez le mot de passe à vérifier", type="password"
        )
        hash_stocke = st.text_input(
            "📋 Entrez le hash stocké", help="Copiez-collez le hash généré ci-dessus."
        )

        verify_button = st.form_submit_button("Vérifier le mot de passe")

        if verify_button:
            if mdp_a_verifier and hash_stocke:
                try:
                    if bcrypt.checkpw(
                        mdp_a_verifier.encode("utf-8"), hash_stocke.encode("utf-8")
                    ):
                        st.success("✅ Le mot de passe est correct !")
                    else:
                        st.error("❌ Le mot de passe est incorrect.")
                except Exception as e:
                    st.error(f"❌ Erreur lors de la vérification : {e}")
            else:
                st.warning("⚠️ Veuillez remplir les deux champs pour la vérification.")


if __name__ == "__main__":
    render()
