import streamlit as st
import math
import requests


G_cgs = 6.67430e-8             # cm^3 g^-1 s^-2
R_sun_cm = 6.957e10            # cm
R_sun_AU = 0.00465047          # AU
M_sun_g = 1.98847e33           # g
sigma_sb_cgs = 5.670374419e-5  # erg cm^-2 s^-1 K^-4
T_sun_K = 5772.0

def _stellar_mass_from_logg_R(logg_cgs: float, R_solar: float) -> float:
    """Return stellar mass in solar masses from log g (cgs) and radius in solar radii."""
    g = 10 ** logg_cgs              # cm s^-2
    R_cm = R_solar * R_sun_cm
    M_g = g * R_cm**2 / G_cgs
    return M_g / M_sun_g

def _a_from_Teq_Teff_Rstar(Teq_K: float, Teff_K: float, R_solar: float) -> float:
    """
    Equilibrium temperature (A=0, full redistribution):
    Teq = Teff * sqrt(R*/(2a))  => a = R*/[2*(Teq/Teff)^2]
    Returns a in AU.
    """
    if Teq_K <= 0 or Teff_K <= 0 or R_solar <= 0:
        return float("nan")
    ratio = Teq_K / Teff_K
    a_over_Rstar = 1.0 / (2.0 * ratio * ratio)   # a / R*
    a_AU = a_over_Rstar * (R_solar * R_sun_AU)
    return a_AU

def _period_from_kepler(a_AU: float, M_star_solar: float) -> float:
    """Kepler's 3rd law in solar units: P[yr]^2 = a[AU]^3 / M[Msun]"""
    if a_AU <= 0 or M_star_solar <= 0:
        return float("nan")
    P_years = math.sqrt((a_AU**3) / M_star_solar)
    return P_years * 365.25  # days

def _depth_from_radii(Rp_Re: float, Rstar_Rsun: float) -> float:
    """Transit depth (fraction) ≈ (Rp/R*)^2 using Earth & Solar radii."""
    if Rp_Re <= 0 or Rstar_Rsun <= 0:
        return float("nan")
    R_earth_over_R_sun = 6371e5 / R_sun_cm
    Rp_over_Rstar = (Rp_Re * R_earth_over_R_sun) / Rstar_Rsun
    return (Rp_over_Rstar ** 2)

def _flux_rel_earth(Teff_K: float, Rstar_Rsun: float, a_AU: float) -> float:
    """S/S_earth = (L*/Lsun) / a^2 with L ∝ R^2 T^4."""
    if Teff_K <= 0 or Rstar_Rsun <= 0 or a_AU <= 0:
        return float("nan")
    L_rel = (Rstar_Rsun*2) * ((Teff_K / T_sun_K) * 4)
    return L_rel / (a_AU ** 2)

def _central_transit_duration_hours(P_days: float, a_AU: float, Rstar_Rsun: float) -> float:
    """
    Approx central transit duration for b≈0, small Rp:
    T ≈ (P/π) * arcsin(R*/a)  ~ (P/π)(R/a) for small angles.
    Returns hours.
    """
    if P_days <= 0 or a_AU <= 0 or Rstar_Rsun <= 0:
        return float("nan")
    Rstar_AU = Rstar_Rsun * R_sun_AU
    x = min(1.0, Rstar_AU / a_AU)
    T_days = (P_days / math.pi) * math.asin(x)
    return T_days * 24.0

def _rel_err(x, y):
    if not (math.isfinite(x) and math.isfinite(y)) or y == 0:
        return float("inf")
    return abs(x - y) / abs(y)

def _go_home():
    """Navigate back to the main role-selection page."""
    try:
        st.switch_page("app.py")
    except Exception:
        st.session_state.update(role=None)
        st.rerun()

