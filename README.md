# Undangan Pernikahan Digital — Rian & Syherli

Undangan pernikahan berbasis website (`index.html` + `assets/`), dirancang untuk HP; di layar lebar tampil sebagai kolom HP.
Gaya "Pusaka Marawa": perkamen, merah marawa, emas songket, ilustrasi vintage rumah gadang.
Font: Cinzel, Cormorant Garamond, Pinyon Script.

## Alur
1. **Sampul** — ilustrasi hidup, nama mempelai, tanggal, nama tamu (bila ada di link), tombol Buka Undangan.
2. **Buka** — kelopak memancar, musik mulai, kamera mendekat ke rumah gadang dengan cahaya hangat, lalu halaman meluncur ke Salam.
3. **Isi** — Salam & ayat, Kedua Mempelai, Rangkaian Acara + hitung mundur, Kisah Kami, RSVP (WhatsApp), Pepatah, Penutup.
4. Tombol **gulir bercerita** (pil di bawah) membawa tamu bab demi bab; setelah selesai muncul bilah RSVP / Kado.

## Ilustrasi & gerak
- `assets/base.webp` — ilustrasi utuh (burung & kupu-kupu bawaan dihapus oleh `tools/layers.py`).
- `assets/wind.png`, `assets/flowermap.png` — peta angin & peta per-bunga; di WebGL pohon berayun dan tiap bunga + tangkainya
  bergoyang dari pangkalnya sendiri (`tools/flowermap.py`).
- Burung = siluet vektor hitam dengan kepak sayap, terbang berkelompok. Kupu-kupu (`assets/bf*.webp`) melayang pelan di area bunga.
- Latar halaman isi = ilustrasi yang sama, dipudarkan, diam saat digulir.
- `assets/flowers/*.webp` — bunga lepas bertepi bersih (`tools/flowers.py`). Di balik sudut atas tiap kartu ada buket
  (2 bunga + kuncup + ranting berdaun) dan di sudut seberangnya rumpun ranting; tangkai tersembunyi di belakang kartu,
  tumbuh saat kartu muncul, lalu berayun pelan.
- Efek WebGL butuh http(s); bila file dibuka langsung, ilustrasi tampil diam. `prefers-reduced-motion` dihormati.

## Musik
`assets/akad.mp3` — "Akad", Payung Teduh (hak cipta milik pencipta & label; dipakai atas keputusan pemilik undangan).

## Mengubah isi
Semua data ada di objek `WEDDING` di bagian bawah `index.html`. Isian `[..]` masih sementara; kolom kosong (`''`) tidak ditampilkan
(gala, suku, Instagram, foto, kota). Nama tamu: `index.html?to=Nama%20Tamu` atau `index.html#Nama-Tamu`.

## Membuat ulang aset
`pip install opencv-python-headless pillow numpy`, lalu
`python3 tools/layers.py sumber.png assets`, `python3 tools/flowers.py sumber.png assets/flowers`.
