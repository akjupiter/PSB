import pandas as pd

class Restaurant:
    def __init__(self, spark_session, spark_dataframe):
        self.spark = spark_session
        spark_dataframe.createOrReplaceTempView("t_eats_restaurant_names")
        self.df_restaurant_id_name = self.spark.sql("select Restaurant_ID, Restaurant_Name from t_eats_restaurant_names")


    def get_favorite_restaurant(self):
        df_restaurant_name = self.df_restaurant_id_name.toPandas().drop(columns = ['Restaurant_ID'])
        df_restaurant_name = df_restaurant_name.Restaurant_Name.value_counts().to_frame()
        df_restaurant_name['Restaurant_Name_tmp'] = df_restaurant_name.index
        df_restaurant_name = df_restaurant_name.rename(columns={"Restaurant_Name": "Count"})
        df_restaurant_name = df_restaurant_name.rename(columns={"Restaurant_Name_tmp": "Restaurant Name"})
        df_restaurant_name = df_restaurant_name.sort_values(by='Count', ascending=True)
        return df_restaurant_name
