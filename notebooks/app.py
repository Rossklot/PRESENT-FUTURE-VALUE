import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(page_title="FIRE & Coast FIRE Tracker", page_icon="🔥", layout="wide")

st.title("🔥 Advanced Financial Independence (FIRE) Dashboard")
st.markdown("Model your timeline to complete financial freedom or find your **Coast FIRE** milestone.")

# --- Sidebar Inputs ---
st.sidebar.header("👤 Personal Profile")
current_age = st.sidebar.number_input("Current Age", value=30, step=1)
target_retirement_age = st.sidebar.number_input("Traditional Retirement Age (For Coast calculation)", value=65, step=1)

st.sidebar.header("💰 Financial Metrics")
current_net_worth = st.sidebar.number_input("Current Net Worth ($)", value=25000, step=5000)
annual_income = st.sidebar.number_input("Annual Income (After Tax) ($)", value=90000, step=5000)
annual_expenses = st.sidebar.number_input("Annual Expenses ($)", value=45000, step=2000)

st.sidebar.header("📈 Market Assumptions")
expected_return_rate = st.sidebar.slider("Expected Annual Return (Inflation Adjusted %)", 1.0, 12.0, 7.0, 0.5) / 100

st.caption("🔒 Privacy Note: This app runs entirely in your browser session. No personal financial data is collected, stored, or transmitted.")
# --- Coast FIRE Toggle ---
st.sidebar.header("⚙️ Feature Toggles")
enable_coast = st.sidebar.toggle("Calculate Coast FIRE?", value=True)

# --- Core Calculations ---
fire_target = annual_expenses * 25
monthly_savings = (annual_income - annual_expenses) / 12
monthly_return_rate = expected_return_rate / 12
years_to_retire = max(0, target_retirement_age - current_age)

# Calculate Coast FIRE Target if enabled
if enable_coast:
    # Formula: Coast Target = FIRE Target / (1 + r)^years_left
    coast_fire_target = fire_target / ((1 + expected_return_rate) ** years_to_retire)
else:
    coast_fire_target = 0

# --- Validation & Accumulation Loop ---
if monthly_savings <= 0:
    st.error("⚠️ Your expenses exceed or equal your income. You cannot reach financial goals without a positive savings rate!")
else:
    balance = current_net_worth
    months = 0
    coast_hit_age = None
    full_fire_hit_age = None
    data_log = []

    # Run loop up to 50 years (600 months)
while months <= 600:
        age_at_step = current_age + (months / 12)
        
        # Log data point
        row = {
            "Age": round(age_at_step, 2),
            "Net Worth": round(balance, 2),
            "Full FIRE Target": fire_target
        }
        if enable_coast:
            row["Coast FIRE Target"] = round(coast_fire_target, 2)
        data_log.append(row)
        
        # Check milestones
        if enable_coast and balance >= coast_fire_target and coast_hit_age is None:
            coast_hit_age = age_at_step
        if balance >= fire_target and full_fire_hit_age is None:
            full_fire_hit_age = age_at_step
            # If we don't care about looking past full FIRE, we could break, 
            # but continuing lets us see the trajectory up to the max window.
            
        # Standard monthly accumulation
        months += 1
        interest_earned = balance * monthly_return_rate
        balance = balance + interest_earned + monthly_savings

df_timeline = pd.DataFrame(data_log) 
savings_rate = (annual_income - annual_expenses) / annual_income * 100

# --- KPI Dashboard Metrics ---
metrics_cols = st.columns(4 if enable_coast else 3)
with metrics_cols[0]: 
    st.metric("Full FIRE Target", f"${fire_target:,.0f}")
with metrics_cols[1]:
        age_str = f"Age {full_fire_hit_age:.1f}" if full_fire_hit_age else "50+ Years Out"
        st.metric("Age to Full FIRE", age_str)
        
if enable_coast:
        with metrics_cols[2]:
            st.metric("Coast FIRE Target", f"${coast_fire_target:,.0f}")
        with metrics_cols[3]:
            # If current NW already exceeds Coast target
            if current_net_worth >= coast_fire_target:
                age_str_coast = "🎉 Achieved!"
            else:
                age_str_coast = f"Age {coast_hit_age:.1f}" if coast_hit_age else "50+ Years Out"
            st.metric("Age to Coast FIRE", age_str_coast)
else:
        with metrics_cols[2]:
            st.metric("Savings Rate", f"{savings_rate:.1f}%")
            st.markdown("---")

    # --- Explanatory Callout for Coast FIRE ---
if enable_coast and current_net_worth < coast_fire_target:
        st.markdown(f"""
**What this means:** Once you reach your Coast FIRE target, you can completely stop saving for retirement. 
If you choose to touch nothing and let your current net worth grow at your expected market return rate, 
your nest egg will compound to your full FIRE target by the time you reach your traditional retirement age.
""")
elif enable_coast and current_net_worth >= coast_fire_target:
        st.balloons()
        st.success(f"🌟 **You have already coasted!** Your current net worth is compounding fast enough to hit your target by age {target_retirement_age} without you saving another dollar.")

    # --- Visual Chart ---
st.subheader("📈 Projection Timeline vs Targets")
    
y_lines = ["Net Worth", "Full FIRE Target"]
color_map = {"Net Worth": "#1f77b4", "Full FIRE Target": "#ff7f0e"}
    
if enable_coast:
        y_lines.append("Coast FIRE Target")
        color_map["Coast FIRE Target"] = "#2ca02c"

fig = px.line(
        df_timeline, 
        x="Age", 
        y=y_lines,
        labels={"value": "Amount ($)", "variable": "Financial Lines"},
        color_discrete_map=color_map
    )
    
fig.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
st.plotly_chart(fig, width='stretch')

# Create a beautiful visual block for the milestone message 
if current_net_worth >= coast_fire_target:
    st.balloons()
    st.success(f"🎉 **Coast FIRE Status:** You have already achieved Coast FIRE! Your current net worth of **${current_net_worth:,.0f}** is greater than your target.")
else:
    st.info(f"💡 **What this means:** Once you reach **${coast_fire_target:,.0f}**, you can stop saving entirely. If you just touch nothing and let it grow at **{expected_return_rate * 100:.1f}%**, compound interest will carry it to **${fire_target:,.0f}** by the time you turn **{target_retirement_age}**.")
