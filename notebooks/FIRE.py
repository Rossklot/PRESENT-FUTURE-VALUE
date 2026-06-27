import pandas as pd

def calculate_fire_timeline(current_net_worth, annual_income, annual_expenses, expected_return_rate):
    """
    Calculates the month-by-month path to Financial Independence.
    Assumes an annual investment return rate (adjusted for inflation, typically 6-8%).
    """
    # 1. Calculate Core FIRE Metrics
    fire_target = annual_expenses * 25
    monthly_savings = (annual_income - annual_expenses) / 12
    monthly_return_rate = expected_return_rate / 12
    
    if monthly_savings <= 0:
        return "Your expenses exceed or equal your income. You cannot reach FIRE without saving!", None

    # 2. Accumulation Loop
    balance = current_net_worth
    months = 0
    data_log = []
    
    # Record baseline
    data_log.append({"Month": months, "Net Worth": balance, "Target": fire_target})
    
    # Run the accumulator until the target is hit (capped at 50 years to prevent infinite loops)
    while balance < fire_target and months < 600:
        months += 1
        interest_earned = balance * monthly_return_rate
        balance = balance + interest_earned + monthly_savings
        
        data_log.append({
            "Month": months, 
            "Net Worth": round(balance, 2), 
            "Target": fire_target
        })
        
    df_timeline = pd.DataFrame(data_log)
    return fire_target, df_timeline

# --- Example Usage ---
income = 90000
expenses = 45000
starting_net_worth = 10000
market_return = 0.07 # 7% average annual return adjusted for inflation

target, timeline_df = calculate_fire_timeline(starting_net_worth, income, expenses, market_return)

if isinstance(target, str):
    print(target)
else:
    years_to_fire = timeline_df["Month"].max() / 12
    print(f"Target FIRE Number: ${target:,.2f}")
    print(f"Time required to reach freedom: {years_to_fire:.1f} years")
    print("\nFirst few months of accumulation:")
    print(timeline_df.head(12))