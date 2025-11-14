import pandas as pd

class Datas:
    def __init__(self):
        self.parquet_file = "models/PredictionModel/sorted_fires_australia.parquet"

    def importDatasetsOnFirms(self):
        try:
            df = pd.read_parquet(self.parquet_file)

            df = df.query("type == 0 & confidence >= 95")

            drop_columns = ["Invalid API call.", "version", "instrument", "type"]
            df = df.drop(drop_columns, axis=1)

            df["year"] = df["acq_date"].dt.year
            df["month"] = df["acq_date"].dt.month
            df["day"] = df["acq_date"].dt.day

            df["daynight"] = df["daynight"].replace("D", 1)
            df["daynight"] = df["daynight"].replace("N", 0)

            print(f"Dataset loaded sucessfull!")
        except Exception as e:
            print(f"Error to execute importDatasetsOnFirms method.\n{e}")
        
        return df
        