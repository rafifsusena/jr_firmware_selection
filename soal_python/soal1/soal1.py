'''
Writing rule :  variable, file name = snake_case
                constant = UPPER_CASE
                func/method = camelCase
                class = PascalCase
                string = double quote
                function gap = 2 blank line

1.  Buat fungsi untuk mencari nilai maks, min, rata" dan modus
    dari list angka dg panjang 10 tanpa menggunakan fungsi bawaan.
    Output :    ●	Value : (List Value)
                ●	Nilai Maksimum : (Value Maksimum)
                ●	Nilai Minimum : (Value Minimum)
                ●	Nilai Rata-Rata : (Value Rata-Rata)
                ●	Nilai Modus : (Value Modbus)
'''

from random import randint #generate random number for the input list
from soal_python.function.function import get_user_input_series

class CalcStat():
    def __init__(self, input_list: list):
        self.input_list = input_list

    
    def getResult(self)->None:
        mean, list_len = self.getMean()
        min_num, max_num = self.getMinMax()
        modes = self.getMode()

        print("●	Value \t\t: ", end="")
        print(*self.input_list, sep=", ")
        print(f"●	Nilai Maksimum \t: {max_num}")
        print(f"●	Nilai Minimum \t: {min_num}")
        print(f"●	Nilai Rata-Rata : {mean}")
        print(f"●	Nilai Modus \t: " + ", ".join(map(str, modes)))


    def getMean(self)->tuple:
        mean, list_len = 0, 0
        for i in self.input_list:
            mean+=i
            list_len+=1
        mean /= list_len
        return mean, list_len
    
    
    def getMinMax(self)->tuple:
        min_val, max_val = None, None
        for i in self.input_list:
            if min_val == None or max_val == None:
                min_val = i
                max_val = min_val
            if i < min_val:
                min_val = i
            if i > max_val:
                max_val = i
        
        return min_val, max_val
    
    
    def getMode(self)->list:
        freq = {}
        for val in self.input_list:
            if val in freq:
                freq[val] += 1
            else:
                freq[val] = 1

        # Cari frekuensi maksimum
        max_freq = 0
        for key in freq:
            if freq[key] > max_freq:
                max_freq = freq[key]

        # Kumpulkan semua angka dengan frekuensi maksimum
        modes = []
        for key in freq:
            if freq[key] == max_freq:
                modes.append(key)
        
        return modes
    

def main()->None:
    angka = get_user_input_series()
    if angka == None:
        print("✅ Hasilkan angka acak", end="\n\n")
        input_val = [randint(0, 100) for n in range(10)]
    else:
        print("✅ Deret angka yang dimasukkan:", angka, end="\n\n")
        input_val = angka

    CalcResult = CalcStat(input_list=input_val)
    CalcResult.getResult()


if __name__=="__main__":
    main()