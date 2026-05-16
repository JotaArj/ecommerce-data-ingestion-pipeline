import pandas as pd



def get_genre_unified_genre_data(primary_genre_data: pd.DataFrame) -> pd.DataFrame:

    secondary_genre_data = primary_genre_data
    tertiary_genre_data = primary_genre_data

    primary_genre_data = primary_genre_data[
        primary_genre_data["primary_genre"] != "unknown"]
    secondary_genre_data = secondary_genre_data[
        secondary_genre_data["secondary_genre"] != "unknown"]
    tertiary_genre_data = tertiary_genre_data[
        tertiary_genre_data["tertiary_genre"] != "unknown"]

    primary_genre_data["unified_genre"] = primary_genre_data[
        "primary_genre"]
    secondary_genre_data["unified_genre"] = secondary_genre_data[
        "secondary_genre"]
    tertiary_genre_data["unified_genre"] = tertiary_genre_data[
        "tertiary_genre"]



    return pd.concat([primary_genre_data, 
                                        secondary_genre_data, 
                                        tertiary_genre_data]
)
