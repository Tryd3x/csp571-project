# This file serves to download the 100k most recent chicago crime data from: 
# https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2/about_data
#
# This download and saves the data in the datasets folder

import os
from sodapy import Socrata
from pathlib import Path
import pandas as pd

def load_crime_dataset(limit=2000000):
    try:
        # Authenticating database servers
        client = Socrata("data.cityofchicago.org", os.getenv('API_KEY'))
        
        print(f"Fetching data...")

        # Get crime records dating from 2019 to present
        results = client.get(
            dataset_identifier="ijzp-q8t2",
            where="year between '2019' and '2024'",
            limit=2000000
        )

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
