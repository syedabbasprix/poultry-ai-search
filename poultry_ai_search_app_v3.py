
import streamlit as st
import pandas as pd
import difflib

@st.cache_data
def load_data():
    df = pd.read_csv("poultry_medicines_for_app.csv")
    return df

df = load_data()

# Symptom-to-disease map
symptom_disease_map = {'bloody droppings': 'coccidiosis', 'green droppings': 'salmonellosis', 'swollen head': 'infectious coryza', 'nasal discharge': 'chronic respiratory disease', 'watery eyes': 'newcastle disease', 'coughing': 'chronic respiratory disease', 'labored breathing': 'infectious bronchitis', 'ruffled feathers': 'avian influenza', 'weight loss': 'colibacillosis', 'paralysis': "marek's disease"}

# Synonyms
synonyms = {
    "e coli": "colibacillosis",
    "crd": "chronic respiratory disease",
    "ib": "infectious bronchitis",
    "ai": "avian influenza",
    "nd": "newcastle disease",
    "coccidia": "coccidiosis",
    "cocci": "coccidiosis",
    "flu": "avian influenza"
}

st.set_page_config(page_title="Poultry Medicine Search App", layout="wide")
st.image("https://raw.githubusercontent.com/syedabbasprix/poultry-ai-search/main/company_logo.png", width=150)
st.title("🔍 Poultry Medicine Search App")
st.write("Search by disease, symptom, brand, or ingredient.")

# Voice input hint
st.markdown("🗣️ Tip: On mobile, use mic icon to search by voice.")

query = st.text_input("Search (disease, symptom, ingredient, or brand):").strip().lower()

def enhanced_match(row, query):
    fields = [
        str(row.get("Diseases Treated", "")).lower(),
        str(row.get("Name of Brand", "")).lower(),
        str(row.get("Formulation", "")).lower(),
        str(row.get("Dosage Form", "")).lower()
    ]
    combined = " ".join(fields)
    if query in symptom_disease_map:
        query = symptom_disease_map[query]
    if query in synonyms:
        query = synonyms[query]
    return (
        query in combined or
        any(query in field for field in fields) or
        any(difflib.get_close_matches(query, field.split(), cutoff=0.6) for field in fields)
    )

if query:
    results = df[df.apply(lambda row: enhanced_match(row, query), axis=1)]
    if not results.empty:
        st.success(f"Found {len(results)} product(s) matching your search.")
        st.dataframe(results)
    else:
        st.warning("No results found. Try a different spelling or symptom.")
else:
    st.info("Enter a disease, symptom, or ingredient to begin.")

with st.expander("🔬 Filter by Disease Type"):
    category_options = ["All", "Bacterial", "Viral", "Protozoal", "Nutritional", "Others"]
    selected_category = st.selectbox("Disease Category", options=category_options)
    if selected_category != "All":
        df = df[df["Diseases Treated"].str.lower().str.contains(selected_category.lower(), na=False)]

with st.expander("🔧 Advanced Filters"):
    selected_form = st.selectbox("Filter by Dosage Form", options=["All"] + sorted(df["Dosage Form"].dropna().unique().tolist()))
    selected_brand = st.selectbox("Filter by Brand", options=["All"] + sorted(df["Name of Brand"].dropna().unique().tolist()))

    filtered = df.copy()
    if selected_form != "All":
        filtered = filtered[filtered["Dosage Form"] == selected_form]
    if selected_brand != "All":
        filtered = filtered[filtered["Name of Brand"] == selected_brand]

    if not filtered.empty:
        st.subheader("Filtered Results")
        st.dataframe(filtered)
    else:
        st.info("No products match your filter selections.")
