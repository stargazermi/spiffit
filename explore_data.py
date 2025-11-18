import pandas as pd
import os

# Explore the test data files
data_dir = "test-data"

files = [
    "AE Ethernet Incentive Data.xlsx",
    "Voice_Incentive_data.xlsx"
]

for file in files:
    file_path = os.path.join(data_dir, file)
    print(f"\n{'='*60}")
    print(f"FILE: {file}")
    print(f"{'='*60}")
    
    # Read Excel file
    xls = pd.ExcelFile(file_path)
    
    print(f"\nSheets: {xls.sheet_names}")
    
    # Examine each sheet
    for sheet in xls.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet)
        print(f"\n--- Sheet: {sheet} ---")
        print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"\nColumns: {list(df.columns)}")
        print(f"\nFirst 3 rows:")
        print(df.head(3))
        print(f"\nData types:")
        print(df.dtypes)

