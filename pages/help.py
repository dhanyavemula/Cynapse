import streamlit as st

# --- START OF PAGE CONTENT ---

# 1. Page Headers (Removed 'Elif' and un-indented)
st.title("🆘 Emergency Cyber Help")
st.caption("If you've been scammed — act fast. Every minute counts.")

# ── Emergency contacts ─────────────────────────────────────────────
st.markdown("### 📞 Emergency Contacts")
e1, e2, e3 = st.columns(3)

# Note: Added inline styles for the cards to ensure they look good 
# in the multi-page layout without needing external CSS.

with e1:
    st.markdown("""
    <div style='border: 2px solid #00e676; padding: 20px; border-radius: 12px; text-align:center; background-color: rgba(0, 230, 118, 0.05);'>
        <div style='font-size:2rem;'>🚨</div>
        <div style='font-size:0.8rem;color:#4a9a7a;letter-spacing:0.1em;margin:4px 0;font-weight:bold;'>
            CYBER CRIME HELPLINE
        </div>
        <div style='font-size:2.5rem; font-weight:bold; color:#00e676;'>1930</div>
        <div style='font-size:0.75rem;color:#4a9a7a;margin-top:6px;'>
            Available 24×7 · Free call
        </div>
    </div>
    """, unsafe_allow_html=True)

# with e2:
#     st.markdown("""
#     <div style='border: 2px solid #4fc3f7; padding: 20px; border-radius: 12px; text-align:center; background-color: rgba(79, 195, 247, 0.05);'>
#         <div style='font-size:2rem;'>👮</div>
#         <div style='font-size:0.8rem;color:#2a6a9a;letter-spacing:0.1em;margin:4px 0;font-weight:bold;'>
#             POLICE
#         </div>
#         <div style='font-size:2.5rem; font-weight:bold; color:#4fc3f7;'>100</div>
#         <div style='font-size:0.75rem;color:#2a6a9a;margin-top:6px;'>
#             Emergency police line
#         </div>
#     </div>
#     """, unsafe_allow_html=True)


with e2:
    st.markdown("""
    <div style='border: 2px solid #4fc3f7; padding: 20px; border-radius: 12px; text-align:center; background-color: rgba(79, 195, 247, 0.05); height: 220px;'>
        <div style='font-size:2rem;'>🛡️</div>
        <div style='font-size:0.8rem;color:#2a6a9a;letter-spacing:0.1em;margin:4px 0;font-weight:bold;'>
            CERT-In INCIDENT DESK
        </div>
        <div style='font-size:1.5rem; font-weight:bold; color:#4fc3f7; margin: 10px 0;'>1800-11-4432</div>
        <div style='font-size:0.75rem;color:#2a6a9a;margin-top:6px;'>
            Report hacking, malware, or data breaches to the National Response Team
        </div>
    </div>
    """, unsafe_allow_html=True)

with e3:
    st.markdown("""
    <div style='border: 2px solid #ff6b35; padding: 20px; border-radius: 12px; text-align:center; background-color: rgba(255, 107, 53, 0.05);'>
        <div style='font-size:2rem;'>🌐</div>
        <div style='font-size:0.8rem;color:#9a4a2a;letter-spacing:0.1em;margin:4px 0;font-weight:bold;'>
            REPORT ONLINE
        </div>
        <div style='font-size:1.2rem; font-weight:700; color:#ff8c60; font-family:monospace; margin:8px 0;'>
            cybercrime.gov.in
        </div>
        <a href='https://cybercrime.gov.in' target='_blank'
           style='background:#ff6b35;color:#fff;padding:8px 14px;
                  border-radius:6px;text-decoration:none;font-size:0.8rem;display:inline-block;margin-top:5px;'>
            Open Portal →
        </a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Immediate action steps ─────────────────────────────────────────
st.markdown("### 🧭 Immediate Action Steps")
st.caption("If you suspect a scam or have been defrauded — follow these steps **right now**:")

steps = [
    ("🚫", "Do NOT share OTP",
     "Never share your OTP, PIN, CVV, or password — not even with "
     "someone claiming to be from your bank or government."),
    ("🏦", "Block your bank account",
     "Call your bank immediately (or use the app) to block your card/account "
     "and freeze any suspicious transactions."),
    ("🔑", "Change all passwords",
     "Change passwords for your banking app, email, and social media right away. "
     "Enable 2FA where possible."),
    ("📱", "Block the scammer",
     "Block the phone number, WhatsApp, or email used by the scammer. "
     "Take screenshots before blocking for evidence."),
    ("🚔", "File a complaint immediately",
     "Call 1930 or visit cybercrime.gov.in. Report within 24 hours for "
     "the best chance of fund recovery."),
    ("🗣️", "Warn your contacts",
     "Alert family and friends. Scammers often re-use the same link/number "
     "on multiple victims from the same network."),
]

for icon, title, desc in steps:
    st.markdown(f"""
    <div style='border: 1px solid #1e3a5f; padding: 15px; border-radius: 10px; margin-bottom: 10px; background-color: rgba(30, 58, 95, 0.1);'>
        <div style='display:flex;align-items:flex-start;gap:1rem;'>
            <div style='font-size:2rem;'>{icon}</div>
            <div>
                <div style='font-weight:700;font-size:1.1rem;'>{title}</div>
                <div style='color:#7a9ab8;font-size:0.9rem;margin-top:4px;'>{desc}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Common scam types ──────────────────────────────────────────────
st.markdown("### 🧠 Recognize Common Scam Types")
scam_types = {
    "💳 Banking / KYC Scam": "Fake calls/SMS claiming your account will be blocked. Never share OTP.",
    "💼 Job Offer Scam":     "Fake HR offering dream jobs. Asks for 'registration fee' upfront.",
    "📦 Delivery Scam":      "Fake courier SMS with 'pay customs fee' link — always check the official app.",
    "📈 Investment Scam":    "'Double your money' Telegram groups with fake screenshots.",
    "🎁 Prize / Lottery Scam": "Congratulations! You won! Pay processing fee to claim…",
    "💞 Romance Scam":       "Online relationship that eventually asks for money transfers.",
}

cols = st.columns(2)
for i, (name, desc) in enumerate(scam_types.items()):
    with cols[i % 2]:
        st.markdown(f"""
        <div style='border: 1px solid #1e3a5f; padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
            <div style='font-weight:700;color:#4fc3f7;'>{name}</div>
            <div style='margin-top:6px;font-size:0.86rem;color:#7a9ab8;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer note ────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;padding:2rem 0 1rem;color:gray;font-size:0.8rem;'>
    🛡️ CyberShield · Smart Cyber Risk Analyzer · Always stay alert online.<br>
    This tool provides risk indicators only and is not a substitute for professional cyber-legal advice.
</div>
""", unsafe_allow_html=True)