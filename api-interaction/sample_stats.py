import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

def summary_table():
    file_path = Path(__file__).parent / "output/history.csv"
    df = pd.read_csv(file_path)

    summary = df.describe().round(2)
    summary = summary.drop(index = 'count')
    print(summary)

if __name__ == "__main__":
    summary_table()