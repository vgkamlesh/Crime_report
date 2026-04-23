from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def rename():
    keywords = ['IPC', 'SLL', 'Women', 'Children', 'SC', 'ST']
    for year in range(2016, 2024):
        root = Path(f'data/{year}')
        for file in root.iterdir():
            for key in keywords:
                if key in file.name:
                    file.rename(root / f'{key}{year}.xlsx')
                    break

def refine():
    for year in range(2016, 2024):
        root = Path(f"data/{year}")
        for file in root.iterdir():
            df = pd.read_excel(file)
            row = df.iloc[:, 0].astype(str).str.strip() == "1"
            if not row.any():
                continue
            start = df.index[row][0]
            reduced_df = df.iloc[start:, [1, -2]]
            reduced_df.to_excel(file, index=False)

def correct_dist():
    dist = pd.read_excel('data/Districts.xlsx')
    dist_col = dist.iloc[2:, 1].fillna('').astype(str).str.replace(" ", "").str.lower()
    for year in range(2016, 2024):
        root = Path(f'data/{year}')
        for file in root.iterdir():
            df = pd.read_excel(file)
            col = df.iloc[:, 0].fillna('').astype(str).str.replace(" ", "").str.lower()
            new_df = df[col.isin(dist_col)]
            new_df.to_excel(file, index=False)

def proper():
    for year in range(2016, 2024):
        root = Path(f"data/{year}")
        for file in root.iterdir():
            df = pd.read_excel(file)
            df.columns = ['District', file.stem[:-4]]
            df.to_excel(file, index=False)

def combine_year():
    for year in range(2016, 2024):
        root = Path(f"data/{year}")
        df1 = pd.read_excel(root / f'IPC{year}.xlsx')
        for file in root.iterdir():
            if file.name == f'IPC{year}.xlsx':
                continue
            df2 = pd.read_excel(file)
            df1 = pd.merge(df1, df2, on='District', how='left')
        df1.to_excel(f'{year}.xlsx', index=False)

def merge_to_one():
    dfs = []
    for year in range(2016, 2024):
        df = pd.read_excel(f'{year}.xlsx')
        df.insert(0, 'Year', year)
        dfs.append(df)
    final = pd.concat(dfs, ignore_index=True)
    final = final.drop_duplicates(subset=['Year', 'District'])
    final.to_csv('crime_data.csv', index=False)

# rename()
# refine()
# correct_dist()
# proper()
# combine_year()
# merge_to_one()

df = pd.read_csv("crime_data.csv")
df = df.fillna(0)

crime_cols = ["IPC", "SLL", "Women", "Children", "SC", "ST"]
predictions = []

for district in df["District"].unique():
    d = df[df["District"] == district].sort_values("Year")

    X = d["Year"].values.reshape(-1, 1)
    y = d[crime_cols].values

    model = LinearRegression()
    model.fit(X, y)

    pred = model.predict([[2024]])[0]
    pred = np.maximum(pred, 0)
    pred = np.round(pred).astype(int)

    row = {"District": district, "Year": 2024}
    for i, col in enumerate(crime_cols):
        row[f"Pred_{col}"] = pred[i]

    predictions.append(row)

pred_df = pd.DataFrame(predictions)
pred_df.to_csv("crime_prediction_2024.csv", index=False)