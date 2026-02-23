import streamlit as st
from PIL import Image

# ==============================
# Heures astrales Rêve de Dragon
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
# Fonction calcul bonus/malus
# ==============================
def calc_bonus_astral(heure_astrale, heure_naissance, nombre_astral):
    diff = (heure_astrale + nombre_astral - heure_naissance) % 12
    if diff == 0:
        return 4
    elif diff in (1, 11):
        return 3
    elif diff in (2, 10):
        return 2
    elif diff in (3, 9):
        return 0
    elif diff in (4, 8):
        return -2
    elif diff in (5, 7):
        return -3
    elif diff == 6:
        return -4

def texte_astral(bonus, nom_heure):
    if bonus == 4:
        return f"✨ Heure de Grand Destin ({nom_heure}) : la chance et la puissance sont maximales !"
    elif bonus == 3:
        return f"🌟 Très favorable ({nom_heure}) : tout semble tourner en votre faveur."
    elif bonus == 2:
        return f"👍 Favorable ({nom_heure}) : les astres vous sourient légèrement."
    elif bonus == 0:
        return f"⚪ Neutre ({nom_heure}) : aucun avantage ni désavantage particulier."
    elif bonus == -2:
        return f"⚠️ Un peu défavorable ({nom_heure}) : prudence conseillée."
    elif bonus == -3:
        return f"❌ Défavorable ({nom_heure}) : les difficultés sont probables."
    elif bonus == -4:
        return f"💀 Chaos astral ({nom_heure}) : les astres sont contre vous !"

# ==============================
# Stockage des joueurs et de leur HN
# ==============================
if "joueurs" not in st.session_state:
    st.session_state.joueurs = {}  # clé = nom du joueur, valeur = HN (1-12)

st.subheader("🧙‍♂️ Gestion des joueurs")

# Ajouter un joueur
nom_joueur = st.text_input("Nom du joueur à enregistrer")
hn_selection = st.selectbox("Heure de naissance du joueur", [f"{num} - {nom}" for num, nom in heures_ast.items()])
heure_naissance = int(hn_selection.split(" - ")[0])

if st.button("Enregistrer le joueur"):
    if nom_joueur:
        st.session_state.joueurs[nom_joueur] = heure_naissance
        st.success(f"Joueur {nom_joueur} enregistré avec HN = {heure_naissance} ({heures_ast[heure_naissance]})")
    else:
        st.warning("Veuillez entrer un nom de joueur valide.")

# ==============================
# Calcul du bonus/malus astral
# ==============================
st.subheader("🔮 Calcul du Bonus/Malus Astral")

# Affichage de la roue astrologique
try:
    from PIL import Image
    image = Image.open("rdd_roueAstrologique-300x283.jpg")
    st.image(image, caption="Roue astrologique de Rêve de Dragon", use_column_width=True)
except FileNotFoundError:
    st.warning("⚠️ Image de la roue astrologique introuvable ! Vérifiez le chemin du fichier.")

# Heure astrale actuelle
heures_options = [f"{num} - {nom}" for num, nom in heures_ast.items()]
heure_selection_astrale = st.selectbox("Sélectionnez l'heure astrale actuelle", heures_options)
heure_astrale = int(heure_selection_astrale.split(" - ")[0])

# Choisir le joueur pour utiliser son HN
if st.session_state.joueurs:
    joueur_selection = st.selectbox("Sélectionnez le joueur", list(st.session_state.joueurs.keys()))
    heure_naissance_joueur = st.session_state.joueurs[joueur_selection]

    nombre_astral = st.number_input("Nombre Astral du personnage (NA, 1-12)", min_value=1, max_value=12, value=3)

    if st.button("Calculer le modificateur astral pour ce joueur"):
        bonus = calc_bonus_astral(heure_astrale, heure_naissance_joueur, nombre_astral)
        nom_heure = heures_ast[heure_astrale]
        st.success(f"Modificateur astral pour {joueur_selection} : {bonus:+d}")
        st.info(texte_astral(bonus, nom_heure))
else:
    st.info("⚠️ Aucun joueur enregistré. Veuillez ajouter un joueur pour calculer le bonus astral.")
