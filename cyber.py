import streamlit as st
import sqlite3
import re
import os
import urllib.parse
from datetime import datetime

# Optional heavy imports with graceful fallback
try:
    import cv2
    import numpy as np
    #from pyzbar import pyzbar
    from PIL import Image
    QR_SUPPORT = False
except ImportError:
    QR_SUPPORT = False

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Cyber Risk Analyzer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# GLOBAL STYLES
# ──────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ── */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}
code, pre, .mono { font-family: 'JetBrains Mono', monospace; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d1a 0%, #0a1628 100%);
    border-right: 1px solid #1e3a5f;
}
[data-testid="stSidebar"] * { color: #c9d8f0 !important; }

/* ── Main ── */
.main .block-container { padding-top: 2rem; max-width: 1100px; }

/* ── Cards ── */
.report-card {
    background: #0d1626;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    margin: 0.6rem 0;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# DATABASE LAYER
# ══════════════════════════════════════════════

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cyber_reports.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            scam_type   TEXT    NOT NULL,
            money_lost  TEXT    NOT NULL,
            amount      REAL,
            link        TEXT,
            description TEXT,
            timestamp   TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Initialize DB on load
init_db()

# ══════════════════════════════════════════════
# SESSION STATE INIT
# ══════════════════════════════════════════════

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

USERS = {
    "admin": "admin123",
    "demo":  "demo123",
    "sriyaparijatha103@gmail.com": "sriya2",
    "vaishnavicherkuri@gmail.com":"chvaishu94",
    "arjunvallabh@yahoo.com":"arjun23"
}

# ══════════════════════════════════════════════
# SIDEBAR (Branding & Auth Only)
# ══════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1.2rem 0 0.5rem 0;">
        <div style="font-size:2.5rem;">🛡️</div>
        <div style="font-size:1.1rem;font-weight:800;letter-spacing:0.05em;
                    color:#4fc3f7;margin-top:4px;">CyberShield</div>
        <div style="font-size:0.72rem;color:#4a7aa0;letter-spacing:0.08em;">
            SMART RISK ANALYZER
        </div>
    </div>
    <hr style="border-color:#1e3a5f;margin:0.8rem 0;">
    """, unsafe_allow_html=True)

    # Note: Navigation is now handled AUTOMATICALLY by the 'pages' folder.
    # No st.radio needed here.

    if st.session_state.logged_in:
        st.success(f"👤 {st.session_state.username}")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
    else:
        with st.expander("🔐 Login", expanded=False):
            u = st.text_input("Username", key="sb_user")
            p = st.text_input("Password", type="password", key="sb_pass")
            if st.button("Login", use_container_width=True, key="sb_login_btn"):
                if u in USERS and USERS[u] == p:
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.success("Logged in!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    st.markdown("""
    <hr style="border-color:#1e3a5f;margin:0.8rem 0;">
    <div style="font-size:0.7rem;color:#2e4a6a;text-align:center;">
        v1.0 · Built with Streamlit<br>
        🚨 Helpline: <b style="color:#ff6b6b;">1930</b>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# MAIN PAGE CONTENT (Right Side)
# ══════════════════════════════════════════════

# The requested Title and Welcome screen
st.title("🛡️ Smart Cyber Risk Analyzer")
st.markdown("### Your Digital Shield Against Scams")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    Welcome to **CyberShield**. This platform is designed to help you identify 
    and report cyber threats before they cause harm. 
    
    **How to use this tool:**
    Select a module from the sidebar on the left to get started:
    
    * **🔍 Analyzer**: Upload images, QR codes, or paste links to check for fraud indicators.
    * **🌐 Community**: Browse real-time reports from other users or contribute your own.
    * **🆘 Help**: Find immediate action steps and emergency contact numbers if you've been targeted.
    """)
    
    st.info("💡 **Stay Alert:** Scammers often use urgency and fear. Always verify before you click.")

with col2:
    st.markdown("""
    <div style="background:#0d1626; border:1px solid #1e3a5f; padding:20px; border-radius:12px;">
        <h4 style="margin-top:0; color:#4fc3f7;">Quick Stats</h4>
        <p style="font-size:0.9rem;">🛡️ Engine: Active</p>
        <p style="font-size:0.9rem;">📡 Database: Connected</p>
        <p style="font-size:0.9rem;">🔐 Security: Encrypted</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Footer note
st.caption("© 2026 CyberShield Project. Protecting users from digital fraud.")