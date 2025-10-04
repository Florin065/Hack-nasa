import streamlit as st

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