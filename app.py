import streamlit as st
import re
import string
import random
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Password Strength Meter",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"  # Sidebar is open by default
)

# Initialize session state variables
if 'password_history' not in st.session_state:
    st.session_state.password_history = []
if 'show_password' not in st.session_state:
    st.session_state.show_password = False
if 'generated_password' not in st.session_state:
    st.session_state.generated_password = ""

# Common passwords list
COMMON_PASSWORDS = [
    "password", "123456", "qwerty", "admin", "welcome",
    "123456789", "12345678", "abc123", "password1", "1234567"
]

def is_common_password(password):
    return password.lower() in COMMON_PASSWORDS

def check_password_strength(password):
    if not password:
        return {"score": 0, "strength": "None", "color": "#e0e0e0", "feedback": []}

    score = 0
    feedback = []

    # Criteria checks
    has_length = len(password) >= 8
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    # Check for common password
    if is_common_password(password):
        feedback.append("❌ This is a commonly used password and can be easily guessed")
        score = 1
    else:
        if has_length:
            score += 1
        else:
            feedback.append("❌ Password should be at least 8 characters long")

        if has_upper and has_lower:
            score += 1
        else:
            feedback.append("❌ Password should contain both uppercase and lowercase letters")

        if has_digit:
            score += 1
        else:
            feedback.append("❌ Password should contain at least one digit (0-9)")

        if has_special:
            score += 1
        else:
            feedback.append("❌ Password should contain at least one special character (!@#$%^&*)")

        # Bonus for longer passwords
        if len(password) >= 12:
            score += 0.5

        # Check for sequential patterns
        if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|012|123|234|345|456|567|678|789|890)', password.lower()):
            score -= 0.5
            feedback.append("❌ Password contains sequential patterns")

        # Check for repeated characters
        if re.search(r'(.)\1{2,}', password):
            score -= 0.5
            feedback.append("❌ Password contains repeated characters")

    score = max(0, score)  # prevent negative scores

    # Determine strength category and color
    if score < 2:
        strength = "Very Weak"
        color = "#e74c3c"  # Red
    elif score < 3:
        strength = "Weak"
        color = "#f39c12"  # Orange
    elif score < 4:
        strength = "Moderate"
        color = "#f1c40f"  # Yellow
    elif score < 5:
        strength = "Strong"
        color = "#2ecc71"  # Green
    else:
        strength = "Very Strong"
        color = "#27ae60"  # Dark Green
        if not feedback:
            feedback.append("✅ Your password meets all security criteria!")

    # Positive feedback for criteria met
    positive_feedback = []
    if has_length:
        positive_feedback.append("✅ Good length")
    if has_upper and has_lower:
        positive_feedback.append("✅ Good mix of uppercase and lowercase")
    if has_digit:
        positive_feedback.append("✅ Contains digits")
    if has_special:
        positive_feedback.append("✅ Contains special characters")

    feedback = positive_feedback + feedback

    return {
        "score": min(5, score),
        "strength": strength,
        "color": color,
        "feedback": feedback
    }

def generate_password(length=12):
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    # Ensure at least one character from each category
    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]
    password.extend(random.choice(characters) for _ in range(length - 4))
    random.shuffle(password)
    return ''.join(password)

def toggle_password_visibility():
    st.session_state.show_password = not st.session_state.show_password

