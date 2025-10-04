import streamlit as st
import base64

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

def show_datascientist_view():
    """Afișează componentele pentru rolul de Data Scientist."""
    st.header("🔭 Panoul Analistului de Date", divider='blue')
    st.info("Încarcă seturi de date, analizează curbe de lumină și aplică algoritmi pentru a descoperi noi lumi.")

    uploaded_file = st.file_uploader(
        "Încarcă un fișier CSV cu date despre luminozitatea unei stele",
        type=['csv']
    )

    if uploaded_file is not None:
        st.success("Fișier încărcat cu succes!")
        # Aici poți adăuga logica pentru procesarea datelor
        st.line_chart(uploaded_file)


def show_explorer_view():
    """Afișează componentele pentru rolul de Explorer."""
    st.header("🚀 Panoul Exploratorului Cosmic", divider='violet')
    st.info("Navighează prin galaxie, descoperă statistici uimitoare și învață despre cele mai fascinante exoplanete.")

    # Aici poți adăuga statistici, grafice, imagini, etc.
    st.subheader("Statistici cheie")
    col1, col2, col3 = st.columns(3)
    col1.metric("Exoplanete Descoperite", "5,000+", "lumi noi")
    col2.metric("Sisteme Planetare", "3,800+", "stele cu planete")
    col3.metric("Tipuri de Planete", "Giganți gazoși, Super-Pământuri", "etc.")


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