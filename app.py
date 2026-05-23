import streamlit as st
import pandas as pd
from filters import load_data, apply_filters
from charts import (
    line_population, bar_top_regions, pie_region_share,
    histogram_growth, scatter_lex_tfr, box_life_expectancy,
    heatmap_correlation, area_birth_death,
    count_growth_category, violin_fertility
)

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="UN World Population Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .block-container { padding-top: 1.5rem; }
    .kpi-card {
        background: #1a1f2e;
        border: 1px solid #2a2a3e;
        border-radius: 12px;
        padding: 18px 22px;
        text-align: center;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #4C9BE8;
    }
    .kpi-label {
        font-size: 0.8rem;
        color: #aaa;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .section-title {
        color: #4C9BE8;
        font-size: 1.1rem;
        font-weight: 600;
        border-left: 4px solid #4C9BE8;
        padding-left: 10px;
        margin: 1.5rem 0 0.8rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_data()

df = get_data()

# ── Sidebar filters ───────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/UN_emblem_blue.svg/200px-UN_emblem_blue.svg.png", width=60)
    st.title("🌍 Filters")
    st.markdown("---")

    # Year range filter
    st.markdown("**📅 Year Range**")
    year_min = int(df["Time"].min())
    year_max = int(df["Time"].max())
    year_range = st.slider("", year_min, year_max,
                           (1950, 2024), step=1, key="year")

    st.markdown("---")

    # Region multi-select filter
    st.markdown("**🌐 Select Regions**")
    all_locations = sorted(df["Location"].unique().tolist())
    selected_regions = st.multiselect(
        "Choose one or more regions",
        options=all_locations,
        default=[]
    )

    st.markdown("---")

    # Population range slider
    st.markdown("**👥 Population Range (Thousands)**")
    pop_min = float(df["TPopulation1July"].min())
    pop_max = float(df["TPopulation1July"].max())
    pop_range = st.slider("", pop_min, pop_max,
                          (pop_min, pop_max), key="pop")

    st.markdown("---")

    # Search / text filter
    st.markdown("**🔍 Search Location**")
    search_text = st.text_input("Type a country or region name", value="")

    st.markdown("---")

    # Reset button
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()

# ── Apply filters ─────────────────────────────────────────────
filtered_df = apply_filters(df, year_range, selected_regions,
                            pop_range, search_text)

# ── Header ────────────────────────────────────────────────────
st.markdown("""
<h1 style='color:#4C9BE8; margin-bottom:0'>
    🌍 UN World Population Dashboard
</h1>
<p style='color:#aaa; margin-top:4px'>
    UN Population Division · 1950–2100 · Medium Variant ·
    SAP ID: 70154596
</p>
<hr style='border-color:#2a2a3e'>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Key Indicators</div>',
            unsafe_allow_html=True)

latest = filtered_df[filtered_df["Time"] == filtered_df["Time"].max()]

total_records  = len(filtered_df)
total_pop      = latest["TPopulation1July"].sum() / 1e6
avg_lex        = filtered_df["LEx"].mean()
avg_tfr        = filtered_df["TFR"].mean()
avg_growth     = filtered_df["PopGrowthRate"].mean()
max_pop_loc    = latest.groupby("Location")["TPopulation1July"].sum().idxmax() \
                 if not latest.empty else "N/A"

c1, c2, c3, c4, c5, c6 = st.columns(6)

def kpi(col, value, label):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>""", unsafe_allow_html=True)

kpi(c1, f"{total_records:,}",       "Total Records")
kpi(c2, f"{total_pop:.2f}B",        "Total Population")
kpi(c3, f"{avg_lex:.1f} yrs",       "Avg Life Expectancy")
kpi(c4, f"{avg_tfr:.2f}",           "Avg Fertility Rate")
kpi(c5, f"{avg_growth:.2f}%",       "Avg Growth Rate")
kpi(c6, str(max_pop_loc)[:14],      "Largest Region")

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────

# Row 1 — Line + Bar
st.markdown('<div class="section-title">📈 Population Trends</div>',
            unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.pyplot(line_population(filtered_df))
with col2:
    st.pyplot(bar_top_regions(filtered_df))

# Row 2 — Pie + Histogram
st.markdown('<div class="section-title">🔵 Distribution Analysis</div>',
            unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    st.pyplot(pie_region_share(filtered_df))
with col4:
    st.pyplot(histogram_growth(filtered_df))

# Row 3 — Scatter + Box
st.markdown('<div class="section-title">🔬 Statistical Insights</div>',
            unsafe_allow_html=True)
col5, col6 = st.columns(2)
with col5:
    st.pyplot(scatter_lex_tfr(filtered_df))
with col6:
    st.pyplot(box_life_expectancy(filtered_df))

# Row 4 — Heatmap (full width)
st.markdown('<div class="section-title">🌡️ Correlation Heatmap</div>',
            unsafe_allow_html=True)
st.pyplot(heatmap_correlation(filtered_df))

# Row 5 — Area + Count
st.markdown('<div class="section-title">📉 Rate Comparisons</div>',
            unsafe_allow_html=True)
col7, col8 = st.columns(2)
with col7:
    st.pyplot(area_birth_death(filtered_df))
with col8:
    st.pyplot(count_growth_category(filtered_df))

# Row 6 — Violin (full width)
st.markdown('<div class="section-title">🎻 Fertility Distribution</div>',
            unsafe_allow_html=True)
st.pyplot(violin_fertility(filtered_df))

# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<hr style='border-color:#2a2a3e; margin-top:2rem'>
<p style='text-align:center; color:#555; font-size:0.8rem'>
    UN Population Division · EDA Project · SAP ID 70154596 ·
    Instructor: Ali Hassan Sherazi · Course: Exploratory Data Analysis
</p>
""", unsafe_allow_html=True)