import json
import os
import requests
from bs4 import BeautifulSoup


def cari_informasi_web(keyword):
    """Fungsi untuk mencari informasi di website (Contoh: Wikipedia atau portal berita)"""
    print(f"[AI] Sedang mencari informasi tentang: {keyword}...")

    # Kita contohkan mencari ke Wikipedia Indonesia
    url = f"https://id.wikipedia.org/wiki/{keyword.replace(' ', '_')}"

    try:
        response = requests.get(url)

        # Jika website ditemukan
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Mengambil paragraf pertama sebagai informasi utama
            paragraf = soup.find_all("p")
            if paragraf:
                # Ambil teks paragraf pertama yang ada isinya
                for p in paragraf:
                    if len(p.text.strip()) > 20:
                        return p.text.strip()

            return "Halaman ditemukan, tapi teks tidak dapat dibaca."
        else:
            return f"Maaf, informasi tentang '{keyword}' tidak ditemukan di web."

    except Exception as e:
        return f"Gagal menyambung ke internet: {str(e)}"


def simpan_ke_database(keyword, hasil_pencarian):
    """Fungsi logika untuk menyimpan informasi ke file JSON"""
    file_nama = "informasi_ai.json"

    # 1. Baca data lama jika file sudah ada
    if os.path.exists(file_nama):
        with open(file_nama, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # 2. Masukkan informasi baru ke dalam logika data
    data[keyword] = {
        "informasi": hasil_pencarian,
        "waktu_simpan": "2026-06-02",  # Menandakan waktu update
    }

    # 3. Tulis kembali ke file JSON
    with open(file_nama, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"[AI] Sukses! Informasi '{keyword}' sudah disimpan ke {file_nama}.")


# --- Alur Jalannya Logika AI Python ---
if __name__ == "__main__":
    # Nanti input ini dikirim dari kode JavaScript (JS) Anda
    keyword_dicari = input("Masukkan info yang mau dicari AI: ")

    # AI mencari ke website
    hasil = cari_informasi_web(keyword_dicari)

    # AI menyimpan informasinya ke file untuk GitHub
    simpan_ke_database(keyword_dicari, hasil)
