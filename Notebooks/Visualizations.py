from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Locate main project folder
project_folder = Path(__file__).resolve().parents[1]


# Define input and output paths
data_file = (
    project_folder / "Data" / "Clean" / "housing_cleaned.csv"
)

images_folder = (
    project_folder / "Images"
)

images_folder.mkdir(parents=True, exist_ok=True)


# Load dataset
df = pd.read_csv(data_file)

print(f"CSV exists: {data_file.exists()}")
print(f"Rows loaded: {len(df)}")

# ----------------------------------------------------
# figure 1: average house value by ocean proximity
# ----------------------------------------------------
ocean_values = (
df.groupby("ocean_proximity")["median_house_value"]
    .mean()
    .reset_index()
)

ocean_order = [
    "INLAND",
    "<1H OCEAN",
    "NEAR OCEAN",
    "NEAR BAY",
    "ISLAND"
]

plt.figure(figsize=(10, 6))

ax = sns.barplot(
    data = ocean_values,
    x = "ocean_proximity",
    y = "median_house_value",
    order = ocean_order,
    color = "steelblue"
)

plt.title("Average House Value by Ocean Proximity")
plt.xlabel("Ocean Proximity")
plt.ylabel("Average Median House Value ($)")
plt.xticks(rotation=20)

#formatting y axis as dollars

ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda value, position: f"${value:,.0f}")
)

# display the values on top of the bars
for container in ax.containers:
    ax.bar_label(
        container,
        fmt="${:,.0f}",
        padding = 3,
        fontsize = 9
    )

plt.figtext(
    0.5,
    0.01,
    "Note: The Island category contains only five observations",
    ha="center",
    fontsize = 9
)


plt.tight_layout(rect=[0, 0.04, 1, 1 ])

chart_path = images_folder / "house_value_by_ocean_proximity.png"

plt.savefig(
    chart_path,
    dpi = 300,
    bbox_inches = "tight"
)
plt.close()

print(f"chart saved successfully: {chart_path}")

# -----------------------------------------------------------------
# figure 2: average and median house value by income group
# -----------------------------------------------------------------

df["income_group"] = pd.cut(
    df["median_income"],
    bins = [float("-inf"), 2, 4, 6, float("inf")],
    labels=[
        "Low income",
        "Lower middle income",
        "Upper middle income",
        "High income"
    ],
    right=False
)

income_summary = (
    df.groupby("income_group", observed=False)["median_house_value"]
    .agg(
        Average = "mean",
        Median = "median"
    )
    .reset_index()
)

income_chart_data = income_summary.melt(
    id_vars = "income_group",
    value_vars = ["Average", "Median"],
    var_name = "Measurement",
    value_name = "House Value"
)

plt.figure(figsize=(11,6))

ax = sns.barplot(
    data = income_chart_data,
    x = "income_group",
    y = "House Value",
    hue = "Measurement",
    palette=["steelblue", "darkorange"]
)

plt.title("Average and Median House Value by Income Group")
plt.xlabel("Income Group")
plt.ylabel("House Value ($)")

ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda value, position: f"${value:,.0f}")
)

for container in ax.containers:
    labels = [
        f"${bar.get_height():,.0f}"
        for bar in container
    ]

    ax.bar_label(
        container,
        labels = labels,
        padding = 3,
        fontsize = 8
    )


plt.figtext(
    0.5,
    0.01,
    "Note: 27.73% of high-income observations reached the dataset's $500,001 value cap.",
    ha = "center",
    fontsize = 9
)

plt.legend(title="")
plt.tight_layout(rect=[0, 0.04, 1, 1])

chart_path = images_folder / "house_value_by_income_group.png"

plt.savefig(
    chart_path,
    dpi = 300,
    bbox_inches = "tight"
)

plt.close()

print(f"chart saved successfully: {chart_path}")

# ------------------------------------------------
# figure 3: Average house value by housing age 
# ------------------------------------------------


df["housing_age_group"] = pd.cut(
    df["housing_median_age"],
    bins = [float('-inf'), 10, 20, 30, 40, float("inf")],
    labels= [
        "Under 10 years",
        "10 - 19 years",
        "20 - 29 years",
        "30 - 39 years",
        "40+ years",
    ],
    right = False
)

age_values = (
    df.groupby("housing_age_group", observed = False)["median_house_value"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(10, 6))


ax = sns.barplot(
    data = age_values,
    x = "housing_age_group",
    y = "median_house_value",
    color = "steelblue"
)

plt.title("Average Median House Value by Housing Age")
plt.xlabel("Housing Age Group")
plt.ylabel("Average Median House Value ($)")
plt.xticks(rotation = 15)

ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda value, position: f"${value:,.0f}")
)

for container in ax.containers:
    labels = [
        f"${bar.get_height():,.0f}"
        for bar in container 
    ]

    ax.bar_label(
        container,
        labels = labels,
        padding = 3,
        fontsize = 9
    )

plt.figtext(
    0.5,
    0.01,
    "Housing age showed only a weak correlation with house value (r = 0.106).",
    ha = "center",
    fontsize = 9
)

plt.tight_layout(rect=[0, 0.04, 1, 1])

chart_path =  images_folder / "house_value_by_housing_age.png"


plt.savefig(
    chart_path,
    dpi = 300,
    bbox_inches = "tight"
)

plt.close()

print(f"Chart saved successfully: {chart_path}")

# -------------------------------------------
# figure 4: correlation heatmap
# -------------------------------------------


df["rooms_per_household"] = (
    df["total_rooms"] / df["households"]
)

df["people_per_household"] = (
    df["population"] / df["households"]
)

correlation_data = df[
    [
        "median_income",
        "median_house_value",
        "rooms_per_household",
        "people_per_household",
        "housing_median_age",
    ]
].rename(
    columns={
        "median_income" : "Median Income",
        "median_house_value": "House Value",
        "rooms_per_household" :"Rooms per Household",
        "people_per_household": "People per Household",
        "housing_median_age": "Housing Age",
    }
)

correlation_matrix = correlation_data.corr()

plt.figure(figsize=(10, 7))

sns.heatmap(
    correlation_matrix,
    annot = True,
    fmt = ".2f",
    cmap = "coolwarm",
    center = 0,
    vmin = -1,
    vmax = 1,
    linewidths = 0.5,
    square = True
)

plt.title("Correlation Between California Housing Metrics")
plt.xticks(rotation=30, ha="right")
plt.yticks(rotation = 0 )

plt.tight_layout()

chart_path = images_folder / "correlation_heatmap.png"

plt.savefig(
    chart_path,
    dpi = 300,
    bbox_inches = "tight"
)

plt.close()

print(f"chart saved successfully: {chart_path}")