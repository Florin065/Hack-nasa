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


def set_role(role_name):
    st.session_state.role = role_name


def start_transition(target_role: str):
    """Begin the zoom-right transition before switching to target_role."""
    st.session_state.transitioning = True
    st.session_state.transition_target = target_role
    st.session_state.transition_start = time.time()


# Handle transition animation state first
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

    time.sleep(TRANSITION_DURATION_SEC)
    st.session_state.role = st.session_state.transition_target
    st.session_state.transitioning = False
    st.session_state.transition_target = None
    st.session_state.transition_start = None
    st.rerun()

elif st.session_state.role is None:
    set_page_bg("assets/backgrounds/home.jpeg")

    st.markdown("<h1 style='text-align: center; margin-top: 10%; color: white;'>Alege-ți Călătoria</h1>",
                unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
    with col2:
        st.button("🔬 Data Scientist", on_click=start_transition, args=('datascientist',), use_container_width=True)
    with col3:
        st.button("✨ Explorer", on_click=start_transition, args=('explorer',), use_container_width=True)

elif st.session_state.role == 'datascientist':
    set_page_bg("assets/backgrounds/background.jpeg")
    show_datascientist_view()

elif st.session_state.role == 'explorer':
    set_page_bg("assets/backgrounds/background.jpeg")
    show_explorer_view()