# -*- coding: utf-8 -*-
"""Stock_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14PTUg3qGNt_oDvzIHH0DLE0VwhA_Nj5W
"""

# Description: This program uses an artifitial neural network called long shot term(LSTm) 
#              to predict the closing stock price of a corporation(Apple Inc.) using the past 60 days stock price.

#Import Libreries
import math
import  pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df=web.DataReader('AAPL', data_source='yahoo', start='2012-01-01', end='2019-12-17')
#show data
df

#get the no. of rows and columns
df.shape

#visualize
plt.figure(figsize=(16,8))
plt.title('Close price history')
plt.plot(df['Close'])
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close price USD ($)', fontsize=18)
plt.show()

#create a new dataframe with only 'close' Column
data=df.filter(['Close'])
#convert dataframe to  array
dataset=data.values
#get the no. of rows to train on
training_data_len = math.ceil(len(dataset) * .8)
training_data_len

#scale the data
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)

scaled_data

#create the training dataset
#create the scaled training dataset
train_data = scaled_data[0:training_data_len,:]
#split the data into X and Y
x_train = []
y_train = []

for i in range(60, len(train_data)):
  x_train.append(train_data[i-60:i,0])
  y_train.append(train_data[i,0])
  if i<=61:
    print(x_train)
    print(y_train)
    print()

#convert the x_train and Y_train to np arrays
x_train, y_train = np.array(x_train), np.array(y_train)

#reshape
x_train = np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1))
x_train.shape

#Build the LSTM model
model= Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1],1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

#compile the model
model.compile(optimizer='adam', loss = 'mean_squared_error')

model.fit(x_train, y_train, batch_size=1, epochs=1)

#create the tetsing data set
#create new array 
test_data = scaled_data[training_data_len - 60 :, :]
#create the data sets s_test and y_test
x_test = []
y_test = dataset[training_data_len: ,:]
for i in range(60,len(test_data)):
  x_test.append(test_data[i-60:i,0])

#convert the data to a numpy array
x_test = np.array(x_test)

#reshape the data as LSTM accepts 3D
x_test = np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))

#get the models predicted price and values
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

#modell eveluations
#get the RMSE(Root Mean Square Error)
rmse = np.sqrt(np.mean( predictions - y_test)**2)
rmse

#plot the data
train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = predictions
#visualize the data
plt.figure(figsize=(16,8))
plt.title('Model')
plt.xlabel('Data', fontsize=18)
plt.ylabel('Close Price USD ($)', fontsize=18)
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Train', 'Val', 'Predictions'], loc = 'lower right')
plt.show()

#show the valod and predicted prices
valid

#get the quote9'
apple_quote = web.DataReader('AAPL', data_source='yahoo', start='2012-01-01', end='2019-12-17')
#create a new data frame
new_df = apple_quote.filter(['Close'])
#get last 60 days closing price value and convert the dataframe to an array
last_60_days = new_df[-60:].values
#scale the data to be between 0 and 1
last_60_days_scaled = scaler.transform(last_60_days)
#create an empty list
X_test = []
#append last 60 days
X_test.append(last_60_days_scaled)
#convert the X_test to np array
X_test =  np.array(X_test)
#reshape the data
X_test = np.reshape(X_test,(X_test.shape[0], X_test.shape[1],1))
#get the predicted scaled price
pred_price = model.predict(X_test)
#undo the scaling
pred_price = scaler.inverse_transform(pred_price)
print(pred_price)

#get the qupte
apple_quote = web.DataReader('AAPL', data_source='yahoo', start='2019-12-18', end='2019-12-18')
print(apple_quote['Close'])

