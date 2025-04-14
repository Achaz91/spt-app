import streamlit as st
import numpy as np

# Titre de l'application
st.title("Calculateur d'Essai de Pénétration Standard (SPT)")
st.markdown("Un outil simple pour calculer et corriger la valeur N de l'essai SPT.")

# --- Saisie des données ---
st.subheader("1. Saisie des données de l'essai")

profondeur = st.number_input("Profondeur de l'essai (m)", min_value=0.0, step=0.1)
n1 = st.number_input("Nombre de coups N1 (0-15 cm)", min_value=0, step=1)
n2 = st.number_input("Nombre de coups N2 (15-30 cm)", min_value=0, step=1)
n3 = st.number_input("Nombre de coups N3 (30-45 cm)", min_value=0, step=1)

type_marteau = st.selectbox(
    "Type de marteau",
    options=["Donut (Ce ≈ 0.45-0.60)", "Sécurité (Ce ≈ 0.70-0.85)", "Automatique (Ce ≈ 0.80-1.00)"],
    index=1  # Sélectionne "Sécurité" par défaut
)

longueur_tige = st.number_input("Longueur de la tige de forage (m)", min_value=0.0, step=0.1, value=5.0)
diametre_forage = st.selectbox(
    "Diamètre du forage (mm) (optionnel)",
    options=[60, 75, 100, 115, 150, 200],
    index=0
)
liner = st.checkbox("Présence d'un tubage (liner) dans l'échantillonneur ?")
sigma_vo_prime = st.number_input("Contrainte verticale effective (σ'vo) à la profondeur d'essai (kPa)", min_value=0.0, step=0.1, value=100.0)
pa = st.number_input("Pression atmosphérique de référence (kPa)", min_value=0.0, step=0.1, value=100.0)

# --- Calcul de Nfield ---
n_field = n2 + n3

# --- Détermination des facteurs de correction ---
st.subheader("2. Calcul des corrections")

# Correction d'énergie (Ce)
if "Donut" in type_marteau:
    ce = st.slider("Coefficient d'énergie (Ce)", min_value=0.45, max_value=0.60, value=0.55, step=0.01)
elif "Sécurité" in type_marteau:
    ce = st.slider("Coefficient d'énergie (Ce)", min_value=0.70, max_value=0.85, value=0.80, step=0.01)
else:  # Automatique
    ce = st.slider("Coefficient d'énergie (Ce)", min_value=0.80, max_value=1.00, value=0.90, step=0.01)

# Correction de la longueur de la tige (Cr)
if longueur_tige < 3:
    cr = 0.75
elif longueur_tige <= 4:
    cr = 0.85
elif longueur_tige <= 6:
    cr = 0.95
else:
    cr = 1.00
st.write(f"Coefficient de correction de la longueur de la tige (Cr): {cr:.2f}")

# Correction du diamètre du forage (Cb)
if diametre_forage <= 115:
    cb = 1.00
elif diametre_forage == 150:
    cb = 1.05
elif diametre_forage == 200:
    cb = 1.15
else:
    cb = 1.00
st.write(f"Coefficient de correction du diamètre du forage (Cb): {cb:.2f}")

# Correction du tubage (Cs)
cs = 1.00 if liner else 1.20
st.write(f"Coefficient de correction du tubage (Cs): {cs:.2f}")

# Correction de la pression de confinement (Cn) - Formule de Liao et Whitman
cn = np.sqrt(pa / sigma_vo_prime)
if cn > 2.0:
    cn = 2.0
st.write(f"Coefficient de correction de la pression de confinement (Cn): {cn:.2f}")

# --- Calcul des valeurs N corrigées ---
st.subheader("3. Résultats des calculs")

st.write(f"Valeur N brute (Nfield): **{n_field}**")

n60 = n_field * ce
st.write(f"Valeur N corrigée pour l'énergie (N60): **{n60:.2f}**")

n1_60 = n_field * ce * cn * cr * cb * cs
st.write(f"Valeur N corrigée pour l'énergie et la pression de confinement ((N1)60): **{n1_60:.2f}**")

# --- Notes ---
st.subheader("Notes importantes")
st.markdown("- Les coefficients d'énergie (Ce) sont des valeurs approximatives et peuvent varier.")
st.markdown("- La formule de correction de la pression de confinement utilisée ici est celle de Liao et Whitman (1986). D'autres formules existent.")
st.markdown("- Cette application fournit les calculs de base. L'interprétation des valeurs N corrigées pour estimer les propriétés du sol nécessite des connaissances en géotechnique et l'utilisation de corrélations empiriques appropriées.")
