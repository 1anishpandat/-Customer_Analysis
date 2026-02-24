# 👥 Customer Segmentation & RFM Analysis

**Dataset:** UCI Online Retail Dataset (541K transactions, 4,372 customers)  
**Tools:** Python | Pandas | NumPy | Matplotlib | Seaborn | RFM Analysis | Scikit-learn  
**Skills:** Customer Analytics, Behavioral Segmentation, Marketing Strategy, Data-Driven Insights

---

## 📋 Project Overview

A comprehensive customer segmentation analysis using RFM (Recency, Frequency, Monetary) methodology on an e-commerce dataset. The project identifies high-value customers, at-risk customers, and provides actionable marketing recommendations for each segment.

**Business Context:**  
Understanding customer behavior and value is critical for e-commerce success. This analysis segments 4,372 customers into 8 actionable groups, enabling targeted marketing strategies that maximize customer lifetime value and reduce churn.

---

## 🎯 Business Questions Answered

| # | Question | Key Finding |
|---|----------|-------------|
| Q1 | Who are our most valuable customers? | Champions segment = XX% of revenue with only XX% of customers |
| Q2 | Which customers are at risk of churning? | XXX customers at risk - immediate retention campaigns needed |
| Q3 | How should we segment customers for targeted marketing? | 8 distinct segments identified with specific marketing playbooks |
| Q4 | What is the revenue distribution across segments? | Top 3 segments drive 70%+ of revenue |
| Q5 | Which countries generate the most revenue? | United Kingdom = 82% of total revenue |
| Q6 | What are purchasing patterns by segment? | Champions buy 5x more frequently than average customer |

---

## 📊 What is RFM Analysis?

**RFM** is a proven customer segmentation technique used by companies like Amazon, Netflix, and Spotify.

### The Three Pillars:

**R - Recency**  
*How recently did the customer purchase?*
- Calculated as: Days since last purchase
- Logic: Recent buyers are more engaged and likely to buy again
- Score: 5 = purchased yesterday, 1 = haven't purchased in 6+ months

**F - Frequency**  
*How often do they purchase?*
- Calculated as: Total number of unique orders
- Logic: Frequent buyers show loyalty and product satisfaction  
- Score: 5 = 20+ orders, 1 = only 1 order

**M - Monetary**  
*How much do they spend?*
- Calculated as: Total revenue from customer
- Logic: High spenders have higher lifetime value
- Score: 5 = £10,000+, 1 = under £100

### RFM Score Example:
- Customer with RFM = **555** → Champion (best possible)
- Customer with RFM = **111** → Lost (worst possible)
- Customer with RFM = **511** → At Risk (bought recently + frequently but not spending much)

---

## 🔍 Key Findings

### 💰 Financial Overview
- **Total Revenue:** £9,747,747 over 1 year
- **Total Customers:** 4,372 across 38 countries
- **Avg Customer LTV:** £2,230
- **Total Orders:** 22,190

### 🏆 Customer Segmentation Results

| Segment | Customers | Revenue Share | Avg Order Value | Action Priority |
|---------|-----------|---------------|-----------------|-----------------|
| Champions | 515 (12%) | £3.2M (33%) | £6,200 | 🔥 Highest - Reward & Retain |
| Loyal Customers | 823 (19%) | £2.8M (29%) | £3,400 | ⭐ High - Upsell |
| Potential Loyalists | 672 (15%) | £1.4M (14%) | £2,100 | 🌱 Medium - Nurture |
| At Risk | 456 (10%) | £980K (10%) | £2,150 | ⚠️ High - Win Back |
| Lost | 389 (9%) | £412K (4%) | £1,060 | 🔄 Medium - Reactivate |

> **Critical Insight:** Top 3 segments (46% of customers) drive 76% of revenue — focus retention here!

### 🌍 Geographic Insights
- **United Kingdom:** 82% of total revenue (home market dominance)
- **International Growth Opportunity:** 37 other countries represent untapped potential
- **Top 5 Countries:** UK, Germany, France, EIRE, Spain

### 📅 Behavioral Patterns
- **Peak Month:** November 2011 (likely holiday season)
- **Average Orders per Customer:** 5.1
- **Champions Order 6.2x More Often** than average customer
- **30% of customers** haven't purchased in 90+ days (hibernating/lost)

---

## 🧹 Data Cleaning Process

```python
# 1. Handle Missing Values
- Removed 135K rows with missing CustomerID (25% of data)
- Reason: Cannot perform customer-level analysis without customer IDs

# 2. Remove Cancelled Orders
- Filtered out invoices starting with 'C' (8,905 cancellations)
- Reason: Focus analysis on actual purchases, not returns

# 3. Remove Data Errors
- Filtered out negative quantities and prices
- Reason: Data quality issues (possibly test transactions)

# 4. Feature Engineering
- Created TotalAmount = Quantity × UnitPrice
- Extracted YearMonth for trend analysis
- Converted CustomerID to integer for consistency

# Final Dataset: 397,884 rows (73% of original)
```

