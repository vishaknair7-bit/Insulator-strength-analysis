# 🔌 Insulator Mechanical Strength Analysis

A data analysis project exploring the factors that affect the mechanical degradation of electrical insulators using Python and Pandas.

---

## 📁 Project Structure

```
insulator-strength-analysis/
│
├── insulator_analysis.ipynb   ← Main analysis notebook
├── data/
│   └── insulator_strength.csv ← Dataset (add your own file here)
└── README.md
└──app.py

```

---

## 📊 What This Project Covers

| Section | Question Asked |
|---------|----------------|
| Aging Analysis | Does strength decrease over time? |
| Leakage Current | Does high leakage correlate with low strength? |
| Material Density | Do denser materials perform more efficiently? |
| Core Diameter | Does a larger core mean stronger insulators? |
| Combined Risk | What % of insulators are critically at-risk? |
| Remaining Strength | Which insulators are most degraded right now? |
| Correlation Matrix | How do all variables relate to each other? |

---

## 🔑 Key Findings

- Mechanical strength **decreases with aging duration**
- **High leakage current** is a reliable early-warning indicator of weakness
- **High-density materials** deliver more strength per mm of core diameter
- A larger core diameter does **not** guarantee higher strength — inefficient designs exist
- A subset of insulators have **both** high leakage and low strength — these are highest priority

---

## 🛠️ Tech Stack

- Python 3.10+
- Pandas
- Matplotlib
- plotly express
- Dash


---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/insulator-strength-analysis.git
cd insulator-strength-analysis

# 2. Install dependencies
pip install pandas matplotlib seaborn jupyter

# 3. Add your dataset
#    Place insulator_strength.csv inside the /data folder

# 4. Launch the notebook
jupyter notebook insulator_analysis.ipynb
```

---

## 📌 Next Steps

- [ ] Build a predictive regression model using `scikit-learn`
- [ ] Apply K-Means clustering to segment insulators into risk tiers
- [ ] Build an interactive dashboard with `Streamlit` or `Plotly`
- [ ] Add anomaly detection using Isolation Forest

---

## 👤 Author

**R VISHAK NAIR**  
vishaknair@7@gmail.com