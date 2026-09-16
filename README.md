# California Housing Analysis

## About the Project

For this project, I analyzed a California housing dataset containing 20,640 records. My goal was to understand how factors such as income, ocean proximity, and housing age relate to median house values.

I cleaned the data with Python, imported it into PostgreSQL, used SQL for the analysis, and created the final charts with Matplotlib and Seaborn.

## Tools

* Python
* pandas
* PostgreSQL
* SQL
* pgAdmin
* Matplotlib
* Seaborn

## Data Cleaning

I used pandas to:

* Standardize the column names
* Replace unknown values with missing values
* Convert columns to the correct data types
* Convert whole-number columns to nullable integers
* Export the cleaned dataset for PostgreSQL

The dataset contained 207 missing values in `total_bedrooms`. I kept these rows because the rest of their data was still usable.

## SQL Analysis

After cleaning the data, I imported all 20,640 records into PostgreSQL.

I used SQL to:

* Check for missing values
* Find minimum, maximum, and average values
* Compare house values by ocean proximity
* Create income and housing-age groups
* Calculate rooms and people per household
* Compare average and median house values
* Calculate correlations between variables

I also created a view called `property_metrics` to store the calculated columns used in the analysis.

## Key Findings

### Income and house value

Median income had the strongest relationship with house value, with a correlation of **0.688**.

Average house values increased across each income group:

* Low income: **$112,513**
* Lower-middle income: **$167,921**
* Upper-middle income: **$244,385**
* High income: **$378,207**

![House value by income group](Images/house_value_by_income_group.png)

### Ocean proximity

Inland areas had the lowest average house value at **$124,805**. Areas near the bay averaged **$259,212**, which was about 108% higher than inland areas.

The Island category had the highest average, but it only contained five records, so it was not large enough to make a broad conclusion.

![House value by ocean proximity](Images/house_value_by_ocean_proximity.png)

### Housing age

Housing age had a weak correlation of **0.106** with house value. The oldest housing group had the highest average value, but many of those records were also located near the ocean or bay.

This showed that location was probably more important than housing age by itself.

![House value by housing age](Images/house_value_by_housing_age.png)

### Correlations

The heatmap shows that income had a much stronger relationship with house value than rooms per household, people per household, or housing age.

![Correlation heatmap](Images/correlation_heatmap.png)

## Data Limitations

* There were 207 missing bedroom values.
* The Island category only contained five records.
* House values were capped at $500,001.
* A total of 965 records, or 4.68%, reached the value cap.
* The dataset contains historical housing data and does not represent current California prices.

## Project Files

* `scripts/data_cleaning.py` cleans the original dataset.
* `scripts/create_visualizations.py` creates the four charts.
* `SQL/california_housing_analysis.sql` contains the SQL analysis.
* `Data/Raw` contains the original dataset.
* `Data/Clean` contains the cleaned dataset.
* `Images` contains the completed charts.

## Main Takeaway

Income and ocean proximity had the clearest relationships with median house value. Housing age and household size had much weaker relationships.
