# Undangan Pernikahan Digital — Rian & Syherli

Undangan pernikahan berbasis website (`index.html` + folder `assets/`), dioptimalkan untuk HP.
Gaya ilustrasi vintage Minangkabau: kertas krem, pita songket terakota, pepohonan, rumah gadang,
burung kolibri, kupu-kupu, dan bunga tropis (anggrek, heliconia, lili).

## Ilustrasi hidup
Tampilan mengikuti rancangan "Pusaka Marawa" (Stitch): krem perkamen, merah marawa, emas songket; font Cinzel, Cormorant Garamond, Pinyon Script, Plus Jakarta Sans.
- `assets/base.webp` — ilustrasi utuh; semua burung & kupu-kupu bawaan dihapus (inpaint) oleh `tools/layers.py`
- `assets/wind.png` — peta angin (merah = pohon, hijau = bunga); gambar dilenturkan di WebGL sehingga pohon & bunga bergoyang tanpa dipotong
- `assets/curtainL|curtainR.webp` — tirai bunga & pohon untuk pembuka (dibuat `tools/curtain.py` dari ilustrasi yang sama);
  saat "Buka Undangan" ditekan, tirai membuka perlahan memperlihatkan rumah gadang
- Burung = siluet vektor hitam (SVG) dengan kepak sayap, terbang melintasi langit
- `assets/bf*.webp` — kupu-kupu (latar transparan) yang hanya melayang pelan di area bunga
Efek WebGL butuh halaman dibuka lewat http(s); bila dibuka sebagai file, ilustrasi tampil diam.

Regenerasi: `pip install opencv-python-headless pillow numpy`, lalu
`python3 tools/layers.py sumber.png assets` dan `python3 tools/curtain.py assets/base.webp assets`.

## Fitur
- Sampul dengan tirai bunga; nama tamu dari link (`?to=Nama` / `#Nama-Tamu`) otomatis mengisi kolom nama RSVP
- Musik kotak musik (dibuat di browser) dengan tombol on/off
- Tombol gulir bercerita; menu ☰ dan tombol RSVP muncul setelah cerita selesai
- Konten muncul halus saat digulir dan memudar turun saat digulir ke atas
- Ayat, mempelai, hitung mundur + Google Calendar, acara + peta, love story, galeri, RSVP ke WhatsApp, wedding gift (BCA/BRI)
- Menghormati `prefers-reduced-motion`

## Mengubah isi
Semua data ada di objek `WEDDING` di bagian bawah `index.html`. Bagian bertanda `[DUMMY]` masih data sementara.
