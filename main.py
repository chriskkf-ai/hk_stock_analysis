import pandas as pd
import yfinance as yf
import os
from datetime import datetime

print("🚀 程式開始運行")

# ✅ 自動建立 data folder（避免錯誤）
os.makedirs("data", exist_ok=True)

# ------------------------
# 股票清單（先用少量加快速度）
# ------------------------
stocks = [
    "0005.HK", "0700.HK", "0939.HK",
    "1211.HK", "1810.HK", "3690.HK"
]

# ------------------------
# 板塊分類
# ------------------------
sector_map = {
    "0700.HK": "科技",
    "3690.HK": "科技",
    "1810.HK": "科技",
    "1211.HK": "新能源",

    "0005.HK": "銀行",
    "0939.HK": "銀行"
}

# ------------------------
# 主程序
# ------------------------
data = []

for stock in stocks:
    print(f"📊 正在處理: {stock}")

    try:
        ticker = yf.Ticker(stock)

        df = ticker.history(period="5d")

        # ✅ 防止冇數據
        if df.empty or len(df) < 2:
            print(f"⚠️ 跳過 {stock}")
            continue

        latest = df.iloc[-1]
        prev = df.iloc[-2]

        close_price = latest["Close"]
        volume = latest["Volume"]

        change_pct = (close_price - prev["Close"]) / prev["Close"] * 100

        # ✅ 簡單爆升判斷
        signal = ""
        if change_pct > 3:
            signal = "🔥爆升"

        sector = sector_map.get(stock, "其他")

        data.append({
            "Stock": stock,
            "Sector": sector,
            "Close": round(close_price, 2),
            "Volume": int(volume),
            "Change %": round(change_pct, 2),
            "Signal": signal
        })

    except Exception as e:
        print(f"❌ 錯誤 {stock}: {e}")
        continue

# ------------------------
# 轉 DataFrame
# ------------------------
df = pd.DataFrame(data)

if df.empty:
    print("❌ 沒有數據，請檢查")
    exit()

# 排序
df = df.sort_values(by="Volume", ascending=False)

# ------------------------
# 板塊分析
# ------------------------
sector_summary = df.groupby("Sector").size().reset_index(name="Count")

# ------------------------
# ✅ 輸出 Excel（確保一定成功）
# ------------------------
output_path = "data/output.xlsx"
history_path = "data/history.xlsx"

today = datetime.today().strftime("%Y-%m-%d")
df["Date"] = today

# 歷史
if os.path.exists(history_path):
    old_df = pd.read_excel(history_path)
    df_hist = pd.concat([old_df, df], ignore_index=True)
else:
    df_hist = df

df_hist.to_excel(history_path, index=False)

# Dashboard用
with pd.ExcelWriter(output_path) as writer:
    df.to_excel(writer, sheet_name="Top Stocks", index=False)
    sector_summary.to_excel(writer, sheet_name="Sector Analysis", index=False)

print("✅ 成功生成 data/output.xlsx")
print("✅ 完成！")
