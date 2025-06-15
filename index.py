from  predict_model.menu.symbol_menu import printCompanyCsv
from  predict_model.menu.predict_menu import  predictMenu
import time
from  predict_model.helpers.clear_screen import  clear_screen
def showMenu():
    print("\033[93m====Menu Utama====\033[0m")
    print("1. cetak harga saham perusahaan")
    print("2. prediksi harga saham ke depan")
    print("3. keluar halaman")


def main():
    time.sleep(1)
    clear_screen()
    while True:
        showMenu()
        choice=int(input("\033[96mmasukkan pilihan anda >>>\033[0m"))

        if choice == 1:
            printCompanyCsv() #function buat print nama company
        elif choice == 2:
            predictMenu() #buat predik harga saham
        else:
            print("\033[92minput tidak ada di pilihan\033[0m")


if __name__ == "__main__":
    main()