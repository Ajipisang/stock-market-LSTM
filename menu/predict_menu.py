import  os
from  predict_model.helpers.read_csv import readCsv
import time
from  predict_model.helpers.clear_screen import  clear_screen
from dotenv import load_dotenv
load_dotenv()
from predict_model.models.lstm import predict_using_lstm
from predict_model.models.curve_fitting import  curve_fitting
folderName=os.getenv("FOLDER")

def choice_prediction_model(csv_file):
    while True:
        print("\033[93m=== list model ====\033[0m")
        print("1 . model LSTM (direkomendasikan)")
        print("2.  model curve fitting")
        print("3.  kembali ke menu csv file")
        input_user=int(input("\033[96mkembali ke halaman utama >>>\033[0m"))

        try:
            if  input_user:
                if input_user==1:
                    predict_using_lstm(csv_file)
                elif input_user==2:
                    curve_fitting(csv_file)
                elif input_user == 3:
                    print(" mkembali ke menu csv...\033[0m")
                    clear_screen()
                    time.sleep(1)
                    break
            else :
                time.sleep(1)
                clear_screen()
                print("\033[91minput tidak ada di pilihan ... !!\033[0m")
                continue
        except ValueError:

            print("\033[91minput hanya bernilai angka\033[0m")
            continue


def predictMenu():

    while True:
       try:
           # ambil semua file .csv dalam folder
           csv_file = [f for f in os.listdir(rf"{folderName}\data_csv") if f.endswith(".csv")]
           if not csv_file:
               print("\033[91mbelum ada file csv di folder\033[0m")
               return
           # tampilkan csv yang tersedia
           print("\033[93m====daftar file csv====\033[0m")
           for index, file in enumerate(csv_file):
               print(f"{index + 1}.{file}")

           # menu pilihan
           print(f"{len(csv_file) + 1}.keluar dari menu prediksi")
           choice = int(input("\033[96mpilih nomor file yang ingin dibuka >>\033[0m")) - 1  # index mulai dari 0 maka butuh -1 agar pas

       except ValueError:
           print("\033[91m INPUT HARUS BERUBAH ANGKA\033[0m")
           continue
       if 0 <= choice < len(csv_file):
           csv_file=readCsv(csv_file, choice)
           choice_prediction_model(csv_file)
       elif choice == len(csv_file):
           print("\033[94mkembali ke menu utama...\033[0m")
           time.sleep(1)
           clear_screen()
           break
       else:

           print("\033[91mINPUT TIDAK ADA DI PILIHAN!\033[0m")
           time.sleep(1)
           clear_screen()
