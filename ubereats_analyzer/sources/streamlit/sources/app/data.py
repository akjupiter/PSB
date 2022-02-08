class Data:
    def __init__(self, spark_session, uber_csv_data_file):
        self.spark = spark_session
        self.spark_df = self.spark \
		.read \
		.option("header","true") \
		.csv(uber_csv_data_file)
        for s in self.spark_df.columns:
     	        self.spark_df = self.spark_df.withColumnRenamed(s, s.replace(' ', '_'))
    
    def get_spark_session(self):
        return self.spark
 
    def get_spark_dataframe(self):
        return self.spark_df
