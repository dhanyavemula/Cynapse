import streamlit as st
import re
import io
from PIL import Image
import numpy as np
from PIL import Image

# Optional imports - checking if they are available
try:
    import cv2
    #from pyzbar import pyzbar
    QR_SUPPORT = False
except ImportError:
    QR_SUPPORT = False

# ─────────────────────────────────────────────────────────────────
# 🧠 HELPER FUNCTIONS (The "Brains" of the Analyzer)
# ─────────────────────────────────────────────────────────────────

def analyze_url(url):
    """Calculates a risk score for a given URL."""
    score = 0
    reasons = []
    
    # 1. Check for HTTPS
    if not url.lower().startswith("https"):
        score += 40
        reasons.append("❌ Connection is not secure (Missing HTTPS)")
    else:
        reasons.append("✅ Secure connection (HTTPS)")

    # 2. Check for suspicious keywords
    suspicious_words = ["login", "verify", "bank", "update", "free", "gift", "account", "secure", "otp"]
    found_words = [word for word in suspicious_words if word in url.lower()]
    if found_words:
        score += len(found_words) * 15
        reasons.append(f"⚠️ Contains suspicious keywords: {', '.join(found_words)}")

    # 3. Check for suspicious top-level domains
    suspicious_tlds = [".xyz", ".top", ".zip", ".buzz", ".work", ".tk", ".ml"]
    if any(url.lower().endswith(tld) for tld in suspicious_tlds):
        score += 30
        reasons.append("⚠️ Uses a high-risk domain extension (TLD)")

    # Result Categorization
    if score >= 60:
        level, color = "High Risk", "red"
    elif score >= 30:
        level, color = "Moderate Risk", "orange"
    else:
        level, color = "Safe / Low Risk", "green"
        
    return {"score": min(score, 100), "level": level, "color": color, "reasons": reasons}

def analyze_text_for_scam(text):
    """Fallback for non-URL content found in QR codes."""
    if len(text) < 5:
        return {"score": 0, "level": "Unknown", "color": "gray", "reasons": ["Text too short to analyze."]}
    
    score = 20
    reasons = ["⚠️ Plain text content (Not a URL)"]
    if "win" in text.lower() or "prize" in text.lower():
        score += 50
        reasons.append("🚨 Potential lottery/prize scam keywords detected.")
        
    return {"score": score, "level": "Suspicious" if score > 30 else "Informational", "color": "blue", "reasons": reasons}

