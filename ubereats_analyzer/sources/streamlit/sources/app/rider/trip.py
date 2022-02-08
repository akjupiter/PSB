from datetime import datetime


class Trip:
    def __init__(self, spark_session, spark_dataframe):
        self.spark = spark_session
        self.spark_df = spark_dataframe
        spark_dataframe.createOrReplaceTempView("t_eats_order_details")

    def get_average_delivery_time(self):
        df_trips_data = self.spark_df.toPandas()
        df_trips_data['Dropoff_Time'] = df_trips_data['Dropoff_Time'].apply(lambda x : datetime.strptime(x, "%Y-%m-%d %H:%M:%S %z UTC"))
        df_trips_data['Request_Time'] = df_trips_data['Request_Time'].apply(lambda x : datetime.strptime(x, "%Y-%m-%d %H:%M:%S %z UTC"))
        df_trips_data['time'] = df_trips_data.apply(lambda x : int((x['Dropoff_Time'] - x['Request_Time']).total_seconds() / 60), axis = 1)
        df_trips_data = df_trips_data.rename(columns={"Distance_(miles)": "Distance (miles)"})
        return df_trips_data[['Distance (miles)', 'time']]
