import streamlit as st
import pandas as pd
from processing import load_subscriptions
from processing import process_kaabu
from io import BytesIO

st.set_page_config(page_title="Ranking Interactions", layout="wide")

st.title("📊 Générateur des Ranking Interactions ADAT, ED_CETELUM, SMK et VTO")

st.markdown("Upload les fichiers puis génère automatiquement les rankings.")

subscriptions_file = st.file_uploader("Subscriptions Monthly", type="csv")

adat_file = st.file_uploader("Fichier ADAT", type="xlsx")
citelium_file = st.file_uploader("Fichier ED CITELIUM", type="xlsx")
smk_file = st.file_uploader("Fichier SMK", type="xlsx")
vto_file = st.file_uploader("Fichier VTO", type="xlsx")

date_filter = st.date_input("Date minimum")

if st.button("🚀 Générer le ranking"):

    subscriptions = load_subscriptions(subscriptions_file)

    rankings = {}

    if adat_file:
        rankings["ADAT"] = process_kaabu(adat_file, subscriptions, date_filter)

    if citelium_file:
        rankings["CITELIUM"] = process_kaabu(citelium_file, subscriptions, date_filter)

    if smk_file:
        rankings["SMK"] = process_kaabu(smk_file, subscriptions, date_filter)

    if vto_file:
        rankings["VTO"] = process_kaabu(vto_file, subscriptions, date_filter)

    st.success("Rankings générés !")

    for name, df in rankings.items():
        st.subheader(name)
        st.dataframe(df)

    # Génération Excel
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for name, df in rankings.items():
            df.to_excel(writer, sheet_name=name, index=False)

    st.download_button(
        label="📥 Télécharger le fichier Excel",
        data=output.getvalue(),
        file_name="ranking_interactions.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )