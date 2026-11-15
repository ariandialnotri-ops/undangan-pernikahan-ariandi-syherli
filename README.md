# Undangan Pernikahan Digital — Rian & Syherli

Undangan pernikahan berbasis website (`index.html` + folder `assets/`), dioptimalkan untuk HP.
Gaya ilustrasi vintage Minangkabau: kertas krem, pita songket terakota, pepohonan, rumah gadang,
burung kolibri, kupu-kupu, dan bunga tropis (anggrek, heliconia, lili).

## Ilustrasi hidup
Ilustrasi sumber (768×1376) dipecah oleh `tools/layers.py` menjadi:
- `assets/base.webp` — latar (burung & kupu-kupu sudah dihapus/di-inpaint)
- `assets/treeL|treeR.webp` — pohon kiri/kanan, bergoyang tertiup angin
- `assets/flL|flM|flR.webp` — kelompok bunga bawah, bergoyang dengan ritme berbeda
- `assets/hb*.webp`, `bf*.webp`, `bd4.webp` — burung kolibri, kupu-kupu, burung kecil yang melayang/mengepak
- `assets/band.webp`, `florals.webp` — hiasan kepala & kaki tiap bagian
Ditambah kupu-kupu yang terbang menyeberang dan kelopak yang berjatuhan.

Regenerasi: `pip install opencv-python-headless pillow numpy` lalu
`python3 tools/layers.py sumber.png assets`.

## Fitur
- Sampul + nama tamu (`index.html?to=Nama%20Tamu` atau `index.html#Nama-Tamu`), animasi buka: kamera mendekat ke rumah gadang
- Musik kotak musik (dibuat di browser) dengan tombol on/off
- Tombol gulir bercerita; menu ☰ dan tombol RSVP muncul setelah cerita selesai
- Konten muncul halus saat digulir dan memudar turun saat digulir ke atas
- Ayat, mempelai, hitung mundur + Google Calendar, acara + peta, love story, galeri, RSVP ke WhatsApp, wedding gift (BCA/BRI)
- Menghormati `prefers-reduced-motion`

## Mengubah isi
Semua data ada di objek `WEDDING` di bagian bawah `index.html`. Bagian bertanda `[DUMMY]` masih data sementara.
