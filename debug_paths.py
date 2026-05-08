import os
import pandas as pd

print("Current working directory:", os.getcwd())
print("\nFiles in current directory:")
for file in os.listdir('.'):
    print(f"  - {file}")

print("\nChecking for products.csv:")
if os.path.exists('products.csv'):
    print("✓ products.csv found!")
    df = pd.read_csv('products.csv')
    print("\nColumns:", df.columns.tolist())
    print("\nFirst few rows:")
    print(df.head())
else:
    print("✗ products.csv NOT found in current directory")
    print("\nSearching in parent directory:")
    if os.path.exists('../products.csv'):
        print("✓ products.csv found in parent directory!")
    else:
        print("✗ products.csv not found")