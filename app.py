import streamlit as st
import random
import requests
import pandas as pd
import plotly.express as px
from datetime import date, datetime
from fpdf import FPDF
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit_lottie import st_lottie  # For Lottie animations

# ----------------------------------------------------------------
# 1. SETUP & CONFIGURATION
# ----------------------------------------------------------------
st.set_page_config(page_title="Your Growth Journey", layout="wide")

def fetch_internet_time():
    """
    Fetch current UTC time from worldclockapi.com.
    Fallback to local system time if the API fails.
    """
    try:
        resp = requests.get("http://worldclockapi.com/api/json/utc/now", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        dt_str = data.get("currentDateTime", "")
        if dt_str:
            dt_obj = datetime.strptime(dt_str, "%Y-%m-%dT%H:%MZ")
            return dt_obj.strftime("%Y-%m-%d %H:%M UTC")
        else:
            return datetime.now().strftime("%Y-%m-%d %H:%M (Local)")
    except Exception:
        return datetime.now().strftime("%Y-%m-%d %H:%M (Local)")

def fetch_inspirational_quote():
    """
    Fetch an inspirational quote from quotable.io API.
    """
    try:
        resp = requests.get("https://api.quotable.io/random", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        content = data.get('content', '')
        author = data.get('author', '')
        if content and author:
            return f"\"{content}\" — {author}"
        else:
            return "Quote data unavailable."
    except:
        return "Error fetching quote."

def load_lottieurl(url: str):
    """
    Load a Lottie animation from a URL.
    """
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

# Load Lottie animations for header, challenge, and email reminder
lottie_header = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_u4yrau.json")
lottie_challenge = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
lottie_email = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_i7ixynxd.json")

current_utc_time = fetch_internet_time()

# ----------------------------------------------------------------
# 2. CUSTOM STYLING (RESPONSIVE + ANIMATIONS)
# ----------------------------------------------------------------
st.markdown("""
    <style>
    body {
        background-color: #F0F2F6;
        font-family: 'Segoe UI', sans-serif;
        margin: 0;
        padding: 0;
    }
    .internet-time {
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 14px;
        color: #333;
        background-color: #fff;
        padding: 6px 10px;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(0,0,0,0.2);
        z-index: 9999;
    }
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        padding: 20px;
        margin-top: 40px;
        animation: fadeIn 2s ease-in-out;
    }
    .header {
        color: #2E4053;
        font-size: 32px;
        font-weight: bold;
    }
    .subheader {
        color: #5D6D7E;
        font-size: 20px;
    }
    button[role="tab"] {
        transition: transform 0.3s ease;
    }
    button[role="tab"]:hover {
        transform: scale(1.05);
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @media (max-width: 768px) {
        .header { font-size: 26px; }
        .subheader { font-size: 16px; }
        .internet-time { font-size: 12px; right: 5px; }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(f"<div class='internet-time'>Time: {current_utc_time}</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------
# 3. HEADER SECTION (Humanized with Animation)
# ----------------------------------------------------------------
with st.container():
    cols = st.columns([1, 4])
    with cols[0]:
        if lottie_header:
            st_lottie(lottie_header, height=150, key="header_anim")
    with cols[1]:
        st.markdown('<div class="header-container">', unsafe_allow_html=True)
        st.title("🚀 Welcome to Your Growth Journey!")
        st.markdown("<h4 class='subheader'>Hi there! Let's grow, reflect, and celebrate every step together.</h4>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------
# 4. TABS SETUP (Humanized)
# ----------------------------------------------------------------
tabs = st.tabs([
    "Overview", 
    "Reflection", 
    "Goals", 
    "Inspiration", 
    "Daily Challenge", 
    "Progress Tracker", 
    "Certificate",
    "Email Reminders"
])

# ---------------------------
# Tab 1: Overview
# ---------------------------
with tabs[0]:
    st.header("What's a Growth Mindset?")
    st.write("""
    A growth mindset is about believing in your ability to learn, adapt, and improve. 
    Every challenge is a chance to learn, and every mistake is a stepping stone to success.
    
    Remember: With passion and perseverance, your potential is limitless!
    """)

# ---------------------------
# Tab 2: Reflection
# ---------------------------
with tabs[1]:
    st.header("Share Your Reflections")
    reflection = st.text_area("What's on your mind today?", placeholder="Tell us about your experiences or thoughts...")
    if reflection:
        st.success("Thanks for sharing! Every reflection is a step forward. 😊")

# ---------------------------
# Tab 3: Goals
# ---------------------------
with tabs[2]:
    st.header("Set Your Goals")
    goal = st.text_input("What goal are you setting for today?")
    if goal:
        st.success(f"Great! Your goal '{goal}' is a wonderful step forward. Let's achieve it together!")

# ---------------------------
# Tab 4: Inspiration
# ---------------------------
with tabs[3]:
    st.header("Get Inspired")
    if st.button("Show Me an Inspirational Quote"):
        quote = fetch_inspirational_quote()
        st.info(quote)

# ---------------------------
# Tab 5: Daily Challenge (with Animation)
# ---------------------------
with tabs[4]:
    st.header("Today's Challenge")
    challenges = [
        "Try something new today that you've never done before.",
        "Write down three things you're grateful for.",
        "Reflect on a recent mistake and what you learned from it.",
        "Step out of your comfort zone, even just a bit!",
        "Share a piece of wisdom to help someone grow."
    ]
    if st.button("Get Today's Challenge"):
        chosen_challenge = random.choice(challenges)
        st.success(chosen_challenge)
        if lottie_challenge:
            st_lottie(lottie_challenge, height=150, key="challenge_anim")

# ---------------------------
# Tab 6: Progress Tracker
# ---------------------------
with tabs[5]:
    st.header("Track Your Progress")
    progress = st.slider("On a scale of 0 to 10, how would you rate your progress this week?", 0, 10, 5)
    st.write(f"Your progress rating: {progress}/10. Keep pushing forward!")
    if 'streak' not in st.session_state:
        st.session_state.streak = 0
    if st.button("I Completed Today's Challenge"):
        st.session_state.streak += 1
        st.success(f"Awesome! Your current growth streak is {st.session_state.streak} day(s).")
    st.write("Your current streak:", st.session_state.get('streak', 0), "days")
    days_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    progress_values = [random.randint(0, 10) for _ in range(7)]
    df_progress = pd.DataFrame({'Day': days_list, 'Progress': progress_values})
    fig = px.bar(df_progress, x='Day', y='Progress', title='Weekly Growth Snapshot')
    st.plotly_chart(fig)

# ---------------------------
# Tab 7: Certificate Generator
# ---------------------------
def generate_certificate_condensed(user_name: str):
    """
    Generate an enhanced 'Certificate of Achievement' PDF using DejaVuSansCondensed fonts.
    Features:
      - Outer decorative border.
      - Optional background image.
      - Logo in the upper left corner.
      - Decorative star borders at the top and bottom.
      - A neatly aligned signature area at the bottom-right.
      - Automatic insertion of today's date.
    """
    current_date = date.today().strftime("%B %d, %Y")
    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.set_auto_page_break(False, margin=0)
    
    # Register fonts
    pdf.add_font("DejaVuSansCondensed", "", "assets/DejaVuSansCondensed.ttf", uni=True)
    pdf.add_font("DejaVuSansCondensed", "B", "assets/DejaVuSansCondensed-Bold.ttf", uni=True)
    
    # Optional background image
    bg_path = "assets/certificate_bg.png"
    if os.path.exists(bg_path):
        pdf.image(bg_path, x=5, y=5, w=287, h=200)
    
    # Outer decorative border
    pdf.set_line_width(1.5)
    pdf.rect(5, 5, 287, 200)
    
    # Top star border row
    star_row = "★ " * 40
    pdf.set_font("DejaVuSansCondensed", "", 14)
    pdf.set_y(10)
    pdf.cell(0, 10, star_row, ln=True, align='C')
    
    # Logo in the upper left corner
    pdf.image("assets/logo.png", x=10, y=10, w=30)
    
    # Certificate Title (centered)
    pdf.set_y(35)
    pdf.set_font("DejaVuSansCondensed", "B", 28)
    pdf.cell(0, 12, "Certificate of Achievement", ln=True, align='C')
    pdf.ln(8)
    
    # Awarded-to text
    pdf.set_font("DejaVuSansCondensed", "", 18)
    pdf.cell(0, 10, "This certificate is proudly awarded to", ln=True, align='C')
    pdf.ln(5)
    
    # Recipient Name
    pdf.set_font("DejaVuSansCondensed", "B", 24)
    pdf.cell(0, 12, user_name, ln=True, align='C')
    pdf.ln(8)
    
    # Recognition text (multi-line)
    pdf.set_font("DejaVuSansCondensed", "", 14)
    pdf.multi_cell(0, 8, "In recognition of your unwavering commitment, hard work, and resilience. May you continue to grow and achieve greatness.", align='C')
    pdf.ln(5)
    
    # Date using system date
    pdf.set_font("DejaVuSansCondensed", "", 14)
    pdf.cell(0, 10, f"Date: {current_date}", ln=True, align='C')
    
    # Signature Section at bottom-right
    sig_line_y = 165
    pdf.line(210, sig_line_y, 270, sig_line_y)  # Signature line
    pdf.image("assets/zia_khan_signature.png", x=210, y=sig_line_y - 30, w=40)
    pdf.set_xy(210, sig_line_y + 2)
    pdf.set_font("DejaVuSansCondensed", "", 12)
    pdf.cell(60, 10, "Sir Zia Khan", ln=True, align='C')
    
    # Bottom star border row
    pdf.set_y(-20)
    pdf.set_font("DejaVuSansCondensed", "", 14)
    pdf.cell(0, 10, star_row, ln=True, align='C')
    
    pdf.output("certificate_condensed.pdf")
    return "certificate_condensed.pdf"

with tabs[6]:
    st.header("Certificate Generator")
    st.write("Enter your name below to generate your personalized certificate. Your certificate includes a decorative border, a logo at the top-left, and today's date automatically.")
    
    # Default name changed from "Abdul Wahid" to "User"
    user_name = st.text_input("Your Name:", value="User")
    
    if st.button("Generate My Certificate"):
        cert_file = generate_certificate_condensed(user_name)
        with open(cert_file, "rb") as f:
            st.download_button("Download Your Certificate", data=f, file_name="Certificate.pdf", mime="application/pdf")
        st.success("Congratulations! Your enhanced certificate is ready. Enjoy and keep growing!")

# ---------------------------
# Tab 8: Email Reminders (with Animation)
# ---------------------------
def send_email_reminder(to_email: str):
    """
    Basic function to send a daily reminder email via SMTP.
    Replace the placeholder SMTP credentials with your actual credentials.
    """
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    username = "YOUR_GMAIL_ADDRESS@gmail.com"    # Replace with your email address
    password = "YOUR_APP_PASSWORD"               # Replace with your app password or real password
    
    subject = "Your Daily Growth Mindset Reminder"
    body = """Hello,

This is your daily reminder to reflect, set goals, and challenge yourself.
Keep growing and pushing boundaries every day.

Warm regards,
Your Growth Mindset App (Developed by Abdul Wahid)
"""
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

with tabs[7]:
    st.header("Email Reminders")
    st.write("""
    Enter your email address below to receive a daily reminder about your Growth Mindset journey.
    **Note:** To send daily emails automatically, this script must be scheduled on a server.
    """)
    if lottie_email:
        st_lottie(lottie_email, height=150, key="email_anim")
    
    user_email = st.text_input("Your Email Address:")
    if st.button("Send Test Email"):
        if user_email:
            success = send_email_reminder(user_email)
            if success:
                st.success("Test email sent successfully!")
        else:
            st.error("Please enter a valid email address.")

# ----------------------------------------------------------------
# FOOTER (Include Developer Info)
# ----------------------------------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.write("🚀 Keep growing and remember: your journey is unique, and every step counts! 🌟")
st.write("Developed and owned by **Abdul Wahid**.")
