import pandas as pd
import matplotlib.pyplot as plt

# Load tickets
df = pd.read_csv(r'D:\Research\Topics\Future Interns\FUTURE_ML_03\data\raw\customer_support_tickets.csv')

# 1. Ticket‐type distribution
counts = df['Ticket Type'].value_counts()
pct = (counts / counts.sum() * 100).round(1)
print("▶ Ticket Type distribution (%):")
print(pct)

# 2. Bar chart of top 10
counts.head(10).plot(kind='bar', title='Top 10 Ticket Types')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

# 3. Resolution time (in hours)
df['First Response Time'] = pd.to_datetime(df['First Response Time'])
df['Time to Resolution'] = pd.to_datetime(df['Time to Resolution'])
df['Resolution Hours'] = (
    df['Time to Resolution'] - df['First Response Time']
).dt.total_seconds() / 3600
print(f"▶ Avg. resolution time: {df['Resolution Hours'].mean():.1f} hours")

# 4. Customer satisfaction
print(f"▶ Avg. satisfaction rating: {df['Customer Satisfaction Rating'].mean():.2f}")
