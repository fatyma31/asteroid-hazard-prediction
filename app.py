
import streamlit as st
import joblib
import numpy as np

st.set_page_config(page_title="Asteroid Predictor", page_icon="🪐")
model = joblib.load('asteroid_model.pkl')

st.title("🪐 Asteroid Hazard Predictor")
st.markdown("### Is this asteroid dangerous for Earth?")
st.divider()

col1, col2 = st.columns(2)
with col1:
    moid = st.number_input("MOID - Earth distance (AU)", 0.0, 100.0, 0.05, format="%.4f")
    H    = st.number_input("H - Magnitude (brightness)",  0.0,  35.0, 18.0)
    e    = st.number_input("e - Eccentricity",            0.0,   2.0,  0.5)
    q    = st.number_input("q - Perihelion (AU)",         0.0,  10.0,  0.8)
    a    = st.number_input("a - Semi-major axis (AU)",    0.0, 100.0,  1.5)
    om   = st.number_input("om - Ascending node",         0.0, 360.0,100.0)
    i    = st.number_input("i - Inclination (deg)",       0.0, 180.0, 10.0)

with col2:
    w            = st.number_input("w - Arg of perihelion",    0.0, 360.0, 200.0)
    ma           = st.number_input("ma - Mean anomaly",        0.0, 360.0, 150.0)
    n            = st.number_input("n - Mean motion",          0.0,  10.0,   0.5)
    ad           = st.number_input("ad - Aphelion (AU)",       0.0, 200.0,   3.0)
    per_y        = st.number_input("per_y - Period (years)",   0.0,1000.0,   2.0)
    has_diameter = st.selectbox("Diameter known?", [0,1],
                                format_func=lambda x: "Yes" if x==1 else "No")

st.divider()
if st.button("🔍 Predict!", use_container_width=True, type="primary"):
    X = np.array([[e, a, q, i, om, w, ma, n, ad, per_y, moid, H, has_diameter]])
    pred  = model.predict(X)[0]
    proba = model.predict_proba(X)[0]

    if pred == 1:
        st.error(f"## ☠️ DANGEROUS!  Danger: {proba[1]*100:.2f}%")
    else:
        st.success(f"## ✅ SAFE!  Safe: {proba[0]*100:.2f}%")

    st.progress(int(proba[1]*100))
    if moid < 0.05:
        st.warning("⚠️ MOID < 0.05 AU — meets NASA PHA definition!")