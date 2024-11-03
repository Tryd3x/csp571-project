# This file serves to download the 100k most recent chicago crime data from: 
# https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2/about_data
#
# This download and saves the data in the datasets folder

from sodapy import Socrata
from pathlib import Path
import pandas as pd

def load_crime_dataset(limit=100000):
    try:
        # Authenticating database servers
        client = Socrata("data.cityofchicago.org", None)
        
        print(f"Fetching data...")
        # Get crime records dating from 2020 to present
        results = client.get(
            dataset_identifier="ijzp-q8t2",
            # where = "date >= '2020-01-01'",
            limit=limit)

        print(f"Data fetched..")

        df = pd.DataFrame.from_records(results)
        df.drop(columns=df.columns[23:],inplace=True)

        file_path = Path("../datasets/chicago-crime-data.csv")
        df.to_csv(file_path, index=False)
        print(f"File saved to {file_path}")

    except OSError:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path, index=False)
        print(f"Directory created and file saved to {file_path}")

    except Exception as e:
        print(f"Exception Caught: {e}")