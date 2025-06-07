import streamlit as st
import pandas as pd
import difflib

# Load the medicine data
@st.cache_data
def load_data():
    df = pd.read_csv("poultry_medicines_for_app.csv")
    return df

df = load_data()

# Synonym mapping for smarter disease search
synonyms = {
    "e coli": "colibacillosis",
    "crd": "chronic respiratory disease",
    "ib": "infectious bronchitis",
    "ai": "avian influenza",
    "nd": "newcastle disease",
    "coccidia": "coccidiosis"
}

st.set_page_config(page_title="Poultry Medicine Search App", layout="wide")

st.image("https://raw.githubusercontent.com/syedabbasprix/poultry-ai-search/main/company_logo.png", width=150)

st.title("🔍 Poultry Medicine Search App")
st.write("Search by disease, brand, ingredient, or symptoms. Powered by AI.")

# Voice input hint for mobile users
st.markdown("🗣️ Tip: On mobile, tap mic icon on keyboard to use voice search.")

# Search input
query = st.text_input("Search by disease, brand, ingredient, or symptom:").strip().lower()

if query:
    # Expand synonyms
    if query in synonyms:
        query = synonyms[query]

    # Fuzzy search across multiple fields
    def is_match(row):
        searchable = " ".join([
            str(row["Diseases Treated"]),
            str(row["Name of Brand"]),
            str(row["Formulation"]),
            str(row["Dosage Form"]),
        ]).lower()
        return any(word in searchable for word in [query]) or difflib.get_close_matches(query, searchable.split(), cutoff=0.8)

    filtered = df[df.apply(is_match, axis=1)]

    if not filtered.empty:
        st.success(f"Found {len(filtered)} product(s) matching your search.")
        st.dataframe(filtered)
    else:
        st.warning("No results found. Try a different keyword or spelling.")
else:
    st.info("Enter a disease, brand, or ingredient name to begin your search.")

# Optional filters
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
