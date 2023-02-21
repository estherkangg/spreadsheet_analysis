import pandas as pd
import numpy as np
import datetime
import csv

df = pd.read_csv("data/citibike.csv")

# slicing every 1200th row 
df = df[::1200]

# deleting the ride_id and start/end station id columns bc unecessary 
df.drop(columns=["ride_id", "start_station_id", "end_station_id"], inplace = True) 

# delete start lat/long becuz too much
df.drop(columns=["start_lat", "start_lng", "end_lat", "end_lng"], inplace = True) 

# changing the start and end times to datetimes so easy for pandas
df[["started_at", 'ended_at']] = df[['started_at', "ended_at"]].apply(pd.to_datetime)

# sorting started_at column by ascending date
df.sort_values(by= ["started_at", "ended_at"], inplace = True)

# stripping time from the date in both start/end columns
df["started_at"].dt.strftime('%H:%M:%S')
df["ended_at"].dt.strftime('%H:%M:%S')

# find trip duration through difference and make a new column
df['difference'] = df["ended_at"] - df["started_at"]

# made a new column with the time difference in seconds
df['difference in seconds'] = df['difference'].dt.total_seconds().astype(int)

# drop rows that have less than 60 seconds and over 24hrs worth of secs
df.drop(df[df['difference in seconds'] >= 86400].index, inplace = True)
df.drop(df[df['difference in seconds'] <= 60].index, inplace = True)

# finding what is more common classic or ebike
print(df['rideable_type'].mode()[0])

# finding which is most common start station
print(df['start_station_name'].mode()[0])

# finding which is most common end station
print(df['end_station_name'].mode()[0])

# finding member or casual more common
print(df['member_casual'].mode()[0])

# make and write to a new clean file
n = open("data/clean_data.csv", 'w') 
df.to_csv("data/clean_data.csv", index=False)
n.close()

# import original data to markdown
df2 = pd.read_csv("data/citibike.csv")
df3 = df2.head(20)
df3.to_markdown("README.md")

df.info()
