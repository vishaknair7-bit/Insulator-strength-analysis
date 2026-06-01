# ==============================================================================
# 0. ALL IMPORTS GO HERE
# ==============================================================================
import dash
from dash import Dash, dcc, html
import pandas as pd
import plotly.express as px

# Initialize the Dash application
app = Dash(__name__)
server = app.server  # Vital for cloud hosting later

# ==============================================================================
# 1. PANDAS DATA ENGINE (All your notebook data logic processed here)
# ==============================================================================
# Update this path if necessary to point to your dataset location
csv_path = r"C:\Users\Vishak\Documents\Project\insulator strength analysis\insulator_strength (1).csv"
df = pd.read_csv(csv_path)

# Round continuous columns to whole numbers for cleaner grouping
df['Aging_Duration'] = df['Aging_Duration'].round(0)
df['Core_Diameter'] = df['Core_Diameter'].round(0)

# --- 1.1 Calculations for Section 2 (Aging) ---
aging_analysis = df.groupby("Aging_Duration")["Mechanical_Strength"].mean().reset_index()

# --- 1.2 Calculations for Section 3 (Leakage Status) ---
high_threshold = df["Leakage_Current"].quantile(0.75)
low_threshold = df["Leakage_Current"].quantile(0.25)


def classify_leakage(value):
    if value > high_threshold:
        return "High Leakage"
    elif value < low_threshold:
        return "Low Leakage"
    else:
        return "Medium Leakage"


df["Leakage_Status"] = df["Leakage_Current"].apply(classify_leakage)
leakage_strength = df.groupby("Leakage_Status")["Mechanical_Strength"].mean().sort_values().reset_index()

# --- 1.3 Calculations for Section 4 (Material Density Efficiency) ---
df['Strength_Efficiency'] = (df['Mechanical_Strength'] / df['Core_Diameter']).round(4)
low_density_threshold = df['Material_Density'].quantile(0.25)
high_density_threshold = df['Material_Density'].quantile(0.75)

low_eff = df[df['Material_Density'] <= low_density_threshold]['Strength_Efficiency'].mean()
high_eff = df[df['Material_Density'] >= high_density_threshold]['Strength_Efficiency'].mean()

# Creating a summary DataFrame for the efficiency bar chart
efficiency_df = pd.DataFrame({
    "Density Classification": ["Low Density", "High Density"],
    "Strength Efficiency (kN/mm)": [low_eff, high_eff]
})

# --- 1.4 Calculations for Section 5 (Core Diameter Analysis) ---
diameter_strength = df.groupby("Core_Diameter")["Mechanical_Strength"].mean().reset_index()

inefficient = df[
    (df["Core_Diameter"] > df["Core_Diameter"].mean()) &
    (df["Mechanical_Strength"] < df["Mechanical_Strength"].mean())
    ]

# --- 1.5 Calculations for Section 6 (Combined Risk Analysis) ---
low_strength_threshold = df['Mechanical_Strength'].quantile(0.25)
at_risk = df[
    (df['Leakage_Status'] == 'High Leakage') &
    (df['Mechanical_Strength'] < low_strength_threshold)
    ]
pct_at_risk = (len(at_risk) / len(df)) * 100

# --- 1.6 Calculations for Section 7 (Critical Heuristic Top 5) ---
df["Remaining_Strength"] = 100 - (df["Leakage_Current"] * df["Aging_Duration"])
critical_5 = df.nsmallest(5, "Remaining_Strength")[
    ["Aging_Duration", "Leakage_Current", "Mechanical_Strength", "Remaining_Strength"]
]

# --- 1.7 Calculations for Section 8 (Correlation Matrix) ---
cols = ["Aging_Duration", "Leakage_Current", "Mechanical_Strength", "Core_Diameter", "Material_Density"]
corr_matrix = df[cols].corr()

# ==============================================================================
# 2. PLOTLY FIGURES GENERATION (Creating Interactive Visualizations)
# ==============================================================================
# --- 2.1 Aging Figure ---
fig_aging = px.line(
    aging_analysis, x="Aging_Duration", y="Mechanical_Strength", markers=True,
    title="Average Mechanical Strength vs Aging Duration",
    labels={"Aging_Duration": "Aging Duration (years)", "Mechanical_Strength": "Avg Mechanical Strength (kN)"},
    template="plotly_white"
)
fig_aging.update_traces(line_color="steelblue")

