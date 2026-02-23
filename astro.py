import streamlit as st
from PIL import Image

# ==============================
# Affichage de l'image de la roue astrologique
# ==============================
try:
    image = Image.open("rdd_roueAstrologique-300x283.jpg")  # ou "images/rdd_roueAstrologique-300x283.jpg"
    st.image(image, caption="Roue astrologique de Rêve de Dragon", use_column_width=True)
except FileNotFoundError:
    st.warning("⚠️ Image de la roue astrologique introuvable ! Vérifiez le chemin du fichier.")

# ==============================
# Heures astrales officielles Rêve de Dragon
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

# ==============================
# Texte narratif
# ==============================
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
# Interface Streamlit
# ==============================
st.subheader("🔮 Calcul du Bonus/Malus Astral")

# Création de listes pour selectbox avec numéro + nom
heures_options = [f"{num} - {nom}" for num, nom in heures_ast.items()]

# Heure astrale actuelle
heure_selection = st.selectbox("Sélectionnez l'heure astrale actuelle", heures_options)
heure_astrale = int(heure_selection.split(" - ")[0])

# Heure de naissance du personnage
hn_selection = st.selectbox("Sélectionnez l'heure de naissance du personnage (HN)", heures_options, index=3)
heure_naissance = int(hn_selection.split(" - ")[0])

# Nombre astral
nombre_astral = st.number_input("Nombre Astral du personnage (NA, 1-12)", min_value=1, max_value=12, value=3)

# Bouton calcul
if st.button("Calculer le modificateur astral"):
    bonus = calc_bonus_astral(heure_astrale, heure_naissance, nombre_astral)
    nom_heure = heures_ast[heure_astrale]
    st.success(f"Modificateur astral : {bonus:+d}")
    st.info(texte_astral(bonus, nom_heure))
