
import streamlit as st
import pandas as pd
import difflib

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
    "coccidia": "coccidiosis",
    "cocci": "coccidiosis",
    "flu": "avian influenza"
}

st.set_page_config(page_title="Poultry Medicine Search App", layout="wide")

st.image("https://raw.githubusercontent.com/syedabbasprix/poultry-ai-search/main/company_logo.png", width=150)
st.title("🔍 Poultry Medicine Search App")
st.write("Search by disease, brand, ingredient, or symptoms. Powered by AI.")

# Voice input hint for mobile users
st.markdown("🗣️ Tip: On mobile, tap mic icon on keyboard to use voice search.")

query = st.text_input("Search by disease, brand, ingredient, or symptom:").strip().lower()

def enhanced_match(row, query):
    searchable_fields = [
        str(row.get("Diseases Treated", "")).lower(),
        str(row.get("Name of Brand", "")).lower(),
        str(row.get("Formulation", "")).lower(),
        str(row.get("Dosage Form", "")).lower()
    ]
    combined_text = " ".join(searchable_fields)

    # Expand synonyms
    if query in synonyms:
        query_expanded = synonyms[query]
    else:
        query_expanded = query

    return (
        query_expanded in combined_text or
        any(query_expanded in field for field in searchable_fields) or
        any(difflib.get_close_matches(query_expanded, field.split(), cutoff=0.6) for field in searchable_fields)
    )

if query:
    results = df[df.apply(lambda row: enhanced_match(row, query), axis=1)]
    if not results.empty:
        st.success(f"Found {len(results)} product(s) matching your search.")
        st.dataframe(results)
    else:
        st.warning("No results found. Try a different spelling or term.")
else:
    st.info("Enter a disease, symptom, or ingredient to search.")

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
