print(f"   Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
# print(f"   Date range: {df['InvoiceDate'].min().date()} to {df['InvoiceDate'].max().date()}")
# print(f"   Unique customers: {df['CustomerID'].nunique():,}")

# print("\n📋 First 5 rows:")
# print(df.head().to_string())

# print("\n🔍 Column Info:")
# print(df.info())

# print("\n📊 Statistical Summary:")
# print(df.describe().to_string())

# print("\n🔎 Missing Values:")
# missing = pd.DataFrame({
#     'Missing Count': df.isnull().sum(),
#     'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
# })
# print(missing[missing['Missing Count'] > 0].to_string())
