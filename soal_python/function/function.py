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