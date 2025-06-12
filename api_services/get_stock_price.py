import requests
import os
import csv
import requests
from dotenv import load_dotenv
import subprocess
# load file env
load_dotenv()

api_key = os.getenv("API_KEY")
folderName=os.getenv("FOLDER")
def printCsv(data,symbol="meta"):
    folder = fr"{folderName}\data_csv"
    file_path = os.path.join(folder, f"low_data_{symbol}.csv")

    # Buat folder jika belum ada
    os.makedirs(folder, exist_ok=True)
    rows=[]
    # ambil nilai tanggal dan nilai harga terendah
    for date,detail in data.items():
        openPrice=detail["1. open"]
        highPrice=detail["2. high"]
        lowPrice=detail["3. low"]
        closePrice=detail["4. close"]
        rows.append([date,openPrice,highPrice,lowPrice,closePrice])
    rows.sort()
    # Tulis ke file CSV
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["tanggal", "open price","high price","low price","close price"])  # Header
        writer.writerows(rows)

    subprocess.Popen(f'explorer /select,"{file_path}"')
    print("berhasil cetak csv")


def get_price(symbol="test"):
    url=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response=requests.get(url)

    if response.status_code==200:
        print(response)
        rawData=response.json()

        data=rawData["Time Series (Daily)"]
        printCsv(data,symbol)

    else:
        print("ada masalah di server")



if __name__=="__main__":
    get_price()