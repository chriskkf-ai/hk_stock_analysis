import streamlit as st
import pandas as pd

st.set_page_config(page_title="HK Stock Dashboard", layout="wide")

st.title("📊 香港股票市場分析 Dashboard")

# 讀取 Excel
file_path = "data/output.xlsx"

df = pd.read_excel(file_path, sheet_name="Top Stocks")
sector_df = pd.read_excel(file_path, sheet_name="Sector Analysis")

# ------------------------
# 股票表
# ------------------------
st.subheader("🔥 Top 成交量股票")

st.dataframe(df, use_container_width=True)

# ------------------------
# 爆升股
# ------------------------
st.subheader("🚀 爆升股")

hot_stocks = df[df["Signal"] == "🔥爆升"]

if len(hot_stocks) > 0:
    st.dataframe(hot_stocks, use_container_width=True)
else:
    st.write("今日冇明顯爆升股")

# ------------------------
# 板塊分析
# ------------------------
st.subheader("📊 板塊熱度")

st.bar_chart(sector_df.set_index("Sector"))

# ------------------------
# 排名圖（成交量）
# ------------------------
st.subheader("📈 成交量排名")

volume_chart = df.set_index("Stock")["Volume"]

st.bar_chart(volume_chart)
