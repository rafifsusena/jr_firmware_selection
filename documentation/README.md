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
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

* **Linux/macOS:**

```bash
source venv/bin/activate
```
Anda juga bisa langsung menjalankannya tanpa environtment variable, program python dibuat pada laptop dengan instalasi python 3.12.3.

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

```bash
python soal_python/soal3/soal3.py
python soal_python/soal4/soal4.py
```

Ikuti instruksi yang muncul pada terminal setelah program dijalankan.

---

Soal 5 (Soal Wokwi)

Soal 5 atau soal wokwi adalah program untuk melakukan publish nilai dari RTC DS1307 dan sensor DHT22. Program disimulasikan melalui wokwi.com, namun terdapat kendala seperti:

* Program utama lambat dijalankan

* Nilai DHT22 tidak muncul saat digabungkan dengan sistem (walau bisa jika sendiri)

Rekomendasi Alternatif: Jalankan melalui PlatformIO + Wokwi Extension

Install di VS Code:

* PlatformIO IDE

* Wokwi for VS Code

Buat Project Baru:

* PlatformIO sidebar → PIO Home → Open → New Project

* Nama bebas

* Board: Espressif ESP-32-S3-DevKitC-1

* Framework: Arduino

* Klik Finish

* Salin kode Wokwi ke folder src, sesuaikan nama file.

Tambahkan dua file di root project:

* diagram.json (isi dari wokwi)

* wokwi.toml:

[wokwi]
version = 1
firmware = '.pio\build\esp32-s3-devkitc-1\firmware.bin'
elf = '.pio\build\esp32-s3-devkitc-1\firmware.elf'

Atau bisa juga dengan melakukan download file pada : https://github.com/rafifsusena/jr_firmware_selection/tree/platform_io_wokwi

* Lalu pada platform I/O, user hanya perlu melakukan open project ke directory tempat file tersebut terunduh. 

* Build project (klik ikon centang di pojok bawah VS Code (setelah ikon rumah)).

* Tekan Ctrl+Shift+P → pilih Wokwi: Request a new license

* Ikuti instruksi, tekan GET YOUR LICENSE

* Lalu masukkan manual jika perlu dengan Wokwi: Manually Enter License Key

* Start simulasi: Ctrl+Shift+P → Wokwi: Start Simulation

---

Selamat mencoba!