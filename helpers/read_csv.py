import  os
import pandas as pd
from dotenv import load_dotenv


load_dotenv()

folderName=os.getenv("FOLDER")

def readCsv(csv_files,choice):
    choiceFile = os.path.join(rf"{folderName}\data_csv", csv_files[choice])

    # Lewati baris kedua (META), baca CSV
    df = pd.read_csv(
        choiceFile,
        skiprows=[1, 2],  # Ini penting!
        index_col=0,  # 'Price' (alias kolom tanggal) dijadikan index
        parse_dates=True,  # Parsing kolom index jadi datetime
        # date_parser=lambda x: datetime.strptime(x, "%Y-%m-%d")  # Format tanggal
    )

    df.dropna(inplace=True)  # Bersihkan baris kosong
    df.sort_index(inplace=True)  # Urutkan berdasarkan tanggal (optional)
    return  df