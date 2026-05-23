import pandas as pd

def load_data():
    df = pd.read_csv("data/population.csv", encoding="latin1")
    df.columns = df.columns.str.strip()
    df = df[df["Variant"] == "Medium"].copy()
    df["Time"] = pd.to_numeric(df["Time"], errors="coerce")
    df["TPopulation1July"] = pd.to_numeric(df["TPopulation1July"], errors="coerce")
    df["LEx"] = pd.to_numeric(df["LEx"], errors="coerce")
    df["TFR"] = pd.to_numeric(df["TFR"], errors="coerce")
    df["CBR"] = pd.to_numeric(df["CBR"], errors="coerce")
    df["CDR"] = pd.to_numeric(df["CDR"], errors="coerce")
    df["MedianAgePop"] = pd.to_numeric(df["MedianAgePop"], errors="coerce")
    df["NatChangeRT"] = pd.to_numeric(df["NatChangeRT"], errors="coerce")
    df["PopGrowthRate"] = pd.to_numeric(df["PopGrowthRate"], errors="coerce")
    df["NetMigrations"] = pd.to_numeric(df["NetMigrations"], errors="coerce")
    df = df.dropna(subset=["Location", "Time", "TPopulation1July"])
    return df

def apply_filters(df, year_range, selected_regions, pop_range, search_text):
    filtered = df.copy()
    filtered = filtered[
        (filtered["Time"] >= year_range[0]) &
        (filtered["Time"] <= year_range[1])
    ]
    if selected_regions:
        filtered = filtered[filtered["Location"].isin(selected_regions)]
    filtered = filtered[
        (filtered["TPopulation1July"] >= pop_range[0]) &
        (filtered["TPopulation1July"] <= pop_range[1])
    ]
    if search_text.strip():
        filtered = filtered[
            filtered["Location"].str.contains(search_text.strip(), case=False, na=False)
        ]
    return filtered