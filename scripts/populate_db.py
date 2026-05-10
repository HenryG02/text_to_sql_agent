import glob
import os
import pandas as pd
from supabase import create_client, Client

# Loading environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def extract_data(file_path: str) -> pd.DataFrame:
    """
    Read the raw file using the two-delimiter strategy.
    """
    # Reading only headers separated by commas
    columns = pd.read_csv(file_path, sep=",", nrows=0).columns

    # Reading the rest with semicolons as delimiter
    df = pd.read_csv(file_path, sep=";", skiprows=1, names=columns)
    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the DataFrame
    """

    # 1. Dropping scramble column
    if "Scramble" in df.columns:
        df = df.drop("Scramble", axis=1)

    # 2. Puzzle column transformation (333 -> 3x3x3)
    df["Puzzle"] = (
        df["Puzzle"].astype("str").str.replace(r"(?<=\d)(?=\d)", "x", regex=True)
    )

    # 3. Time(millis) -> Time_in_sec
    df["Time(millis)"] = df["Time(millis)"] / 1000
    df = df.rename(columns={"Time(millis)": "time_in_sec"})

    # 4. Date transformation
    df["Date(millis)"] = pd.to_datetime(df["Date(millis)"], unit="ms", utc=True)
    df["Date(millis)"] = (
        df["Date(millis)"].dt.tz_convert("America/Sao_Paulo").dt.tz_localize(None)
    )
    df = df.rename(columns={"Date(millis)": "date"})

    # 5. Normalizing column names (all lowercase)
    df.columns = [col.lower() for col in df.columns]

    # Dealing with NaNs (Supabase prefers None/null)
    df = df.replace({np.nan: None})

    # 6. Convert datetime to string for JSON serialization
    if "date" in df.columns:
        df["date"] = df["date"].dt.strftime("%Y-%m-%d %H:%M:%S")

    return df


def load_to_supabase(df: pd.DataFrame, table_name: str):
    """
    Upload data to Supabase
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("❌ Supabase credentials not found in .env")

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Converting DataFrame to list of dictionaries (preferred format by Supabase)
    records = df.to_dict(orient="records")

    try:
        # Bulk insert
        response = supabase.table(table_name).insert(records).execute()
        print("Data properly populated to Supabase!")
        return response
    except Exception as e:
        print(f"Error while uploading data: {e}")
        raise


if __name__ == "__main__":
    folder_path = "data/*.txt"
    files = glob.glob(folder_path)
    latest_file = max(files, key=os.path.getctime)
    TABLE_NAME = "solves"

    try:
        raw_df = extract_data(latest_file)
        processed_df = transform_data(raw_df)
        load_to_supabase(processed_df, TABLE_NAME)
    except Exception as e:
        print(f"❌ Error in the pipeline: {e}")