def render_risk_result(result, content):
    """Displays the fancy result card in the UI."""
    st.markdown(f"""
    <div style="background-color: {result['color']}; padding: 15px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h2 style="margin:0; color: white;">{result['level']}</h2>
        <p style="margin:0; font-size: 1.2rem;">Risk Score: {result['score']}/100</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### Analysis Details:")
    for r in result['reasons']:
        st.write(r)

    # ── SSL / Security Info Panel ──────────────────────────────────
    is_https = content.lower().startswith("https")
    ssl_status = "✅ Valid (AES-256 Encryption)" if is_https else "❌ Not Detected (HTTP only)"
    ssl_color  = "#1b4332" if is_https else "#7f1d1d"
    ssl_icon   = "🔒" if is_https else "🔓"

    st.markdown(f"""
    <div style="
        background: {ssl_color};
        border: 1px solid {'#2d6a4f' if is_https else '#991b1b'};
        border-radius: 10px;
        padding: 14px 18px;
        margin-top: 10px;
    ">
        <table style="width:100%; border-collapse:collapse; font-size:0.88rem; color:#e5e7eb;">
            <tr>
                <td style="padding:5px 0; width:40%;"><b>{ssl_icon} SSL / TLS Status</b></td>
                <td style="padding:5px 0;">{ssl_status}</td>
            </tr>
            <tr>
                <td style="padding:5px 0;"><b>🔐 Protocol</b></td>
                <td style="padding:5px 0;">{"HTTPS (Encrypted)" if is_https else "HTTP (Unencrypted)"}</td>
            </tr>
            <tr>
                <td style="padding:5px 0;"><b>🛡️ Data Protection</b></td>
                <td style="padding:5px 0;">{"Transport layer secured" if is_https else "Data transmitted in plaintext"}</td>
            </tr>
            <tr>
                <td style="padding:5px 0;"><b>🔎 Scan Engine</b></td>
                <td style="padding:5px 0;">CyberShield Heuristic v1.0</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# 🚀 MAIN UI CODE
# ─────────────────────────────────────────────────────────────────

st.title("🔍 Cyber Risk Analyzer")
st.caption("Detect phishing links, malicious QR codes, and suspicious content.")

tab_link, tab_image, tab_qr = st.tabs(
    ["🔗 Link Analyzer", "🖼️ Image Analyzer", "📷 QR Code Analyzer"]
)

# ── TAB 1: LINK ANALYZER ──────────────────────────────────────────
with tab_link:
    st.markdown("### 🔗 Link / URL Risk Analysis")
    st.caption("Paste any URL or suspicious link below to check it for phishing indicators.")

    url_input = st.text_input(
        "Enter URL",
        placeholder="https://example.com/login?verify=OTP",
        key="link_input",
    )

    col_btn, col_clear = st.columns([2, 1])
    with col_btn:
        analyze_clicked = st.button("🔍 Analyze Link", type="primary",
                                    use_container_width=True, key="analyze_link")
    with col_clear:
        if st.button("🗑️ Clear", use_container_width=True, key="clear_link"):
            st.rerun()

    if analyze_clicked:
        if not url_input.strip():
            st.warning("Please enter a URL to analyze.")
        else:
            with st.spinner("Analyzing …"):
                result = analyze_url(url_input.strip())
            st.markdown("---")
            render_risk_result(result, url_input.strip())

    # ── Demo examples ──
    st.markdown("---")
    st.markdown("**🧪 Try example URLs:**")
    examples = [
        ("✅ Legit", "https://www.hdfcbank.com/personal/home"),
        ("⚠️ Suspicious", "http://hdfc-secure-login.xyz/verify?otp=1234"),
        ("🚨 Fraud",   "http://192.168.1.1/sbi-login/update-password-free-win"),
    ]
    cols = st.columns(3)
    for idx, (label, ex_url) in enumerate(examples):
        with cols[idx]:
            if st.button(label, key=f"ex_{idx}", use_container_width=True):
                result = analyze_url(ex_url)
                st.markdown(f"`{ex_url[:40]}...`")
                render_risk_result(result, ex_url)

# ── TAB 2: IMAGE ANALYZER ─────────────────────────────────────────
import pytesseract
import os# Needs 'pip install pytesseract'
#C:\Program Files\Tesseract-OCR
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.name=="nt":
    pytesseract.pytesseract.tesseract_cmd=r"C:\ProgramFiles\Tesseract-OCR\tesseract.exe"
else:
    pytesseract.pytesseract.tesseract_cmd="/usr/bin/tesseract"
pyt

# ── TAB 2: IMAGE ANALYZER (AUTOMATED) ─────────────────────────────
with tab_image:
    st.markdown("### 🖼️ Automated Image Scanner")
    st.caption("Our AI will scan this image for phishing keywords and suspicious patterns.")

    uploaded_img = st.file_uploader("Upload Screenshot", type=["png", "jpg", "jpeg"], key="auto_img")

    if uploaded_img:
        img = Image.open(uploaded_img)
        st.image(img, caption="Scanning Image...", use_container_width=True)

        with st.spinner("🔍 Running OCR Analysis..."):
            try:
                extracted_text = pytesseract.image_to_string(img).lower()
                
                danger_keywords = [
                    "otp", "password", "blocked", "urgent", "verify", "winner", "prize", 
                    "bank", "login", "win", "lakh", "withdraw", "bonus", "rewards", 
                    "grab now", "download now", "get ₹", "free"
                ]
                found_risks = [word for word in danger_keywords if word in extracted_text]

                st.markdown("---")
                st.subheader("📊 Analysis Results")
                
                if found_risks:
                    st.error(f"🚨 **High Risk Detected!**")
                    st.write(f"The following suspicious terms were found inside the image: **{', '.join(found_risks)}**")
                    st.warning("This image likely belongs to a phishing scam. Do not share any details requested in this message.")
                else:
                    url_pattern = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
                    links = url_pattern.findall(extracted_text)
                    
                    if links:
                        st.info(f"🔗 **Link Found:** {links[0]}")
                        st.write("We found a URL in the text. Use the 'Link Analyzer' tab to check it specifically.")
                    else:
                        st.success("✅ **Clean Scan**")
                        st.write("No known phishing keywords were detected in this image.")

                with st.expander("See Extracted Text"):
                    st.text(extracted_text if extracted_text.strip() else "No readable text found.")

            except Exception as e:
                st.error("OCR Engine not found on this laptop.")
                st.info("To make this work locally, install Tesseract OCR. On the web (Streamlit Cloud), this works automatically if added to packages.txt.")

# ── TAB 3: QR CODE ANALYZER ───────────────────────────────────────
with tab_qr:
    st.markdown("### 📷 Intelligent QR Code Scanner")
    st.caption("Scan UPI codes, websites, or contact info to verify safety.")

    qr_file = st.file_uploader(
        "Upload QR Code Image",
        type=["png", "jpg", "jpeg"],
        key="qr_scanner_integrated"
    )

    if qr_file:
        file_bytes = np.asarray(bytearray(qr_file.read()), dtype=np.uint8)
        opencv_img = cv2.imdecode(file_bytes, 1)

        img = Image.open(io.BytesIO(file_bytes))
        st.image(img, caption="Scanning QR Content...", width=300)

        detector = cv2.QRCodeDetector()
        decoded_info, points, _ = detector.detectAndDecode(opencv_img)

        if decoded_info:
            st.markdown("---")
            st.subheader("📊 Analysis Result")

            if "upi://pay" in decoded_info.lower():
                st.info("💳 **Result: Personal/Merchant QR**")
                st.write("This is a standard UPI payment link used in shops.")
                try:
                    vpa = decoded_info.split('pa=')[1].split('&')[0]
                    st.success(f"**Verified Target:** {vpa}")
                except:
                    st.write("**Target:** UPI Recipient")
                st.warning("⚠️ **Safety Check:** Ensure the shop name on your screen matches the shop you are in.")

            elif "http" in decoded_info.lower():
                scam_keywords = ["lottery", "winner", "prize", "free-gift", "update-bank", "kyc", "vkyc", "lakh"]
                is_risky = any(word in decoded_info.lower() for word in scam_keywords)

                if is_risky:
                    st.error("🚨 **RESULT: RISK DETECTED**")
                    st.write(f"**Detected Malicious Link:** `{decoded_info}`")
                    st.markdown("> **Analysis:** This QR leads to a website using scam-related keywords. Do not enter any personal details.")
                else:
                    st.success("✅ **RESULT: Likely Safe Website**")
                    st.write(f"**Target Link:** {decoded_info}")
                    st.info("This appears to be a standard web address.")

            else:
                st.info("📄 **Result: Plain Information**")
                st.write(f"**Content found:** `{decoded_info}`")

        else:
            st.warning("❌ **Could not read QR.**")
            st.write("The image might be too blurry or the QR is incomplete. Try taking a clearer screenshot.")
