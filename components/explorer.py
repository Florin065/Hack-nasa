import streamlit as st


def show_explorer_view():
    """
    Shows a title and a button. When the button is clicked,
    it reveals the informational expanders with an opaque background.
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

          /* --- NOU: Stil pentru Expander --- */
          [data-testid="stExpander"] {
            border: none;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
          }
          [data-testid="stExpander"] > details > summary {
            background-color: #1a1a2e; /* Culoare de fundal pentru titlul expanderului */
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