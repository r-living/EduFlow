import streamlit as st
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
import pickle
import base64
from streamlit_lottie import st_lottie
import json
from streamlit_extras.stylable_container import stylable_container

# ===== YOUR BACKEND CODE (UNCHANGED) =====
CLIENT_SECRETS_FILE = "credentials.json"
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
          'https://www.googleapis.com/auth/userinfo.email', 'openid']
TOKEN_FILE = "token.pickle"

def is_authenticated():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)
            return creds and creds.valid
    return False

def authenticate():
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri="urn:ietf:wg:oauth:2.0:oob")
    auth_url, _ = flow.authorization_url(prompt="consent")
    return auth_url

def fetch_token(auth_code):
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri="urn:ietf:wg:oauth:2.0:oob")
    flow.fetch_token(code=auth_code)
    return flow.credentials

def detect_user_role(creds):
    try:
        classroom = build("classroom", "v1", credentials=creds)
        results = classroom.courses().list(teacherId="me").execute()
        return "teacher" if results.get('courses') else "student"
    except:
        return "student"

# ===== MAGICAL UI ENHANCEMENTS =====
def load_lottie(url):
    """Load Lottie animation from URL"""
    if url.startswith('http'):
        import requests
        return requests.get(url).json()
    return json.loads(url)

# Embedded Lottie animation (fallback if no internet)
ANIMATION = {
    "v": "5.9.0",
    "fr": 60,
    "ip": 0,
    "op": 60,
    "w": 400,
    "h": 400,
    "nm": "Education",
    "assets": [],
    "layers": [{
        "ddd": 0,
        "ind": 1,
        "ty": 4,
        "nm": "Layer 1",
        "sr": 1,
        "ks": {"o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0}, "p": {"a": 0, "k": [200,200,0]}, "a": {"a": 0, "k": [0,0,0]}, "s": {"a": 0, "k": [100,100,100]}},
        "shapes": [{
            "ty": "gr",
            "it": [{
                "ty": "rc",
                "d": 1,
                "s": {"a": 0, "k": [300,300]},
                "p": {"a": 0, "k": [0,0]},
                "r": {"a": 0, "k": 0},
                "nm": "Rectangle",
                "mn": "ADBE Vector Shape - Rect",
                "hd": False
            }, {
                "ty": "fl",
                "c": {"a": 0, "k": [0.482,0.843,0.929,1]},
                "o": {"a": 0, "k": 100},
                "r": 1,
                "nm": "Fill 1",
                "mn": "ADBE Vector Graphic - Fill",
                "hd": False
            }],
            "nm": "Background",
            "np": 2,
            "mn": "ADBE Vector Group",
            "hd": False
        }]
    }]
}

# Base64 encoded logo (your provided image)
LOGO = "data:image/png;base64,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"
# ===== STREAMLIT UI =====
def main():
    # Page config
    st.set_page_config(
        page_title="EduFlow Login",
        layout="centered"
    )

    # Custom CSS
    st.markdown(f"""
    <style>
        .stApp {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }}
        .login-card {{
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }}
        .google-btn {{
            background: white !important;
            color: #5f6368 !important;
            border: 1px solid #dadce0 !important;
            border-radius: 8px !important;
            padding: 10px 24px !important;
            font-weight: 500 !important;
            transition: all 0.3s !important;
        }}
        .google-btn:hover {{
            box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
        }}
    </style>
    """, unsafe_allow_html=True)

    # Animation at top (try online URL first, fallback to embedded)
    try:
        st_lottie(load_lottie("https://assets1.lottiefiles.com/packages/lf20_ktwnwv5m.json"), 
                 height=200, key="login-anim")
    except:
        st_lottie(ANIMATION, height=200, key="login-fallback")

    # Login card
    with stylable_container(
        key="login_container",
        css_styles="""
        {
            padding: 2rem;
        }
        """
    ):
        # Header with logo
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <img src="{LOGO}" width="80" style="vertical-align: middle; margin-right: 10px;">
            <h1 style="display: inline-block; vertical-align: middle; color: #2563eb;">
                EduFlow Login
            </h1>
        </div>
        """, unsafe_allow_html=True)

        if not is_authenticated():
            # Google auth section
            auth_url = authenticate()
            st.markdown(f"""
            <div style="text-align: center; margin: 2rem 0;">
                <a href="{auth_url}" target="_blank">
                    <button class="google-btn">
                        <img src="https://www.gstatic.com/images/branding/product/1x/google_48dp.png" 
                             width="20" style="vertical-align: middle; margin-right: 10px;">
                        Continue with Google
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)

            # Auth code input
            with stylable_container(
                key="auth_code_box",
                css_styles="""
                {
                    background: rgba(37, 99, 235, 0.05);
                    border-radius: 10px;
                    padding: 1.5rem;
                }
                """
            ):
                auth_code = st.text_input("Paste authorization code:", 
                                         placeholder="Paste code from Google here...",
                                         help="You'll get this after clicking the Google button")

                if auth_code:
                    with st.spinner("Authenticating..."):
                        try:
                            creds = fetch_token(auth_code)
                            with open(TOKEN_FILE, "wb") as token:
                                pickle.dump(creds, token)
                            st.success("✅ Login successful!")
                            st.balloons()
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")

        else:  # Authenticated view
            with open(TOKEN_FILE, "rb") as token:
                creds = pickle.load(token)
            
            user_info = build("oauth2", "v2", credentials=creds).userinfo().get().execute()
            user_email = user_info["email"]
            user_role = detect_user_role(creds)
            
            st.markdown(f"""
            <div style="text-align: center; margin: 2rem 0;">
                <h2 style="color: #2563eb;">Welcome, {user_role.capitalize()}!</h2>
                <p style="color: #555;">{user_email}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Another animation for dashboard transition
            try:
                st_lottie(load_lottie("https://assets1.lottiefiles.com/packages/lf20_2cwDXD.json"), 
                         height=200, key="dashboard-anim")
            except:
                pass
            
            if st.button("Go to Dashboard", type="primary"):
                st.switch_page("pages/dashboard.py")
            
            if st.button("Sign Out"):
                os.remove(TOKEN_FILE)
                st.rerun()

if __name__ == "__main__":
    main()