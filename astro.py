import streamlit as st

def calc_bonus_astral(heure_astrale, heure_naissance, nombre_astral):
    """
    Calcule le bonus/malus astral pour un personnage
    heure_astrale : int, de 1 à 12 (heure courante)
    heure_naissance : int, de 1 à 12 (HN du personnage)
    nombre_astral : int, de 1 à 12 (NA du personnage)
    """
    # Différence ajustée avec le nombre astral
    diff = (heure_astrale + nombre_astral - heure_naissance) % 12

    # Table des modificateurs
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

st.subheader("🔮 Calcul du Bonus/Malus Astral")

heure_astrale = st.number_input("Heure Astrale actuelle (1-12)", min_value=1, max_value=12, value=1)
heure_naissance = st.number_input("Heure de naissance du personnage (HN, 1-12)", min_value=1, max_value=12, value=4)
nombre_astral = st.number_input("Nombre Astral du personnage (NA, 1-12)", min_value=1, max_value=12, value=3)

if st.button("Calculer le modificateur astral"):
    bonus = calc_bonus_astral(heure_astrale, heure_naissance, nombre_astral)
    st.success(f"Modificateur astral : {bonus:+d}")
