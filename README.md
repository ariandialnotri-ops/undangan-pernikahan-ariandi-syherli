# Undangan Pernikahan Digital — Rian & Syherli

Undangan pernikahan berbasis website, satu file (`index.html`), dioptimalkan untuk HP.
Gaya ilustrasi gravir vintage Minang: langit sepia, gunung & danau, rumah gadang, Jam Gadang,
bunga lili, ornamen damask emas, kartu krem melengkung dengan segel lilin. Semua ilustrasi digambar sebagai SVG di dalam file.

## Fitur
- Sampul dengan nama tamu (`index.html?to=Nama%20Tamu` atau `index.html#Nama-Tamu`) dan tombol Buka Undangan
- Animasi buka: kabut tersibak, pemandangan mendekat, bunga menyibak ke sudut
- Musik kotak musik (dibuat di browser, tanpa file) dengan tombol on/off
- Tombol gulir bercerita (bab demi bab); menu ☰ dan tombol RSVP muncul setelah cerita selesai
- Konten muncul halus saat digulir dan memudar turun saat digulir ke atas
- Ayat, mempelai, hitung mundur + Google Calendar, acara + peta, love story, galeri, RSVP ke WhatsApp, wedding gift (BCA/BRI) dengan tombol salin
- Menghormati `prefers-reduced-motion`

## Mengubah isi
Semua data ada di objek `WEDDING` di bagian bawah `index.html`. Bagian bertanda `[DUMMY]` masih data sementara.

## Menjalankan
Buka `index.html` di browser, atau deploy sebagai situs statis (GitHub Pages, Vercel, Netlify, Cloudflare Pages).
