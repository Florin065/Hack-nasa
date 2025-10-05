import streamlit as st
import base64
from components.explorer import show_explorer_view

st.set_page_config(page_title="Explorer", page_icon="✨", layout="wide")

st.markdown(
    """
    <style>
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
    [data-testid="stToolbar"],
    header [data-testid="baseButton-header"],
    header [data-testid="baseLink-logo"] { display: none !important; }
    [data-testid="stHeader"] { display: none !important; }
    .block-container { padding-top: 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


def _set_page_bg(image_file: str):
    try:
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
    except Exception:
        pass


_set_page_bg("assets/backgrounds/background.jpeg")

show_explorer_view()
