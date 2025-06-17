from dotenv import load_dotenv
import os
import time
from  predict_model.helpers.clear_screen import  clear_screen
import requests
from predict_model.api_services.get_stock_price import get_price
# load file env
load_dotenv()
from yahooquery import search

api_key = os.getenv("API_KEY")


def getCompanyList(queryName=""):
    while True:
        result = search(queryName)

        if result:
            if result["quotes"]:
                print(f"\033[92mlist hasil pencarian untuk {queryName} : \033[0m")
                for index, item in enumerate(result['quotes']):
                    print(
                        f"\033[36m{index + 1}.{item['longname'] if 'longname' in item else 'none'}\033[0m \nsimbol : {item['symbol'] or "none"} \nsektor  : {item['sector'] if 'sector' in item else 'none'}")


                choice = input("\033[96minput angka perusahaan yang mau di cetak ke csv (tekan enter untuk kembali ke input) >>>\033[0m")
                if choice == "":
                    return ""
                    break  # atau return kalau ingin kembali langsung
                try:
                    choice = int(choice)
                    if 0 < choice < len(result["quotes"]):
                        selectedSymbol = result["quotes"][choice - 1]
                        return selectedSymbol['symbol']
                    else:
                        print("input di luar list")
                        continue
                except ValueError:
                    print("input hanya boleh angka !")
                    continue
            else:
                print("tidak ditemukan data")
                break
        else:
            print("Gagal mengambil data")

