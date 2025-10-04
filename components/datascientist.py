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

def show_datascientist_view():
    st.markdown(
        "<h2 style='color:white; text-align:center;'>Exoplanet Check</h2>",
        unsafe_allow_html=True,
    )

    # st.info("Here you can test whether the entered parameters correspond to a potential exoplanet, as evaluated by our AI/ML model.")
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
        # Două coloane egale
        cols = st.columns(2)

        # Definim câmpurile numeric (label, kwargs) EXACT ca în codul tău
        fields = [
            ("Orbital period (days)",         dict(min_value=0.0, step=0.1, format="%.4f", key="P_days")),
            ("Transit epoch (e.g., BJD_TDB)", dict(step=0.1, format="%.5f", key="t0")),
            ("Transit duration (hours)",      dict(min_value=0.0, step=0.1, format="%.3f", key="dur_hours")),
            ("Transit depth (ppm)",           dict(min_value=0.0, step=10.0, format="%.3f", key="depth_val")),
            ("Planetary radius (Earth radii)",dict(min_value=0.0, step=0.1, format="%.3f", key="Rp_Re")),
            ("Equilibrium temperature (K)",   dict(min_value=0.0, step=10.0, format="%.1f", key="Teq_K")),
            ("Earth flux",                    dict(min_value=0.0, step=0.1, format="%.3f", key="S_earth")),
            ("Stellar effective temperature (K)", dict(min_value=0.0, step=10.0, format="%.1f", key="Teff_K")),
            ("Stellar surface gravity log g (cgs)", dict(min_value=0.0, step=0.01, format="%.3f", key="logg")),
            ("Stellar radius (Solar radii)",  dict(min_value=0.0, step=0.01, format="%.4f", key="Rstar_Rsun")),
            ("Right ascension (deg, 0–360)",  dict(min_value=0.0, max_value=360.0, step=0.1, format="%.4f", key="RA_deg")),
            ("Declination (deg, -90–+90)",    dict(min_value=-90.0, max_value=90.0, step=0.1, format="%.4f", key="Dec_deg")),
        ]

        # Randează alternativ stânga/dreapta pentru distribuție egală
        for i, (label, kwargs) in enumerate(fields):
            with cols[i % 2]:
                st.number_input(label, **kwargs)

        submitted = st.form_submit_button("Check parameters")

    # Dacă nu a fost apăsat Submit, afișăm mesaj + buton Back
    if not submitted:
        st.divider()
        if st.button("← Back to role selection"):
            st.session_state.update(role=None)
            st.rerun()
        return

    # --- Preluare valori din state (cheile definite în number_input) ---
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

    # Derived a (AU) from Teq, Teff, Rstar (A=0, full redistribution)
    a_AU = _a_from_Teq_Teff_Rstar(Teq_K, Teff_K, Rstar_Rsun)
    Mstar_Msun = _stellar_mass_from_logg_R(logg, Rstar_Rsun)
    P_days_kepler = _period_from_kepler(a_AU, Mstar_Msun)
    depth_frac_expected = _depth_from_radii(Rp_Re, Rstar_Rsun)
    S_pred = _flux_rel_earth(Teff_K, Rstar_Rsun, a_AU)
    dur_pred_hours = _central_transit_duration_hours(P_days, a_AU, Rstar_Rsun)

    # --- Checks ---
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

    if not (0.1 <= Rp_Re <= 25):
        messages.append(("warning", "Planetary radius is outside a typical range (~0.1–25 R⊕)."))
    if not (3.5 <= logg <= 5.0):
        messages.append(("warning", "Stellar log g is unusual for main-sequence/giant stars (3.5–5.0 typical)."))
    if not (0.1 <= Rstar_Rsun <= 50):
        messages.append(("warning", "Stellar radius outside broad typical range (0.1–50 R☉)."))
    if not (0 <= RA_deg <= 360):
        ok = False
        messages.append(("error", "RA must be in [0, 360] degrees."))
    if not (-90 <= Dec_deg <= 90):
        ok = False
        messages.append(("error", "Dec must be in [-90, +90] degrees."))

    if ok:
        if math.isfinite(P_days_kepler):
            kepler_err = _rel_err(P_days, P_days_kepler)
            if kepler_err < 0.1:
                messages.append(("success", f"Kepler consistency ✅ Period matches Teq/Teff/logg/R★ (err ~ {kepler_err*100:.1f}%)."))
            elif kepler_err < 0.25:
                messages.append(("warning", f"Kepler consistency ⚠️ Roughly consistent (err ~ {kepler_err*100:.1f}%). Recheck assumptions/units."))
            else:
                messages.append(("error", f"Kepler consistency ❌ Large mismatch (err ~ {kepler_err*100:.1f}%)."))
                ok = False
        else:
            messages.append(("error", "Unable to compute Kepler period—check Teq, Teff, log g, and R★."))
            ok = False

        if math.isfinite(depth_frac_expected) and math.isfinite(depth_frac_input) and depth_frac_input > 0:
            depth_err = _rel_err(depth_frac_input, depth_frac_expected)
            if depth_err < 0.2:
                messages.append(("success", f"Transit depth ✅ Consistent with radii (err ~ {depth_err*100:.1f}%)."))
            elif depth_err < 0.5:
                messages.append(("warning", f"Transit depth ⚠️ Somewhat off (err ~ {depth_err*100:.1f}%)."))
            else:
                messages.append(("error", f"Transit depth ❌ Inconsistent with radii (err ~ {depth_err*100:.1f}%)."))
        else:
            messages.append(("warning", "Could not assess transit depth consistency (check inputs)."))

        if math.isfinite(S_pred) and S_earth >= 0:
            flux_err = _rel_err(S_earth, S_pred) if S_pred > 0 else float("inf")
            if flux_err < 0.2:
                messages.append(("success", f"Irradiance S/S⊕ ✅ Consistent (err ~ {flux_err*100:.1f}%)."))
            elif flux_err < 0.5:
                messages.append(("warning", f"Irradiance S/S⊕ ⚠️ Somewhat off (err ~ {flux_err*100:.1f}%)."))
            else:
                messages.append(("error", f"Irradiance S/S⊕ ❌ Inconsistent (err ~ {flux_err*100:.1f}%)."))
        else:
            messages.append(("warning", "Could not evaluate irradiance consistency."))

        if math.isfinite(dur_pred_hours):
            dur_err = _rel_err(dur_hours, dur_pred_hours)
            if dur_err < 0.3:
                messages.append(("success", f"Transit duration ✅ Reasonable for central transit (err ~ {dur_err*100:.1f}%)."))
            else:
                messages.append(("warning", f"Transit duration ⚠️ Off for central-transit assumption (err ~ {dur_err*100:.1f}%). "
                                            "High impact parameter or eccentricity could explain this."))
        else:
            messages.append(("warning", "Could not estimate transit duration."))

    # --- Results ---
    st.divider()
    if ok:
        st.success("These parameters are **self-consistent** under standard assumptions (see notes below).")
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
        st.session_state.update(role=None)
        st.rerun()
