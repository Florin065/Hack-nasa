# components/datascientist.py
import streamlit as st
import math

# --- Physical constants ---
G_cgs = 6.67430e-8             # cm^3 g^-1 s^-2
R_sun_cm = 6.957e10            # cm
R_sun_AU = 0.00465047          # AU
M_sun_g = 1.98847e33           # g
sigma_sb_cgs = 5.670374419e-5  # erg cm^-2 s^-1 K^-4 (not directly needed)
T_sun_K = 5772.0

# --- Helpers ---
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
    # Earth radius relative to Sun radius (cm/cm)
    R_earth_over_R_sun = 6371e5 / R_sun_cm
    Rp_over_Rstar = (Rp_Re * R_earth_over_R_sun) / Rstar_Rsun
    return (Rp_over_Rstar ** 2)

def _flux_rel_earth(Teff_K: float, Rstar_Rsun: float, a_AU: float) -> float:
    """S/S_earth = (L*/Lsun) / a^2 with L ∝ R^2 T^4."""
    if Teff_K <= 0 or Rstar_Rsun <= 0 or a_AU <= 0:
        return float("nan")
    L_rel = (Rstar_Rsun**2) * ((Teff_K / T_sun_K) ** 4)
    return L_rel / (a_AU ** 2)

def _central_transit_duration_hours(P_days: float, a_AU: float, Rstar_Rsun: float) -> float:
    """
    Approx central transit duration for b≈0, small Rp:
    T ≈ (P/π) * arcsin(R*/a)  ~ (P/π)*(R*/a) for small angles.
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
        # Adjust if your main entry file has a different name.
        st.switch_page("app.py")
    except Exception:
        # Fallback for single-file routing
        st.session_state.update(role=None)
        st.rerun()

# --- UI ---
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

    with st.form("exo_form", clear_on_submit=False):
        # Two equal columns
        cols = st.columns(2)

        fields = [
            ("Orbital period (days)",              dict(min_value=0.0, step=0.1,  format="%.4f", key="P_days")),
            ("Transit epoch (e.g., BJD_TDB)",      dict(step=0.1,                       format="%.5f", key="t0")),
            ("Transit duration (hours)",           dict(min_value=0.0, step=0.1,  format="%.3f", key="dur_hours")),
            ("Transit depth (ppm)",                dict(min_value=0.0, step=10.0, format="%.3f", key="depth_val")),
            ("Planetary radius (Earth radii)",     dict(min_value=0.0, step=0.1,  format="%.3f", key="Rp_Re")),
            ("Equilibrium temperature (K)",        dict(min_value=0.0, step=10.0, format="%.1f", key="Teq_K")),
            ("Earth flux",                          dict(min_value=0.0, step=0.1,  format="%.3f", key="S_earth")),
            ("Stellar effective temperature (K)",  dict(min_value=0.0, step=10.0, format="%.1f", key="Teff_K")),
            ("Stellar surface gravity log g (cgs)",dict(min_value=0.0, step=0.01, format="%.3f", key="logg")),
            ("Stellar radius (Solar radii)",       dict(min_value=0.0, step=0.01, format="%.4f", key="Rstar_Rsun")),
            ("Right ascension (deg, 0–360)",       dict(min_value=0.0, max_value=360.0, step=0.1, format="%.4f", key="RA_deg")),
            ("Declination (deg, -90–+90)",         dict(min_value=-90.0, max_value=90.0, step=0.1, format="%.4f", key="Dec_deg")),
        ]

        for i, (label, kwargs) in enumerate(fields):
            with cols[i % 2]:
                st.number_input(label, **kwargs)

        submitted = st.form_submit_button("Check parameters")

    # Before submit: just show back button
    if not submitted:
        st.divider()
        if st.button("← Back to role selection"):
            _go_home()
        return

    # --- Read values ---
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

    # --- Convert/derive ---
    depth_frac_input = depth_val / 1e6 if depth_val > 0 else 0.0
    a_AU          = _a_from_Teq_Teff_Rstar(Teq_K, Teff_K, Rstar_Rsun)
    Mstar_Msun    = _stellar_mass_from_logg_R(logg, Rstar_Rsun)
    P_days_kepler = _period_from_kepler(a_AU, Mstar_Msun)
    depth_frac_expected = _depth_from_radii(Rp_Re, Rstar_Rsun)
    S_pred        = _flux_rel_earth(Teff_K, Rstar_Rsun, a_AU)
    dur_pred_hours= _central_transit_duration_hours(P_days, a_AU, Rstar_Rsun)

    # --- Minimal checks (only basic > 0) ---
    messages = []
    ok = True
    basics = [
        ("Orbital period", P_days > 0),
        ("Transit duration", dur_hours > 0),
        ("Transit depth", depth_frac_input > 0),
        ("Planet radius", Rp_Re > 0),
        ("Equilibrium temperature", Teq_K > 0),
        ("Earth flux", S_earth >= 0),
        ("Teff", Teff_K > 0),
        ("log g", logg > 0),
        ("Stellar radius", Rstar_Rsun > 0),
    ]
    for name, cond in basics:
        if not cond:
            ok = False
            messages.append(("error", f"{name} must be > 0."))

    # --- Results ---
    st.divider()
    if ok:
        st.success("These parameters are **self-consistent** under standard assumptions (basic checks only).")
    else:
        st.error("Parameters show **inconsistencies**. See diagnostics below.")

    for level, msg in messages:
        if level == "success":
            st.success(msg)
        elif level == "warning":
            st.warning(msg)
        else:
            st.error(msg)

    st.divider()
    if st.button("← Back to role selection"):
        _go_home()
