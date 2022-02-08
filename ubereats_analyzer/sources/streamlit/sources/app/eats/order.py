from datetime import datetime

from pyspark.sql.functions import udf,col
from pyspark.sql.types import StringType
from pyspark.ml.feature import RegexTokenizer
from pyspark.sql.types import IntegerType
from pyspark.ml.feature import StopWordsRemover

import pandas as pd

import re

class Order:
    def __init__(self, spark_session, spark_dataframe):
        self.spark = spark_session
        spark_dataframe.createOrReplaceTempView("t_eats_order_details")
        self.df_wordcloud = self.spark.sql("select Restaurant_ID, Item_Name from t_eats_order_details")
        self.df_order_price = self.spark.sql("select year(Order_Time) as year, \
                                                    month(Order_Time) as month, \
                                                    weekofyear(Order_Time) as week, \
                                                    Order_Id, \
                                                    Order_Price \
                                                from t_eats_order_details \
                                                    group by year, month, week, Order_ID, Order_Price \
                                                    order by year desc, month desc, week desc")
        self.df_order_price.createOrReplaceTempView("t_eats_order_price")
        self.df_total_spend = self.spark.sql("select sum(Order_Price) from t_eats_order_price")
        self.df_years_spending = self.spark.sql("select year, sum(Order_Price) as spending \
                                    			    from t_eats_order_price \
                                        		        group by year \
                                          		        order by year desc")
        self.df_months_spending = self.spark.sql("select year, month, sum(Order_Price) as spending \
                                    			    from t_eats_order_price \
                                        		        group by year, month \
                                          		        order by year desc, month desc")
        self.df_count_order_month = self.spark.sql("select year, month, count(Order_Price) as spending \
                                                     from t_eats_order_price \
                                                        group by year, month \
                                                        order by year desc, month desc")
        self.df_order_time = self.spark.sql("select Order_Time from t_eats_order_details")
    

    def get_year(self, index):
        return str(self.df_years_spending.collect()[index][0])

    def get_month(self, index):
        year = str(self.df_months_spending.collect()[index][0])
        month_number = str(self.df_months_spending.collect()[index][1])
        datetime_object = datetime.strptime(month_number, "%m")
        return (year, datetime_object.strftime("%B"))
 
    def get_total_spending(self):
        return str(round(self.df_total_spend.collect()[0][0], 2)) 
   
    def get_year_spending(self, row_index):
        return str(round(self.df_years_spending.collect()[row_index]["spending"], 2))

    def get_month_spending(self, row_index):
        return str(round(self.df_months_spending.collect()[row_index]["spending"], 2))

    def get_week_spending(self, row_index):
        return str(round(self.df_weeks_spending.collect()[row_index]["spending"], 2))

    def get_year_delta(self, row_index):
        return str(round((self.df_years_spending.collect()[row_index][1] - self.df_years_spending.collect()[row_index + 1][1]) / self.df_years_spending.collect()[row_index + 1][1] * 100, 2))

    def get_month_delta(self, row_index):
        return str(round((self.df_months_spending.collect()[row_index][2] - self.df_months_spending.collect()[row_index + 1][2]) / self.df_months_spending.collect()[row_index + 1][2] * 100, 2))

    def get_orders_frequency(self):
        date_concat = udf(lambda x, y : datetime(x, y, 1).strftime('%Y-%m'), StringType())
        df_tmp = self.df_count_order_month.withColumn("date", date_concat(col("year"), col("month")))
        df_tmp = df_tmp.drop('year', 'month')
        return df_tmp.toPandas().rename(columns={'spending': 'count'})
         
    def get_eating_hours(self):
        morning = 0
        afternoon = 0
        evening = 0
        night = 0
        df = self.df_order_time.toPandas()
        df['Order_Time'] = df['Order_Time'].apply(lambda x : datetime.strptime(x, "%Y-%m-%d %H:%M:%S %z UTC"))
        df['hour'] = df['Order_Time'].apply(lambda x : x.hour)
        hours_l = df['hour'].to_list()
        for i in hours_l:
            if 6 <= i < 12:
                morning = morning + 1
            elif 12 <= i < 18:
                afternoon = afternoon + 1
            elif 18 <= i < 24:
                evening = evening + 1
            else:
                night = night + 1
        labels = ['morning: 06-12h', 'afternoon: 12-18h', 'evening: 18-00h', 'night: 00-06h']
        values = [morning, afternoon, evening, night]
        d = {'labels': labels, "values": values}
        df = pd.DataFrame(data=d)
        return df

    def get_favorite_products(self):
        regexTokenizer = RegexTokenizer(inputCol="Item_Name", outputCol="words", pattern="\\W")
        countTokens = udf(lambda words: len(words), IntegerType())
        regexTokenized = regexTokenizer.transform(self.df_wordcloud)
        sdf_tokenised = regexTokenized.select("Item_Name", "words").withColumn("tokens", countTokens(col("words")))
        remover = StopWordsRemover(inputCol="words", outputCol="filtered", stopWords=StopWordsRemover.loadDefaultStopWords("french"))
        df_stop_words = remover.transform(sdf_tokenised).toPandas()
        df_stop_words = df_stop_words.explode("filtered").groupby("filtered").count()
        df_stop_words['filtered'] = df_stop_words.index
        text = []
        for i in df_stop_words['filtered']:
            x = re.search("^[A-Z]|^[a-z]", i)
            if x and len(i) > 3:
                text.append(i)
        return (text)        
