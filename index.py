
def showMenu():
    print("pilih menu")
    print("1. cari simbol perusahaan")
    print("2. cetak harga saham perusahaan")
    print("3. prediksi harga saham ke depan")
    print("4. keluar halaman")


def main():
    while True:
        showMenu()
        choice=int(input("masukkan pilihan anda >>>"))

        if choice == 1:
            print("buat pilihan 1")
        elif choice == 2:
            print("buat pilihan 2")
        elif choice == 3:
            print("buat pilihan 3")
        else:
            print("ga ada di pilihan")


if __name__ == "__main__":
    main()