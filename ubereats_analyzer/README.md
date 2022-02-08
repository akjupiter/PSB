# UberEats Data Analyzer

### How to use

Request your UberEats datas in: 
+ https://help.uber.com/ubereats/article/request-a-copy-of-your-uber-data?nodeId=394400d4-20f2-4059-9451-765426cfaa57

You must put these files in this project folder "datas/":
+ eats_order_details.csv
+ trips_data.csv

Run the docker-compose command: 
```sh
docker-compose up -d
```

This will create the streamlit and fastapi images and start these services in 2 separate containers.

### Streamlit

Go to the webbrowser in this address: 
+ http://localhost:8501/


### FastAPI

This project is in developement.

But you can use some available features:
+ get data len
+ get data columns
+ get data dtypes

Exemple:

First you have to read your data:

+ docker exec -it fastapi bash -c "/code/client/app/request_fastapi.sh read csv_filename_without_extension"

And you can get the data len, columns and dtypes:

+ docker exec -it fastapi bash -c "/code/client/app/request_fastapi.sh len"
+ docker exec -it fastapi bash -c "/code/client/app/request_fastapi.sh columns"
+ docker exec -it fastapi bash -c "/code/client/app/request_fastapi.sh dtypes"
