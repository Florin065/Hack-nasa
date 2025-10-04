import streamlit as st


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