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
- `assets/branchL|branchR.webp` — ranting pohon dari ilustrasi (`tools/branches.py`) yang mengintip di tepi tiap halaman dan bergoyang pelan
- Sudut setiap kartu dihiasi rangkaian 3 bunga dari `assets/flowers/`; tiap bunga mekar masuk saat kartu muncul lalu bergoyang dengan ritmenya sendiri
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
