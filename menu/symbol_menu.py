from  predict_model.api_services.get_symbol import getCompanyList
import time
from  predict_model.helpers.clear_screen import  clear_screen
from  predict_model.helpers.get_valid_date import get_valid_date
from  predict_model.api_services.get_stock_price import get_price
def choiceToStop():
    choice=input("lanjut ke menu utama ? y/n")
    if choice == "y":

        return False
    elif choice=="n":
        return  True
    else:
        print("mohon masukin nilai yang valid")
def printCompanyCsv():
    time.sleep(1)
    clear_screen()
    while True:
        queryName=str(input("input masukkan nama perusahaan  >> (mis : meta) (tekan exit untuk keluar)"))
        if queryName =="":
            print("kembali ke menu utama ...")
            break
        if(len(queryName) !=0):
            company_symbol=getCompanyList(queryName)
            if company_symbol != "":
                user_start_date = get_valid_date("Input tanggal mulai (yyyy-mm-dd) >>> ")
                user_end_date = get_valid_date("Input tanggal akhir(yyyy-mm-dd) >>> ")
                get_price(company_symbol, user_start_date=user_start_date, user_end_date=user_end_date)
            else:
                continue
        else:
            print("mohon masukkan input yang valid")
            continue
        if not choiceToStop():
            print("\033[93mKembali ke menu utama...\033[0m")
            time.sleep(1)
            clear_screen()
            break

