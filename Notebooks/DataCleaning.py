import pandas as pd
from pathlib import Path
# reading datasets
#df = pd.read_csv('C:/Users/Ricar/Desktop/PythonProjects/CaliforniaHousingProject/Data/Raw/housing.csv')

# locate main project folder
project_folder = Path(__file__).resolve().parents[1]

# Define input and output paths
raw_data_file = (
    project_folder / "Data" / "Raw" / "housing.csv"
)

clean_data_folder = (
    project_folder / "Data" / "Clean"
)

clean_data_file = (
    clean_data_folder / "housing_cleaned.csv"
)

clean_data_folder.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(raw_data_file)


#formatting headers
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

#finding and dropping unknowns
unknown_tokens = ['ERROR', 'Unknown', 'UNKNOWN', 'UNK', "?", "", " "]
df = df.replace(unknown_tokens, pd.NA)

#making sure all columns are in the correct data type

numeric_columns = ['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income', 'median_house_value']
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

integer_columns = [
    "housing_median_age",
    "total_rooms",
    "total_bedrooms",
    "population",
    "households",
    "median_house_value"
]

df[integer_columns] = df[integer_columns].astype("Int64")

##df.to_csv('C:/Users/Ricar/Desktop/PythonProjects/CaliforniaHousingProject/Data/Clean/housing_cleaned.csv', index=False)

df.to_csv(clean_data_file, index=False)

print(f"Rows cleaned: {len(df)}")
print(f"Cleaned dataset saved to: {clean_data_file}")