def save_to_history(password, strength_info):
    if password:
        st.session_state.password_history.append({
            "password": password,
            "strength": strength_info["strength"],
            "score": strength_info["score"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

def apply_custom_styles():
    """
    Same gradient background, no glass-card containers, no copy button.
    Sidebar styling is also lightly updated to match the rest of the dark theme.
    """
    st.markdown("""
        <style>
        html {
            color-scheme: dark;
        }
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
            overflow-x: hidden;
            font-family: 'Poppins', sans-serif;
        }
        body::before {
            content: "";
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            background: linear-gradient(135deg, #1f1c2c, #928dab);
            z-index: -999;
        }
        .stApp, .block-container {
            background: transparent !important;
        }

        /* Sidebar glass effect */
        [data-testid="stSidebar"] > div:first-child {
            background: rgba(255,255,255,0.1) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            box-shadow: 0 8px 32px rgba(31,38,135,0.37) !important;
        }

        /* Header container */
        .header {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(12px);
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 8px 32px rgba(31,38,135,0.37);
            padding: 3rem 2rem;
            text-align: center;
            margin-bottom: 2rem;
        }
        .header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: #ffffff;
        }
        .header p {
            font-size: 1.2rem;
            color: #e0e0e0;
        }

        /* Section titles */
        .section-title {
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            color: #fff;
        }

        /* Text input fields */
        .stTextInput>div>div>input {
            background: rgba(255,255,255,0.2) !important;
            border: 1px solid rgba(255,255,255,0.3) !important;
            color: #fff !important;
        }

        /* Buttons */
        .stButton button {
            background-color: #007FFF !important;
            color: #fff !important;
            border-radius: 8px !important;
            padding: 0.6rem 1rem !important;
            border: none !important;
            font-weight: 600 !important;
            transition: all 0.2s ease-in-out !important;
        }
        .stButton button:hover {
            background-color: #005FCC !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
        }

        /* Slider styling */
        .stSlider {
            color: #fff !important;
        }
        .stSlider>div>div>div {
            background: linear-gradient(90deg, #00d4ff, #007FFF) !important;
        }

        /* Progress bar styling */
        .stProgress > div > div > div > div {
            background-color: #00d4ff;
            border-radius: 5px;
        }

        /* Password history items */
        .password-history-item {
            margin-bottom: 8px;
            padding: 8px;
            border-left: 4px solid #fff;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
        }

        /* Expander styling (for tips) */
        .st-expander {
            background: rgba(255,255,255,0.1) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            backdrop-filter: blur(12px) !important;
            border-radius: 8px !important;
            margin-bottom: 2rem;
        }
        .st-expander summary {
            color: #fff !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
        }

        /* Hide default Streamlit elements if desired */
        #MainMenu, footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

def add_sidebar():
    """Add a sidebar with info about the app and social links."""
    st.sidebar.title("About This App")
    st.sidebar.write("**Created By :** Talal Shoaib")
    st.sidebar.write("**Made With :** Streamlit")

    st.sidebar.markdown("---")
    st.sidebar.write("**Connect With Me To Make More Inventions:**")
    # Replace these links with your actual URLs
    st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/m-talal-shoaib-8b40322b5/)")
    st.sidebar.markdown("[GitHub](https://github.com/M-TalalSid)")

def main():
    apply_custom_styles()

    # Add sidebar
    add_sidebar()

    # Header Section (we keep this)
    st.markdown("""
        <div class='header'>
            <h1>🔒 Password Strength Meter</h1>
            <p>Evaluate & Generate Secure Passwords For Your Accounts</p>
        </div>
    """, unsafe_allow_html=True)

    # Password Evaluation Section
    st.markdown("<h2 class='section-title'>Password Evaluation</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])
    with col1:
        # Use "default" when visible and "password" when hidden
        password_type = "default" if st.session_state.show_password else "password"
        if st.session_state.generated_password:
            password = st.text_input(
                "Enter Your Password",
                value=st.session_state.generated_password,
                type=password_type,
                key="password_input"
            )
        else:
            password = st.text_input(
                "Enter Your Password",
                type=password_type,
                key="password_input",
                placeholder="Type or generate a password"
            )
    with col2:
        # Toggle visibility button (copy button removed)
        if st.button("👁️" if st.session_state.show_password else "🔒", key="visibility_toggle"):
            toggle_password_visibility()

    if password:
        strength_info = check_password_strength(password)
        score = strength_info["score"]
        strength = strength_info["strength"]
        color = strength_info["color"]
        feedback = strength_info["feedback"]

        st.markdown(f"<b>Password Strength:</b> <span style='color:{color};'>{strength}</span>", unsafe_allow_html=True)
        progress_percent = int((score / 5) * 100)
        st.progress(progress_percent)

        for item in feedback:
            st.write(item)

        if st.button("Save to History", key="save_btn"):
            save_to_history(password, strength_info)
            st.success("Password saved to history!")
    else:
        st.info("Enter a password to see its strength evaluation.")

    # Password Generator Section
    st.markdown("<h2 class='section-title'>Password Generator</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        password_length = st.slider("Password Length", min_value=8, max_value=32, value=16, key="slider_length")
    with col2:
        if st.button("Generate", key="gen_btn"):
            st.session_state.generated_password = generate_password(password_length)

    # Password History Section
    st.markdown("<h2 class='section-title'>Password History</h2>", unsafe_allow_html=True)
    if st.session_state.password_history:
        for i, entry in enumerate(reversed(st.session_state.password_history[-5:])):
            password_display = entry["password"]
            if len(password_display) > 10:
                password_display = (
                    password_display[:3]
                    + "•" * (len(password_display) - 6)
                    + password_display[-3:]
                )

            strength_color = "#e74c3c"  # Default red
            if entry["strength"] == "Moderate":
                strength_color = "#f39c12"
            elif entry["strength"] in ["Strong", "Very Strong"]:
                strength_color = "#27ae60"

            st.markdown(f"""
                <div class="password-history-item" style='border-left-color: {strength_color};'>
                    <strong>{password_display}</strong><br>
                    <small>{entry["timestamp"]}</small>
                    <span style='color:{strength_color}; float:right;'>{entry["strength"]}</span>
                </div>
            """, unsafe_allow_html=True)
        if st.button("Clear History", key="clear_btn"):
            st.session_state.password_history = []
    else:
        st.info("No password history yet. Save passwords to see them here.")

    # Password Security Tips Section
    with st.expander("Password Security Tips"):
        st.markdown("""
            ### Best Practices for Password Security

            **Creating Strong Passwords:**
            - Use passphrases: combine random words with special characters.
            - Aim for at least 12 characters.
            - Include uppercase, lowercase, digits, and symbols.
            - Avoid personal info like birthdays or names.
            - Use unique passwords for every account.

            **Additional Measures:**
            - Enable two-factor authentication.
            - Use a trusted password manager.
            - Change passwords periodically.
            - Monitor for security breaches.
        """)

    # Footer
    st.markdown("---")
    st.write("Password Strength Meter | Professional Edition")
    st.write("Secure Your Digital Life With Strong, Unique Passwords")

if __name__ == "__main__":
    main()