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

# --- Création des fichiers de langue (lang_spt_fr.json et lang_spt_en.json) ---
# Assurez-vous que ces fichiers sont dans le même répertoire que votre script Streamlit

# Contenu de lang_spt_fr.json :
"""
{
  "title": "Calculateur d'Essai de Pénétration Standard (SPT)",
  "subtitle": "Un outil simple pour calculer et corriger la valeur N de l'essai SPT.",
  "input_data_header": "1. Saisie des données de l'essai",
  "depth": "Profondeur de l'essai (m)",
  "n_blows_1": "Nombre de coups N1 (0-15 cm)",
  "n_blows_2": "Nombre de coups N2 (15-30 cm)",
  "n_blows_3": "Nombre de coups N3 (30-45 cm)",
  "hammer_type": "Type de marteau",
  "hammer_donut": "Donut (Ce ≈ 0.45-0.60)",
  "hammer_safety": "Sécurité (Ce ≈ 0.70-0.85)",
  "hammer_automatic": "Automatique (Ce ≈ 0.80-1.00)",
  "rod_length": "Longueur de la tige de forage (m)",
  "borehole_diameter": "Diamètre du forage (mm) (optionnel)",
  "liner": "Présence d'un tubage (liner) dans l'échantillonneur ?",
  "effective_stress": "Contrainte verticale effective (σ'vo) à la profondeur d'essai (kPa)",
  "atmospheric_pressure": "Pression atmosphérique de référence (kPa)",
  "calculation_header": "2. Calcul des corrections",
  "energy_coefficient": "Coefficient d'énergie (Ce)",
  "rod_length_coefficient": "Coefficient de correction de la longueur de la tige (Cr):",
  "borehole_coefficient": "Coefficient de correction du diamètre du forage (Cb):",
  "liner_coefficient": "Coefficient de correction du tubage (Cs):",
  "confinement_coefficient": "Coefficient de correction de la pression de confinement (Cn):",
  "results_header": "3. Résultats des calculs",
  "n_field_value": "Valeur N brute (Nfield):",
  "n60_value": "Valeur N corrigée pour l'énergie (N60):",
  "n1_60_value": "Valeur N corrigée pour l'énergie et la pression de confinement ((N1)60):",
  "notes_header": "Notes importantes",
  "note_1": "- Les coefficients d'énergie (Ce) sont des valeurs approximatives et peuvent varier.",
  "note_2": "- La formule de correction de la pression de confinement utilisée ici est celle de Liao et Whitman (1986). D'autres formules existent.",
  "note_3": "- Cette application fournit les calculs de base. L'interprétation des valeurs N corrigées pour estimer les propriétés du sol nécessite des connaissances en géotechnique et l'utilisation de corrélations empiriques appropriées.",
  "select_language": "Sélectionnez la langue :"
}
"""

# Contenu de lang_spt_en.json :
"""
{
  "title": "Standard Penetration Test (SPT) Calculator",
  "subtitle": "A simple tool to calculate and correct the SPT N-value.",
  "input_data_header": "1. Input Test Data",
  "depth": "Test Depth (m)",
  "n_blows_1": "Blow Count N1 (0-15 cm)",
  "n_blows_2": "Blow Count N2 (15-30 cm)",
  "n_blows_3": "Blow Count N3 (30-45 cm)",
  "hammer_type": "Hammer Type",
  "hammer_donut": "Donut (Ce ≈ 0.45-0.60)",
  "hammer_safety": "Safety (Ce ≈ 0.70-0.85)",
  "hammer_automatic": "Automatic (Ce ≈ 0.80-1.00)",
  "rod_length": "Drill Rod Length (m)",
  "borehole_diameter": "Borehole Diameter (mm) (optional)",
  "liner": "Split-spoon sampler with liner?",
  "effective_stress": "Effective Vertical Stress (σ'vo) at test depth (kPa)",
  "atmospheric_pressure": "Reference Atmospheric Pressure (kPa)",
  "calculation_header": "2. Correction Calculations",
  "energy_coefficient": "Energy Ratio (Ce)",
  "rod_length_coefficient": "Rod Length Correction Factor (Cr):",
  "borehole_coefficient": "Borehole Diameter Correction Factor (Cb):",
  "liner_coefficient": "Sampler with Liner Correction Factor (Cs):",
  "confinement_coefficient": "Overburden Pressure Correction Factor (Cn):",
  "results_header": "3. Calculation Results",
  "n_field_value": "Raw N-value (Nfield):",
  "n60_value": "Energy-Corrected N-value (N60):",
  "n1_60_value": "Overburden and Energy-Corrected N-value ((N1)60):",
  "notes_header": "Important Notes",
  "note_1": "- Energy ratios (Ce) are approximate and can vary.",
  "note_2": "- The overburden pressure correction formula used here is from Liao and Whitman (1986). Other formulas exist.",
  "note_3": "- This application provides basic calculations. The interpretation of corrected N-values for estimating soil properties requires geotechnical knowledge and the use of appropriate empirical correlations.",
  "select_language": "Select language:"
}
"""

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
