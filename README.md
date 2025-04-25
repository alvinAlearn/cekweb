# cekweb
cek website

🔍 Deteksi CMS (WordPress, Joomla, Shopify, dll) secara manual dari tag, path, dan keyword

✉️ Ekstrak email dari HTML

💾 Tetap menyimpan hasil analisis ke file .txt

✅ Ambil Title + Meta Tag

✅ Ambil semua <link> (CSS, icon, canonical)

✅ Ambil semua <script> (JavaScript)

✅ Ambil favicon otomatis (jika ada)

✅ Ambil isi robots.txt

✅ Cek jika ada error page tersembunyi dalam HTML (500, 403, SQL error, PHP error, dll)

✅ Deteksi pesan MySQL error atau path disclosure

✅ Scan teks HTML dan komentar untuk petunjuk debug info, seperti stack trace atau file path


Langkah awal
pip install requests beautifulsoup4

jalankan script 
example : python3 cekweb.py
masukan url : https://example.com
==================================================================================
Untuk Versi GUI
==================================================================================
(+) Jika kamu pakai Linux (Debian/Ubuntu):

sudo apt update
sudo apt install python3-tk

(+) Jika kamu pakai Arch/Manjaro:

sudo pacman -S tk

(+) Jika kamu pakai Windows dengan Python bawaan dari python.org: tkinter biasanya sudah termasuk, tapi pastikan kamu tidak pakai venv minimalis tanpa GUI support.
