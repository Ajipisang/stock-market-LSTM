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
    # ubah index data mentah  ke date time agar bisa diolah
    data.index = pd.to_datetime(data.index)

    # ambil harga data close dari csv
    stock_close = data["Close"]

    # ambil nilai data close aja masukin ke variabel dataset
    dataset = stock_close.values

    # hitung panjang dari data training len, ini 80% dari data yang di pake
    training_data_len = int(np.ceil(len(dataset) * 0.80))

    # melakukan skalalisasi training data
    #membuat scaler (alat normalisasi data) yang akan mengubah data sebesar apa pun menjadi rentang antara 0 dan 1.
    #penting membuat scaler ini kecil agar si model belajar dengan lebih baik
    scaler = MinMaxScaler(feature_range=(0, 1))

    # dataset adalah array 1 dimensi
    #reshape(-1, 1) mengubahnya jadi array 2 dimensi, karena si minmaxscaler butuh array 2 dimensi
    # fit disini mempelajari data dan menghitung nilai min dan maxnya
    # Hitung min-max dari data, lalu transform langsung ubah datanya ke skala 0–1
    scaled_data = scaler.fit_transform(dataset.reshape(-1, 1))


    # data yang udah discaling lalu di masukin ke variabel training data buat melatih modelnya dalam mempelajari model yang ada
    #disini ada 80% data trainingnya

    # model lstm hanya nerima 2dimensi array dan data harus sudah dinormalisasikan dengan fit_transform tadi
    training_data = scaled_data[:training_data_len]



    X_train, Y_train = [], []

    # buat sliding window untuk harga saham (60 hari)
    # nanti dalam array index pertama - index array.length-1 adalah data asli, untuk index terakhir coba si model yang cari sendiri


    for i in range(60, len(training_data)):
        #Mulai dari indeks ke-60 karena butuh 60 hari data sebelumnya
        # x y dalam konteks ini masih 1 row, jadi bukan sumbu koordinat, x adalah data aktual, y adalah data yang bakal di predik sama si model
        X_train.append(training_data[i - 60: i, 0]) #ini hari dari 0 ke 59
        Y_train.append(training_data[i, 0]) #ini hari ke 61

    # Ini untuk mengubah list Python biasa menjadi array NumPy, agar bisa diproses lebih efisien di TensorFlow
    X_train, Y_train = np.array(X_train), np.array(Y_train)


    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))



    # membuat model dengan library sequensial
    #sequensial berarti model dibangun lapis per lapis
    model = keras.models.Sequential()


    # buat layer 1
    # tambahkan model dengan 64 unit neuron
    #return sequence artinya dia akan mengembalikan output dari tiap waktu untuk dilanjutkan ke layer berikutnya
    model.add(LSTM(64, return_sequences=True, input_shape=(X_train.shape[1], 1)))

    # buat layer 2
    # membuat layer baru dengan 64 neuron
    # return sequence karena hanya ingin mengembalikan 1 data terakhir aja
    # ini buat output dari layer ini berbentuk array 1 dimensi
    model.add(LSTM(64, return_sequences=False))

    # buat layer 3
    #Setiap neuron akan menerima semua output dari LSTM dan memprosesnya.
    # fungsi relu ini akan membuat model belajar pola linear
    model.add(keras.layers.Dense(128, activation="relu"))

    # buat layer 4
    # 10% neuron akan dimatikan secara acak saat proses mempelajari data agar model tidak overfitting
    # kalo overfitting model hanya menghapal data lama bukan mempelajari sehingga jika model disuruh untuk memprediksi akan jelek hasilnya
    model.add(keras.layers.Dropout(0.1)) #mencegah overfitting dengan toleransi 0.1

    # final layer
    # layer akhir dimana hasil prediksi di keluarkan
    # hanya butuh 1 neuron karena data prediksi yang dibutuhkan hanya 1 buah
    model.add(keras.layers.Dense(1))



    #Berhenti otomatis kalau model udah gak membaik setelah 5 kali epoch
    # yang di pantau adalah loss nya
    # loss menunjukan seberapa jauh hasil prediksi dengan training datanya
    early_stop = EarlyStopping(monitor='loss', patience=5)


    # Menurunkan nilai learning rate saat performa model stagnant
    # learning rate otomatis dari optimizer
    # factor akan menurunkan learning rate jadi 0.5x dari sebelumnya
    # learning rate tidak akan turun lebih kecil dari min_lr
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=0.0001)
    model.summary()

    # compile agar model bisa melakukan prediksi
    # compile ini adalah aturan belajar buat si model
    #optimizer ini berguna biar si model bisa memperbaiki diri kalo terjadi kesalahan prediksi
    # mse root mean square error adalah besar error yang terjadi saat model sedang memprediksi semakin kecil makin bagus
    #metrik ini digunakan untuk evaluasi
    model.compile(optimizer="adam", loss="mse", metrics=[RootMeanSquaredError(),"mae"])


    # proses dimana model belajar dari data data yang sudah dikasi
    # x train adalah input data yang mau di latih
    # y train adalah output prediksi
    # epochs disini Model akan mengulang seluruh data sebanyak 100 kali untuk belajar
    #	bach size berarti tiap 64 data dilatih bersama, lalu model update bobotnya sekali
    model.fit(X_train, Y_train, epochs=100, batch_size=64, callbacks=[early_stop,reduce_lr])

    # prep test data
    # menyiapkan data test setelah melatih model untuk mengecheck ke akuratan model

    # test data mengambil data yang udah di scaling - 60 karena panjang sliding windownya nanti bakal 60
    test_data = scaled_data[training_data_len - 60:]

    # y_test harga asli untuk membandingkan hasil predik
    # x_test akan diisi data window 60 hari untuk testing
    X_test, Y_test = [], dataset[training_data_len:]


    # loop buat sliding window
    for i in range(60, len(test_data)):
        #Ini mengambil window 60 data ke belakang dari data i, dan ambil kolom ke-0
        # (karena test_data bentuknya 2 dimensi hasil dari MinMaxScaler)
        X_test.append(test_data[i - 60:i, 0])

    # ubah x_test jadi numpy array agar mudah di olah
    X_test = np.array(X_test)


    # proses untuk mengubah bentuk array (reshape) menjadi format yang dimengerti oleh LSTM.
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    #model yang sudah dilatih akan disuruh melakukan prediksi berdasarkan nilai X_test , hasilnya nilai dalam bentuk scaled
    predictions = model.predict(X_test)

    #ini mengembalikan nilai yang tadi di scale jadi kecil balik ke harga saham normal
    predictions = scaler.inverse_transform(predictions)

    # buat plotting
    train = data[:training_data_len]
    test = data[training_data_len:]

    test = test.copy()

    # ini membuat kolom baru pada test dengan isi nya adalah predictions
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
            # autoregresive forecasting , prediksi berulang berdasarkan prediksi sebelumnya
            for i in range(int(user_input)):
                #memakai window (data terakhir) untuk memprediksi harga satu hari ke depan (hari ke-1 dari sekarang)
                #Hasil model.predict() adalah array 2D , dan [0][0] dipakai untuk ambil nilai prediksi scalar-nya.
                pred = model.predict(input_seq)[0][0]
                # ini akan mengeser window kedepan sebanyak user input  dan menambahkan prediksi baru di akhir window
                input_seq = np.append(input_seq[:, 1:, :], [[[pred]]], axis=1)

            # ini membalik harga yang di scale ke harga normal
            pred_day = scaler.inverse_transform(np.array([[pred]]))[0][0]
            print(
                f"Prediksi harga saham pada hari ke-{user_input} setelah data terakhir: \033[36m${pred_day:.2f}\033[0m")
            continue
        except ValueError as e:
            print(e)
            continue



