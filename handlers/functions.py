import pandas as pd

from handlers.config import *


def db_to_df() -> pd.DataFrame:

    """Retrieves all values from my Redis DB"""

    pipe = r.pipeline()
    length = len(r.keys())

    for key in r.keys():

        pipe.hgetall(key)

    list_of_rows = pipe.execute()

    df = pd.DataFrame(list_of_rows)

    df['float'] = df['float'].str.strip()
    df['float'] = df['float'].astype(str).replace(' ', '')
    df['float'] = df['float'].astype(float)
    df['price'] = df['price'].str.replace(' ', '')
    df['price'] = df['price'].astype(float)
    df['id'] = df['id'].astype(int)

    return df


def filter_df(filters: dict, df: pd.DataFrame) -> pd.DataFrame:

    """Returns a filtered DataFrame object"""
    if filters.items():
        for f_key, f_value in filters.items():

            df = df[df[f_key] == f_value]
    else:

        df = df

    return df

