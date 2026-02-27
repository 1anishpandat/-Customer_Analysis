import pandas as pd 
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for VS Code
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] =(12,6)
sns.set_palette('Set2')

print("="*70)
print("PROJECT 2: CUSTOMER SEGMENTATION & TFM ANALYSIS")
print("="*70)
print("LIBRARIES IMPORTED SUCCESSFULLY!")

print("━" * 70)
print("  SECTION 1: DATA LOADING & EXPLORATION")
print("━" * 70)

df = pd.read_excel('data/or.xlsx')

print(f"\n📦 Dataset loaded!")


# ══════════════════════════════════════════════════════════════════
# SECTION 1: DATA LOADING & EXPLORATION
# ══════════════════════════════════════════════════════════════════
print(f"   Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"   Date range: {df['InvoiceDate'].min().date()} to {df['InvoiceDate'].max().date()}")
print(f"   Unique customers: {df['CustomerID'].nunique():,}")

print("\n📋 First 5 rows:")
print(df.head().to_string())

print("\n🔍 Column Info:")
print(df.info())

print("\n📊 Statistical Summary:")
print(df.describe().to_string())

print("\n🔎 Missing Values:")
missing = pd.DataFrame({
    'Missing Count': df.isnull().sum(),
    'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
})
print(missing[missing['Missing Count'] > 0].to_string())

# ══════════════════════════════════════════════════════════════════
# SECTION 2: DATA CLEANING
# ══════════════════════════════════════════════════════════════════
print("\n" + "━" * 70)
print("  SECTION 2: DATA CLEANING")
print("━" * 70)

print(f"\nBefore cleaning: {len(df):,} rows")

df_clean = df.dropna(subset=['CustomerID']).copy()
print(f'after removing missing CustomerID {len(df_clean):,}rows')

df_clean = df_clean[~df_clean['InvoiceNo'].astype(str).str.startswith('C')]
print(f'after removing cancellations : {len(df_clean):,}rows')

df_clean = df_clean[(df_clean['Quantity']>0)&(df_clean['UnitPrice']>0)]
print(f'After removing negative values: {len(df_clean):,}rows')

df_clean['TotalAmount'] = df_clean['Quantity'] * df_clean['UnitPrice']

df_clean['CustomerID'] = df_clean['CustomerID'].astype(int)


print(f'cleaning completed! ')
print(f'final dataset :{len(df_clean):,}rows')
print(f'customers : {df_clean['CustomerID'].nunique():,}')
print(f'total revenue : ${df_clean['TotalAmount'].sum():,.2f}')


print(f" missing values after cleaning: {df_clean.isnull().sum().sum()}")



# ══════════════════════════════════════════════════════════════════
# SECTION 3: EXPLORATORY DATA ANALYSIS (EDA)
# ══════════════════════════════════════════════════════════════════

print("\n" + "━" * 70)
print("  SECTION 3: EXPLORATORY DATA ANALYSIS")
print("━" * 70)

total_revenue = df_clean['TotalAmount'].sum()
total_orders = df_clean['InvoiceNo'].nunique()
total_customers = df_clean['CustomerID'].nunique()
avg_order_value = df_clean.groupby('InvoiceNo')['TotalAmount'].sum().mean()

print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Customers: {total_customers:,}")
print(f"Average Order Value: ${avg_order_value:,.2f}")


#top 10 countries by revenue
print(f' top 10 countries by revenue :')
country_revenue = df_clean.groupby('Country').agg(
    revenue = ('TotalAmount','sum'),
    orders = ('InvoiceNo','nunique'),
    customers = ('CustomerID','nunique')
).sort_values('revenue',ascending = False)
country_revenue['revenue_share_%'] = (country_revenue['revenue']/ total_revenue * 100).round(2)
print(country_revenue.head(10).to_string())

print(f'top 10 Product by Revenue :')
product_revenue = df_clean.groupby(['StockCode','Description']).agg(
    revenue = ('TotalAmount','sum'),
    quantity_Sold = ('Quantity','sum'),
    time_ordered = ('InvoiceNo','nunique')
).sort_values('revenue',ascending = False).reset_index()
print(product_revenue.head(10).to_string(index=False))



# Monthly revenue trend
df_clean['YearMonth'] = df_clean['InvoiceDate'].dt.to_period('M')
monthly_revenue = df_clean.groupby('YearMonth').agg(
    revenue = ('TotalAmount', 'sum'),
    orders = ('InvoiceNo', 'nunique'),
    customers = ('CustomerID', 'nunique')
).reset_index()
monthly_revenue['YearMonth'] = monthly_revenue['YearMonth'].astype(str)

print("\n📊 Monthly Revenue Trend:")
print(monthly_revenue.to_string(index=False))


# ══════════════════════════════════════════════════════════════════
# SECTION 4: RFM ANALYSIS - THE CORE
# ══════════════════════════════════════════════════════════════════
print("\n" + "━" * 70)
print("  SECTION 4: RFM ANALYSIS")
print("━" * 70)

# Set analysis date as 1 day after the last transaction
ANALYSIS_DATE = df_clean['InvoiceDate'].max() + pd.Timedelta(days=1)
print(f"\n📅 Analysis Date: {ANALYSIS_DATE.date()}")
print(f"   (This is the 'today' for RFM calculation)\n")

# Calculate RFM metrics per customer
rfm = df_clean.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (ANALYSIS_DATE - x.max()).days,  # Recency
    'InvoiceNo': 'nunique',                                    # Frequency
    'TotalAmount': 'sum'                                       # Monetary
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

print(f"✓ RFM calculated for {len(rfm):,} customers")
print("\n📊 RFM Statistics:")
print(rfm.describe().to_string())

print("\n📋 Sample RFM Data (First 10 customers):")
print(rfm.head(10).to_string(index=False))

# Create RFM scores (1-5 scale, 5 is best)
print("\n🔧 Creating RFM Scores...")
rfm['R_Score'] = pd.qcut(rfm['Recency'], q=5, labels=[5,4,3,2,1], duplicates='drop')
rfm['F_Score'] = pd.qcut(
    rfm['Frequency'],
    q=5,
    duplicates='drop'
)

rfm['F_Score'] = rfm['F_Score'].cat.codes + 1
rfm['M_Score'] = pd.qcut(rfm['Monetary'], q=5, labels=[1,2,3,4,5], duplicates='drop')

# Convert to int
rfm['R_Score'] = rfm['R_Score'].astype(int)
rfm['F_Score'] = rfm['F_Score'].astype(int)
rfm['M_Score'] = rfm['M_Score'].astype(int)

# Create RFM Score string
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

# Overall RFM Score (average)
rfm['RFM_Score_Avg'] = rfm[['R_Score', 'F_Score', 'M_Score']].mean(axis=1).round(2)

print("✓ RFM Scores calculated!")
print("\n📋 Sample RFM Scores (First 10):")
print(rfm[['CustomerID', 'Recency', 'Frequency', 'Monetary', 'R_Score', 'F_Score', 'M_Score', 'RFM_Score']].head(10).to_string(index=False))

# ══════════════════════════════════════════════════════════════════
# SECTION 5: CUSTOMER SEGMENTATION
# ══════════════════════════════════════════════════════════════════
print("\n" + "━" * 70)
print("  SECTION 5: CUSTOMER SEGMENTATION")
print("━" * 70)

def segment_customer(row):
    r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
    
    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'
    elif r >= 3 and f >= 3 and m >= 3:
        return 'Loyal Customers'
    elif r >= 4 and f >= 2 and m >= 2:
        return 'Potential Loyalists'
    elif r >= 4 and f <= 2:
        return 'New Customers'
    elif r <= 2 and f >= 3 and m >= 3:
        return 'At Risk'
    elif r <= 3 and f <= 3 and m <= 3:
        return 'Need Attention'
    elif r <= 2 and f <= 2:
        return 'Hibernating'
    elif r == 1:
        return 'Lost'
    else:
        return 'Others'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)
