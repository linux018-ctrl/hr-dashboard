# 👥 HR 人力報表系統

互動式人力資源報表 Dashboard，使用 Streamlit + Plotly 建構。

## 📊 報表功能

| 頁面 | 說明 |
|------|------|
| **Dashboard 總覽** | KPI 卡片、部門分佈、月度新進 vs 離職趨勢 |
| **招募與人才配置** | 招募漏斗、月度招募趨勢、各部門錄取率、缺編情況 |
| **人才結構與異動** | 6 維結構分析、人力異動紀錄、離職率分析、重點流失警示 |

## 🚀 本機執行

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 🌐 Streamlit Cloud 部署

1. 將此專案推送至 GitHub
2. 前往 [share.streamlit.io](https://share.streamlit.io)
3. 選擇 repo → 主檔案設為 `streamlit_app.py`
4. 點擊 Deploy

## 技術棧

- **Streamlit** — 互動式 Web UI
- **Plotly** — 圖表視覺化
- **Pandas** — 資料處理
