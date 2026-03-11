import streamlit as st
import pandas as pd
from processing import load_subscriptions, process_kaabu
from io import BytesIO

st.set_page_config(page_title="Kaabu - Interaction du mois", layout="wide")

st.title("📊 Kaabu - Interaction du mois")

st.sidebar.header("Upload des fichiers")

subscriptions_file = st.sidebar.file_uploader("Subscriptions", type="csv")

files = {
    "VTO": st.sidebar.file_uploader("VTO", type="xlsx"),
    "ED CITELIUM": st.sidebar.file_uploader("ED CITELIUM", type="xlsx"),
    "SMK": st.sidebar.file_uploader("SMK", type="xlsx"),
    "ADAT": st.sidebar.file_uploader("ADAT", type="xlsx")
}

date_filter = st.sidebar.date_input("Date minimum")

if st.sidebar.button("🚀 Générer le reporting"):

    subscriptions = load_subscriptions(subscriptions_file)

    rankings = {}
    rankings_valid = {}
    kpis = {}

    for name, file in files.items():

        if file:

            ranking, ranking_valid, kpi = process_kaabu(file, subscriptions, date_filter)

            rankings[name] = ranking
            rankings_valid[name] = ranking_valid
            kpis[name] = kpi

    st.header("📈 Résultats")

    cols = st.columns(len(kpis))

    for i,(name,kpi) in enumerate(kpis.items()):

        with cols[i]:

            st.subheader(name)

            st.metric("Interactions", kpi["interactions"])
            st.metric("Vraies interactions", kpi["vraies_interactions"])
            st.metric("Demandes", kpi["demandes"])
            st.metric("Validées", kpi["valides"])

    st.header("📊 Rankings Interactions")

    for name,df in rankings.items():

        st.subheader(name)
        st.dataframe(df)

    st.header("📊 Rankings Interactions Validées")

    for name,df in rankings_valid.items():

        st.subheader(name)
        st.dataframe(df)

    # Excel interactions
    output1 = BytesIO()

    with pd.ExcelWriter(output1, engine="openpyxl") as writer:

        for name, df in rankings.items():
            df.to_excel(writer, sheet_name=name, index=False)

    st.download_button(
        "📥 Télécharger Rankings Interactions",
        output1.getvalue(),
        "ranking_interactions.xlsx"
    )

    # Excel validés
    output2 = BytesIO()

    with pd.ExcelWriter(output2, engine="openpyxl") as writer:

        for name, df in rankings_valid.items():
            df.to_excel(writer, sheet_name=name, index=False)

    st.download_button(
        "📥 Télécharger Rankings Interactions Validées",
        output2.getvalue(),
        "ranking_valides.xlsx"
    )