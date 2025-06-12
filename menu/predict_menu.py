import  os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
folderName=os.getenv("FOLDER")


def readCsv(csv_files,choice):
    choiceFile=os.path.join(rf"{folderName}\data_csv",csv_files[choice])
    df=pd.read_csv(choiceFile)
    # ubah kolom tanggal jadi date time
    df["date"]=pd.to_datetime(df["tanggal"])
    # jadikan date jadi index utama
    df.set_index("date",inplace=True)

    ts=df["close price"]
    print(ts)


def predictMenu():
    #ambil semua file .csv dalam folder
    csv_file=[f for f in os.listdir(rf"{folderName}\data_csv") if f.endswith(".csv")]
    if not csv_file:
        print("belum ada file csv di folder")
        return
   # tampilkan csv yang tersedia
    print("daftar file csv :")
    for index,file in enumerate(csv_file):
        print(f"{index+1}.{file}")
   # menu pilihan
    while True:
           try:
               choice=int(input("pilih nomro fire yang ingin dibuka"))-1 #index mulai dari 0 maka butuh -1 agar pas
               if 0 <=choice < len(csv_file):
                   readCsv(csv_file,choice)
                   break
               else:
                   print("nomor tidak valid")
           except ValueError:
               print("masukkan hanya angka")
if __name__ == "__main__":
    predictMenu()