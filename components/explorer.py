import streamlit as st
import base64
from pathlib import Path


ASSETS_DIR = Path('assets/explorer')
SLIDES = [
    ASSETS_DIR / 'slide1.jpeg',
    ASSETS_DIR / 'slide2.jpeg',
    ASSETS_DIR / 'slide3.jpeg',
    ASSETS_DIR / 'slide4.jpeg',
]


def _img_to_data_uri(path: Path) -> str:
    try:
        with open(path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"data:image/jpeg;base64,{b64}"
    except Exception:
        return ""


def show_explorer_view():
    """Explorer view with a centered title and a bottom-centered arrow.
    Clicking the arrow reveals a carousel and smoothly scrolls down to it.
    """
    if 'explorer_show_carousel' not in st.session_state:
        st.session_state.explorer_show_carousel = False
    if 'explorer_scrolled' not in st.session_state:
        st.session_state.explorer_scrolled = False

    if not st.session_state.explorer_show_carousel:
        st.markdown(
            """
            <style>
              .explorer-center {
                height: 70vh; /* occupy most of the viewport to center vertically */
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 0 1rem;
              }
              .explorer-center h1 {
                color: #ffffff;
                margin: 0 0 16px 0;
                font-size: 2.2rem;
                text-shadow: 0 2px 6px rgba(0,0,0,0.6);
              }
              /* Center the arrow below the title */
              .arrow-inline {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 0 1rem;
                
              /* Make the arrow button large and minimal */
              .arrow-inline .stButton > button {
                font-size: 2rem;
                line-height: 1;
                padding: 10px 18px;
                border-radius: 999px;
                border: 2px solid rgba(255,255,255,0.75);
                background: rgba(0,0,0,0.25);
                color: #ffffff;
                box-shadow: 0 6px 16px rgba(0,0,0,0.35);
                backdrop-filter: blur(2px);
              }
              .arrow-inline .stButton > button:hover { background: rgba(255,255,255,0.15); }
            </style>
            <div class="explorer-center">
              <h1>Why are exoplanets important for humanity?</h1>
              <div class="arrow-inline">
                <!-- The actual Streamlit button is rendered next -->
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Centered arrow button directly under the title (aligned like the title)
        st.markdown('<div class="arrow-inline">', unsafe_allow_html=True)
        if st.button("⬇️", key="explorer_start_carousel"):
            st.session_state.explorer_show_carousel = True
            st.session_state.explorer_scrolled = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # If we reach here, show a vertical scrolling image transition (no rocket, no carousel)
    data_uris = [_img_to_data_uri(p) for p in SLIDES]
    data_uris = [u for u in data_uris if u]

    # Build full-viewport image sections stacked vertically
    sections_html = []
    anchors_js = []
    for i, uri in enumerate(data_uris):
        sec_id = f"exp-seq-{i}"
        anchors_js.append(f"'{sec_id}'")
        sections_html.append(
            f"""
            <section id="{sec_id}" class="exp-section">
              <img src="{uri}" alt="Explorer slide {i+1}" />
            </section>
            """
        )
    sections_html_str = "\n".join(sections_html)
    anchors_js_list = ", ".join(anchors_js)

    st.markdown(
        f"""
        <style>
          .exp-top-spacer {{ height: 18vh; }}
          .exp-wrap {{
            width: 100%;
            max-width: 1100px;
            margin: 0 auto;
          }}
          .exp-section {{
            position: relative;
            width: 100%;
            height: 100vh; /* each image fills the viewport height */
            overflow: hidden;
            border-radius: 14px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.45);
            border: 1px solid rgba(255,255,255,0.25);
            backdrop-filter: blur(2px);
            margin: 0 0 16px 0;
          }}
          .exp-section img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
          }}
          /* Soft gradient at the very top to blend with background */
          .exp-gradient-top {{
            position: sticky;
            top: 0; height: 60px; margin-top: -60px; z-index: 2;
            background: linear-gradient(to bottom, rgba(0,0,0,0.65), rgba(0,0,0,0));
            pointer-events: none;
          }}
        </style>
        <div id="explorer-seq-anchor" class="exp-top-spacer"></div>
        <div class="exp-wrap">
          <div class="exp-gradient-top"></div>
          {sections_html_str}
        </div>
        <script>
          window.addEventListener('load', function() {{
            setTimeout(function() {{
              // Smoothly scroll to the sequence start, then progressively through images
              var anchor = document.getElementById('explorer-seq-anchor');
              if (anchor && anchor.scrollIntoView) {{
                anchor.scrollIntoView({{behavior:'smooth', block:'start'}});
              }}

              var ids = [{anchors_js_list}];
              var baseDelay = 1200;    // wait a bit after render
              var step = 3800;         // time between section scrolls (ms)
              ids.forEach(function(id, idx) {{
                setTimeout(function() {{
                  var el = document.getElementById(id);
                  if (el && el.scrollIntoView) {{
                    el.scrollIntoView({{behavior:'smooth', block:'start'}});
                  }}
                }}, baseDelay + idx * step);
              }});
            }}, 200);
          }});
        </script>
        """,
        unsafe_allow_html=True,
    )

    # Mark that we've triggered the automated scroll so it doesn't re-run on next renders
    if not st.session_state.explorer_scrolled:
        st.session_state.explorer_scrolled = True
    