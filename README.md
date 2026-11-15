# Undangan Pernikahan Digital — Rian & Syherli

Undangan pernikahan berbasis website (`index.html` + folder `assets/`), dioptimalkan untuk HP.
Gaya ilustrasi vintage Minangkabau: kertas krem, pita songket terakota, pepohonan, rumah gadang,
burung kolibri, kupu-kupu, dan bunga tropis (anggrek, heliconia, lili).

## Ilustrasi hidup
Tampilan mengikuti rancangan "Pusaka Marawa" (Stitch): krem perkamen, merah marawa, emas songket; font Cinzel, Cormorant Garamond, Pinyon Script, Plus Jakarta Sans.
- `assets/base.webp` — ilustrasi utuh; semua burung & kupu-kupu bawaan dihapus (inpaint) oleh `tools/layers.py`
- `assets/wind.png` — peta angin (merah = pohon, hijau = bunga); gambar dilenturkan di WebGL sehingga pohon & bunga bergoyang tanpa dipotong
- `assets/flowers/*.png` — 16 bunga lepas berlatar transparan (dipotong satu-satu oleh `tools/flowers.py`, posisi di `flowers.json`)
- `assets/flowermap.png` — peta gerak per bunga (`tools/flowermap.py`): tiap bunga + tangkainya punya wilayah dan titik pangkal sendiri,
  lalu di WebGL masing-masing berayun kiri-kanan pelan dari pangkalnya dengan ritme berbeda, ditambah hembusan angin yang lewat
- Latar halaman isi: ilustrasi rumah gadang (`base.webp`) yang dipudarkan, tetap di tempat saat digulir dan bergerak sangat pelan
- Buket bunga (2 bunga dari `assets/flowers/` + kuncup + ranting berdaun SVG) menyembul dari BALIK sudut atas kartu; sudut seberangnya dihiasi rumpun ranting berdaun. Tangkai tersembunyi di belakang kartu, tumbuh saat kartu muncul, lalu berayun pelan. Ukuran menyesuaikan ruang kosong agar tidak menutupi teks
- Kawanan burung siluet hitam terbang bersamaan di latar halaman isi dan penutup
- Penutup menampilkan ilustrasi rumah gadang utuh (atap tidak terpotong)
- Musik: `assets/akad.mp3` — "Akad", Payung Teduh (hak cipta milik pencipta & label; dipakai atas keputusan pemilik undangan)
- Burung = siluet vektor hitam (SVG) dengan kepak sayap, terbang melintasi langit
- `assets/bf*.webp` — kupu-kupu (latar transparan) yang hanya melayang pelan di area bunga
Efek WebGL butuh halaman dibuka lewat http(s); bila dibuka sebagai file, ilustrasi tampil diam.

Regenerasi: `pip install opencv-python-headless pillow numpy`, lalu
`python3 tools/layers.py sumber.png assets`, `python3 tools/flowers.py sumber.png assets/flowers`, lalu
`python3 tools/flowermap.py assets/base.webp assets/flowers assets/flowermap.png`.

## Fitur
- Sampul ilustrasi hidup; nama tamu dari link (`?to=Nama` / `#Nama-Tamu`) otomatis mengisi kolom nama RSVP
- Musik kotak musik (dibuat di browser) dengan tombol on/off
- Tombol gulir bercerita; menu ☰ dan tombol RSVP muncul setelah cerita selesai
- Konten muncul halus saat digulir dan memudar turun saat digulir ke atas
- Ayat, mempelai, hitung mundur + Google Calendar, acara + peta, love story, galeri, RSVP ke WhatsApp, wedding gift (BCA/BRI)
- Menghormati `prefers-reduced-motion`

## Mengubah isi
Semua data ada di objek `WEDDING` di bagian bawah `index.html`. Bagian bertanda `[DUMMY]` masih data sementara.
