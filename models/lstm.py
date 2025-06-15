from tensorflow.python.keras.metrics import RootMeanSquaredError
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
from  keras.layers import  LSTM,Dense
from tensorflow.keras.callbacks import EarlyStopping,ReduceLROnPlateau
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from  predict_model.helpers.clear_screen import  clear_screen
import random
import tensorflow as tf
import os
def set_seed(seed=123):
    np.random.seed(seed)
    random.seed(seed)
    tf.random.set_seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)

# Pasang seed dulu
set_seed(128)

def predict_using_lstm(data):
    # ubah data ke date time dan buat date fillter
    data.index = pd.to_datetime(data.index)

    # persiapan untuk sekuensial model
    stock_close = data["Close"]
    # conver ke numpy array
    dataset = stock_close.values
    training_data_len = int(np.ceil(len(dataset) * 0.80))
    print(training_data_len)

    # preprocessing stages

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset.reshape(-1, 1))
    training_data = scaled_data[:training_data_len]

    X_train, Y_train = [], []

    # buat sliding window untuk harga saham (60 hari)
    for i in range(60, len(training_data)):
        X_train.append(training_data[i - 60: i, 0])
        Y_train.append(training_data[i, 0])

    X_train, Y_train = np.array(X_train), np.array(Y_train)

    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))



    # membuat model
    model = keras.models.Sequential()

    # buat layer 1 dari lstm
    model.add(LSTM(64, return_sequences=True, input_shape=(X_train.shape[1], 1)))

    # buat layer 2
    model.add(LSTM(64, return_sequences=False))

    # buat layer 3
    model.add(keras.layers.Dense(128, activation="relu"))

    # buat layer 4
    model.add(keras.layers.Dropout(0.1))

    # final layer
    model.add(keras.layers.Dense(1))

    early_stop = EarlyStopping(monitor='loss', patience=5)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=0.0001)
    model.summary()
    model.compile(optimizer="adam", loss="mse", metrics=[RootMeanSquaredError(),"mae"])
    model.fit(X_train, Y_train, epochs=100, batch_size=64, callbacks=[early_stop,reduce_lr])

    # prep test data
    test_data = scaled_data[training_data_len - 60:]
    X_test, Y_test = [], dataset[training_data_len:]

    for i in range(60, len(test_data)):
        X_test.append(test_data[i - 60:i, 0])

    X_test = np.array(X_test)

    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # Lakukan prediksi pada data test
    predicted = model.predict(X_test)

    # buat prediksi
    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions)

    # buat plotting
    train = data[:training_data_len]
    test = data[training_data_len:]

    test = test.copy()

    test["Predictions"] = predictions

    plt.figure(figsize=(12, 8))
    plt.plot(train.index, train["Close"], label="train data (actual)", color="blue")
    plt.plot(test.index, test["Close"], label="test data (actual)", color="green")
    plt.plot(test.index, test["Predictions"], label="prediksi", color="red")
    plt.title("prediksi")
    plt.xlabel("date")
    plt.ylabel("close")
    plt.legend()

    plt.figure(figsize=(12, 8))
    plt.plot(test.index, test["Close"], label="test data (actual)", color="green")
    plt.plot(test.index, test["Predictions"], label="prediksi", color="red")
    plt.title("prediksi vs realita ")
    plt.xlabel("date")
    plt.ylabel("close")
    plt.legend()
    plt.show()

    last_60_days = scaled_data[-60:]
    input_seq = last_60_days.reshape(1, 60, 1)


    while True:
        user_input = input("\033[96minput hari ke berapa yang mau di prediksi (ketik enter untuk exit) >>>\033[0m")
        if user_input =="":
            print("\033[93mkembali ke menu pilihan model...\033[0m")
            time.sleep(1)
            clear_screen()
            break
        try:
            if not user_input.isdigit():
                raise ValueError("Input hanya boleh angka!")
            for i in range(int(user_input)):
                pred = model.predict(input_seq)[0][0]
                # Geser window dan tambahkan prediksi
                input_seq = np.append(input_seq[:, 1:, :], [[[pred]]], axis=1)

            pred_day = scaler.inverse_transform(np.array([[pred]]))[0][0]
            print(
                f"Prediksi harga saham pada hari ke-{user_input} setelah data terakhir: \033[36m${pred_day:.2f}\033[0m")
            continue
        except ValueError:
            print("input hanya boleh berbentuk anga !")
            continue



