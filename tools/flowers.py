"""Potong setiap bunga dari ilustrasi menjadi WebP transparan terpisah (satu file per bunga), bertepi halus.
Kotak tiap bunga ditentukan manual. Topeng dibangun dari warna KELOPAK (merah/pink/krem + inti kuning) pada
resolusi 3x, dihaluskan, lalu dikikis 1px supaya tidak ada sisa tinta/daun gelap di tepi."""
import sys, json, numpy as np, cv2
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
im = np.array(Image.open(src).convert('RGB')); H, W = im.shape[:2]
paper = np.array([249,242,224],np.float32)
BOX = {  # nama: (x0,y0,x1,y1)  koordinat ilustrasi 768x1376
 'anggrek-1':(203,1028,302,1118), 'anggrek-2':(106,1100,238,1210), 'anggrek-merah':(188,1145,312,1268), 'anggrek-3':(46,1182,184,1312),
 'mawar-pink':(580,1110,676,1192), 'lili-pink-1':(410,1158,530,1278), 'lili-pink-2':(252,1258,372,1376),
 'mawar-liar':(534,1184,656,1306), 'mawar-merah-1':(666,1150,768,1250), 'mawar-merah-2':(656,1252,768,1352),
}
# batas elips (lokal kotak: cx, cy, rx, ry) agar kelopak bunga tetangga tidak ikut
CLIP = {'anggrek-1':(48,42,46,40),'anggrek-2':(66,48,63,48),'anggrek-merah':(62,68,60,55),'anggrek-3':(76,62,60,58),
        'mawar-merah-1':(45,50,42,46),'lili-pink-1':(64,62,58,58),'lili-pink-2':(62,62,60,58),
        'mawar-liar':(62,56,58,54),'mawar-merah-2':(56,50,52,48),'mawar-pink':(46,34,46,32)}
SPIKY = {'lili-pink-1':250,'lili-pink-2':250}     # kelopak runcing: hanya lubang kecil yang diisi
K = 3                                              # kerja pada resolusi 3x agar tepi halus
meta = []
for name,(x0,y0,x1,y1) in BOX.items():
    c8 = cv2.resize(im[y0:y1,x0:x1], None, fx=K, fy=K, interpolation=cv2.INTER_CUBIC)
    c = c8.astype(np.float32); hsv = cv2.cvtColor(c8, cv2.COLOR_RGB2HSV); hh, ss, vv = [hsv[...,i].astype(int) for i in range(3)]
    red   = ((hh <= 14) | (hh >= 150)) & (ss > 34) & (vv > 78)            # kelopak merah / pink
    blush = ((hh <= 18) | (hh >= 150)) & (ss > 14) & (vv > 190)           # pink sangat muda
    gold  = (hh > 14) & (hh < 30) & (ss > 80) & (vv > 150)                # inti kuning
    m = (red | blush | gold).astype(np.uint8)
    if name in CLIP:
        ex = np.zeros_like(m); cxl,cyl,rx,ry = [v*K for v in CLIP[name]]; cv2.ellipse(ex,(cxl,cyl),(rx,ry),0,0,360,1,-1); m &= ex
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(17,17)))
    n, lab, st, cen = cv2.connectedComponentsWithStats(m)
    if n < 2: continue
    cx, cy = m.shape[1]/2, m.shape[0]/2
    score = [st[i,cv2.CC_STAT_AREA] / (1 + ((cen[i][0]-cx)**2+(cen[i][1]-cy)**2)**.5/(40*K)) for i in range(1,n)]
    k = 1 + int(np.argmax(score)); keep = (lab==k).astype(np.uint8)
    if name in SPIKY:
        inv = (1-keep).astype(np.uint8); nh, lh, sh, _ = cv2.connectedComponentsWithStats(inv); sil = keep.copy()
        for i in range(1,nh):
            x_,y_,w_,h_,a_ = sh[i]
            if a_ < SPIKY[name]*K*K and x_>0 and y_>0 and x_+w_<keep.shape[1] and y_+h_<keep.shape[0]: sil[lh==i] = 1
    else:
        cs,_ = cv2.findContours(keep, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE); sil = np.zeros_like(keep); cv2.drawContours(sil, cs, -1, 1, -1)
    # haluskan kontur, kikis ~1px (skala asli) agar tepi bersih, lalu lembutkan
    sm = (cv2.GaussianBlur(sil.astype(np.float32),(0,0),2.2) > .5).astype(np.uint8)
    sm = cv2.erode(sm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
    a = cv2.GaussianBlur(sm.astype(np.float32),(0,0),1.3)
    ys, xs = np.where(a > .02); bx0, by0, bx1, by1 = xs.min(), ys.min(), xs.max()+1, ys.max()+1
    rgba = np.dstack([c, a*255]).clip(0,255).astype(np.uint8)[by0:by1, bx0:bx1]
    w2, h2 = (bx1-bx0)*2//K, (by1-by0)*2//K                 # simpan pada 2x
    Image.fromarray(rgba,'RGBA').resize((w2,h2), Image.LANCZOS).save(f'{out}/{name}.webp', quality=90, method=6)
    meta.append({'id':name,'x':int(x0+bx0//K),'y':int(y0+by0//K),'w':int(w2//2),'h':int(h2//2)})
json.dump(meta, open(f'{out}/flowers.json','w'), indent=1)
print(len(meta), 'bunga')
