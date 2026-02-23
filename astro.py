import streamlit as st

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
# Fonction de calcul bonus/malus astral
# ==============================
def calc_bonus_astral(heure_astrale, heure_naissance, nombre_astral):
    diff = (heure_astrale + nombre_astral - heure_naissance) % 12
    if diff == 0:
        return 4  # Heure de Grand Destin
    elif diff in (1, 11):
        return 3  # Très favorable
    elif diff in (2, 10):
        return 2  # Favorable
    elif diff in (3, 9):
        return 0  # Neutre
    elif diff in (4, 8):
        return -2  # Un peu défavorable
    elif diff in (5, 7):
        return -3  # Défavorable
    elif diff == 6:
        return -4  # Chaos astral

# ==============================
# Texte narratif en fonction du modificateur
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
    else:
        return f"{nom_heure} : modificateur inconnu."

# ==============================
# Interface Streamlit
# ==============================
st.subheader("🔮 Calcul du Bonus/Malus Astral")

heure_astrale = st.number_input("Heure Astrale actuelle (1-12)", min_value=1, max_value=12, value=1)
heure_naissance = st.number_input("Heure de naissance du personnage (HN, 1-12)", min_value=1, max_value=12, value=4)
nombre_astral = st.number_input("Nombre Astral du personnage (NA, 1-12)", min_value=1, max_value=12, value=3)

if st.button("Calculer le modificateur astral"):
    bonus = calc_bonus_astral(heure_astrale, heure_naissance, nombre_astral)
    nom_heure = heures_ast[heure_astrale]
    st.success(f"Modificateur astral : {bonus:+d}")
    st.info(texte_astral(bonus, nom_heure))
