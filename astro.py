import streamlit as st
from PIL import Image
import sqlite3
import os

# ==============================
# Configuration base SQLite
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "joueurs.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS joueurs (
            nom TEXT PRIMARY KEY,
            heure_naissance INTEGER
        )
    """)
    conn.commit()
    conn.close()

def ajouter_joueur(nom, heure_naissance):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO joueurs (nom, heure_naissance) VALUES (?, ?)",
        (nom, heure_naissance)
    )
    conn.commit()
    conn.close()

def supprimer_joueur(nom):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM joueurs WHERE nom = ?", (nom,))
    conn.commit()
    conn.close()

def charger_joueurs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nom, heure_naissance FROM joueurs")
    data = cursor.fetchall()
    conn.close()
    return {nom: hn for nom, hn in data}

init_db()

# ==============================
# Heures astrales
# ==============================

heures_ast = {
    1: "Le Vaisseau",
    2: "La Sirène",
    3: "Le Faucon",
    4: "La Couronne",
    5: "Le Dragon",
    6: "Les Epées",
    7: "La Lyre",
    8: "Le Serpent",
    9: "Le Poisson Acrobate",
    10: "L’Araignée",
    11: "Le Roseau",
    12: "Le Château Dormant"
}

# ==============================
# Calcul bonus/malus
# ==============================

def calc_bonus_astral(heure_astrale, heure_naissance, nombre_astral):
    diff = (heure_astrale + nombre_astral - heure_naissance) % 12
    if diff == 0:
        return 4
    elif diff in (1, 11):
        return 2
    elif diff in (2, 3, 5, 7, 9, 10):
        return 0
    elif diff in (4, 8):
        return -2
    elif diff == 6:
        return -4
    return 0

def texte_astral(bonus, nom_heure):
    if bonus == 4:
        return f"✨ Très favorable ({nom_heure}) : la chance est maximale !"
    elif bonus == 2:
        return f"👍 Favorable ({nom_heure}) : les astres vous sourient."
    elif bonus == 0:
        return f"⚪ Neutre ({nom_heure}) : aucun effet particulier."
    elif bonus == -2:
        return f"❌ Défavorable ({nom_heure}) : prudence."
    elif bonus == -4:
        return f"💀 Très défavorable ({nom_heure}) : les astres sont contre vous !"

# ==============================
# Chargement session
# ==============================

if "joueurs" not in st.session_state:
    st.session_state.joueurs = charger_joueurs()

# ==============================
# Interface
# ==============================

st.title("🔮 Rêve de Dragon - Calcul Astral")

# ==============================
# Ajouter joueur
# ==============================

st.subheader("🧙‍♂️ Ajouter un joueur")

nom_joueur = st.text_input("Nom du joueur")

hn_selection = st.selectbox(
    "Heure de naissance",
    [f"{num} - {nom}" for num, nom in heures_ast.items()]
)

heure_naissance = int(hn_selection.split(" - ")[0])

if st.button("Enregistrer le joueur"):
    if nom_joueur:
        ajouter_joueur(nom_joueur, heure_naissance)
        st.session_state.joueurs = charger_joueurs()
        st.success(f"{nom_joueur} enregistré.")
        st.rerun()
    else:
        st.warning("Veuillez entrer un nom valide.")

# ==============================
# Supprimer joueur
# ==============================

if st.session_state.joueurs:
    st.subheader("🗑️ Supprimer un joueur")

    joueur_suppr = st.selectbox(
        "Choisir un joueur",
        list(st.session_state.joueurs.keys()),
        key="suppr"
    )

    if st.button("Supprimer ce joueur"):
        supprimer_joueur(joueur_suppr)
        st.session_state.joueurs = charger_joueurs()
        st.success(f"{joueur_suppr} supprimé.")
        st.rerun()

# ==============================
# Calcul astral
# ==============================

st.subheader("🔮 Calcul du Bonus/Malus Astral")

try:
    image = Image.open("rdd_roueAstrologique-300x283.jpg")
    st.image(image, caption="Roue astrologique", use_column_width=True)
except:
    st.info("Image roue astrologique non trouvée.")

heure_selection_astrale = st.selectbox(
    "Heure astrale actuelle",
    [f"{num} - {nom}" for num, nom in heures_ast.items()]
)

heure_astrale = int(heure_selection_astrale.split(" - ")[0])

if st.session_state.joueurs:

    joueur_selection = st.selectbox(
        "Sélectionnez le joueur",
        list(st.session_state.joueurs.keys()),
        key="joueur_calc"
    )

    heure_naissance_joueur = st.session_state.joueurs[joueur_selection]

    nombre_astral = st.selectbox(
        "Nombre Astral du jour",
        options=list(range(1, 13)),
        index=2
    )

    if st.button("Calculer le modificateur astral"):

        bonus = calc_bonus_astral(
            heure_astrale,
            heure_naissance_joueur,
            nombre_astral
        )

        nom_heure = heures_ast[heure_astrale]

        st.markdown(f"""
        ### ✨ Résultat Astral

        **Joueur :** {joueur_selection}  
        **Heure astrale :** {nom_heure}  
        **Modificateur :** `{bonus:+d}`
        """)

        st.info(texte_astral(bonus, nom_heure))

else:
    st.warning("Ajoutez au moins un joueur pour effectuer un calcul.")
