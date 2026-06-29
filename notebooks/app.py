import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="FIRE & Coast FIRE Tracker", layout="centered")

st.title("🔥 FIRE & Coast FIRE Tracker")

# Sidebar inputs
st.sidebar.header("Your Financial Details")
current_age = st.sidebar.slider("Current Age", 18, 80, 30)
retirement_age = st.sidebar.slider("Target Retirement Age", 18, 80, 60)
current_net_worth = st.sidebar.number_input("Current Net Worth ($)", min_value=0.0, value=50000.0, step=5000.0, max_value=1000000000.0)
annual_expenses = st.sidebar.number_input("Future Annual Expenses ($)", min_value=0.0, value=40000.0, step=2000.0, max_value=1000000000.0)
expected_return = st.sidebar.slider("Expected Market Return (%)", 1.0, 15.0, 7.0)

# Calculations
fire_target = annual_expenses * 25
years_to_retire = max(0, retirement_age - current_age)
coast_fire_target = fire_target / ((1 + (expected_return / 100)) ** years_to_retire)

# Display Metrics
col1, col2 = st.columns(2)
with col1:
    st.metric("Full FIRE Target", f"${fire_target:,.0f}")
with col2:
    st.metric("Coast FIRE Target", f"${coast_fire_target:,.0f}")

# Main Text Explanation
st.markdown(f"""
**What this means:** Once you reach your Coast FIRE target, you can completely stop saving for retirement. 
If you choose to touch nothing and let your current net worth grow at your expected market return rate, 
your nest egg will compound to your full FIRE target by the time you reach your traditional retirement age.
""")

# Simple projection chart data
ages = list(range(current_age, retirement_age + 1))
if ages:
    balances = [current_net_worth * ((1 + (expected_return / 100)) ** (age - current_age)) for age in ages]
    df = pd.DataFrame({"Age": ages, "Net Worth": balances})
    fig = px.line(df, x="Age", y="Net Worth", title="Net Worth Growth Projection")
    fig.update_layout(yaxis=dict(tickformat="$,"))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info(f"💡 **What this means:** Once you reach **${coast_fire_target:,.0f}**, you can stop saving entirely. If you just touch nothing and let it grow at **{expected_return_rate * 100:.1f}%**, compound interest will carry it to **${fire_target:,.0f}** by the time you turn **{target_retirement_age}**.")
