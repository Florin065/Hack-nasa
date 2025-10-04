import streamlit as st


def show_interactive_planets():
    """
    Displays an interactive gallery of exoplanets.
    Clicking a button opens a dialog (pop-up) with details.
    """

    # --- Data for the Exoplanets ---
    # Make sure the image paths match your folder structure (e.g., "assets/planets/Kepler-22b.jpeg")
    PLANET_DATA = {
        "Kepler-22b": {
            "image": "assets/explorer/planets/Kepler-22b.png",
            "description": "One of the first 'Super-Earths' found within its star's habitable zone. It's about 2.4 times the size of Earth and orbits a Sun-like star, making it a famous candidate in the search for potentially habitable worlds."
        },
        "Kepler-452b": {
            "image": "assets/explorer/planets/Kepler-452b.png",
            "description": "Often called 'Earth's Cousin,' this exoplanet orbits a star very similar to our Sun. It is located in the habitable zone, but its larger size means it could be a rocky 'Super-Earth' or a small gas planet."
        },
        "WASP-96b": {
            "image": "assets/explorer/planets/WASP-96b.png",
            "description": "A hot, puffy gas giant famous for being one of the first targets of the James Webb Space Telescope. Webb's observations provided a detailed atmospheric analysis, revealing the unambiguous signature of water."
        }
    }

    st.header("Featured Exoplanets", divider="rainbow")

    # --- Create the Gallery ---
    cols = st.columns(3)
    col_index = 0

    for planet_name, data in PLANET_DATA.items():
        with cols[col_index]:
            with st.container(border=False):
                st.image(data["image"])

                # Button to open the dialog
                if st.button(f"Details about {planet_name}", key=planet_name, use_container_width=True):
                    with st.dialog(f"Information: {planet_name}"):
                        st.image(data["image"])
                        st.write(data["description"])

        col_index = (col_index + 1) % 3


def show_explorer_view():
    """
    Shows a title and a button. When clicked, it reveals the
    informational expanders and the interactive planet gallery.
    """
    if 'show_details' not in st.session_state:
        st.session_state.show_details = False

    def reveal_details():
        st.session_state.show_details = True

    # --- CSS Styling ---
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
              <p class="subtitle">Discover the worlds beyond our solar system</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        _, center_col, _ = st.columns([2, 1, 2])
        with center_col:
            st.button("Let's find out", on_click=reveal_details, use_container_width=True)

    else:
        st.header("The Importance of Exoplanets", divider="rainbow")

        with st.expander("What Are Exoplanets? 🪐"):
            st.write(
                """
                An **exoplanet** is any planet that orbits a star outside our solar system. The first confirmed discovery occurred in the early 1990s. Since then, telescopes like Kepler and TESS have revolutionized astronomy by revealing thousands of distant worlds. These findings have shown that planets are, in fact, incredibly common throughout the galaxy.
                """
            )

        with st.expander("How Do We Find Worlds Light-Years Away? 🔭"):
            st.write(
                """
                Detecting exoplanets is challenging because they are extremely small and dim compared to their host stars. Astronomers use ingenious, indirect methods to find them:
                """
            )
            st.markdown(
                """
                - **The Transit Method:** This is the most successful technique. When an exoplanet passes in front of its star (a "transit"), it blocks a tiny fraction of the star's light.

                - **The Radial Velocity Method:** A planet's gravity tugs on its star, causing it to "wobble" slightly. Astronomers can detect this wobble by analyzing the star's light.
                """
            )

        with st.expander("So, Why Are Exoplanets Important? 🤔"):
            st.write(
                """
                The study of exoplanets is more than just cataloging new worlds. Their importance is profound and touches on three essential pillars of our existence:
                """
            )
            st.markdown(
                """
                1.  **The Search for Life:** For the first time in history, exoplanets give us a realistic chance to answer the question, "Are we alone in the Universe?"

                2.  **Understanding Our Own Origin:** By studying thousands of other solar systems, we learn about the rules that govern planet formation. This helps us understand the cosmic context of our own Earth.

                3.  **Driving Innovation:** The challenge of detecting these distant worlds pushes the boundaries of technology, leading to more powerful telescopes and advanced data analysis algorithms.
                """
            )
            st.write(
                """
                In essence, every exoplanet discovered is a piece of a giant puzzle that helps us understand the Universe and, ultimately, ourselves.
                """
            )

        # --- Call the new function to display the interactive gallery ---
        show_interactive_planets()