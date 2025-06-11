from  arima_model.api_services.get_symbol import getCompanyList

def choiceToStop():
    choice=input("lanjut ? y/n")
    if choice == "y":
        return True
    elif choice=="n":
        return  False
    else:
        print("mohon masukin nilai yang valid")
def printCompanyCsv():
    while True:
        queryName=str(input("masukkan nama perusahaan  >> (mis : meta)"))

        if(len(queryName) !=0):
            getCompanyList(queryName)
        else:
            print("mohon masukkan input yang valid")
            continue
        if not choiceToStop():
            break

if __name__ == "__main__":
    printCompanyCsv()