print("✓ Customers segmented!")

# Segment distribution
print("\n📊 Customer Segment Distribution:")
segment_counts = rfm['Segment'].value_counts().reset_index()
segment_counts.columns = ['Segment', 'Customer_Count']
segment_counts['Percentage'] = (segment_counts['Customer_Count'] / len(rfm) * 100).round(2)
print(segment_counts.to_string(index=False))

# Detailed segment analysis
print("\n📊 Detailed Segment Analysis:")
segment_analysis = rfm.groupby('Segment').agg({
    'CustomerID': 'count',
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': 'mean',
    'RFM_Score_Avg': 'mean'
}).round(2).reset_index()

segment_analysis.columns = ['Segment', 'Customer_Count', 'Avg_Recency',
                            'Avg_Frequency', 'Avg_Monetary', 'Avg_RFM_Score']

# Calculate total revenue per segment
segment_revenue = rfm.groupby('Segment')['Monetary'].sum().reset_index()
segment_revenue.columns = ['Segment', 'Total_Revenue']

segment_analysis = segment_analysis.merge(segment_revenue, on='Segment')
segment_analysis['Revenue_Share_%'] = (segment_analysis['Total_Revenue'] / rfm['Monetary'].sum() * 100).round(2)
segment_analysis = segment_analysis.sort_values('Total_Revenue', ascending=False)

