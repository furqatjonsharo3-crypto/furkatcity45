import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
st.set_page_config(page_title="Asaxiy Dashboard", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    con = sqlite3.connect("./asaxiy.db")
    df = pd.read_sql("SELECT * FROM asaxiy_products", con)
    con.close()
    return df

df = load_data()

st.sidebar.header("Filtrlar")
kats = st.sidebar.multiselect("Kategoriya", sorted(df["category"].unique()), default=sorted(df["category"].unique()))

brendlar = st.sidebar.multiselect("Brend", sorted(df["brand"].unique()))
faqat_chegirma = st.sidebar.checkbox("Faqat chegirmadagilar")
f = df[df["category"].isin(kats)]

if brendlar:
    f = f[f["brand"].isin(brendlar)]
if faqat_chegirma:
    f = f[f["old_price"].notna()]


# --- KPI ---
st.title("Asaxiy — tahliliy dashboard")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Mahsulotlar", len(f))
c2.metric("O'rtacha narx", f"{int(f['price'].mean()):,}" if len(f) else "0")
c3.metric("Chegirmadagilar", int(f["old_price"].notna().sum()))
c4.metric("Brendlar", f["brand"].nunique())

# --- Grafiklar va jadval ---
tab1, tab2, tab3 = st.tabs(["Eng qimmat", "Brend bo'yicha", "Jadval"])
with tab1:
    st.bar_chart(f.nlargest(10, "price").set_index("name")["price"])
with tab2:
    st.bar_chart(f.groupby("brand")["price"].mean().sort_values(ascending=False))
with tab3:
    st.dataframe(f, width="stretch")
