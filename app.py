import streamlit as st

# ======================
# 固定暗黑模式（無切換）
# ======================
bg = "#0d1117"
section = "#111827"
card = "#1f2933"
text_main = "#ffffff"
text_sub = "#9ca3af"

# ======================
# CSS
# ======================
st.markdown(f"""
<style>
body {{
    background-color: {bg};
}}

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

/* 標題 */
.title {{
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 20px;
    color: {text_main};
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
    font-size: 18px;
    color: {text_sub};
    margin-left: 2px;
}}
</style>
""", unsafe_allow_html=True)

# ======================
# 標題（改成錢符號）
# ======================
st.markdown(f"""
<h1 style="text-align:center;color:{text_main};">
💰 槓桿+倉位計算器
</h1>
<p style="text-align:center;color:{text_sub};">
倉位 × 槓桿 × 風險，一眼掌握
</p>
""", unsafe_allow_html=True)

# ======================
# 上半部：輸入區
# ======================
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="title">⚙️ 條件設定</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    balance = st.number_input("合約帳戶本金 (USDT)", value=1000.0)
    risk_amount = st.number_input("單筆最大可虧損 (USDT)", value=50.0)

with col2:
    margin_pct = st.number_input("投入保證金佔本金 (%)", value=10.0)
    sl_pct = st.number_input("止損距離 (%)", value=5.0)

st.markdown('</div>', unsafe_allow_html=True)

# ======================
# 計算
# ======================
if sl_pct > 0 and margin_pct > 0:

    position_size = risk_amount / (sl_pct / 100)
    actual_margin = balance * (margin_pct / 100)
    leverage = position_size / actual_margin

    # ======================
    # 下半部：結果區
    # ======================
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
        card_ui("開倉價值 (USDT)", position_size, "#22d3ee")   # 藍

    with colB:
        card_ui("槓桿倍數 (x)", leverage, "#facc15")          # 黃

    with colC:
        card_ui("保證金 (USDT)", actual_margin, "#4ade80")    # 綠

    # ======================
    # 補充說明
    # ======================
    st.markdown(f"""
    <div style="
        margin-top:15px;
        background:{card};
        padding:14px;
        border-radius:12px;
        color:{text_sub};
    ">
    若價格反向 <b>{sl_pct}%</b>，預計虧損 <b>{risk_amount} USDT</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
