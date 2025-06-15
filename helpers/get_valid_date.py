from datetime import datetime

def get_valid_date(prompt):
    while True:
        user_input = input(prompt)
        try:
            # Coba parse tanggal
            valid_date = datetime.strptime(user_input, "%Y-%m-%d")
            return valid_date.strftime("%Y-%m-%d")  # kembalikan dalam format string yang rapi
        except ValueError:
            print("Format salah!, Gunakan format: yyyy-mm-dd (contoh: 2025-06-15)")

