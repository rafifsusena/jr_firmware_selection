def get_user_input_series():
    while True:
        user_input = input("Masukkan 10 angka, dipisahkan dengan spasi: ")
        tokens = user_input.strip().split()

        # Periksa jumlah elemen
        if len(tokens) == 0:
            return None
        elif len(tokens) != 10:
            print("❌ Jumlah angka tidak tepat. Harus 10 angka yang dipisahkan oleh spasi.\n")
            continue

        try:
            # Coba konversi semua elemen ke float
            number_list = [float(token) for token in tokens]
            return number_list
        except ValueError:
            print("❌ Input mengandung nilai yang bukan angka. Harap hanya masukkan angka yang valid.\n")

def getSamplingInterval()->float:
    while True:
        sampling_interval = input("Input the sampling interval (in sec, > 0): ")
        try:
            interval = float(sampling_interval)
            if interval>0:
                return interval
            else:
                print("Interval must be above 0, try again ...")
        except ValueError:
            print("Invalid input, must be a number and above 0")


def getCityName()->str:
    return str(input("Name of the city : "))

def getCandidateName()->str:
    name = input("Masukkan nama kandidat (satu kata, tanpa spasi): ").strip()
    if " " in name or not name:
        print("Nama kandidat harus satu kata tanpa spasi dan tidak boleh kosong.")
        return
    return name