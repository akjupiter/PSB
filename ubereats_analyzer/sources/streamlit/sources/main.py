import streamlit as st
from app import Data
from app.eats import Order
from app.eats import Restaurant
from app.rider import Trip

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud

from pyspark.sql import SparkSession
from pyspark.sql.functions import *



st.sidebar.write("Adrien JUPITER")
st.sidebar.write("https://github.com/akjupiter")


st.title("Uber Eat Data Analyzer")

spark = SparkSession \
    		.builder \
    	        .appName("Python Spark SQL Streamlit") \
    	        .getOrCreate()


order_data = Data(spark, "/datas/eats_order_details.csv")
order = Order(order_data.get_spark_session(), order_data.get_spark_dataframe())

restaurant_data = Data(spark, "/datas/eats_restaurant_names.csv")
restaurant = Restaurant(restaurant_data.get_spark_session(), restaurant_data.get_spark_dataframe())

trip_data = Data(spark, "/datas/trips_data.csv")
trip = Trip(trip_data.get_spark_session(), trip_data.get_spark_dataframe())


##########################################################   CHART 1   ########################################################## 
#st.subheader('Annual & Monthly spendings')
st.metric("Total Uber Eat Spending", order.get_total_spending() + " €")

col1, col2, col3 = st.columns(3)

try:
	delta = order.get_year_delta(2) + " %"
except:
	delta = "0 %"

col1.metric(order.get_year(0), order.get_year_spending(0) + " €", order.get_year_delta(0) + " %")
col2.metric(order.get_year(1), order.get_year_spending(1) + " €", order.get_year_delta(1) + " %")
col3.metric(order.get_year(2), order.get_year_spending(2) + " €", delta)

try:
	delta = order.get_month_delta(2) + " %"
except:
	delta = "0 %"

col1.metric(order.get_month(0)[1] + " (" + order.get_month(0)[0] + ')', order.get_month_spending(0) + " €", order.get_month_delta(0) + " %")
col2.metric(order.get_month(1)[1] + " (" + order.get_month(1)[0] + ')', order.get_month_spending(1) + " €", order.get_month_delta(1) + " %")
col3.metric(order.get_month(2)[1] + " (" + order.get_month(2)[0] + ')', order.get_month_spending(2) + " €", delta)


##########################################################   CHART 2   ##########################################################
st.subheader('Average delivery time')
fig = px.line(trip.get_average_delivery_time().sort_values(by="Distance (miles)"), x="Distance (miles)", y="time", color="Distance (miles)")
st.plotly_chart(fig)


##########################################################   CHART 3   ##########################################################
st.subheader('Orders frequency')
fig = px.bar(order.get_orders_frequency(), x='date', y='count', color='count', color_continuous_scale=px.colors.sequential.RdBu)
st.plotly_chart(fig)


##########################################################   CHART 4   ##########################################################
st.subheader('Eating hours')
fig = px.pie(order.get_eating_hours(), values='values', names='labels', color='labels',
             color_discrete_map={'morning: 06-12h':'lightcyan',
                                 'afternoon: 12-18h':'cyan',
                                 'evening: 18-00h':'royalblue',
                                 'night: 00-06h':'darkblue'})
st.plotly_chart(fig)


##########################################################   CHART 5   ##########################################################
st.subheader('Favorite restaurants')
df = restaurant.get_favorite_restaurant()
fig = px.bar(df.tail(20), x="Count", y="Restaurant Name", orientation='h', color="Count", color_continuous_scale=px.colors.diverging.BrBG)
st.plotly_chart(fig)


##########################################################   CHART 6   ##########################################################
st.subheader('Favorite products')
text = order.get_favorite_products()
wordcloud = WordCloud(mode = "RGBA", background_color=None).generate(" ".join(text))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()
