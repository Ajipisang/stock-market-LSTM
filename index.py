from  menu.symbol_menu import printCompanyCsv
from  menu.predict_menu import  predictMenu
def showMenu():
    print("pilih menu")
    print("1. cetak harga saham perusahaan")
    print("2. prediksi harga saham ke depan")
    print("3. keluar halaman")


def main():
    while True:
        showMenu()
        choice=int(input("masukkan pilihan anda >>>"))

        if choice == 1:
            printCompanyCsv()
        elif choice == 2:
            predictMenu()
        else:
            print("ga ada di pilihan")


if __name__ == "__main__":
    main()