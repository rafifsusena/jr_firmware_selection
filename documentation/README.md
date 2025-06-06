# JR\_FIRMWARE\_SELECTION

Ikuti langkah-langkah berikut untuk menjalankan program dengan benar. Sebelum menjalankan semua program yang ada, silahkan download terlebih dahulu repository ini lalu extract file atau clone repository pada komputer anda.

Pada script editor seperti VS Code, klik File>>Open Folder atau Ctrl+K+O lalu cari lokasi dimana anda menyimpan unduhan file atau clone repository, buka filder JR_FIRMWARE_SELECTION.

---

## 📆 Persiapan Awal

1. **Masuk ke folder proyek:**

```bash
cd JR_FIRMWARE_SELECTION
```

2. **Buat virtual environment:**

```bash
python -m venv venv
```

3. **Aktifkan virtual environment:**

* **Windows:**

```bash
venv\Scripts\activate
```

* **Linux/macOS:**

```bash
source venv/bin/activate
```

4. **Install dependensi yang dibutuhkan:**

```bash
pip install -r requirements.txt
```

---

## ✅ Menjalankan Program

### Soal 1

Untuk menjalankan soal 1, gunakan perintah berikut di terminal:

```bash
python -m soal_python.soal1.soal1
```

* Anda akan diminta memasukkan 10 angka acak yang dipisahkan oleh spasi.
* Jika Anda menekan **Enter** tanpa mengisi angka, maka program akan otomatis meng-generate angka secara acak.

---

### Soal 2

1. Jalankan program API:

```bash
python soal_python/soal2/soal2.py
```

2. Untuk menguji jalannya API secara otomatis:

```bash
python soal_python/soal2/test_api.py
```

3. **(Opsional)** Pengujian manual menggunakan ekstensi Thunder Client:

* Buka **VS Code** dan instal ekstensi **Thunder Client**.
* Klik logo Thunder Client di sidebar.
* Klik `New Request`.
* Ganti metode dari `GET` menjadi `POST`.
* Isi URL dengan IP dan port yang tampil di terminal saat Anda menjalankan `soal2.py`.
* Klik tab `Body` > pilih `JSON`.
* Masukkan data JSON yang sesuai.
* Klik `Send` untuk mengirim request.

---

### Soal 3 dan Soal 4

Untuk menjalankan soal 3 dan soal 4, cukup jalankan file Python langsung:

* **Melalui terminal VS Code:**

  * Klik kanan pada file `soal3.py` atau `soal4.py`
  * Pilih `Run Code` atau `Run Python File in Terminal`

* **Atau jalankan manual:**

```bash
python soal_python/soal3/soal3.py
python soal_python/soal4/soal4.py
```

Ikuti instruksi yang muncul pada terminal setelah program dijalankan.

---

Selamat mencoba!