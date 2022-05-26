import pandas as pd
import sqlalchemy as sql_a
import os
from ast import literal_eval

class Database:
    engine = None
    
    def __init__(self, con_str: str) -> None:
        self.engine = sql_a.create_engine(con_str, connect_args={'connect_timeout': 5})
        self.engine.connect()
        print("INFO: Database Connected")
        
    def query(self, sql: str) -> None:
        return pd.read_sql(sql, con=self.engine)
    
    @staticmethod
    def evaluate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for i in df.columns:
            if df.dtypes[i] == "O":
                try:
                    df[i] = df[i].apply(literal_eval)
                except:
                    print(f"Cannot evaluate {i}")
        return df

# Instantiate Database Cache
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database_name = os.getenv("DB_NAME")
con_str = os.getenv("DB_CON_STRING")

final_con_str = "mysql://"
if con_str is not None:
    final_con_str += con_str
else:
    final_con_str += f"{username}:{password}@{host}:{port}/{database_name}"
    
db = Database(final_con_str)