# --- 2.2 Leakage Status Figure ---
fig_leakage = px.bar(
    leakage_strength, x="Leakage_Status", y="Mechanical_Strength", color="Leakage_Status",
    title="Average Mechanical Strength by Leakage Status",
    labels={"Leakage_Status": "Leakage Status", "Mechanical_Strength": "Avg Mechanical Strength (kN)"},
    color_discrete_map={"Low Leakage": "green", "Medium Leakage": "orange", "High Leakage": "red"},
    template="plotly_white"
)

# --- 2.3 Density Efficiency Figure ---
fig_density = px.bar(
    efficiency_df, x="Density Classification", y="Strength Efficiency (kN/mm)", color="Density Classification",
    title="Strength Efficiency: Low vs High Density Materials",
    color_discrete_map={"Low Density": "#e07b54", "High Density": "#5b8db8"},
    template="plotly_white"
)

# --- 2.4 Core Diameter Figure ---
fig_diameter = px.line(
    diameter_strength, x="Core_Diameter", y="Mechanical_Strength", markers=True,
    title="Average Mechanical Strength by Core Diameter",
    labels={"Core_Diameter": "Core Diameter (mm)", "Mechanical_Strength": "Average Mechanical Strength (kN)"},
    template="plotly_white"
)

# --- 2.5 Correlation Heatmap Figure ---
# Use "RdBu_r" to get the reversed blue-to-red continuous color scale
fig_corr = px.imshow(
    corr_matrix,
    text_auto=".2f",
    color_continuous_scale="RdBu_r", # This is the correct way to reverse a heatmap scale
    zmin=-1, zmax=1,
    title="Correlation Matrix — Key Variables",
    template="plotly_white"
)

# ==============================================================================
# 3. DASH DISPLAY LAYOUT (Assembling the Webpage)
# ==============================================================================
# Unified professional styles using variable maps
card_style = {'backgroundColor': 'white', 'padding': '25px', 'marginBottom': '25px', 'borderRadius': '6px',
              'boxShadow': '0 2px 4px rgba(0,0,0,0.05)'}
