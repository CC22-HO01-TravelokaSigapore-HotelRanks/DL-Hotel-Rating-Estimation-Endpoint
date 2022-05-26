import pandas as pd
import sqlalchemy as sql_a
import os
from ast import literal_eval

class Database:
    engine = None
    cached = {
        "user": None,
        "hotel": None
    }
    
    def __init__(self, con_str: str) -> None:
        self.engine = sql_a.create_engine(con_str, connect_args={'connect_timeout': 5})
        self.engine.connect()
        print("INFO: Database Connected")
        self.cache_database()
        
    def query(self, sql: str) -> None:
        return pd.read_sql(sql, con=self.engine)
    
    def user(self) -> pd.DataFrame:
        return self.cached["user"]
    
    def hotel(self) -> pd.DataFrame:
        return self.cached["hotel"]
    
    def cache_database(self) -> None:
        print("INFO: Caching Database")
        self.__update_user()
        self.__update_hotel()
        print("INFO: All Databases Cached")
    
    def __update_user(self) -> None:
        print("INFO: Caching User Database")
        df = self.query("SELECT id, special_needs FROM Users")
        df.dropna(inplace=True)
        df = self.evaluate_dataframe(df)
        df = df.apply(self.one_hot_special_needs, axis=1)
        df.drop(columns=["special_needs"], inplace=True)
        df.set_index("id", inplace=True)
        self.cached["user"] = df.copy()
        print("INFO: User Database Cached")

    def __update_hotel(self) -> None:
        print("INFO: Caching Hotel Database")
        df = self.query("SELECT id, latitude, longitude, hotel_star, price_per_night, free_refund, nearby_destination, breakfast, pool, wifi, parking, smoking, air_conditioner, wheelchair_access, average_bed_size, staff_vaccinated, child_area FROM hotel_dummy_photos")
        df.dropna(inplace=True)
        df = self.evaluate_dataframe(df)
        df[["free_refund", "breakfast","pool","wifi","parking","smoking","air_conditioner","wheelchair_access","average_bed_size","staff_vaccinated","child_area"]] = df[["free_refund", "breakfast","pool","wifi","parking","smoking","air_conditioner","wheelchair_access","average_bed_size","staff_vaccinated","child_area"]].astype(int)
        df.set_index("id", inplace=True)
        self.cached["hotel"] = df.copy()
        print("INFO: Hotel Database Cached")
    
    @staticmethod
    def one_hot_special_needs(x):
        # x is pandas rows
        disability_list = ["tunadaksa", "tunawicara", "tunarungu", "tunanetra"]
        for i in disability_list:
            if i in x["special_needs"]:
                x[i] = 1
            else:
                x[i] = 0
        return x    
    
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