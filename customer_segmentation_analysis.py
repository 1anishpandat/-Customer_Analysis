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





