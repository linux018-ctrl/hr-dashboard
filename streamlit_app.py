"""
HR Dashboard - 人力資源報表系統 (Streamlit 版)
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data.mock_data import (
    get_recruitment_funnel,
    get_recruitment_by_department,
    get_vacancy_status,
    get_monthly_recruitment_trend,
    get_headcount_overview,
    get_monthly_movement,
    get_turnover_by_department,
    get_turnover_by_rank,
    get_turnover_trend,
    get_leave_reason_distribution,
    get_department_rank_turnover_detail,
)

# ── 頁面設定 ──────────────────────────────────────────────
st.set_page_config(
    page_title="HR 人力報表系統",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 全域樣式 ──────────────────────────────────────────────
st.markdown("""
<style>
    :root { --accent: #3498db; --success: #2ecc71; --danger: #e74c3c; --warn: #f39c12; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50 0%, #1a252f 100%);
    }
    [data-testid="stSidebar"] * { color: #ecf0f1 !important; }
    [data-testid="stSidebar"] .stRadio label { font-size: 1rem; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.15); }

    .kpi-card {
        background: #fff;
        border-radius: 12px;
        padding: 24px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,.06);
        text-align: center;
        transition: transform .2s, box-shadow .2s;
        border-top: 4px solid var(--accent);
    }
    .kpi-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,.12); }
    .kpi-value { font-size: 2.2rem; font-weight: 800; color: #2c3e50; line-height: 1.1; }
    .kpi-label { font-size: .85rem; color: #7f8c8d; margin-top: 6px; }
    .kpi-blue   { border-top-color: #3498db; }
    .kpi-orange { border-top-color: #f39c12; }
    .kpi-green  { border-top-color: #2ecc71; }
    .kpi-red    { border-top-color: #e74c3c; }

    .section-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: #2c3e50;
        padding-bottom: 8px;
        border-bottom: 3px solid #3498db;
        margin-bottom: 12px;
        display: inline-block;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# ── Plotly 共用 ──────────────────────────────────────────
COLORS = ["#3498db", "#2ecc71", "#e74c3c", "#f39c12", "#9b59b6",
          "#1abc9c", "#e67e22", "#34495e", "#16a085", "#c0392b"]

PLOTLY_LAYOUT = dict(
    font=dict(family="Segoe UI, Microsoft JhengHei, sans-serif"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(font=dict(size=11)),
)


def styled_fig(fig, height=380):
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(0,0,0,.06)")
    return fig


# ── 側邊欄 ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 👥 HR 報表系統")
    st.markdown("---")
    page = st.radio(
        "選擇報表",
        ["🏠 Dashboard 總覽", "📋 招募與人才配置", "📊 人才結構與異動"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("© 2026 HR Analytics｜2026 年度")
    st.caption("🟢 即時模擬資料")


# ══════════════════════════════════════════════════════════
#  PAGE 1 — Dashboard 總覽
# ══════════════════════════════════════════════════════════
if page == "🏠 Dashboard 總覽":
    st.markdown("# 🏠 Dashboard 總覽")

    overview = get_headcount_overview()
    movement = get_monthly_movement()
    vacancy = get_vacancy_status()
    total_hc = overview["total"]
    total_vacancy = sum(v["vacancy"] for v in vacancy)
    total_new_hires = sum(m["new_hires"] for m in movement)
    total_resignations = sum(m["resignations"] for m in movement)
    avg_turnover = round(sum(m["monthly_turnover_rate"] for m in movement) / len(movement), 2)

    # KPI 卡片
    c1, c2, c3, c4 = st.columns(4)
    for col, val, label, css in [
        (c1, total_hc, "在職總人數", "kpi-blue"),
        (c2, total_vacancy, "總缺編人數", "kpi-orange"),
        (c3, total_new_hires, "年度新進人數", "kpi-green"),
        (c4, total_resignations, "年度離職人數", "kpi-red"),
    ]:
        col.markdown(
            f'<div class="kpi-card {css}">'
            f'<div class="kpi-value">{val}</div>'
            f'<div class="kpi-label">{label}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("")
    k1, k2, k3 = st.columns([1, 1.3, 1.3])

    with k1:
        st.markdown(
            f'<div class="kpi-card" style="padding:36px 20px; border-top-color:#e74c3c">'
            f'<div class="kpi-label">平均月離職率</div>'
            f'<div class="kpi-value" style="color:#e74c3c; font-size:3rem">{avg_turnover}%</div>'
            f'<div class="kpi-label" style="margin-top:8px">基於本年度 12 個月平均</div></div>',
            unsafe_allow_html=True,
        )

    with k2:
        df_dept = pd.DataFrame(overview["by_department"])
        fig = px.pie(df_dept, names="label", values="count", color_discrete_sequence=COLORS,
                     title="部門人數分佈", hole=0.4)
        st.plotly_chart(styled_fig(fig, 340), key="overview_dept_pie")

    with k3:
        df_mv = pd.DataFrame(movement)
        fig = go.Figure()
        fig.add_bar(x=df_mv["month"], y=df_mv["new_hires"], name="新進", marker_color="#2ecc71")
        fig.add_bar(x=df_mv["month"], y=df_mv["resignations"], name="離職", marker_color="#e74c3c")
        fig.update_layout(title="月度新進 vs 離職", barmode="group")
        st.plotly_chart(styled_fig(fig, 340), key="overview_mv_bar")

    # 月度異動表
    st.markdown('<div class="section-header">📋 月度人力異動摘要</div>', unsafe_allow_html=True)
    df_mv_display = df_mv.rename(columns={
        "month": "月份", "beginning_hc": "期初人數", "new_hires": "新進",
        "resignations": "離職", "transfers_in": "調入", "transfers_out": "調出",
        "ending_hc": "期末人數", "monthly_turnover_rate": "月離職率(%)",
    })
    st.dataframe(
        df_mv_display.style.format({"月離職率(%)": "{:.2f}"})
        .background_gradient(subset=["月離職率(%)"], cmap="Reds"),
        hide_index=True, height=460,
    )


# ══════════════════════════════════════════════════════════
#  PAGE 2 — 招募與人才配置
# ══════════════════════════════════════════════════════════
elif page == "📋 招募與人才配置":
    st.markdown("# 📋 招募與人才配置報表")

    r1, r2 = st.columns(2)

    with r1:
        st.markdown('<div class="section-header">🔻 招募漏斗</div>', unsafe_allow_html=True)
        funnel = get_recruitment_funnel()
        df_funnel = pd.DataFrame(funnel)
        fig = go.Figure(go.Funnel(
            y=df_funnel["stage"], x=df_funnel["count"],
            textinfo="value+percent initial",
            marker=dict(color=["#3498db", "#2980b9", "#1abc9c", "#16a085",
                                "#2ecc71", "#27ae60", "#f39c12"]),
            connector=dict(line=dict(color="#ddd")),
        ))
        fig.update_layout(title="招募漏斗 (Recruitment Funnel)")
        st.plotly_chart(styled_fig(fig, 400), key="rec_funnel")

    with r2:
        st.markdown('<div class="section-header">📈 月度招募趨勢</div>', unsafe_allow_html=True)
        trend = get_monthly_recruitment_trend()
        df_trend = pd.DataFrame(trend)
        fig = go.Figure()
        for col_name, color, label in [
            ("applications", "#3498db", "投遞"),
            ("interviews", "#f39c12", "面試"),
            ("offers", "#2ecc71", "錄取"),
            ("hires", "#9b59b6", "報到"),
        ]:
            fig.add_scatter(x=df_trend["month"], y=df_trend[col_name],
                            mode="lines+markers", name=label,
                            line=dict(color=color, width=2.5))
        fig.update_layout(title="月度招募趨勢")
        st.plotly_chart(styled_fig(fig, 400), key="rec_trend")

    # 各部門招募統計
    st.markdown('<div class="section-header">🏢 各部門招募統計</div>', unsafe_allow_html=True)
    dept_data = get_recruitment_by_department()
    df_dept_r = pd.DataFrame(dept_data).rename(columns={
        "department": "部門", "applied": "投遞", "screened": "篩選通過",
        "interviewed": "面試", "offered": "錄取", "accepted": "報到",
        "acceptance_rate": "錄取率(%)",
    })
    st.dataframe(
        df_dept_r.style
        .format({"錄取率(%)": "{:.1f}"})
        .background_gradient(subset=["錄取率(%)"], cmap="Greens"),
        hide_index=True,
    )

    r3, r4 = st.columns(2)
    with r3:
        st.markdown('<div class="section-header">✅ 各部門錄取率</div>', unsafe_allow_html=True)
        fig = px.bar(df_dept_r, x="部門", y="錄取率(%)", color="錄取率(%)",
                     color_continuous_scale="Greens", text="錄取率(%)")
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(styled_fig(fig, 380), key="rec_accept")

    with r4:
        st.markdown('<div class="section-header">⏱ 各部門平均錄取天數</div>', unsafe_allow_html=True)
        vac = get_vacancy_status()
        df_vac = pd.DataFrame(vac)
        fig = px.bar(df_vac, x="department", y="avg_days_to_fill",
                     color="avg_days_to_fill", color_continuous_scale="Oranges",
                     text="avg_days_to_fill", labels={"department": "部門", "avg_days_to_fill": "天數"})
        fig.update_traces(texttemplate="%{text} 天", textposition="outside")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(styled_fig(fig, 380), key="rec_days")

    # 缺編表
    st.markdown('<div class="section-header">⚠️ 缺編情況與錄取時間</div>', unsafe_allow_html=True)
    df_vac_display = df_vac.rename(columns={
        "department": "部門", "budget_headcount": "編制人數", "current_headcount": "現有人數",
        "vacancy": "缺編", "vacancy_rate": "缺編率(%)", "avg_days_to_fill": "平均錄取天數",
    })
    df_vac_display["狀態"] = df_vac_display["缺編"].apply(
        lambda v: "✅ 滿編" if v == 0 else ("🔴 急缺" if v > 8 else "🟡 缺編中")
    )
    st.dataframe(
        df_vac_display.style
        .format({"缺編率(%)": "{:.1f}"})
        .background_gradient(subset=["缺編"], cmap="Reds"),
        hide_index=True,
    )


# ══════════════════════════════════════════════════════════
#  PAGE 3 — 人才結構與異動
# ══════════════════════════════════════════════════════════
elif page == "📊 人才結構與異動":
    st.markdown("# 📊 人才結構與異動報表")

    # ═══ 在職人數總覽 ═══
    st.markdown('<div class="section-header">👥 在職人數總覽</div>', unsafe_allow_html=True)
    hc = get_headcount_overview()

    t1, t2, t3 = st.columns(3)
    with t1:
        df = pd.DataFrame(hc["by_department"])
        fig = px.pie(df, names="label", values="count", title="部門分佈",
                     color_discrete_sequence=COLORS, hole=0.45)
        st.plotly_chart(styled_fig(fig, 320), key="tal_dept")
    with t2:
        df = pd.DataFrame(hc["by_rank"])
        fig = px.bar(df, x="label", y="count", title="職級分佈",
                     color="count", color_continuous_scale="Blues", text="count")
        fig.update_traces(textposition="outside")
        fig.update_layout(coloraxis_showscale=False, xaxis_title="", yaxis_title="人數")
        st.plotly_chart(styled_fig(fig, 320), key="tal_rank")
    with t3:
        df = pd.DataFrame(hc["by_gender"])
        fig = px.pie(df, names="label", values="count", title="性別分佈",
                     color_discrete_sequence=["#3498db", "#e74c3c"], hole=0.45)
        st.plotly_chart(styled_fig(fig, 320), key="tal_gender")

    t4, t5, t6 = st.columns(3)
    with t4:
        df = pd.DataFrame(hc["by_education"])
        fig = px.pie(df, names="label", values="count", title="學歷分佈",
                     color_discrete_sequence=COLORS, hole=0.45)
        st.plotly_chart(styled_fig(fig, 320), key="tal_edu")
    with t5:
        df = pd.DataFrame(hc["by_age_group"])
        fig = px.bar(df, x="label", y="count", title="年齡分佈",
                     color="count", color_continuous_scale="Purples", text="count")
        fig.update_traces(textposition="outside")
        fig.update_layout(coloraxis_showscale=False, xaxis_title="", yaxis_title="人數")
        st.plotly_chart(styled_fig(fig, 320), key="tal_age")
    with t6:
        df = pd.DataFrame(hc["by_tenure_group"])
        fig = px.bar(df, x="label", y="count", title="年資分佈",
                     color="count", color_continuous_scale="Oranges", text="count")
        fig.update_traces(textposition="outside")
        fig.update_layout(coloraxis_showscale=False, xaxis_title="", yaxis_title="人數")
        st.plotly_chart(styled_fig(fig, 320), key="tal_tenure")

    st.divider()

    # ═══ 人力異動紀錄 ═══
    st.markdown('<div class="section-header">🔄 人力異動紀錄</div>', unsafe_allow_html=True)

    m1, m2 = st.columns([1.6, 1])

    with m1:
        mv = get_monthly_movement()
        df_mv = pd.DataFrame(mv)
        fig = go.Figure()
        fig.add_scatter(x=df_mv["month"], y=df_mv["new_hires"], name="新進",
                        mode="lines+markers", line=dict(color="#2ecc71", width=2.5))
        fig.add_scatter(x=df_mv["month"], y=df_mv["resignations"], name="離職",
                        mode="lines+markers", line=dict(color="#e74c3c", width=2.5))
        fig.add_scatter(x=df_mv["month"], y=df_mv["ending_hc"], name="期末人數",
                        mode="lines+markers", line=dict(color="#3498db", width=2.5),
                        yaxis="y2")
        fig.update_layout(
            title="月度人力異動趨勢",
            yaxis=dict(title="人數 (新進/離職)"),
            yaxis2=dict(title="期末人數", overlaying="y", side="right", showgrid=False),
        )
        st.plotly_chart(styled_fig(fig, 370), key="tal_mv_trend")

    with m2:
        yt = get_turnover_trend()
        df_yt = pd.DataFrame(yt)
        fig = go.Figure()
        fig.add_scatter(x=df_yt["year"], y=df_yt["annual_turnover_rate"],
                        name="總離職率", mode="lines+markers",
                        line=dict(color="#e74c3c", width=3))
        fig.add_scatter(x=df_yt["year"], y=df_yt["voluntary_rate"],
                        name="自願離職", mode="lines+markers",
                        line=dict(color="#f39c12", width=2.5))
        fig.add_scatter(x=df_yt["year"], y=df_yt["involuntary_rate"],
                        name="非自願離職", mode="lines+markers",
                        line=dict(color="#95a5a6", width=2))
        fig.update_layout(title="年度離職率趨勢 (近 5 年)", yaxis_title="%")
        st.plotly_chart(styled_fig(fig, 370), key="tal_yr_trend")

    # 月度異動明細表
    st.markdown('<div class="section-header">📋 月度人力異動明細</div>', unsafe_allow_html=True)
    df_mv_display = df_mv.rename(columns={
        "month": "月份", "beginning_hc": "期初人數", "new_hires": "新進",
        "resignations": "離職", "transfers_in": "調入", "transfers_out": "調出",
        "ending_hc": "期末人數", "monthly_turnover_rate": "月離職率(%)",
    })
    st.dataframe(
        df_mv_display.style
        .format({"月離職率(%)": "{:.2f}"})
        .background_gradient(subset=["月離職率(%)"], cmap="Reds"),
        hide_index=True, height=460,
    )

    st.divider()

    # ═══ 流動率/離職率分析 ═══
    st.markdown('<div class="section-header">📉 流動率 / 離職率分析</div>', unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    with a1:
        td = get_turnover_by_department()
        df_td = pd.DataFrame(td)
        fig = px.bar(df_td, x="department", y="turnover_rate", title="各部門離職率",
                     color="turnover_rate", color_continuous_scale="Reds",
                     text="turnover_rate",
                     labels={"department": "部門", "turnover_rate": "離職率(%)"})
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(styled_fig(fig, 380), key="tal_dept_to")

    with a2:
        tr = get_turnover_by_rank()
        df_tr = pd.DataFrame(tr)
        fig = px.bar(df_tr, x="rank", y="turnover_rate", title="各職級離職率",
                     color="turnover_rate", color_continuous_scale="YlOrRd",
                     text="turnover_rate",
                     labels={"rank": "職級", "turnover_rate": "離職率(%)"})
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(styled_fig(fig, 380), key="tal_rank_to")

    a3, a4 = st.columns([1, 1.5])
    with a3:
        lr = get_leave_reason_distribution()
        df_lr = pd.DataFrame(lr)
        fig = px.pie(df_lr, names="reason", values="count", title="離職原因分佈",
                     color_discrete_sequence=COLORS, hole=0.45)
        st.plotly_chart(styled_fig(fig, 400), key="tal_leave_pie")

    with a4:
        st.markdown("##### 🔴 重點流失分析 — 部門 × 職級 (Top 15)")
        detail = get_department_rank_turnover_detail()
        df_detail = pd.DataFrame(detail).rename(columns={
            "department": "部門", "rank": "職級", "headcount": "人數",
            "resignations": "離職數", "turnover_rate": "離職率(%)",
        })
        df_detail["警示"] = df_detail["離職率(%)"].apply(
            lambda r: "🔴 高風險" if r > 40 else ("🟡 注意" if r > 25 else "🟢 正常")
        )
        st.dataframe(
            df_detail.style
            .format({"離職率(%)": "{:.1f}"})
            .background_gradient(subset=["離職率(%)"], cmap="Reds"),
            hide_index=True, height=540,
        )

    # 各部門離職率 & 原因
    st.markdown('<div class="section-header">📑 各部門離職率 & 離職原因</div>', unsafe_allow_html=True)
    rows = []
    for d in td:
        reasons_str = "、".join(f'{k}({v})' for k, v in d["reasons"].items())
        rows.append({
            "部門": d["department"], "人數": d["headcount"],
            "離職數": d["resignations"], "離職率(%)": d["turnover_rate"],
            "主要離職原因": reasons_str,
        })
    df_dept_to = pd.DataFrame(rows)
    st.dataframe(
        df_dept_to.style
        .format({"離職率(%)": "{:.1f}"})
        .background_gradient(subset=["離職率(%)"], cmap="Reds"),
        hide_index=True,
    )
