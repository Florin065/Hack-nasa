import streamlit as st
import base64
import time
from components.explorer import show_explorer_view
from components.datascientist import show_datascientist_view

st.set_page_config(
    page_title="Exoplanet Detector",
    page_icon="🔭",
    layout="wide"
)

# Hide Streamlit multipage navigation (tabs/sidebar) to remove visible page tabs
st.markdown(
    """
    <style>
    /* Hide multipage navigation and sidebar elements */
    [data-testid="stSidebarNav"] { display: none !important; }
    nav[aria-label="Page navigation"] { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="sidebar-collapsed-control"],
    button[title="Toggle sidebar"],
    button[aria-label="Toggle sidebar"],
    button[aria-label="Open sidebar"],
    button[aria-label="Close sidebar"] { display: none !important; }
    /* Hide the top toolbar/hamburger menu */
    [data-testid="stToolbar"],
    header [data-testid="baseButton-header"],
    header [data-testid="baseLink-logo"] { display: none !important; }
    /* Hide Streamlit's top header bar */
    [data-testid="stHeader"] { display: none !important; }
    /* Remove extra top padding when header is hidden */
    .block-container { padding-top: 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

def set_page_bg(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{b64_encoded});
            background-size: cover;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)


if 'role' not in st.session_state:
    st.session_state.role = None
if 'transitioning' not in st.session_state:
    st.session_state.transitioning = False
if 'transition_target' not in st.session_state:
    st.session_state.transition_target = None
if 'transition_start' not in st.session_state:
    st.session_state.transition_start = None
if 'buttons_disabled' not in st.session_state:
    st.session_state.buttons_disabled = False


def set_role(role_name):
    st.session_state.role = role_name


def start_transition(target_role: str):
    """Begin the zoom-right transition before switching to target_role."""
    st.session_state.transitioning = True
    st.session_state.transition_target = target_role
    st.session_state.transition_start = time.time()
    st.session_state.buttons_disabled = True


TRANSITION_DURATION_SEC = 0.85
if st.session_state.transitioning:
    set_page_bg("assets/backgrounds/home.jpeg")

    st.markdown(
        """
        <style>
        .stApp { 
            animation: zoomRight 0.85s ease forwards; 
            transform-origin: center right;
        }
        @keyframes zoomRight {
            from { transform: scale(1) translateX(0); }
            to { transform: scale(2) translateX(4vw); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.empty()

    time.sleep(TRANSITION_DURATION_SEC)
    target = st.session_state.transition_target
    # Clear flags before navigation
    st.session_state.transitioning = False
    st.session_state.transition_target = None
    st.session_state.transition_start = None
    st.session_state.buttons_disabled = False

    # Prefer navigating to multipage targets if available
    try:
        if target == 'explorer':
            st.switch_page("pages/1_Explorer.py")
        elif target == 'datascientist':
            st.switch_page("pages/2_Data_Scientist.py")
        else:
            raise RuntimeError("Unknown target")
    except Exception:
        # Fallback to in-app role switching if switch_page is unavailable
        st.session_state.role = target
        st.rerun()

elif st.session_state.role is None:
    set_page_bg("assets/backgrounds/home.jpeg")

    st.markdown(
        "<h1 style='text-align:center; margin-top:10%; color:white; font-size:clamp(48px, 8vw, 120px);'>Exodetect</h1>",
        unsafe_allow_html=True,
    )

    # ⬇️ Descriptive text block under the title
    st.markdown(
        """
        <div style="
          max-width: 900px;
          margin: 12px auto 28px auto;
          text-align: center;
          color: #f5fff7;
          background: rgba(0, 0, 0, 0.28);      /* subtle translucent bg (≈28% opaque) */
          border: 1px solid rgba(255,255,255,0.10);
          border-radius: 14px;
          padding: 14px 20px;
          box-shadow: 0 8px 22px rgba(0,0,0,0.25);
          backdrop-filter: blur(4px);           /* soft glass effect */
          -webkit-backdrop-filter: blur(4px);
        ">
            <p style="margin:0.2rem 0 0.5rem 0; font-size: 1.05rem; line-height:1.5; text-shadow: 0 1px 2px rgba(0,0,0,0.45);">
                Welcome to the fascinating world of exoplanet discovery!<br>
                If you’re eager to explore the mysteries of distant worlds and understand their importance, you’re an <b>Explorer</b>.<br>
                If you’re a researcher looking to test whether your <i>measurements</i> could reveal a new planet beyond our Solar System, you’re a <b>Data Scientist</b>.
            </p>
            <p style="margin:0; opacity:0.9; text-shadow: 0 1px 2px rgba(0,0,0,0.35);">
                This platform is built for both <b>curious beginners</b> taking their first steps into exoplanet science
                and <b>experienced researchers</b> seeking to analyze and classify new data.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        /* Base button */
        .stButton > button {
            background: rgba(255,255,255,0.92) !important;
            color: #0b1736 !important;
            border: 1px solid rgba(6, 78, 59, 0.35) !important; /* dark green border */
            border-radius: 10px !important;
            padding: 0.6rem 1rem !important;
            font-weight: 600 !important;
            box-shadow:
                0 6px 16px rgba(6, 78, 59, 0.55),
                0 2px 6px rgba(6, 78, 59, 0.35) !important;      /* dark green shadow */
            backdrop-filter: blur(2px);
            transition: transform .12s ease,
                        box-shadow .12s ease,
                        border-color .12s ease,
                        background-color .12s ease !important;
        }

        /* Hover: green tint + green border/shadow */
        .stButton > button:hover {
            background-color: #e9fce9 !important;                 /* light green */
            border-color: rgba(34, 197, 94, 0.6) !important;      /* emerald */
            box-shadow:
                0 8px 22px rgba(6, 78, 59, 0.65),
                0 4px 10px rgba(6, 78, 59, 0.45) !important;      /* darker green shadow */
            transform: translateY(-1px);
        }

        /* Active (mouse down): slightly darker green */
        .stButton > button:active {
            background-color: #d8f8d8 !important;                 /* darker light green */
            border-color: rgba(22, 163, 74, 0.8) !important;      /* deeper emerald */
            box-shadow:
                0 5px 12px rgba(6, 78, 59, 0.50),
                0 2px 6px rgba(6, 78, 59, 0.35) !important;
            transform: translateY(0) scale(0.99);
        }

        /* Keyboard focus: green focus ring (no blue) */
        .stButton > button:focus,
        .stButton > button:focus-visible {
            outline: none !important;
            border-color: rgba(34, 197, 94, 0.85) !important;
            box-shadow:
                0 0 0 3px rgba(34, 197, 94, 0.28),
                0 10px 24px rgba(6, 78, 59, 0.30) !important;
        }

        /* Disabled */
        .stButton > button:disabled,
        .stButton > button[disabled] {
            background: rgba(255,255,255,0.6) !important;
            color: rgba(11,23,54,0.6) !important;
            border-color: rgba(6, 78, 59, 0.25) !important;
            box-shadow: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
    with col2:
        st.button(
            "🔬 Data Scientist",
            on_click=start_transition,
            args=('datascientist',),
            use_container_width=True,
            disabled=st.session_state.buttons_disabled,
        )
    with col3:
        st.button(
            "✨ Explorer",
            on_click=start_transition,
            args=('explorer',),
            use_container_width=True,
            disabled=st.session_state.buttons_disabled,
        )

elif st.session_state.role == 'datascientist':
    set_page_bg("assets/backgrounds/background.jpeg")
    show_datascientist_view()

elif st.session_state.role == 'explorer':
    set_page_bg("assets/backgrounds/background.jpeg")
    show_explorer_view()
