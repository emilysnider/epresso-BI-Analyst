import numpy as np
import pandas as pd
import streamlit as st

# --- 1. Page setup ---------------------------------------------------------
st.set_page_config(page_title="Sales BI Dashboard", layout="wide")


# --- 2. Data loading -------------------------------------------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    """Create a small synthetic sales dataset (replace with a CSV/DB later)."""
    rng = np.random.default_rng(42)
    dates = pd.date_range("2025-01-01", periods=365, freq="D")
    regions = ["North", "South", "East", "West"]

    df = pd.DataFrame(
        {
            "date": np.repeat(dates, len(regions)),
            "region": np.tile(regions, len(dates)),
        }
    )
    df["revenue"] = rng.normal(1000, 200, len(df)).round(2)
    df["orders"] = rng.integers(10, 60, len(df))
    return df


df = load_data()

# --- 3. Title --------------------------------------------------------------
st.title("Sales Dashboard")

# --- 4. Sidebar filter -----------------------------------------------------
st.sidebar.header("Filters")
all_regions = sorted(df["region"].unique())
selected_regions = st.sidebar.multiselect(
    "Region", options=all_regions, default=all_regions
)
filtered = df[df["region"].isin(selected_regions)]

# --- 5. KPI metrics --------------------------------------------------------
total_revenue = filtered["revenue"].sum()
total_orders = filtered["orders"].sum()
rev_per_order = total_revenue / total_orders if total_orders else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total revenue", f"${total_revenue:,.0f}")
col2.metric("Total orders", f"{total_orders:,}")
col3.metric("Revenue per order", f"${rev_per_order:,.2f}")

# --- 6. Chart --------------------------------------------------------------
st.subheader("Monthly revenue")
monthly = filtered.set_index("date").resample("MS")["revenue"].sum()
st.line_chart(monthly)

# --- 7. Raw data table -----------------------------------------------------
st.subheader("Data")
st.dataframe(filtered, use_container_width=True)