print(segment_analysis.to_string(index=False))


# ══════════════════════════════════════════════════════════════════
# SECTION 6: VISUALIZATIONS
# ══════════════════════════════════════════════════════════════════
print("\n" + "━" * 70)
print("  SECTION 6: CREATING VISUALIZATIONS")
print("━" * 70)

import os
os.makedirs('charts', exist_ok=True)

# Chart 1: Segment Distribution
print("\n📊 Chart 1: Segment Distribution...")
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

colors = sns.color_palette('Set2', len(segment_counts))
axes[0].pie(segment_counts['Customer_Count'], labels=segment_counts['Segment'],
            autopct='%1.1f%%', colors=colors, startangle=90)
axes[0].set_title('Customer Distribution by Segment', fontsize=14, fontweight='bold')

axes[1].barh(segment_counts['Segment'], segment_counts['Customer_Count'], color=colors)
axes[1].set_xlabel('Number of Customers')
axes[1].set_title('Customer Count by Segment', fontsize=14, fontweight='bold')
axes[1].grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('charts/chart1_segment_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✓ Saved: chart1_segment_distribution.png")

# Chart 2: Revenue by Segment
print("📊 Chart 2: Revenue by Segment...")
fig, ax = plt.subplots(figsize=(12, 6))

segment_rev_sorted = segment_analysis.sort_values('Total_Revenue', ascending=True)
colors_rev = sns.color_palette('RdYlGn', len(segment_rev_sorted))

bars = ax.barh(segment_rev_sorted['Segment'], segment_rev_sorted['Total_Revenue'], color=colors_rev)
ax.set_xlabel('Total Revenue (£)', fontsize=12)
ax.set_title('Total Revenue by Customer Segment', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

for bar, val, pct in zip(bars, segment_rev_sorted['Total_Revenue'], segment_rev_sorted['Revenue_Share_%']):
    ax.text(bar.get_width() + 5000, bar.get_y() + bar.get_height()/2,
            f'£{val:,.0f} ({pct}%)', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('charts/chart2_revenue_by_segment.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✓ Saved: chart2_revenue_by_segment.png")

# Chart 3: RFM Scatter Plots
print("📊 Chart 3: RFM Scatter Plots...")
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for segment in rfm['Segment'].unique():
    seg_data = rfm[rfm['Segment'] == segment]
    axes[0].scatter(seg_data['Recency'], seg_data['Monetary'],
                   alpha=0.6, s=50, label=segment)
axes[0].set_xlabel('Recency (days)', fontsize=11)
axes[0].set_ylabel('Monetary (£)', fontsize=11)
axes[0].set_title('Recency vs Monetary', fontsize=13, fontweight='bold')
axes[0].legend(bbox_to_anchor=(1, 1), fontsize=8)
axes[0].grid(alpha=0.3)

for segment in rfm['Segment'].unique():
    seg_data = rfm[rfm['Segment'] == segment]
    axes[1].scatter(seg_data['Frequency'], seg_data['Monetary'],
                   alpha=0.6, s=50, label=segment)
axes[1].set_xlabel('Frequency (orders)', fontsize=11)
axes[1].set_ylabel('Monetary (£)', fontsize=11)
axes[1].set_title('Frequency vs Monetary', fontsize=13, fontweight='bold')
axes[1].grid(alpha=0.3)

for segment in rfm['Segment'].unique():
    seg_data = rfm[rfm['Segment'] == segment]
    axes[2].scatter(seg_data['Recency'], seg_data['Frequency'],
                   alpha=0.6, s=50, label=segment)
axes[2].set_xlabel('Recency (days)', fontsize=11)
axes[2].set_ylabel('Frequency (orders)', fontsize=11)
axes[2].set_title('Recency vs Frequency', fontsize=13, fontweight='bold')
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('charts/chart3_rfm_scatter.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✓ Saved: chart3_rfm_scatter.png")

# Chart 4: Monthly Revenue Trend
print("📊 Chart 4: Monthly Revenue Trend...")
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(monthly_revenue['YearMonth'], monthly_revenue['revenue'],
        marker='o', linewidth=2.5, markersize=8, color='#2ecc71')
ax.fill_between(range(len(monthly_revenue)), monthly_revenue['revenue'], alpha=0.3, color='#2ecc71')
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Revenue (£)', fontsize=12)
ax.set_title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
ax.tick_params(axis='x', rotation=45)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('charts/chart4_monthly_trend.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✓ Saved: chart4_monthly_trend.png")

# Chart 5: Top 10 Countries
print("📊 Chart 5: Top Countries...")
fig, ax = plt.subplots(figsize=(12, 6))

top10_countries = country_revenue.head(10).sort_values('revenue')
colors_country = sns.color_palette('viridis', len(top10_countries))

bars = ax.barh(top10_countries.index, top10_countries['revenue'], color=colors_country)
ax.set_xlabel('Revenue (£)', fontsize=12)
ax.set_title('Top 10 Countries by Revenue', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

for bar, val in zip(bars, top10_countries['revenue']):
    ax.text(bar.get_width() + 10000, bar.get_y() + bar.get_height()/2,
            f'£{val:,.0f}', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('charts/chart5_top_countries.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✓ Saved: chart5_top_countries.png")

# Chart 6: Segment Heatmap
print("📊 Chart 6: Segment Heatmap...")
heatmap_data = segment_analysis[['Segment', 'Avg_Recency', 'Avg_Frequency', 'Avg_Monetary']].set_index('Segment')

# Normalize for better visualization
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
heatmap_normalized = pd.DataFrame(
    scaler.fit_transform(heatmap_data),
    columns=heatmap_data.columns,
    index=heatmap_data.index
)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(heatmap_normalized.T, annot=False, cmap='RdYlGn', linewidths=0.5, ax=ax,
            cbar_kws={'label': 'Normalized Score'})
ax.set_title('Customer Segment Comparison (Normalized RFM)', fontsize=14, fontweight='bold')
ax.set_ylabel('RFM Metric', fontsize=12)
ax.set_xlabel('Customer Segment', fontsize=12)

plt.tight_layout()
plt.savefig('charts/chart6_segment_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✓ Saved: chart6_segment_heatmap.png")
# ══════════════════════════════════════════════════════════════════
# SECTION 7: KEY FINDINGS & INSIGHTS
# ══════════════════════════════════════════════════════════════════