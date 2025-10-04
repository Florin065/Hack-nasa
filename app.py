import streamlit as st
import base64
from components.explorer import show_explorer_view
from components.datascientist import show_datascientist_view

# --- SETĂRI GENERALE ---
st.set_page_config(
    page_title="Exoplanet Explorer",
    page_icon="🔭",
    layout="wide"
)


# --- FUNCȚII UTILITARE ---

# Funcție pentru a seta o imagine locală ca fundal al paginii
def set_page_bg(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: cover;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)


# --- FUNCȚII PENTRU VIZUALIZĂRI ---

# --- LOGICA PRINCIPALĂ A APLICAȚIEI ---

# Inițializăm starea în session_state dacă nu există
if 'role' not in st.session_state:
    st.session_state.role = None


# Funcții callback pentru butoane
def set_role(role_name):
    st.session_state.role = role_name


# Verificăm starea curentă și afișăm vizualizarea corespunzătoare
if st.session_state.role is None:
    # STAREA 1: ECRANUL DE START
    set_page_bg("assets/home.jpeg")

    st.markdown("<h1 style='text-align: center; margin-top: 10%; color: white;'>Alege-ți Călătoria</h1>",
                unsafe_allow_html=True)

    # Folosim coloane pentru a centra butoanele
    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
    with col2:
        st.button("🔬 Data Scientist", on_click=set_role, args=('datascientist',), use_container_width=True)
    with col3:
        st.button("✨ Explorer", on_click=set_role, args=('explorer',), use_container_width=True)

elif st.session_state.role == 'datascientist':
    # STAREA 2: VIZUALIZAREA DATA SCIENTIST
    set_page_bg("assets/background.jpeg")
    show_datascientist_view()

elif st.session_state.role == 'explorer':
    # STAREA 3: VIZUALIZAREA EXPLORER
    set_page_bg("assets/background.jpeg")
    show_explorer_view()