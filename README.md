# Undangan Pernikahan Digital — Rian & Syherli

Undangan pernikahan berbasis website (`index.html` + folder `assets/`), dioptimalkan untuk HP.
Gaya ilustrasi vintage Minangkabau: kertas krem, pita songket terakota, pepohonan, rumah gadang,
burung kolibri, kupu-kupu, dan bunga tropis (anggrek, heliconia, lili).

## Ilustrasi hidup
Tampilan mengikuti rancangan "Pusaka Marawa" (Stitch): krem perkamen, merah marawa, emas songket; font Cinzel, Cormorant Garamond, Pinyon Script, Plus Jakarta Sans.
`tools/layers.py` mengolah ilustrasi sumber (768×1376) menjadi:
- `assets/base.webp` — ilustrasi utuh; burung & kupu-kupu dihapus lalu ditambal (inpaint)
- `assets/wind.png` — peta angin (merah = pohon, hijau = bunga). Gambar utuh dilenturkan di WebGL sesuai peta ini,
  jadi pohon & bunga bergoyang tanpa dipotong-potong
- `assets/hb*.webp`, `bf*.webp`, `bd4.webp` — burung kolibri, kupu-kupu, burung kecil dengan latar transparan bersih (2× resolusi)
Catatan: efek WebGL butuh halaman dibuka lewat http(s); bila dibuka langsung sebagai file, ilustrasi tampil diam.

Regenerasi: `pip install opencv-python-headless pillow numpy` lalu `python3 tools/layers.py sumber.png assets`.

## Fitur
- Sampul + nama tamu (`index.html?to=Nama%20Tamu` atau `index.html#Nama-Tamu`), animasi buka: kamera mendekat ke rumah gadang
- Musik kotak musik (dibuat di browser) dengan tombol on/off
- Tombol gulir bercerita; menu ☰ dan tombol RSVP muncul setelah cerita selesai
- Konten muncul halus saat digulir dan memudar turun saat digulir ke atas
- Ayat, mempelai, hitung mundur + Google Calendar, acara + peta, love story, galeri, RSVP ke WhatsApp, wedding gift (BCA/BRI)
- Menghormati `prefers-reduced-motion`

## Mengubah isi
Semua data ada di objek `WEDDING` di bagian bawah `index.html`. Bagian bertanda `[DUMMY]` masih data sementara.