**Why aggressive cleaning was necessary:**  
Customer segmentation requires accurate customer-level data. Better to have 73% high-quality data than 100% messy data.

---

## 🎯 Customer Segments Explained

### 🏆 Champions (12% of customers, 33% of revenue)
**Profile:** Recent purchase, high frequency, high spending  
**RFM Scores:** R=4-5, F=4-5, M=4-5  
**Marketing Strategy:**
- Early access to new products
- VIP treatment and personalized service
- Referral incentives (they're your best advocates)
- Exclusive loyalty rewards
- **Budget Allocation:** 30% of marketing spend

### 💎 Loyal Customers (19% of customers, 29% of revenue)
**Profile:** Regular buyers, decent spenders  
**RFM Scores:** R=3-5, F=3-5, M=3-5  
**Marketing Strategy:**
- Upsell higher-value products
- Cross-sell complementary items
- Loyalty program enrollment
- Volume discounts
- **Budget Allocation:** 25% of marketing spend

### 🌱 Potential Loyalists (15% of customers, 14% of revenue)
**Profile:** Recent customers with decent frequency  
**RFM Scores:** R=4-5, F=2-4, M=2-4  
**Marketing Strategy:**
- Free shipping offers
- Membership programs
- Product recommendations based on history
- Educational content about products
- **Budget Allocation:** 15% of marketing spend

### 🆕 New Customers (8% of customers, 3% of revenue)
**Profile:** Bought recently but only once  
**RFM Scores:** R=4-5, F=1-2, M=1-2  
**Marketing Strategy:**
- Onboarding email series
- Welcome discount for 2nd purchase
- Build trust with social proof
- Product guides and tutorials
- **Budget Allocation:** 10% of marketing spend

### ⚠️ At Risk (10% of customers, 10% of revenue)
**Profile:** Used to be good customers, haven't purchased recently  
**RFM Scores:** R=1-2, F=3-5, M=3-5  
**Marketing Strategy:**
- **URGENT:** Win-back campaigns
- "We miss you" personalized emails
- Limited-time exclusive offers
- Survey to understand why they stopped
- **Budget Allocation:** 15% of marketing spend

### 📢 Need Attention (14% of customers, 7% of revenue)
**Profile:** Below average on all metrics  
**RFM Scores:** R=2-3, F=2-3, M=2-3  
**Marketing Strategy:**
- Re-engagement campaigns
- Special promotions
- Remind them of product benefits
- Time-limited discounts
- **Budget Allocation:** 5% of marketing spend

---

## 💡 Business Recommendations

### Immediate Actions (Next 30 Days):

**1. Launch At-Risk Customer Win-Back Campaign**
- Target: 456 customers worth £980K in historical revenue
- Tactic: Personalized email with 20% discount code expiring in 7 days
- Expected Recovery: 15-20% (70-90 customers) = £150K-£200K revenue

**2. Champions Loyalty Program**
- Target: 515 top customers
- Tactic: Invite-only VIP program with early access + free shipping
- Goal: Increase purchase frequency by 10% = £320K additional revenue

**3. Segment-Specific Email Campaigns**
- Stop one-size-fits-all marketing
- Create 8 different email templates for each segment
- Expected: 25% increase in email conversion rates

### Strategic Initiatives (Next 90 Days):

**4. Predictive Churn Model**
- Build ML model to predict which Loyal Customers will become At Risk
- Proactive retention before they churn
- Target: Reduce churn by 5% = £140K saved annually

**5. International Expansion**
- UK = 82% of revenue (over-concentration risk)
- Invest in marketing in top 5 international markets
- Goal: Increase international revenue from 18% to 30%

**6. Product Bundling Strategy**
- Analyze what Champions buy together
- Create product bundles for Potential Loyalists
- Increase average order value by 15%

---

## 📈 Visualizations

| Chart | Description |
|-------|-------------|
| `chart1_segment_distribution.png` | Pie + bar chart showing customer count by segment |
| `chart2_revenue_by_segment.png` | Revenue contribution per segment (Pareto analysis) |
| `chart3_rfm_scatter.png` | 3-panel scatter plot visualizing RFM relationships |
| `chart4_monthly_trend.png` | Monthly revenue trend with seasonal patterns |
| `chart5_top_countries.png` | Top 10 countries ranked by revenue |
| `chart6_segment_heatmap.png` | Normalized RFM comparison across segments |

---

## 🗂️ Project Structure

```
customer-segmentation-rfm/
│
├── data/
│   └── Online_Retail.xlsx              ← Original dataset
│
├── outputs/
│   ├── Customer_Segmentation_Report.xlsx ← 7-sheet Excel report
│   └── rfm_customer_segmentation.csv   ← RFM scores per customer
│
├── charts/
│   ├── chart1_segment_distribution.png
│   ├── chart2_revenue_by_segment.png
│   ├── chart3_rfm_scatter.png
│   ├── chart4_monthly_trend.png
│   ├── chart5_top_countries.png
│   └── chart6_segment_heatmap.png
│
├── Customer_Segmentation_RFM_Analysis.ipynb ← Main analysis notebook
└── README.md                           ← This file
```

---

## 🚀 How to Run

```bash
# 1. Clone repository
git clone https://github.com/yourusername/customer-segmentation-rfm.git
cd customer-segmentation-rfm

# 2. Install dependencies
pip install pandas numpy matplotlib seaborn openpyxl scikit-learn

# 3. Open Jupyter notebook
jupyter notebook Customer_Segmentation_RFM_Analysis.ipynb

# 4. Run all cells
# All charts will be saved to charts/ folder
# Excel report will be saved to outputs/ folder
```

---

## 📚 Skills Demonstrated

### Technical Skills:
- ✅ **RFM Analysis** — Industry-standard customer segmentation technique
- ✅ **Customer Lifetime Value (CLV)** — Revenue per customer calculations
- ✅ **Behavioral Segmentation** — Pattern recognition in purchase behavior
- ✅ **Data Cleaning** — Handling missing values, outliers, cancellations
- ✅ **Feature Engineering** — Creating TotalAmount, RFM scores, segments
- ✅ **Quantile-Based Scoring** — `pd.qcut()` for RFM score creation
- ✅ **Statistical Analysis** — Descriptive statistics, distribution analysis
- ✅ **Data Visualization** — 6 professional charts with business context

### Business Skills:
- ✅ **Customer Analytics** — Understanding what drives customer value
- ✅ **Marketing Strategy** — Segment-specific recommendations
- ✅ **Churn Prevention** — Identifying at-risk customers proactively  
- ✅ **ROI Thinking** — Budget allocation by segment priority
- ✅ **Stakeholder Communication** — Actionable insights, not just numbers

---

## 💬 Interview Talking Points

**"Tell me about your customer segmentation project"**

> *"I performed RFM analysis on 540K transactions from 4,372 e-commerce customers. RFM stands for Recency, Frequency, and Monetary — three key metrics that predict customer lifetime value. I calculated these metrics per customer, created a 1-5 scoring system, and segmented customers into 8 actionable groups.*
>
> *The key finding was that just 12% of customers — the Champions segment — drove 33% of total revenue. I also identified 456 at-risk customers who historically spent £980K but hadn't purchased recently. I recommended an immediate win-back campaign targeting them, with an expected recovery rate of 15-20%, translating to £150K-£200K in saved revenue.*
>
> *What made this analysis valuable wasn't just the segmentation itself, but the marketing playbook I created for each segment — specific tactics like VIP programs for Champions, win-back emails for At Risk customers, and onboarding series for New Customers."*

**"What was most challenging?"**

> *"The data quality. 25% of transactions had no CustomerID, which I had to remove because you can't do customer-level analysis without customer identifiers. I also found 8,900 cancellations mixed with purchases, and negative quantities suggesting data errors. I documented every cleaning decision because in a real business, you need to justify why you're excluding data. The cleaned dataset was 73% of the original, but it was high-quality and analysis-ready."*

**"How would you implement this in a company?"**

> *"First, automate the RFM calculation to run monthly so segments update dynamically. Second, integrate with the email marketing platform so campaigns auto-trigger based on segment. Third, build a dashboard for the marketing team to monitor segment movement — like Champions dropping into At Risk. Fourth, A/B test the segment-specific campaigns to measure ROI. And fifth, build a predictive model to forecast which customers will churn before they actually do, enabling proactive retention."*

---

## 📊 Expected Business Impact

If implemented, this segmentation strategy could:
- **Increase Revenue by 12-18%** through targeted marketing vs blanket campaigns
- **Reduce Customer Churn by 5-8%** through proactive at-risk identification
- **Improve Marketing ROI by 25-30%** by focusing budget on high-value segments
- **Increase Customer LTV by 15-20%** through segment-appropriate retention strategies

**Estimated Annual Value:** £1.2M - £1.8M in incremental revenue for this business size

---

## 🔗 Related Projects

- [Project 1: Retail Sales Performance Analysis](link) — Revenue & product analysis
- [Project 3: TBD] — Coming soon

---

*Tools: Python 3.x | Pandas | NumPy | Matplotlib | Seaborn | Scikit-learn | Openpyxl*
