import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import time
from  predict_model.helpers.clear_screen import  clear_screen
def curve_fitting(data):
    # Proses data
    data = data.reset_index()
    # mengubah row date dari index jadi row biasa, agar tidak dihitung index
    x = np.arange(len(data)) #urutan angka dari 0,1,2,3,4 , ini menghasilkan array
    y = data['Close'].to_numpy().flatten() #mengubah row pandasr menjadi array numpy . flatten dipake buat memastikan array 1 dimensi supaya bisa di proses sama polyfit

    # Curve fitting (polinomial derajat 2)
    # ini membuat model persamaan kuadrat ax^2 + bx + c
    degree = 2
    coefs = np.polyfit(x, y, degree) #ungsi dari NumPy yang digunakan untuk mencari koefisien buat fungsi polinomial terbaik yang mendekati pola data
    poly = np.poly1d(coefs) #bikin fungsi rumusnya dari koefisien tadi

    # Plot hasil fitting
    x_pred = np.linspace(0, len(x) - 1, 100) #Membuat 100 titik rata dan halus antara 0 sampai hari terakhir.
    y_pred = poly(x_pred) # adalah hasil harga saham prediksi untuk setiap titik waktu x_pred.

    plt.figure(figsize=(10, 5))
    plt.plot(x, y, 'bo-', label='Data Asli')
    plt.plot(x_pred, y_pred, 'r--', label=f'Fit Polinomial derajat {degree}')

    plt.title(f'Curve Fitting Harga Saham ')
    plt.xlabel('Tanggal')
    plt.ylabel('Harga Penutupan')
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()

    while True:
        # Prediksi ke depan
        future_days = input("input berapa hari ke depan yang mau di prediksi (tekan enter untuk keluar) >>>")
        if future_days == "":
            print("\033[93mkembali ke menu pilihan model ...\033[0m")
            time.sleep(1)
            clear_screen()
            break
        try :

            if not future_days.isdigit():
                raise ValueError("Input hanya boleh angka!")
            future_days=int(future_days)
            print(f"\nPrediksi harga  untuk {future_days} hari ke depan:")
            # prediksi dari hari selanjutnya setelah data terakhir
            hari = len(x) - 1 + future_days
            harga_prediksi = poly(hari)
            print(f"Hari ke-{future_days} dari akhir data: ${harga_prediksi:.2f}")
            continue
        except ValueError as e:
            print(e)
            continue
