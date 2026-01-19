import streamlit as st
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="⚡ Ultimate Electrical Hub", layout="wide")
st.title("⚡ Ultimate Offline Electrical Hub App (AC/DC + Wiring + Advanced Calculators)")

# Sidebar menu
st.sidebar.title("⚡ Electrical Hub Menu")
menu = st.sidebar.radio("Select Calculator:", [
    "Resistor Calculator",
    "Ohm's Law Calculator",
    "Light Bill Calculator",
    "Solar Designer",
    "Pump Estimator",
    "Home Wiring & MCB",
    "Voltage Drop Calculator",
    "Battery Backup Calculator",
    "Motor / Transformer Sizing",
    "Troubleshooting Guide"
])

# -------------------------
# 1️⃣ Resistor Calculator
# -------------------------
if menu == "Resistor Calculator":
    st.subheader("🌈 Resistor Calculator")
    colors = {"black":0,"brown":1,"red":2,"orange":3,"yellow":4,"green":5,"blue":6,"violet":7,"grey":8,"white":9}
    b1 = st.selectbox("Band 1", list(colors.keys()), key="res_b1")
    b2 = st.selectbox("Band 2", list(colors.keys()), key="res_b2")
    b3 = st.selectbox("Multiplier Band", list(colors.keys()), key="res_b3")
    tolerance = st.selectbox("Tolerance (%)", ["±1","±2","±5","±10"], key="res_tol")
    if st.button("Calculate Resistance", key="res_btn"):
        val = (colors[b1]*10 + colors[b2]) * (10**colors[b3])
        if val >= 1e6:
            st.success(f"Resistance = {val/1e6:.2f} MΩ {tolerance}")
        elif val >= 1e3:
            st.success(f"Resistance = {val/1e3:.2f} kΩ {tolerance}")
        else:
            st.success(f"Resistance = {val:.2f} Ω {tolerance}")

# -------------------------
# 2️⃣ Ohm's Law Calculator
# -------------------------
elif menu == "Ohm's Law Calculator":
    st.subheader("🔢 Ohm's Law Calculator (DC / AC)")
    mode = st.radio("Select Mode:", ["DC", "AC Single Phase", "AC Three Phase"], key="acdc_mode")
    st.write("Input at least two known values:")

    v = st.number_input("Voltage (V)", min_value=0.0, key="ohm_v")
    i = st.number_input("Current (A)", min_value=0.0, key="ohm_i")
    r = st.number_input("Resistance (Ω)", min_value=0.0, key="ohm_r")
    p = st.number_input("Power (W)", min_value=0.0, key="ohm_p")
    pf = 1.0
    if "AC" in mode:
        pf = st.number_input("Power Factor (0-1)", 0.0, 1.0, 1.0, 0.01, key="pf")

    if st.button("Calculate Ohm's Law", key="ohm_btn"):
        try:
            if mode == "DC":
                if v>0 and i>0: r, p = v/i, v*i
                elif v>0 and r>0: i, p = v/r, (v**2)/r
                elif i>0 and r>0: v, p = i*r, (i**2)*r
                elif p>0 and v>0: i, r = p/v, (v**2)/p
                elif p>0 and i>0: v, r = p/i, p/(i**2)
                st.success(f"DC → V={v:.2f} V, I={i:.4f} A, R={r:.2f} Ω, P={p:.2f} W")
            elif mode == "AC Single Phase":
                if v>0 and i>0: p = v*i*pf; r = v/i
                st.success(f"AC Single Phase → V={v:.2f} V, I={i:.4f} A, R={r:.2f} Ω, Real Power={p:.2f} W, PF={pf}")
            elif mode == "AC Three Phase":
                if v>0 and i>0: p = math.sqrt(3)*v*i*pf; r = v/i
                st.success(f"AC Three Phase → V={v:.2f} V, I={i:.4f} A, R={r:.2f} Ω, Real Power={p:.2f} W, PF={pf}")
            
            # Voltage vs Current graph
            if v>0 and i>0:
                currents = [i*x/10 for x in range(1,11)]
                voltages = [r*curr for curr in currents]
                plt.figure(figsize=(4,3))
                plt.plot(currents, voltages, marker='o')
                plt.xlabel("Current (A)")
                plt.ylabel("Voltage (V)")
                plt.title("Voltage vs Current")
                st.pyplot(plt)
        except:
            st.error("काही चुकलं आहे, दोन values द्या")

# -------------------------
# 3️⃣ Light Bill Calculator
# -------------------------
elif menu == "Light Bill Calculator":
    st.subheader("💡 Light Bill Calculator")
    load = st.number_input("Load (Watts)", 1000, key="light_load")
    hours = st.slider("Hours per day", 1, 24, 6, key="light_hours")
    rate = st.number_input("Rate per Unit (₹)", 7.0, key="light_rate")
    if st.button("Calculate Bill", key="light_btn"):
        units = (load*hours*30)/1000
        st.success(f"Estimated Monthly Bill = ₹{units*rate:.2f}")

