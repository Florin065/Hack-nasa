import streamlit as st

st.set_page_config(
    page_title="Exoplanet Explorer",
    page_icon="🪐",
    layout="wide"
)

st.title("Bun venit la Exoplanet Explorer! 🌌")
st.sidebar.success("Selectează o pagină de mai sus.")

st.markdown(
    """
    Aceasta este aplicația ta interactivă pentru descoperirea și analiza exoplanetelor.
    Folosește meniul din stânga pentru a naviga între pagini.

    ### Ce poți face aici?
    - **Introducere**: Află concepte de bază despre exoplanete și metodele de detecție.
    - **Detecție**: Încarcă date și încearcă să detectezi o exoplanetă.
    - **Statistici**: Explorează statistici interesante bazate pe o bază de date existentă.
    """
)