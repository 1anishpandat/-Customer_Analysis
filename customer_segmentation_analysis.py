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
# ═════════════════════════════════════════════════════════════════
print("\n" + "━" * 70)
print("  SECTION 5: CUSTOMER SEGMENTATION")     
print("━" * 70)

# Define segments based on RFM scores