title_color = '#2c3e50'
text_color = '#34495e'

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '30px 50px', 'backgroundColor': '#f8f9fa'},
                      children=[

                          # Header Section
                          html.Div(style={'textAlign': 'center', 'marginBottom': '40px'}, children=[
                              html.H1("🔌 Insulator Mechanical Strength Analysis Dashboard",
                                      style={'color': title_color, 'fontWeight': 'bold'}),
                              html.H4("Author: R VISHAK NAIR | Comprehensive Research Analysis",
                                      style={'color': '#7f8c8d', 'marginTop': '5px'}),
                              html.P(
                                  "Goal: Analyze factors that affect the mechanical strength of electrical insulators, including aging, leakage current, core diameter, and material density.",
                                  style={'color': text_color, 'fontSize': '15px'}),
                              html.Hr(style={'borderTop': '2px solid #dee2e6', 'width': '80%', 'margin': '20px auto'})
                          ]),

                          # Section 2: Aging Analysis
                          html.Div(style=card_style, children=[
                              html.H2("1. Aging Duration vs Mechanical Strength", style={'color': title_color}),
                              html.P(
                                  "Finding: A downward trend in strength as aging duration increases confirms material degradation over time. Insulators with higher aging durations should be prioritized for inspection or replacement.",
                                  style={'color': text_color}),
                              dcc.Graph(figure=fig_aging)
                          ]),

                          # Section 3: Leakage Current Analysis
                          html.Div(style=card_style, children=[
                              html.H2("2. Leakage Current Analysis", style={'color': title_color}),
                              html.P(
                                  "Finding: Insulators classified as 'High Leakage' tend to have lower average mechanical strength. This suggests leakage current is a reliable stress indicator and can be used as an early warning signal.",
                                  style={'color': text_color}),
                              dcc.Graph(figure=fig_leakage)
                          ]),

                          # Section 4: Material Density & Strength Efficiency
                          html.Div(style=card_style, children=[
                              html.H2("3. Material Density & Strength Efficiency", style={'color': title_color}),
                              html.P(
                                  f"Efficiency Metrics: Low Density (≤25th pct): {low_eff:.4f} kN/mm | High Density (≥75th pct): {high_eff:.4f} kN/mm",
                                  style={'fontWeight': 'bold', 'color': title_color}),
                              html.P(
                                  "Finding: Higher-density materials show greater strength efficiency — meaning they deliver more mechanical strength per mm of core diameter. This supports using denser materials in high-stress environments.",
                                  style={'color': text_color}),
                              dcc.Graph(figure=fig_density)
                          ]),

                          # Section 5: Core Diameter Analysis
                          html.Div(style=card_style, children=[
                              html.H2("4. Core Diameter vs Mechanical Strength", style={'color': title_color}),
                              html.P(f"Inefficient design count (large core, weak strength): {len(inefficient)} units.",
                                     style={'fontWeight': 'bold', 'color': '#c0392b'}),
                              html.P(
                                  "Finding: A larger core diameter does not always guarantee higher strength. Insulators with oversized cores but weak strength may point to material quality issues or manufacturing defects.",
                                  style={'color': text_color}),
                              dcc.Graph(figure=fig_diameter)
                          ]),

                          # Section 6: Combined Risk Metrics
                          html.Div(style=card_style, children=[
                              html.H2("5. Combined Risk Candidates", style={'color': title_color}),
                              html.P(
                                  f"At-risk insulators identified (High Leakage + Low Strength): {len(at_risk)} units ({pct_at_risk:.2f}% of total dataset).",
                                  style={'fontWeight': 'bold', 'color': '#c0392b', 'fontSize': '16px'}),
                              html.P(
                                  "Finding: A measurable percentage of insulators meet both risk criteria simultaneously. These individual assets represent critical operational failure vulnerabilities and should be the highest priority for preventive maintenance or immediate field replacement.",
                                  style={'color': text_color})
                          ]),

                          # Section 7: Top 5 Urgent Actions
                          html.Div(style=card_style, children=[
                              html.H2("6. Heuristic Remaining Strength: Top 5 Most Critical Insulators",
                                      style={'color': title_color}),
                              html.P(
                                  "Finding: The simplified degradation metric formula flags the most heavily degraded physical assets requiring immediate intervention.",
                                  style={'color': text_color}),

                              # Displaying data as a styled structural HTML Table
                              html.Table(
                                  style={'width': '100%', 'borderCollapse': 'collapse', 'marginTop': '15px',
                                         'textAlign': 'left'},
                                  children=[
                                      html.Thead(
                                          html.Tr(style={'backgroundColor': '#2c3e50', 'color': 'white'}, children=[
                                              html.Th("Aging Duration (years)", style={'padding': '12px'}),
                                              html.Th("Leakage Current (mA)", style={'padding': '12px'}),
                                              html.Th("Mechanical Strength (kN)", style={'padding': '12px'}),
                                              html.Th("Heuristic Remaining Strength Score", style={'padding': '12px'})
                                          ])
                                      ),
                                      html.Tbody([
                                          html.Tr(style={'borderBottom': '1px solid #dddddd',
                                                         'backgroundColor': '#f9f9f9' if i % 2 == 0 else 'white'},
                                                  children=[
                                                      html.Td(str(row['Aging_Duration']), style={'padding': '12px'}),
                                                      html.Td(f"{row['Leakage_Current']:.2f}",
                                                              style={'padding': '12px'}),
                                                      html.Td(f"{row['Mechanical_Strength']:.2f}",
                                                              style={'padding': '12px'}),
                                                      html.Td(f"{row['Remaining_Strength']:.2f}",
                                                              style={'padding': '12px', 'color': '#c0392b',
                                                                     'fontWeight': 'bold'})
                                                  ]) for i, row in critical_5.iterrows()
                                      ])
                                  ]
                              )
                          ]),

                          # Section 8: Correlation Matrix Heatmap
                          html.Div(style=card_style, children=[
                              html.H2("7. Research Correlation Matrix Summary", style={'color': title_color}),
                              html.P(
                                  "Finding: The matrix highlights the direct cross-relationships governing component lifespan. Strong negative correlations corresponding with aging and leakage current metrics analytically confirm our isolated decay findings.",
                                  style={'color': text_color}),
                              dcc.Graph(figure=fig_corr)
                          ])
                      ])

# ==============================================================================
# 4. START RUNNING THE DASHBOARD
# ==============================================================================
if __name__ == '__main__':
    app.run(debug=True)