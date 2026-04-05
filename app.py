import streamlit as st

# ======================
# 🔥 頁面設定
# ======================
st.set_page_config(
    page_title="槓桿+倉位計算器",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ======================
# 🔥 強制隱藏 UI
# ======================
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ======================
# 🔥 強制全域暗黑（關鍵修正）
# ======================
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0d1117 !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ======================
# 顏色系統
# ======================
section = "#111827"
card = "#1f2933"
text_main = "#ffffff"
text_sub = "#9ca3af"

# ======================
# CSS
# ======================
st.markdown(f"""
<style>
.block-container {{
    max-width: 900px;
    padding-top: 2rem;
}}

/* 區塊 */
.section {{
    background: {section};
    padding: 28px;
    border-radius: 20px;
    margin-bottom: 30px;
}}

/* 卡片 */
.card {{
    background: {card};
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0,0,0,0.35);
}}

/* 🔥 標題（改成高對比色） */
.main-title {{
    font-size: 22px;
    font-weight: 700;
    text-align: center;
    color: #facc15;
}}

/* 副標 */
.sub-title {{
    text-align: center;
    color: {text_sub};
    font-size: 13px;
    margin-bottom: 25px;
}}

/* 區塊標題 */
.title {{
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 20px;
}}

/* 卡片標題 */
.card-title {{
    font-size: 13px;
    color: {text_sub};
    margin-bottom: 8px;
}}

/* 數值 */
.card-value {{
    font-size: 34px;
    font-weight: 700;
}}

/* 小數 */
.decimal {{
    font-size: 16px;
    color: {text_sub};
}}
</style>
""", unsafe_allow_html=True)

# ======================
# 標題
# ======================
st.markdown("""
<div class="main-title">💰 槓桿+倉位計算器</div>
<div class="sub-title">倉位 × 槓桿 × 風險，一眼掌握</div>
""", unsafe_allow_html=True)

# ======================
# 輸入區
# ======================
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="title">⚙️ 條件設定</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    balance = st.number_input("合約帳戶本金 (USDT)", value=1000.00, format="%.2f")
    risk_amount = st.number_input("單筆最大可虧損 (USDT)", value=50.00, format="%.2f")

with col2:
    margin_pct = st.number_input("投入保證金佔本金 (%)", value=10.00, format="%.2f")
    sl_pct = st.number_input("止損距離 (%)", value=5.00, format="%.2f")

st.markdown('</div>', unsafe_allow_html=True)

# ======================
# 🔥 防呆邏輯（禁止開單）
# ======================
error_msg = None

if balance <= 0:
    error_msg = "本金不可為 0"
elif risk_amount <= 0:
    error_msg = "虧損金額需大於 0"
elif margin_pct <= 0 or margin_pct > 100:
    error_msg = "保證金比例需在 0~100%"
elif sl_pct <= 0:
    error_msg = "止損需大於 0"

# ======================
# 如果有錯 → 顯示錯誤 + 不計算
# ======================
if error_msg:
    st.markdown(f"""
    <div style="
        background:#2b0000;
        padding:14px;
        border-radius:12px;
        color:#ff4d4f;
        margin-top:10px;
    ">
    ❌ {error_msg}
    </div>
    """, unsafe_allow_html=True)

# ======================
# 正常才顯示結果
# ======================
else:

    position_size = risk_amount / (sl_pct / 100)
    actual_margin = balance * (margin_pct / 100)
    leverage = position_size / actual_margin

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">📊 計算結果</div>', unsafe_allow_html=True)

    colA, colB, colC = st.columns(3)

    def format_num(x):
        main = int(x)
        dec = abs(x - main)
        return f"{main:,}", f"{dec:.2f}"[1:]

    def card_ui(title, val, color):
        main, dec = format_num(val)
        st.markdown(f"""
        <div class="card">
            <div class="card-title" style="color:{color};">{title}</div>
            <div class="card-value" style="color:{color};">
                {main}<span class="decimal">{dec}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with colA:
        card_ui("開倉價值", position_size, "#22d3ee")

    with colB:
        card_ui("槓桿倍數", leverage, "#facc15")

    with colC:
        card_ui("保證金", actual_margin, "#4ade80")

    st.markdown(f"""
    <div style="
        margin-top:15px;
        background:#2b0000;
        padding:14px;
        border-radius:12px;
        color:#ff4d4f;
    ">
    若價格反向 <b>{sl_pct:.2f}%</b>，預計虧損 <b>{risk_amount:.2f} USDT</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
