import streamlit as st
import base64
import streamlit.components.v1 as components


def _inject_green_divider_css():
    if st.session_state.get("_green_divider_css_injected"):
        return
    st.session_state["_green_divider_css_injected"] = True
    st.markdown(
        """
        <style>
        .exo-divider {
          height: 3px;
          border: 0;
          margin: .25rem 0 1rem 0;
          border-radius: 999px;
          background: linear-gradient(
            90deg,
            rgba(16,185,129,0) 0%,
            rgba(16,185,129,1) 15%,
            rgba(5,150,105,1) 50%,
            rgba(16,185,129,1) 85%,
            rgba(16,185,129,0) 100%
          );
          box-shadow: 0 0 10px rgba(16,185,129,.35);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def green_header(text: str, level: int = 2):
    _inject_green_divider_css()
    tag = f"h{level}"
    st.markdown(
        f"<{tag} style='margin:0'>{text}</{tag}><div class='exo-divider'></div>",
        unsafe_allow_html=True
    )


def _img_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _anchored_modal_card(
    name: str,
    img_path: str,
    body_html: str,
    key: str,
    height: int = 640,
    img_scale: float = 0.75,   # <— imagine mai mică (75% din lățimea cardului)
    offset_px: int = 0         # <— offset vertical al cardului (px)
):
    """
    Renders a card where clicking the image toggles a glass/blur 'modal-like' panel
    that appears directly below the image (anchored to the card). The panel scrolls
    internally so text never gets cut off by the card height.
    """
    b64 = _img_b64(img_path)
    img_width_percent = int(img_scale * 100)
    html_block = f"""
    <div style="max-width: 720px; margin: 0 auto; margin-top:{offset_px}px;">
      <style>
        .card-{key} {{
          position: relative;  /* anchor for the panel */
          border-radius: 14px;
          padding: 10px;
        }}
        .card-{key} img {{
          width: {img_width_percent}%;
          display: block;
          border-radius: 12px;
          cursor: pointer;
          border: none;
          margin: 0 auto;      
          box-shadow: none;
        }}
        .hint-{key} {{
          margin-top: 8px; text-align: center; color: #cfeede; font-size: 0.9rem;
        }}

        #panel-{key} {{
          display: none;
          margin-top: 10px;
          border-radius: 12px;
          background: rgba(14, 17, 23, 0.30);
          backdrop-filter: blur(12px) saturate(120%);
          color: #f5fff7;
          border: 1px solid rgba(255,255,255,0.18);
          box-shadow: 0 16px 40px rgba(0,0,0,0.45);
          padding: 14px 16px 16px 16px;
        }}

        #panel-content-{key} {{
          max-height: 50vh;
          overflow: auto;
          line-height: 1.6;
        }}

        .panel-close-{key} {{
          position: sticky;
          top: 0;
          display: inline-block;
          margin-left: auto;
          float: right;
          cursor: pointer;
          color: #cfeede;
          font-size: 22px;
          padding: 2px 6px;
          border-radius: 8px;
        }}
        .panel-close-{key}:hover {{
          background: rgba(255,255,255,0.08);
        }}

        
      </style>

      <div class="card-{key}">
        <img id="img-{key}" src="data:image/png;base64,{b64}" alt="{name}">
        

        <div id="panel-{key}">
          <span class="panel-close-{key}" id="close-{key}" title="Close">✕</span>
          <div class="panel-arrow-{key}"></div>
          <div id="panel-content-{key}">
            {body_html}
          </div>
        </div>
      </div>

      <script>
        (function() {{
          const img   = document.getElementById("img-{key}");
          const panel = document.getElementById("panel-{key}");
          const close = document.getElementById("close-{key}");

          function togglePanel() {{
            if (!panel) return;
            panel.style.display = (panel.style.display === "none" || !panel.style.display) ? "block" : "none";
          }}

          if (img)   img.addEventListener("click", togglePanel);
          if (close) close.addEventListener("click", () => panel.style.display = "none");
        }})();
      </script>
    </div>
    """
    # height controls the iframe that hosts this card; make it tall enough for the panel
    components.html(html_block, height=height, scrolling=False)


# ───────────────────────────────────────────────────────────────────────────────
# Gallery
# ───────────────────────────────────────────────────────────────────────────────
def show_interactive_planets():
    """
    Displays an interactive gallery of exoplanets.
    Clicking the image opens a modal-like pop-up panel below the picture.
    """

    PLANET_DATA = {
        "Kepler-22b": {
            "image": "assets/explorer/planets/Kepler-22b.png",
            "body": """
                <b>Kepler-22 b — Possible water world</b><br>
                <b>Discovered 2011:</b> A possible ocean world orbiting in the habitable zone—the region around a star
                where the temperature is right for liquid water, a requirement for life on Earth.
            """
        },
        "Kepler-452b": {
            "image": "assets/explorer/planets/Kepler-452b.png",
            "body": """
                <b>Kepler-452 b — Earth's older cousin</b><br>
                <b>Discovered 2015:</b> An "Earth-cousin" that orbits a star like our sun in the habitable zone,
                where liquid water could exist.
            """
        },
        "WASP-96b": {
            "image": "assets/explorer/planets/WASP-96b.png",
            "body": """
                <b>WASP-96 b — Hot and puffy with a signature of water</b><br>
                <b>Discovered 2014:</b> An international team found that WASP-96 b is a world with a sodium rich atmosphere.
                The planet, located nearly 1,150 light-years from Earth, orbits its star every 3.4 days. It has about half
                the mass of Jupiter, and its discovery was announced in 2014.
            """
        }
    }

    green_header("Featured Exoplanets", level=2)

    cols = st.columns(3)
    idx = 0
    for name, data in PLANET_DATA.items():
        with cols[idx]:
            _anchored_modal_card(
                name=name,
                img_path=data["image"],
                body_html=data["body"],
                key=name.replace(" ", "_"),
                height=720,  # increase if you want more space for the open panel
            )
        idx = (idx + 1) % 3


def show_explorer_view():
    """
    Shows a title and a button. When clicked, it reveals the
    informational expanders and the interactive planet gallery.
    """
    if 'show_details' not in st.session_state:
        st.session_state.show_details = False

    def reveal_details():
        st.session_state.show_details = True

    # CSS for expanders and hero title
    st.markdown(
        """
        <style>
          .title-container {
            height: 85vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
          }
          .big-title {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-size: 3.5rem;
            font-weight: 100;
            letter-spacing: 2px;
            color: white;
            text-shadow: 0 2px 8px rgba(0,0,0,0.7);
            margin: 0;
            padding: 0;
          }
          .subtitle {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-size: 1.1rem;
            font-weight: 300;
            color: rgba(255, 255, 255, 0.8);
            margin-top: 10px;
            margin-bottom: 40px;
          }
          [data-testid="stExpander"] {
            border: none;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
          }
          [data-testid="stExpander"] > details > summary {
            background-color: #1a1a2e;
            color: #ffffff;
            border-radius: 10px;
          }
          [data-testid="stExpander"] > details > div {
            background-color: #0e1117;
            border-radius: 0 0 10px 10px;
            padding: 1rem;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.show_details:
        st.markdown(
            """
            <div class="title-container">
              <h1 class="big-title">Why are exoplanets important for humanity?</h1>
              <p class="subtitle">Let's discover the worlds beyond our solar system</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        _, center_col, _ = st.columns([2, 1, 2])
        with center_col:
            st.button("Let's find out", on_click=reveal_details, use_container_width=True)

    else:
        green_header("The Importance of Exoplanets", level=2)

        with st.expander("What are exoplanets? 🪐"):
            st.write(
                """
                An **exoplanet** is any planet that orbits a star outside our solar system. The first confirmed discovery
                occurred in the early 1990s. Since then, telescopes like Kepler and TESS have revealed thousands of distant
                worlds. These findings show that planets are incredibly common across the galaxy.
                """
            )

        with st.expander("Types of Exoplanets 🔭"):
            st.markdown(
                """
                The thousands of exoplanets discovered so far fall into a few broad categories, many of which are unlike anything in our own solar system:
                - **Gas Giants:** Large planets like Jupiter or Saturn. "Hot Jupiters" are a famous sub-class that orbit extremely close to their stars.
                - **Super-Earths:** Rocky planets larger than Earth but smaller than Neptune. They are one of the most common types of planets discovered.
                - **Mini-Neptunes:** Worlds smaller than Neptune but larger than Earth, likely with thick hydrogen-helium atmospheres.
                - **Terrestrial Planets:** Rocky, Earth-sized worlds or smaller. Finding these in the habitable zone is a primary goal of many missions.
                """
            )

        with st.expander("How do we find exoplanets? 🛰️"):
            st.write(
                "Detecting exoplanets is challenging because they are far dimmer than their host stars. Two key methods:"
            )
            st.markdown(
                """
                - **Transit method:** When a planet passes in front of its star, it blocks a tiny fraction of starlight.  
                - **Radial velocity:** A planet’s gravity makes its star wobble; we detect the wobble in the star’s spectrum.
                """
            )

        with st.expander("The 'Goldilocks' Zone 🎯"):
            st.write(
                """
                The **habitable zone**, often called the "Goldilocks Zone," is the orbital region around a star where conditions are "just right"—not too hot and not too cold—for liquid water to exist on a planet's surface.

                While it's a crucial starting point in the search for life, it's not a guarantee. Other factors, like a planet's atmosphere, composition, and its star's activity, also play a huge role in true habitability.
                """
            )

        with st.expander("So, why are exoplanets important? 🤔"):
            st.write("Three core reasons this field matters:")
            st.markdown(
                """
                1. **Life:** Exoplanets offer our best shot at answering “Are we alone?”  
                2. **Origins:** Comparing many systems teaches us how planets form and how Earth fits in.  
                3. **Innovation:** The search drives advances in telescopes and data science.
                """
            )
            st.write(
                "Every exoplanet adds a piece to the cosmic puzzle—and helps us understand our place in the universe.")

        with st.expander("The future of Exoplanet hunting"):
            st.write(
                """
                The search is just getting started. The next generation of telescopes will move from simply detecting planets to characterizing them in detail.
                - **Nancy Grace Roman Space Telescope (NASA):** Will discover thousands more exoplanets using a wide-field view to conduct a massive galactic survey.
                - **Extremely Large Telescope (ESO):** A ground-based telescope with a massive 39-meter mirror that will be able to directly image larger exoplanets and analyze their atmospheres.
                """
            )

        show_interactive_planets()


if __name__ == "__main__":
    show_explorer_view()
