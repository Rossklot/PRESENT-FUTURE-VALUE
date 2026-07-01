import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="FIRE & Coast FIRE Tracker", layout="centered")

# --- 1. THE WELCOME INTRO ---
st.title("🔥 FIRE & Coast FIRE Tracker")
st.markdown("""
Welcome! **FIRE** (Financial Independence, Retire Early) is the milestone where your investments can fund your lifestyle forever. 
**Coast FIRE** is the tipping point where your *current* savings are enough to grow to your full FIRE goal by retirement age—meaning you can officially stop saving and just cover your current expenses.

Use the tool below to instantly map out your personalized financial freedom timeline.
""")

st.divider()

# --- 2. MAIN SCREEN INPUTS ---
st.subheader("📊 1. Enter Your Financial Details")

# Splitting inputs into clean columns on the main screen
col_left, col_right = st.columns(2)

with col_left:
    current_age = st.slider("Your Current Age", 18, 80, 30)
    retirement_age = st.slider("Target Retirement Age", 18, 80, 60)
    expected_return = st.slider("Expected Annual Market Return (%)", 1.0, 15.0, 7.0)

with col_right:
    current_net_worth = st.number_input("Current Savings / Net Worth ($)", min_value=0.0, value=50000.0, step=5000.0, max_value=1000000000.0)
    annual_expenses = st.number_input("Estimated Future Annual Expenses ($)", min_value=0.0, value=40000.0, step=2000.0, max_value=1000000000.0)

st.divider()

# --- CALCULATIONS ---
fire_target = annual_expenses * 25
years_to_retire = max(0, retirement_age - current_age)
coast_fire_target = fire_target / ((1 + (expected_return / 100)) ** years_to_retire)

# --- 3. DISPLAY TARGETS ---
st.subheader("🎯 2. Your Freedom Milestones")
metric_col1, metric_col2 = st.columns(2)
with metric_col1:
    st.metric("Full FIRE Target (25x Expenses)", f"${fire_target:,.0f}")
with metric_col2:
    st.metric("Coast FIRE Target", f"${coast_fire_target:,.0f}")

st.markdown(f"""
👉 **What this tells you:** Once your net worth hits **${coast_fire_target:,.0f}**, you have down-shifted your retirement stress to zero. 
Even if you never add another dollar to your savings, your nest egg is projected to compound into your full **${fire_target:,.0f}** goal by the time you hit **{retirement_age}**.
""")

st.divider()

# --- 4. GRAPH PROJECTION ---
st.subheader("📈 3. Your Growth Timeline")

ages = list(range(current_age, retirement_age + 1))
if ages:
    balances = [current_net_worth * ((1 + (expected_return / 100)) ** (age - current_age)) for age in ages]
    df = pd.DataFrame({"Age": ages, "Projected Net Worth": balances})
    
    fig = px.line(df, x="Age", y="Projected Net Worth", title="How Your Savings Will Grow (Assuming No New Contributions)")
    fig.update_layout(yaxis=dict(tickformat="$,"))
    
    # This config line hides the messy chart options until the user hovers, keeping it clean
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': 'hover'})
