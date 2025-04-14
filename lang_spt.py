import streamlit as st
import numpy as np
import json

# --- Fonction pour charger le texte en fonction de la langue ---
def load_text(language):
    try:
        with open(f"lang_spt_{language}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Le fichier de langue 'lang_spt_{language}.json' n'a pas été trouvé.")
        return {}

# --- Sélection de la langue ---
languages = ["fr", "en"]
selected_language = st.sidebar.selectbox(
    "🌐 " + load_text(st.session_state.get("language", "fr")).get("select_language", "Select language:"),
    languages,
    index=languages.index(st.session_state.get("language", "fr")) if st.session_state.get("language") else 0,
    format_func=lambda lang: "Français" if lang == "fr" else "English",
    key="language_selector"
)

# --- Mise à jour de la langue dans la session state ---
if "language" not in st.session_state or st.session_state["language"] != selected_language:
    st.session_state["language"] = selected_language
    st.rerun()

# --- Chargement du texte dans la langue sélectionnée ---
text = load_text(st.session_state["language"])

# --- Titre de l'application ---
st.title(text.get("title", "Standard Penetration Test (SPT) Calculator"))
st.markdown(text.get("subtitle", "A simple tool to calculate and correct the SPT N-value."))

# --- Saisie des données ---
st.subheader(text.get("input_data_header", "1. Input Test Data"))

profondeur = st.number_input(text.get("depth", "Test Depth (m)"), min_value=0.0, step=0.1)
n1 = st.number_input(text.get("n_blows_1", "Blow Count N1 (0-15 cm)"), min_value=0, step=1)
n2 = st.number_input(text.get("n_blows_2", "Blow Count N2 (15-30 cm)"), min_value=0, step=1)
n3 = st.number_input(text.get("n_blows_3", "Blow Count N3 (30-45 cm)"), min_value=0, step=1)

type_marteau = st.selectbox(
    text.get("hammer_type", "Hammer Type"),
    options=[
        text.get("hammer_donut", "Donut (Ce ≈ 0.45-0.60)"),
        text.get("hammer_safety", "Safety (Ce ≈ 0.70-0.85)"),
        text.get("hammer_automatic", "Automatic (Ce ≈ 0.80-1.00)"),
    ],
    index=1 if text["select_language"] == "Select language:" else 1 # Garder l'index par défaut
)

longueur_tige = st.number_input(text.get("rod_length", "Drill Rod Length (m)"), min_value=0.0, step=0.1, value=5.0)
diametre_forage = st.selectbox(
    text.get("borehole_diameter", "Borehole Diameter (mm) (optional)"),
    options=[60, 75, 100, 115, 150, 200],
    index=0
)
liner = st.checkbox(text.get("liner", "Split-spoon sampler with liner?"))
sigma_vo_prime = st.number_input(text.get("effective_stress", "Effective Vertical Stress (σ'vo) at test depth (kPa)"), min_value=0.0, step=0.1, value=100.0)
pa = st.number_input(text.get("atmospheric_pressure", "Reference Atmospheric Pressure (kPa)"), min_value=0.0, step=0.1, value=101.3)

# --- Calcul de Nfield ---
n_field = n2 + n3

# --- Détermination des facteurs de correction ---
st.subheader(text.get("calculation_header", "2. Correction Calculations"))

# Correction d'énergie (Ce)
if text.get("hammer_donut", "Donut") in type_marteau:
    ce = st.slider(text.get("energy_coefficient", "Energy Ratio (Ce)"), min_value=0.45, max_value=0.60, value=0.55, step=0.01)
elif text.get("hammer_safety", "Safety") in type_marteau:
    ce = st.slider(text.get("energy_coefficient", "Energy Ratio (Ce)"), min_value=0.70, max_value=0.85, value=0.80, step=0.01)
else:  # Automatique
    ce = st.slider(text.get("energy_coefficient", "Energy Ratio (Ce)"), min_value=0.80, max_value=1.00, value=0.90, step=0.01)

# Correction de la longueur de la tige (Cr)
if longueur_tige < 3:
    cr = 0.75
elif longueur_tige <= 4:
    cr = 0.85
elif longueur_tige <= 6:
    cr = 0.95
else:
    cr = 1.00
st.write(f"{text.get('rod_length_coefficient', 'Rod Length Correction Factor (Cr):')} {cr:.2f}")

# Correction du diamètre du forage (Cb)
if diametre_forage <= 115:
    cb = 1.00
elif diametre_forage == 150:
    cb = 1.05
elif diametre_forage == 200:
    cb = 1.15
else:
    cb = 1.00
st.write(f"{text.get('borehole_coefficient', 'Borehole Diameter Correction Factor (Cb):')} {cb:.2f}")

# Correction du tubage (Cs)
cs = 1.00 if liner else 1.20
st.write(f"{text.get('liner_coefficient', 'Sampler with Liner Correction Factor (Cs):')} {cs:.2f}")

# Correction de la pression de confinement (Cn) - Formule de Liao et Whitman
cn = np.sqrt(pa / sigma_vo_prime)
if cn > 2.0:
    cn = 2.0
st.write(f"{text.get('confinement_coefficient', 'Overburden Pressure Correction Factor (Cn):')} {cn:.2f}")

# --- Calcul des valeurs N corrigées ---
st.subheader(text.get("results_header", "3. Calculation Results"))

st.write(f"{text.get('n_field_value', 'Raw N-value (Nfield):')} **{n_field}**")

n60 = n_field * ce
st.write(f"{text.get('n60_value', 'Energy-Corrected N-value (N60):')} **{n60:.2f}**")

n1_60 = n_field * ce * cn * cr * cb * cs
st.write(f"{text.get('n1_60_value', 'Overburden and Energy-Corrected N-value ((N1)60):')} **{n1_60:.2f}**")

# --- Notes ---
st.subheader(text.get("notes_header", "Important Notes"))
st.markdown(text.get("note_1", "- Energy ratios (Ce) are approximate and can vary."))
st.markdown(text.get("note_2", "- The overburden pressure correction formula used here is from Liao and Whitman (1986). Other formulas exist."))
st.markdown(text.get("note_3", "- This application provides basic calculations. The interpretation of corrected N-values for estimating soil properties requires geotechnical knowledge and the use of appropriate empirical correlations."))

st.sidebar.markdown("---")
st.sidebar.markdown(f"Langue sélectionnée : **{text.get('select_language', '').replace('Sélectionnez la langue :', 'Français').replace('Select language:', 'English').split(': ')[0]}**: **{'Français' if st.session_state.language == 'fr' else 'English'}**")
