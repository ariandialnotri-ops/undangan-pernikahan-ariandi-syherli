# Undangan Pernikahan Digital — Rian & Syherli

Undangan pernikahan berbasis website (`index.html` + `assets/`), dirancang untuk HP; di layar lebar tampil sebagai kolom HP.
Palet: putih, hitam, emas, dengan bunga merah. Ornamen Minangkabau: rumah gadang & pepohonan bergaya ukiran tinta, pita songket emas.
`tools/recolor.py assets` mewarnai ulang semua aset ilustrasi ke palet ini (jalankan setelah `scene.py`/`flowers.py`).
Font: Cinzel, Cormorant Garamond, Pinyon Script.

## Alur
1. **Sampul** — ilustrasi hidup, nama mempelai, tanggal, nama tamu (bila ada di link), tombol Buka Undangan.
2. **Buka** — kelopak memancar, musik mulai, kamera mendekat ke rumah gadang dengan cahaya hangat, lalu halaman meluncur ke Salam.
3. **Isi** — Salam & ayat, Kedua Mempelai, Rangkaian Acara + hitung mundur, Kisah Kami, Potret Kami, RSVP (WhatsApp), Pepatah, Penutup.
4. Tombol **gulir bercerita** (pil di bawah) membawa tamu bab demi bab; setelah selesai muncul bilah RSVP / Kado.

## Ilustrasi & gerak
- `tools/layers.py` → `assets/base.webp` (ilustrasi utuh tanpa burung/kupu bawaan; dipakai sebagai latar halaman isi).
- `tools/scene.py` → lapisan pembuka: `house.webp` (rumah gadang), `treeL.webp`, `treeR.webp`, `flowers.webp` (transparan).
  Saat halaman dibuka: rumah gadang masuk dengan zoom, pohon muncul dari kiri & kanan, bunga naik dari bawah,
  lalu semuanya berayun halus kiri-kanan (CSS, tanpa efek getar). Penutup memakai lapisan yang sama.
- Burung = siluet vektor hitam dengan kepak sayap, terbang berkelompok. Kupu-kupu (`assets/bf*.webp`) melayang pelan di area bunga.
- `assets/flowers/*.webp` — bunga lepas bertepi bersih (`tools/flowers.py`) untuk buket di balik sudut kartu.
- `assets/photos/` — foto mempelai (potret bulat di kartu mempelai, dua foto di bagian "Potret Kami").

## Musik
`assets/akad.mp3` — "Akad", Payung Teduh (hak cipta milik pencipta & label; dipakai atas keputusan pemilik undangan).

## Mengubah isi
Semua data ada di objek `WEDDING` di bagian bawah `index.html`. Isian `[..]` masih sementara; kolom kosong (`''`) tidak ditampilkan
(gala, suku, Instagram, foto, kota). Nama tamu: `index.html?to=Nama%20Tamu` atau `index.html#Nama-Tamu`.

## Membuat ulang aset
`pip install opencv-python-headless pillow numpy`, lalu
`python3 tools/layers.py sumber.png assets`, `python3 tools/scene.py assets/base.webp assets`, `python3 tools/flowers.py sumber.png assets/flowers`.

## Versi 2 — "Noir" (`v2/`)
Rancangan kedua yang berdiri sendiri: nuansa studio gelap mengikuti foto mempelai (hitam, abu, putih, emas, aksen merah),
gaya editorial dengan huruf Bodoni Moda, Jost, dan Monsieur La Doulaise.
- Sampul foto penuh dengan sorot lampu & bingkai tipis; saat dibuka, sampul terangkat seperti tirai.
- Pembuka foto dengan paralaks dan debu emas di sorot lampu; judul muncul dari balik garis; foto tersingkap dari hitam-putih ke warna.
- Mempelai, tanggal besar + hitung mundur, acara, kisah, RSVP (WhatsApp), amplop digital, penutup. Garis progres merah-emas di atas.
- Data di objek `WEDDING` dalam `v2/index.html`; foto di `v2/assets/`; musik memakai `assets/akad.mp3`.
