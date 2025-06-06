import streamlit as st
import pandas as pd

# Load the medicine data
@st.cache_data
def load_data():
    df = pd.read_csv("poultry_medicines_for_app.csv")
    return df

df = load_data()

st.title("🔍 Poultry Medicine Search App")
st.write("Search for medicines by disease name. Designed for veterinary sales teams.")

# Search input
query = st.text_input("Enter disease name (e.g., CRD, E. coli, Coccidiosis):").strip().lower()

if query:
    # Filter rows where disease is mentioned
    results = df[df["Diseases Treated"].str.lower().str.contains(query, na=False)]
    if not results.empty:
        st.success(f"Found {len(results)} product(s) matching: '{query}'")
        st.dataframe(results)
    else:
        st.error("No products found for this disease.")
else:
    st.info("Please enter a disease name to begin.")
