import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

PALETTE = "Blues_d"
BG = "#0f1117"
TEXT = "white"
ACCENT = "#4C9BE8"

def style():
    plt.rcParams.update({
        "figure.facecolor": BG,
        "axes.facecolor":   "#1a1f2e",
        "axes.edgecolor":   "#333",
        "axes.labelcolor":  TEXT,
        "xtick.color":      TEXT,
        "ytick.color":      TEXT,
        "text.color":       TEXT,
        "grid.color":       "#2a2a3e",
        "grid.linestyle":   "--",
        "grid.alpha":       0.5,
    })

# 1 - Line Chart
def line_population(df):
    style()
    data = df.groupby("Time")["TPopulation1July"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(data["Time"], data["TPopulation1July"] / 1e6,
            color=ACCENT, linewidth=2.5, marker="o", markersize=3)
    ax.fill_between(data["Time"], data["TPopulation1July"] / 1e6,
                    alpha=0.15, color=ACCENT)
    ax.set_title("Global Population Over Time", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Population (Billions)")
    ax.grid(True)
    plt.tight_layout()
    return fig

# 2 - Bar Chart
def bar_top_regions(df):
    style()
    year = df["Time"].max()
    data = (df[df["Time"] == year]
            .groupby("Location")["TPopulation1July"]
            .sum()
            .nlargest(15)
            .reset_index())
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(data["Location"], data["TPopulation1July"] / 1e3,
            color=sns.color_palette("Blues_d", 15))
    ax.set_title(f"Top 15 Regions by Population ({int(year)})",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Population (Thousands)")
    ax.invert_yaxis()
    ax.grid(True, axis="x")
    plt.tight_layout()
    return fig

# 3 - Pie Chart
def pie_region_share(df):
    style()
    year = df["Time"].max()
    data = (df[df["Time"] == year]
            .groupby("Location")["TPopulation1July"]
            .sum()
            .nlargest(8))
    others = (df[df["Time"] == year]["TPopulation1July"].sum() - data.sum())
    if others > 0:
        data["Others"] = others
    if data.empty:
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.text(0.5, 0.5, "No data available",
                ha="center", va="center", color=TEXT, fontsize=13)
        ax.set_facecolor("#1a1f2e")
        return fig
    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        data.values,
        labels=data.index,
        autopct="%1.1f%%",
        colors=sns.color_palette("Blues", len(data)),
        startangle=140,
        pctdistance=0.82,
        wedgeprops=dict(edgecolor=BG, linewidth=1.5)
    )
    for t in texts + autotexts:
        t.set_color(TEXT)
    ax.set_title(f"Population Share by Region ({int(year)})",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    return fig

# 4 - Histogram
def histogram_growth(df):
    style()
    data = df["PopGrowthRate"].dropna()
    fig, ax = plt.subplots(figsize=(9, 4))
    if len(data) == 0:
        ax.text(0.5, 0.5, "No data available",
                ha="center", va="center", color=TEXT, fontsize=13)
        ax.set_facecolor("#1a1f2e")
        return fig
    ax.hist(data, bins=40, color=ACCENT, edgecolor=BG, alpha=0.85)
    ax.axvline(data.mean(), color="orange", linewidth=2,
               linestyle="--", label=f"Mean: {data.mean():.2f}%")
    ax.set_title("Distribution of Population Growth Rate",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Growth Rate (%)")
    ax.set_ylabel("Frequency")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    return fig

# 5 - Scatter Plot
def scatter_lex_tfr(df):
    style()
    sample = df.dropna(subset=["LEx", "TFR"])
    if len(sample) == 0:
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.text(0.5, 0.5, "No data available",
                ha="center", va="center", color=TEXT, fontsize=13)
        ax.set_facecolor("#1a1f2e")
        return fig
    sample = sample.sample(min(2000, len(sample)), random_state=42)
    fig, ax = plt.subplots(figsize=(9, 5))
    sc = ax.scatter(sample["LEx"], sample["TFR"],
                    c=sample["Time"], cmap="Blues",
                    alpha=0.6, s=15, edgecolors="none")
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("Year", color=TEXT)
    cbar.ax.yaxis.set_tick_params(color=TEXT)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=TEXT)
    ax.set_title("Life Expectancy vs Fertility Rate",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Life Expectancy (Years)")
    ax.set_ylabel("Total Fertility Rate")
    ax.grid(True)
    plt.tight_layout()
    return fig

# 6 - Box Plot
def box_life_expectancy(df):
    style()
    decades = df.copy()
    decades["Decade"] = (decades["Time"] // 10 * 10).astype(int)
    data = decades.dropna(subset=["LEx"])
    if data.empty:
        fig, ax = plt.subplots(figsize=(11, 5))
        ax.text(0.5, 0.5, "No data available",
                ha="center", va="center", color=TEXT, fontsize=13)
        ax.set_facecolor("#1a1f2e")
        return fig
    fig, ax = plt.subplots(figsize=(11, 5))
    decade_list = sorted(data["Decade"].unique())
    plot_data = [data[data["Decade"] == d]["LEx"].values for d in decade_list]
    plot_data = [arr for arr in plot_data if len(arr) > 0]
    decade_list = [d for d, arr in zip(
        decade_list,
        [data[data["Decade"] == d]["LEx"].values for d in decade_list]
    ) if len(arr) > 0]
    bp = ax.boxplot(plot_data, patch_artist=True, notch=False,
                    medianprops=dict(color="orange", linewidth=2))
    colors = sns.color_palette("Blues", len(decade_list))
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
    ax.set_xticklabels([str(d) + "s" for d in decade_list], rotation=45)
    ax.set_title("Life Expectancy Distribution by Decade",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Decade")
    ax.set_ylabel("Life Expectancy (Years)")
    ax.grid(True, axis="y")
    plt.tight_layout()
    return fig

# 7 - Heatmap
def heatmap_correlation(df):
    style()
    cols = ["TPopulation1July", "LEx", "TFR", "CBR",
            "CDR", "MedianAgePop", "NatChangeRT", "PopGrowthRate"]
    corr_data = df[cols].dropna()
    if corr_data.empty:
        fig, ax = plt.subplots(figsize=(9, 7))
        ax.text(0.5, 0.5, "No data available",
                ha="center", va="center", color=TEXT, fontsize=13)
        ax.set_facecolor("#1a1f2e")
        return fig
    corr = corr_data.corr()
    labels = ["Population", "Life Exp", "Fertility",
              "Birth Rate", "Death Rate", "Median Age",
              "Nat Change", "Growth Rate"]
    fig, ax = plt.subplots(figsize=(9, 7))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f",
                cmap="Blues", ax=ax,
                xticklabels=labels, yticklabels=labels,
                linewidths=0.5, linecolor="#1a1f2e",
                annot_kws={"size": 9})
    ax.set_title("Feature Correlation Heatmap",
                 fontsize=14, fontweight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    return fig

# 8 - Area Chart
def area_birth_death(df):
    style()
    data = df.groupby("Time")[["CBR", "CDR"]].mean().reset_index()
    if data.empty:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.text(0.5, 0.5, "No data available",
                ha="center", va="center", color=TEXT, fontsize=13)
        ax.set_facecolor("#1a1f2e")
        return fig
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.fill_between(data["Time"], data["CBR"],
                    alpha=0.5, color="#4C9BE8", label="Birth Rate")
    ax.fill_between(data["Time"], data["CDR"],
                    alpha=0.5, color="#E8734C", label="Death Rate")
    ax.plot(data["Time"], data["CBR"], color="#4C9BE8", linewidth=1.5)
    ax.plot(data["Time"], data["CDR"], color="#E8734C", linewidth=1.5)
    ax.set_title("Birth Rate vs Death Rate Over Time",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Rate per 1,000 population")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    return fig

# 9 - Count Plot
def count_growth_category(df):
    style()
    data = df.copy()
    data["GrowthCategory"] = pd.cut(
        data["PopGrowthRate"],
        bins=[-99, 0, 1, 2, 3, 99],
        labels=["Negative", "0–1%", "1–2%", "2–3%", "3%+"]
    )
    counts = data["GrowthCategory"].value_counts().sort_index()
    if counts.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, "No data available",
                ha="center", va="center", color=TEXT, fontsize=13)
        ax.set_facecolor("#1a1f2e")
        return fig
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(counts.index.astype(str), counts.values,
                  color=sns.color_palette("Blues_d", len(counts)),
                  edgecolor=BG)
    for bar, val in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 20, str(val),
                ha="center", va="bottom", fontsize=9, color=TEXT)
    ax.set_title("Count of Records by Growth Rate Category",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Growth Rate Category")
    ax.set_ylabel("Count")
    ax.grid(True, axis="y")
    plt.tight_layout()
    return fig

# 10 - Violin Plot
def violin_fertility(df):
    style()
    data = df.copy()
    data["Era"] = pd.cut(data["Time"],
                         bins=[1949, 1970, 1990, 2010, 2100],
                         labels=["1950–1970", "1971–1990",
                                 "1991–2010", "2011–2100"])
    data = data.dropna(subset=["TFR", "Era"])
    era_labels = data["Era"].cat.categories
    plot_data = [data[data["Era"] == era]["TFR"].values
                 for era in era_labels]
    valid = [(arr, label) for arr, label in zip(plot_data, era_labels)
             if len(arr) > 1]
    if not valid:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.text(0.5, 0.5, "Not enough data for violin plot",
                ha="center", va="center", color=TEXT, fontsize=13)
        ax.set_facecolor("#1a1f2e")
        return fig
    arrays, labels = zip(*valid)
    fig, ax = plt.subplots(figsize=(10, 5))
    parts = ax.violinplot(arrays,
                          positions=range(len(arrays)),
                          showmedians=True, showextrema=True)
    for pc in parts["bodies"]:
        pc.set_facecolor(ACCENT)
        pc.set_alpha(0.7)
    parts["cmedians"].set_color("orange")
    parts["cmaxes"].set_color(TEXT)
    parts["cmins"].set_color(TEXT)
    parts["cbars"].set_color(TEXT)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_title("Fertility Rate Distribution by Era",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Era")
    ax.set_ylabel("Total Fertility Rate")
    ax.grid(True, axis="y")
    plt.tight_layout()
    return fig