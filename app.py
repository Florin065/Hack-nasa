import streamlit as st
import base64
import time
from components.explorer import show_explorer_view
from components.datascientist import show_datascientist_view

st.set_page_config(
    page_title="Exoplanet Explorer",
    page_icon="🔭",
    layout="wide"
)

# Hide Streamlit multipage navigation (tabs/sidebar) to remove visible page tabs
st.markdown(
    """
    <style>
    /* Hide multipage navigation and sidebar elements */
    /* Hide the sidebar navigation list of pages */
    [data-testid="stSidebarNav"] { display: none !important; }
    /* Hide any header page navigation bar if present */
    nav[aria-label="Page navigation"] { display: none !important; }
    /* Hide the sidebar entirely (including expander button area) */
    section[data-testid="stSidebar"] { display: none !important; }
    /* Hide sidebar collapsed control / toggle (various Streamlit versions) */
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

    st.markdown("<h1 style='text-align: center; margin-top: 10%; color: white;'>Alege-ți Călătoria</h1>",
                unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        .stButton > button {
            background: rgba(255,255,255,0.92) !important;
            color: #0b1736 !important;
            border: 1px solid rgba(0,0,0,0.2) !important;
            border-radius: 10px !important;
            padding: 0.6rem 1rem !important;
            font-weight: 600 !important;
            box-shadow: 0 6px 16px rgba(0,0,0,0.35) !important;
            backdrop-filter: blur(2px);
        }
        .stButton > button:hover {
            background: #e7f1ff !important;
            border-color: rgba(0, 123, 255, 0.6) !important;
            box-shadow: 0 8px 20px rgba(7, 86, 170, 0.35) !important;
        }
        .stButton > button:disabled, .stButton > button[disabled] {
            background: rgba(255,255,255,0.6) !important;
            color: rgba(11,23,54,0.6) !important;
            border-color: rgba(0,0,0,0.15) !important;
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