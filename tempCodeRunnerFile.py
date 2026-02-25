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