# -------------------------
# 4️⃣ Solar System Designer
# -------------------------
elif menu == "Solar Designer":
    st.subheader("☀️ Solar System Designer")
    total_load = st.number_input("Total Load (W)", 2000, key="solar_load")
    backup_hours = st.number_input("Backup Hours", 5, key="solar_backup")
    panel_watt = st.number_input("Panel Wattage (W)", 300, key="solar_panel")
    battery_watt = st.number_input("Battery Capacity (Wh)", 2000, key="solar_battery")
    if st.button("Estimate Solar System", key="solar_btn"):
        panels = math.ceil(total_load/panel_watt)
        batteries = math.ceil((total_load*backup_hours)/battery_watt)
        st.success(f"Panels ≈ {panels}, Batteries ≈ {batteries}")

# -------------------------
# 5️⃣ Pump Estimator
# -------------------------
elif menu == "Pump Estimator":
    st.subheader("🏗️ Pump Estimator")
    depth = st.number_input("Well Depth (ft)", 100, key="pump_depth")
    flow = st.number_input("Required Flow (L/min)", 50, key="pump_flow")
    if st.button("Estimate Pump HP", key="pump_btn"):
        hp = 1 if depth<100 else 2 if depth<200 else 5
        hp *= flow/50
        st.success(f"Pump Required ≈ {math.ceil(hp)} HP")

# -------------------------
# 6️⃣ Home Wiring & MCB Calculator
# -------------------------
elif menu == "Home Wiring & MCB":
    st.subheader("⚡ Home Wiring & MCB Calculator")
    appliance_watt = st.number_input("Appliance Wattage (W)", 1000, key="mcb_watt")
    supply_voltage = st.number_input("Supply Voltage (V)", 230, key="mcb_voltage")
    num_wires = st.number_input("Number of Wires", 1, 3, key="mcb_wires")
    if st.button("Calculate MCB & Wire", key="mcb_btn"):
        current = appliance_watt / supply_voltage
        mcb_rating = math.ceil(current * 1.25)
        wire_size = 1.5 if current <= 10 else 2.5 if current <= 20 else 4
        st.success(f"Estimated Current = {current:.2f} A\nRecommended MCB = {mcb_rating} A\nSuggested Wire Size = {wire_size} mm²")

# -------------------------
# 7️⃣ Voltage Drop Calculator
# -------------------------
elif menu == "Voltage Drop Calculator":
    st.subheader("📉 Voltage Drop Calculator")
    length = st.number_input("Wire Length (m)", 10, key="vd_length")
    vd_current = st.number_input("Current (A)", 5, key="vd_current")
    vd_voltage = st.number_input("Voltage (V)", 230, key="vd_voltage")
    resistivity = 0.017  # ohm mm²/m for copper
    area = st.number_input("Wire Area (mm²)", 1.5, key="vd_area")
    if st.button("Calculate Voltage Drop", key="vd_btn"):
        drop = (resistivity*length*vd_current)/area
        percent_drop = (drop/vd_voltage)*100
        st.success(f"Voltage Drop = {drop:.2f} V ({percent_drop:.2f}%)")

# -------------------------
# 8️⃣ Battery Backup Calculator
# -------------------------
elif menu == "Battery Backup Calculator":
    st.subheader("🔋 Battery Backup Calculator")
    battery_capacity = st.number_input("Battery Capacity (Wh)", 2000, key="bat_capacity")
    load = st.number_input("Load (W)", 500, key="bat_load")
    if st.button("Calculate Backup Time", key="bat_btn"):
        backup_time = battery_capacity / load
        st.success(f"Approx Backup Time = {backup_time:.2f} hours")

# -------------------------
# 9️⃣ Motor / Transformer Sizing
# -------------------------
elif menu == "Motor / Transformer Sizing":
    st.subheader("⚙️ Motor / Transformer Sizing")
    load_kw = st.number_input("Load (kW)", 5, key="mt_load")
    efficiency = st.number_input("Efficiency (%)", 80, key="mt_eff")/100
    if st.button("Estimate Motor / Transformer", key="mt_btn"):
        kva = load_kw / efficiency
        st.success(f"Approx Transformer / Motor Rating = {kva:.2f} kVA")

# -------------------------
# 🔟 Troubleshooting Guide
# -------------------------
elif menu == "Troubleshooting Guide":
    st.subheader("🛠️ Electrical Troubleshooting Guide")
    st.write("""
- Motor not starting → Check Supply, MCB, Capacitor  
- Overheating → Check Load & Wiring  
- Flickering lights → Check connections & voltage  
- Fuse blowing → Check Short circuits
""")