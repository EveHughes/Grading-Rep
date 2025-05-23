### Setting up Workspace ###
import pandas as pd
from pathlib import Path
import kagglehub
from kagglehub import KaggleDatasetAdapter

### Downloading dataset ##
def download():
    # Set the path to the file you'd like to load
    file_path = "penguins.csv"

    # Load the latest version
    df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "satyajeetrai/palmer-penguins-dataset-for-eda",
    file_path
    )

    #write to csv
    path = Path(__file__).parent / "data/raw_data.csv"
    df.to_csv(path, index=False)

### Clean dataset ###
def clean():
    #read in data
    path = Path(__file__).parent / "data/raw_data.csv"
    df = pd.read_csv(path)
    
    #sum number of each species
    species_data = dict()
    for index, row in df.iterrows():
        species = row["species"]

        if species in species_data:
            species_data[species] += 1
        else:
            species_data[species] = 1
    
    #save cleaned data
    path = path = Path(__file__).parent / "data/cleaned_data.csv"
    cleaned_df = pd.DataFrame(list(species_data.items()), columns=["species", "count"])
    cleaned_df.to_csv(path, index=False)

if __name__ == "__main__":
    download()
    clean()
