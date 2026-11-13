# Undangan Pernikahan Digital

Undangan pernikahan (baralek) berbasis website, satu file (`index.html`), gaya luxury elegant khas Minangkabau: warna marawa (hitam–merah–kuning emas), motif batik kaluak paku, songket pucuak rabuang, dan ilustrasi rumah gadang beranimasi.

## Fitur
- Sampul rumah gadang: pintu ukir berayun terbuka, cahaya dari dalam, lalu kamera masuk melewati pintu; nama tamu lewat `index.html#Nama-Tamu`
- Bingkai lengkung, mandala parallax, partikel emas, kelopak berjatuhan, reveal saat scroll
- Mempelai, ayat, hitung mundur + Simpan ke Google Calendar
- Waktu & tempat (Akad, Resepsi) dengan tautan peta
- Kisah kami (timeline), galeri foto
- RSVP & ucapan dikirim ke WhatsApp
- Amplop digital dengan tombol salin nomor rekening
- Menghormati `prefers-reduced-motion`

## Mengubah isi
Semua data ada di objek `WEDDING` di bagian bawah `index.html`:
nama, orang tua, tanggal, acara, lokasi, kisah, foto, rekening, nomor WhatsApp.

## Menjalankan
Buka `index.html` langsung di browser, atau deploy sebagai situs statis
(GitHub Pages, Vercel, Netlify, Cloudflare Pages) tanpa proses build.
