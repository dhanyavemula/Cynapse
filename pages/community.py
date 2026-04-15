import streamlit as st
import sqlite3
from datetime import datetime

# --- DATABASE SETUP ---
def get_db_connection():
    conn = sqlite3.connect("cyber_reports.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

db = get_db_connection()

# Create table if it doesn't exist to prevent errors
db.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scam_type TEXT,
        platform TEXT,
        money_lost TEXT,
        amount REAL,
        link TEXT,
        description TEXT,
        timestamp TEXT
    )
''')
db.commit()

# --- PAGE CONFIG & STYLING ---
st.set_page_config(page_title="CyberShield Intelligence", layout="wide")

# Formal UI Styling
st.markdown("""
    <style>
    .report-card {
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #2d3139;
        background-color: #1a1c23;
        margin-bottom: 1rem;
    }
    .metadata-text {
        color: #8a8d96;
        font-size: 0.85rem;
        font-family: 'Inter', sans-serif;
    }
    .status-tag {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 4px;
        background: #2d3139;
        color: #4fc3f7;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 Community Intelligence Ledger")
st.caption("Official repository of reported digital threats and scam indicators.")

# Auth Check (Mocking session state for this example)
if 'connected' not in st.session_state:
    st.session_state['connected'] = False
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = None

is_logged_in = st.session_state.get('connected', False)
user_info = st.session_state.get('user_info', None)

tab_view, tab_post = st.tabs(["📋 Recent Alerts", "📝 Report a Threat"])

# --- TAB: VIEW ALERTS ---
with tab_view:
    st.markdown("### Public Awareness Feed")
    st.write("Click on any report below to view full details and technical indicators.")
    
    # Fetch reports from DB
    cursor = db.execute('SELECT * FROM reports ORDER BY timestamp DESC')
    rows = cursor.fetchall()

    if not rows:
        st.info("No reports currently logged in the database.")
    
    for row in rows:
        # We use an expander as the "Button" to see complete details
        with st.expander(f"⚠️ {row['scam_type']} | {row['platform']} | {row['timestamp'][:10]}"):
            # Detailed View
            st.markdown(f"""
                <div class="report-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="status-tag">Verified Community Report</span>
                        <span class="metadata-text">Log ID: #{row['id']}</span>
                    </div>
                    <hr style="margin: 10px 0; border-color: #2d3139;">
                    <p style="font-size: 1.1rem; font-weight: 500;">Incident Description:</p>
                    <p style="color: #d1d5db; line-height: 1.6;">{row['description']}</p>
                    <div style="margin-top: 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div>
                            <p class="metadata-text"><b>Reported Indicators:</b><br>{row['link'] if row['link'] else 'None provided'}</p>
                        </div>
                        <div>
                            <p class="metadata-text"><b>Financial Impact:</b><br>₹{row['amount'] if row['money_lost'] == 'Yes' else '0.00'}</p>
                        </div>
                    </div>
                    <hr style="margin: 15px 0; border-color: #2d3139;">
                    <p class="metadata-text">Reported by Anonymous User at {row['timestamp']}</p>
                </div>
            """, unsafe_allow_html=True)

# --- TAB: SUBMIT REPORT ---
with tab_post:
    if not is_logged_in:
        # For professional look, we use a structured warning
        st.markdown("""
            <div style="padding: 2rem; border: 1px dashed #4fc3f7; border-radius: 10px; text-align: center;">
                <p style="font-size: 1.2rem; color: #4fc3f7;">Authentication Required</p>
                <p style="color: #8a8d96;">Please login via the secure sidebar to contribute to the community ledger.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("### Share Your Experience")
        st.info("By sharing, you help prevent someone else from falling into the same trap. Your data is handled securely.")
        
        with st.form("new_report", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                scam_type = st.selectbox("Type of Threat", 
                    ["Phishing/Fake Link", "UPI/QR Payment Fraud", "Job/Work-from-home Scam", "Identity Theft", "Social Media Hacking"])
                platform = st.selectbox("Platform where it happened", 
                    ["WhatsApp", "Instagram/Facebook", "SMS/Text Message", "Email", "Phone Call", "Other"])
            
            with col2:
                money_lost = st.radio("Did financial loss occur?", ["No", "Yes"])
                amount = st.number_input("Amount (in ₹) if applicable", min_value=0.0)

            link_or_handle = st.text_input("Suspicious Link, Phone Number, or ID involved")
            description = st.text_area("Describe the situation (What happened? What did they say?)")
            
            st.caption("Note: This submission will be audited and shared publicly for communal safety.")
            
            submit = st.form_submit_button("📢 Submit Report for Awareness")
            
            if submit:
                if len(description) < 20:
                    st.error("Formal Requirement: Please provide a bit more detail (min 20 chars) so others can learn from your report.")
                else:
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    db.execute('''
                        INSERT INTO reports (scam_type, platform, money_lost, amount, link, description, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (scam_type, platform, money_lost, amount, link_or_handle, description, now))
                    db.commit()
                    
                    st.success("✅ Transaction Logged. Your contribution to communal safety is appreciated.")
                    st.info("Reference: Review the 'Emergency Contacts' section for immediate mitigation steps.")

# --- FOOTER ---
st.markdown("""
<div style='text-align:center;padding:3rem 0 1rem;color:#4b5563;font-size:0.8rem; border-top: 1px solid #2d3139;'>
    ⚖️ Confidentiality Notice: All reports are submitted voluntarily for public safety purposes.<br>
    CyberShield © 2026. All Rights Reserved.
</div>
""", unsafe_allow_html=True)