def show_datascientist_view():
    st.markdown(
        "<h2 style='color:white; text-align:center;'>Exoplanet Check</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style="
            text-align:center;
            color:white;
            background:rgba(255,255,255,0.08);
            border:1px solid rgba(255,255,255,0.25);
            border-radius:10px;
            padding:0.8rem;
            margin:0.8rem auto 1.2rem auto;
            max-width:900px;
            backdrop-filter: blur(4px);
        ">
            Here you can test whether the entered parameters correspond to a potential exoplanet,<br>
            as evaluated by our <b>AI/ML model</b>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    API_URL = st.sidebar.text_input(
        "Backend URL (Colab/Cloudflare)",
        value="https://stripes-compiler-longitude-zshops.trycloudflare.com"
    ).strip()
    API_TOKEN = st.sidebar.text_input("API token (optional)", type="password")

    if st.sidebar.button("Ping backend"):
        try:
            r = requests.get(f"{API_URL.rstrip('/')}/", timeout=10)
            st.sidebar.success(f"Ping OK: {r.status_code}")
        except Exception as e:
            st.sidebar.error(f"Ping failed: {e}")

    with st.form("exo_form", clear_on_submit=False):
        cols = st.columns(2)

        fields = [
            ("Orbital period (days)",               dict(min_value=0.0, step=0.1,  format="%.5f", key="P_days")),
            ("Transit epoch (e.g., BJD_TDB)",       dict(step=0.1,                 format="%.5f", key="t0")),
            ("Transit duration (hours)",            dict(min_value=0.0, step=0.1,  format="%.5f", key="dur_hours")),
            ("Transit depth (ppm)",                 dict(min_value=0.0, step=10.0, format="%.5f", key="depth_val")),
            ("Planetary radius (Earth radii)",      dict(min_value=0.0, step=0.1,  format="%.5f", key="Rp_Re")),
            ("Equilibrium temperature (K)",         dict(min_value=0.0, step=10.0, format="%.5f", key="Teq_K")),
            ("Earth flux",                          dict(min_value=0.0, step=0.1,  format="%.5f", key="S_earth")),
            ("Stellar effective temperature (K)",   dict(min_value=0.0, step=10.0, format="%.5f", key="Teff_K")),
            ("Stellar surface gravity log g (cgs)", dict(min_value=0.0, step=0.01, format="%.5f", key="logg")),
            ("Stellar radius (Solar radii)",        dict(min_value=0.0, step=0.01, format="%.5f", key="Rstar_Rsun")),
            ("Right ascension (deg, 0–360)",        dict(min_value=0.0, max_value=360.0, step=0.1, format="%.5f", key="RA_deg")),
            ("Declination (deg, -90–+90)",          dict(min_value=0.0, max_value=90.0, step=0.1, format="%.5f", key="Dec_deg")),
        ]

        for i, (label, kwargs) in enumerate(fields):
            with cols[i % 2]:
                st.number_input(label, **kwargs)

        submitted = st.form_submit_button("Check parameters")

    if not submitted:
        st.divider()
        if st.button("← Back to role selection"):
            _go_home()
        return

    P_days       = st.session_state.get("P_days", 0.0)
    t0           = st.session_state.get("t0", 0.0)
    dur_hours    = st.session_state.get("dur_hours", 0.0)
    depth_val    = st.session_state.get("depth_val", 0.0)
    Rp_Re        = st.session_state.get("Rp_Re", 0.0)
    Teq_K        = st.session_state.get("Teq_K", 0.0)
    S_earth      = st.session_state.get("S_earth", 0.0)
    Teff_K       = st.session_state.get("Teff_K", 0.0)
    logg         = st.session_state.get("logg", 0.0)
    Rstar_Rsun   = st.session_state.get("Rstar_Rsun", 0.0)
    RA_deg       = st.session_state.get("RA_deg", 0.0)
    Dec_deg      = st.session_state.get("Dec_deg", 0.0)

    payload = {
        "period_days": P_days,
        "t0": t0,
        "duration_hours": dur_hours,
        "transit_depth_ppm": depth_val,
        "radius_earth": Rp_Re,
        "teq_K": Teq_K,
        "S_earth": S_earth,
        "teff_star_K": Teff_K,
        "logg_cgs": logg,
        "rstar_rsun": Rstar_Rsun,
        "ra_deg": RA_deg,
        "dec_deg": Dec_deg,
    }

    st.divider()
    if not API_URL:
        st.error("Setează URL-ul backendului în sidebar.")
        if st.button("← Back to role selection"):
            _go_home()
        return

    headers = {"Content-Type": "application/json"}
    if API_TOKEN:
        headers["X-API-Key"] = API_TOKEN

    try:
        with st.spinner("Contacting backend…"):
            resp = requests.post(f"{API_URL.rstrip('/')}/predict", json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        probability = data.get("probability", 0.0)
        label = data.get("label", 0)
        threshold = data.get("threshold", 0.5)
        echo = data.get("echo", {})

        planet_radius = echo.get("radius_earth", "N/A")
        eq_temp_k = echo.get("teq_K", "N/A")
        orbital_period_days = echo.get("period_days", "N/A")
        star_temp_k = echo.get("teff_star_K", "N/A")

        eq_temp_c = eq_temp_k - 273.15 if isinstance(eq_temp_k, (int, float)) else "N/A"

        star_type = "Unknown"
        if isinstance(star_temp_k, (int, float)):
            if star_temp_k >= 7500: star_type = "A-type (Hot, Blue-White)"
            elif star_temp_k >= 6000: star_type = "F-type (White)"
            elif star_temp_k >= 5200: star_type = "G-type (Sun-like, Yellow)"
            elif star_temp_k >= 3700: star_type = "K-type (Orange Dwarf)"
            else: star_type = "M-type (Red Dwarf)"

        if label == 1:
            verdict_text = "Promising Exoplanet"
            verdict_color = "#28a745"
            verdict_emoji = "✅"
            explanation = (
                "The model suggests this candidate has characteristics consistent with a potentially "
                "viable exoplanet. The probability score is above the decision threshold."
            )
        else:
            verdict_text = "Unlikely Exoplanet"
            verdict_color = "#dc3545"
            verdict_emoji = "❌"
            explanation = (
                "The model indicates a low probability for this candidate. Key factors might place it "
                "outside the typical parameters for a viable exoplanet or habitable zone."
            )

        summary_html = f"""
        <div style="
            background: rgba(10, 20, 30, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 10px;
            padding: 20px;
            margin: 1rem 0;
            color: white;
            backdrop-filter: blur(5px);
        ">
            <h3 style="color: {verdict_color}; text-align: center; margin-top:0;">
                {verdict_emoji} AI/ML Verdict: {verdict_text}
            </h3>
            <p style="text-align: center; font-size: 0.9rem; color: #E0E0E0;">
                {explanation}
            </p>
            <hr style="border-color: rgba(255, 255, 255, 0.2); margin: 15px 0;">
            <div style="display: flex; justify-content: space-around; text-align: center;">
                <div style="flex-basis: 50%;">
                    <h5 style="margin-bottom: 5px; color: #A0C0FF;">System Profile</h5>
                    <p style="margin: 2px; font-size: 0.95rem;"><b>Planet Radius:</b> {planet_radius:.2f} x Earth</p>
                    <p style="margin: 2px; font-size: 0.95rem;"><b>Eq. Temperature:</b> {eq_temp_k} K ({eq_temp_c:.1f}°C)</p>
                    <p style="margin: 2px; font-size: 0.95rem;"><b>Orbital Period:</b> {orbital_period_days} days</p>
                    <p style="margin: 2px; font-size: 0.95rem;"><b>Host Star (Est.):</b> {star_type}</p>
                </div>
                <div style="border-left: 1px solid rgba(255, 255, 255, 0.2); height: 100px; margin: auto 0;"></div>
                <div style="flex-basis: 50%;">
                    <h5 style="margin-bottom: 5px; color: #A0C0FF;">Model Confidence</h5>
                    <p style="margin: 2px; font-size: 0.95rem;"><b>Probability Score:</b> {probability:.2%}</p>
                    <p style="margin: 2px; font-size: 0.95rem;"><b>Decision Threshold:</b> {threshold:.2%}</p>
                </div>
            </div>
        </div>
        """
        st.markdown(summary_html, unsafe_allow_html=True)

        with st.expander("Full JSON response"):
            st.json(data)

    except requests.exceptions.RequestException as e:
        st.error(f"API error: {e}")
        with st.expander("Payload sent)"):
            st.json(payload)

    if st.button("← Back to role selection"):
        _go_home()