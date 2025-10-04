import streamlit as st

st.set_page_config(page_title="Introducere", page_icon="📖")

st.markdown("# Introducere în Lumea Exoplanetelor 📖")
st.sidebar.header("Introducere")

st.write(
    """
    Această pagină este dedicată introducerii în conceptele de bază.
    Vom explora ce sunt exoplanetele și cum au revoluționat astronomia.
    """
)

# Aici poți adăuga animații și text
st.header("Ce este o Exoplanetă?")
st.write(
    """
    O exoplanetă este o planetă care orbitează o altă stea decât Soarele nostru.
    Descoperirea lor a confirmat că sistemele solare sunt comune în galaxia noastră.
    """
)

# Exemplu de cum ai adăuga o imagine sau animație (asigură-te că ai un fișier în assets/imagini)
# st.image("assets/imagini/animatie_intro.gif", caption="Animație a unei exoplanete")