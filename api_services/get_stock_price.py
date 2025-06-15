import requests
import os
import csv
import requests
from dotenv import load_dotenv
import subprocess
import yfinance as yf
# load file env
load_dotenv()

api_key = os.getenv("API_KEY")
folderName=os.getenv("FOLDER")


def get_price(symbol,user_end_date,user_start_date):
    try:
        ticker = symbol
        data = yf.download(ticker, start=user_start_date, end=user_end_date)
        folder = fr"{folderName}\data_csv" #nama folder
        file_path = os.path.join(folder, f"data_{symbol}.csv") #file path nya
        os.makedirs(folderName, exist_ok=True) #kalo foldername buat folder name
        # simpan ke csv
        subprocess.Popen(f'explorer /select,"{file_path}"') #buka otomatis setelah di print csv
        data.to_csv(file_path)
        print("berhasil download csv", file_path)
    except:
        print("ada kesalahan")




