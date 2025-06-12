from dotenv import load_dotenv
import os
import requests
from arima_model.api_services.get_stock_price import get_price
# load file env
load_dotenv()

api_key = os.getenv("API_KEY")


def getCompanyList(queryName=""):
    url =f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={queryName}&apikey={api_key}"  # Contoh API publik

    response = requests.get(url)  # Kirim GET request ke url

    if response.status_code == 200:
        data = response.json()  # Konversi respons ke format JSON
        if(data["bestMatches"]):
            for index,item in enumerate(data["bestMatches"],start=1):
                # print(item)
                print(f"{index}. symbol : {item["1. symbol"]} \n name:{item["2. name"]} \n region={item["4. region"]}")

            choice=int(input("masukkan angka perusahaan yang mau di cetak ke csv >>>"))

            selectedSymbol=data["bestMatches"][choice-1]

            get_price(selectedSymbol['1. symbol'])
        else:
            print("tidak ditemukan data")
    else:
        print("Gagal mengambil data. Kode:", response.status_code)

if __name__ == "__main__":
    getCompanyList()