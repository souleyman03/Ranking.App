import pandas as pd

def load_subscriptions(file):

    df = pd.read_csv(file)

    df = df.sort_values(by=["MSISDN","USSD Date"], ascending=False)
    df = df.drop_duplicates(subset="MSISDN")

    df["Phone"] = df["MSISDN"].astype(str)

    df["USSD Date"] = pd.to_datetime(df["USSD Date"], errors="coerce")
    df["Date"] = df["USSD Date"].dt.strftime('%Y-%m-%d')

    return df[["Phone","Date","Status"]]


def process_kaabu(file, subscriptions, date_filter):

    kaabu = pd.read_excel(file)

    interactions = len(kaabu)
    if "Msisdn Client" not in kaabu.columns:
      raise Exception(f"Colonne 'Msisdn Client' introuvable. Colonnes disponibles: {kaabu.columns}")
    kaabu = kaabu.rename(columns={"Msisdn Client":"Phone"})
    kaabu["Phone"] = kaabu["Phone"].astype(str)

    vraies_interactions_df = kaabu.drop_duplicates(subset="Phone")

    vraies_interactions = len(vraies_interactions_df)

    subscriptions["Phone"] = subscriptions["Phone"].astype(str)

    merged = vraies_interactions_df.merge(subscriptions, on="Phone", how="inner")

    merged = merged[merged["Date"] >= str(date_filter)]

    ranking = (
        merged
        .groupby("Nom vendeur")
        .agg(interactions=("Phone","nunique"))
        .reset_index()
        .sort_values(by="interactions", ascending=False)
    )

    demandes = ranking["interactions"].sum()

    valid = merged[merged["Status"] == "OK"]

    ranking_valid = (
        valid
        .groupby(["Nom vendeur", "Msisdn Vendeur"])
        .agg(interactions=("Phone","nunique"))
        .reset_index()
        .sort_values(by="interactions", ascending=False)
    )

    inscriptions_valides = ranking_valid["interactions"].sum()

    kpi = {
        "interactions": interactions,
        "vraies_interactions": vraies_interactions,
        "demandes": demandes,
        "valides": inscriptions_valides
    }

    return ranking, ranking_valid, kpi