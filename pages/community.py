import streamlit as st
import sqlite3
from datetime import datetime

# --- DATABASE SETUP ---
def get_db_connection():
    conn = sqlite3.connect("scams.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

db = get_db_connection()

# Create the table if it's the first time running
db.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT,
        scam_type TEXT,
        money_lost TEXT,
        amount REAL,
        link TEXT,
        description TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
db.commit()

# --- DATABASE HELPER FUNCTIONS ---
def fetch_reports(limit=50):
    cursor = db.execute('SELECT * FROM reports ORDER BY timestamp DESC LIMIT ?', (limit,))
    return [dict(row) for row in cursor.fetchall()]

def get_repeated_links():
    cursor = db.execute('''
        SELECT link, COUNT(link) as count 
        FROM reports 
        WHERE link IS NOT NULL AND link != ""
        GROUP BY link 
        HAVING count > 1
    ''')
    return {row['link']: row['count'] for row in cursor.fetchall()}

def insert_report(author, scam_type, money_lost, amount, link, description):
    db.execute('''
        INSERT INTO reports (author, scam_type, money_lost, amount, link, description)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (author, scam_type, money_lost, amount, link, description))
    db.commit()

# --- PAGE CONTENT ---

st.title("🌐 Community Intelligence")
st.caption("Real scam reports from real people. Together we stay safer.")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

comm_tab_view, comm_tab_report = st.tabs(["📋 View Reports", "📝 Submit Report"])

# ── TAB: VIEW REPORTS ─────────────────────────────────────────────
with comm_tab_view:
    st.markdown("### 📋 Community Scam Reports")
    st.caption("Latest reports submitted by the community. No login required to view.")

    reports = fetch_reports(limit=50)
    repeated = get_repeated_links()

    if not reports:
        st.info("No reports yet. Be the first to submit one!")
    else:
        # Summary metrics
        mc1, mc2, mc3 = st.columns(3)
        with mc1:
            st.metric("Total Reports", len(reports))
        with mc2:
            money_lost_count = sum(1 for r in reports if r["money_lost"] == "Yes")
            st.metric("💸 Money Lost Cases", money_lost_count)
        with mc3:
            flagged_links = len(repeated)
            st.metric("🔴 Repeated Links", flagged_links)

        st.markdown("---")

        # Filter
        all_types = ["All"] + sorted(list({r["scam_type"] for r in reports}))
        filter_type = st.selectbox("Filter by Scam Type", all_types)

        for row in reports:
            if filter_type != "All" and row["scam_type"] != filter_type:
                continue

            link_val = (row["link"] or "").strip()
            is_repeated = link_val and link_val in repeated
            border_color = "#ff1744" if is_repeated else "#1e3a5f"

            # Badges
            badge = (
                f'<span style="background:#ff1744;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.7rem;margin-left:6px;">🔴 FLAGGED ×{repeated[link_val]}</span>'
                if is_repeated else ""
            )

            money_badge = (
                '<span style="background:#ff6b35;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.7rem;margin-left:4px;">💸 Lost Money</span>'
                if row["money_lost"] == "Yes" else ""
            )

            # Safe texts
            amount_text = (
                f"<br>💰 Amount Lost: <b>₹{row['amount']:,.0f}</b>"
                if row["amount"] is not None else ""
            )

            link_text = (
                f"<br>🔗 Link: <code style='font-size:0.78rem;'>{link_val}</code>"
                if link_val else ""
            )

            # DISPLAY CARD (FIXED)
            st.markdown(
                f"""
                <div style="border: 1px solid {border_color}; padding: 15px; border-radius: 10px; margin-bottom: 10px; background-color: rgba(30, 58, 95, 0.05);">
                    
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-weight:700;font-size:1rem;">
                            {row["scam_type"]} Scam {badge} {money_badge}
                        </span>
                        <span style="color: gray; font-size:0.8rem;">{row["timestamp"]}</span>
                    </div>

                    <div style="margin-top: 10px;">
                        {row["description"] or "<i>No description provided.</i>"}
                        {amount_text}
                        {link_text}
                        <br>
                        <span style="color:gray;font-size:0.8rem;font-style:italic;">
                            Reported by: {row["author"]}
                        </span>
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

# ── TAB: SUBMIT REPORT ────────────────────────────────────────────
with comm_tab_report:
    st.markdown("### 📝 Submit a Scam Report")

    if not st.session_state.logged_in:
        st.warning("🔐 **Login required to submit reports.** Please login using the sidebar.")
    else:
        current_user = st.session_state.get("username", "Anonymous User")
        st.success(f"✅ Logged in as **{current_user}**")

        with st.form("report_form", clear_on_submit=True):
            col_f1, col_f2 = st.columns(2)

            with col_f1:
                scam_type = st.selectbox("Type of Scam *", ["Banking", "Job", "OTP", "Delivery", "Investment", "Other"])
                money_lost = st.radio("Did you lose money? *", ["No", "Yes"], horizontal=True)

            with col_f2:
                amount = st.number_input("Approximate amount lost (₹)", min_value=0.0, step=100.0)
                link = st.text_input("Suspicious link (if any)", placeholder="https://...")

            description = st.text_area("Describe the scam *", placeholder="What happened?", height=140)
            submitted = st.form_submit_button("🚀 Submit Report", type="primary", use_container_width=True)

        if submitted:
            if not description.strip():
                st.error("Please provide a description.")
            else:
                final_amount = float(amount) if money_lost == "Yes" and amount > 0 else None

                insert_report(
                    author=current_user,
                    scam_type=scam_type,
                    money_lost=money_lost,
                    amount=final_amount,
                    link=link.strip(),
                    description=description.strip()
                )

                st.success("✅ Report submitted! Refresh the 'View Reports' tab to see it.")
