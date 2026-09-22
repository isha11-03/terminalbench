"""
Deterministic synthetic time-series data generator for demand forecasting.

Generates realistic daily demand data with:
- Weekly seasonality (higher demand on weekends)
- Price elasticity (demand inversely related to price)
- Promotion effects (demand boost during promotions)
- Trend component (slight upward trend)
- Realistic noise

Fully deterministic with fixed random seed.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def generate_demand_data(
    start_date: str = "2023-01-01",
    n_days: int = 395,  # 365 training + 30 test
    seed: int = 42,
    output_path: str = "demand_data.csv"
) -> pd.DataFrame:
    """
    Generate synthetic demand time-series data.
    
    Args:
        start_date: Start date for time series
        n_days: Number of days to generate
        seed: Random seed for reproducibility
        output_path: Where to save the CSV file
        
    Returns:
        DataFrame with columns: date, demand, price, promotion, day_of_week
    """
    np.random.seed(seed)
    
    # Generate date range
    dates = pd.date_range(start=start_date, periods=n_days, freq='D')
    
    # Day of week (0=Monday, 6=Sunday)
    day_of_week = dates.dayofweek.values
    
    # Base demand level
    base_demand = 100.0
    
    # Trend component (slight upward trend)
    trend = np.linspace(0, 20, n_days)
    
    # Weekly seasonality (higher on weekends)
    # Friday, Saturday, Sunday get boost
    seasonality = np.array([
        1.0 if dow < 4  # Mon-Thu
        else 1.3 if dow == 4  # Fri
        else 1.5 if dow == 5  # Sat
        else 1.4  # Sun
        for dow in day_of_week
    ])
    
    # Generate price (varies slightly around base price)
    base_price = 50.0
    price_noise = np.random.uniform(-5, 5, n_days)
    price = base_price + price_noise
    
    # Generate promotions (15% of days randomly)
    promotion_prob = 0.15
    promotion = np.random.binomial(1, promotion_prob, n_days)
    
    # Price elasticity: -0.5 (1% price increase -> 0.5% demand decrease)
    price_effect = -0.5 * (price - base_price) / base_price
    
    # Promotion effect: +30% demand boost
    promotion_effect = 0.3 * promotion
    
    # Combine all effects
    demand = (
        base_demand
        + trend
        + (base_demand * seasonality - base_demand)  # Seasonality effect
        + (base_demand * price_effect)  # Price elasticity
        + (base_demand * promotion_effect)  # Promotion boost
    )
    
    # Add realistic noise (±5%)
    noise = np.random.normal(0, 0.05 * base_demand, n_days)
    demand = demand + noise
    
    # Ensure demand is non-negative
    demand = np.maximum(demand, 10.0)
    
    # Round demand to integers (units sold)
    demand = np.round(demand).astype(int)
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': dates,
        'demand': demand,
        'price': np.round(price, 2),
        'promotion': promotion,
        'day_of_week': day_of_week
    })
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Generated {n_days} days of demand data")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Demand stats: mean={df['demand'].mean():.1f}, std={df['demand'].std():.1f}")
    print(f"Saved to: {output_path}")
    
    return df


def verify_data_properties(df: pd.DataFrame):
    """Verify the generated data has expected properties."""
    print("\n=== Data Verification ===")
    
    # Check for missing values
    assert df.isnull().sum().sum() == 0, "Data contains missing values"
    print("✓ No missing values")
    
    # Check date continuity
    date_diffs = df['date'].diff().dt.days.dropna()
    assert (date_diffs == 1).all(), "Dates are not continuous"
    print("✓ Dates are continuous")
    
    # Check demand is positive
    assert (df['demand'] > 0).all(), "Demand contains non-positive values"
    print("✓ All demand values are positive")
    
    # Check promotion is binary
    assert set(df['promotion'].unique()).issubset({0, 1}), "Promotion not binary"
    print("✓ Promotion is binary")
    
    # Check day_of_week range
    assert df['day_of_week'].min() >= 0 and df['day_of_week'].max() <= 6
    print("✓ Day of week in valid range")
    
    # Check weekend effect
    weekend_demand = df[df['day_of_week'].isin([5, 6])]['demand'].mean()
    weekday_demand = df[df['day_of_week'].isin([0, 1, 2, 3])]['demand'].mean()
    assert weekend_demand > weekday_demand, "Weekend demand not higher than weekday"
    print(f"✓ Weekend demand ({weekend_demand:.1f}) > Weekday demand ({weekday_demand:.1f})")
    
    # Check promotion effect
    promo_demand = df[df['promotion'] == 1]['demand'].mean()
    no_promo_demand = df[df['promotion'] == 0]['demand'].mean()
    assert promo_demand > no_promo_demand, "Promotion doesn't increase demand"
    print(f"✓ Promotion demand ({promo_demand:.1f}) > No-promotion demand ({no_promo_demand:.1f})")
    
    print("\nAll verifications passed!")


if __name__ == "__main__":
    # Generate the data
    df = generate_demand_data(
        start_date="2023-01-01",
        n_days=395,
        seed=42,
        output_path="demand_data.csv"
    )
    
    # Verify properties
    verify_data_properties(df)
    
    # Show sample
    print("\n=== First 10 rows ===")
    print(df.head(10))
    
    print("\n=== Last 10 rows ===")
    print(df.tail(10))
    
    # Show statistics
    print("\n=== Summary Statistics ===")
    print(df.describe())
