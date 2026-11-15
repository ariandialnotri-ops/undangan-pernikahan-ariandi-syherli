"""Potong setiap bunga dari ilustrasi menjadi PNG transparan terpisah (satu file per bunga).
Kotak tiap bunga ditentukan manual; di dalam kotak, kelopak dipisahkan dari kertas & daun hijau."""
import sys, json, numpy as np, cv2
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
im = np.array(Image.open(src).convert('RGB')); H, W = im.shape[:2]
f = im.astype(np.float32); paper = np.array([249,242,224],np.float32)
hsv = cv2.cvtColor(im, cv2.COLOR_RGB2HSV); h, s, v = [hsv[...,i].astype(int) for i in range(3)]
BOX = {  # nama: (x0,y0,x1,y1)  koordinat ilustrasi 768x1376
 'anggrek-1':(203,1028,302,1118), 'anggrek-2':(106,1100,238,1210), 'anggrek-merah':(188,1145,312,1268), 'anggrek-3':(46,1182,184,1312),
 'kuncup-anggrek':(282,1028,358,1092), 'jahe-merah':(122,972,203,1108),
 'heliconia-1':(598,928,710,1162), 'heliconia-2':(336,1060,424,1262),
 'terompet':(496,1082,562,1152), 'mawar-pink':(580,1110,676,1192), 'lili-pink-1':(410,1158,530,1278), 'lili-pink-2':(252,1258,372,1376),
 'mawar-liar':(534,1184,656,1306), 'mawar-merah-1':(666,1150,768,1250), 'mawar-merah-2':(656,1252,768,1352), 'lili-putih':(364,1262,500,1376),
}
WHITE = {'lili-putih'}
# batas elips (lokal kotak: cx, cy, rx, ry) agar kelopak bunga tetangga tidak ikut
CLIP = {'anggrek-1':(48,42,46,40),'anggrek-2':(66,48,63,48),'anggrek-merah':(62,68,60,55),'anggrek-3':(68,62,66,58),
        'jahe-merah':(30,60,30,64),'alstroemeria':(40,68,42,66),'mawar-merah-1':(45,50,42,46),'lili-putih':(70,62,70,54),
        'lili-pink-1':(64,62,58,58),'lili-pink-2':(62,62,60,58),'terompet':(32,35,34,35),'heliconia-1':(58,132,44,104)}
# bunga berkelopak runcing: hanya lubang kecil yang diisi (daun di sela kelopak tetap transparan)
SPIKY = {'lili-putih':300,'lili-pink-1':250,'lili-pink-2':250,'alstroemeria':200,'heliconia-1':150,'heliconia-2':150,'jahe-merah':400}
meta = []
for name,(x0,y0,x1,y1) in BOX.items():
    c = f[y0:y1,x0:x1]; hh, ss, vv = h[y0:y1,x0:x1], s[y0:y1,x0:x1], v[y0:y1,x0:x1]
    green = (hh >= 22) & (hh <= 90) & (ss > 38)
    near_paper = np.sqrt(((c-paper)**2).sum(-1)) < (14 if name in WHITE else 30)
    m = (~green & ~near_paper).astype(np.uint8)
    if name in WHITE:  # kelopak putih: ambil area terang yang dikelilingi garis tinta
        m |= ((vv > 200) & (ss < 45)).astype(np.uint8) & cv2.dilate(m, np.ones((15,15),np.uint8))
    if name in CLIP:
        ex = np.zeros_like(m); cxl,cyl,rx,ry = CLIP[name]; cv2.ellipse(ex,(cxl,cyl),(rx,ry),0,0,360,1,-1); m &= ex
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((7,7),np.uint8))
    # komponen terbesar yang dekat pusat kotak
    n, lab, st, cen = cv2.connectedComponentsWithStats(m)
    if n < 2: continue
    cx, cy = (x1-x0)/2, (y1-y0)/2
    score = [st[i,cv2.CC_STAT_AREA] / (1 + ((cen[i][0]-cx)**2+(cen[i][1]-cy)**2)**.5/40) for i in range(1,n)]
    k = 1 + int(np.argmax(score)); main = (lab==k).astype(np.uint8)
    keep = main.copy()  # gabungkan potongan kelopak lain yang menempel erat
    for i in range(1,n):
        if i!=k and st[i,cv2.CC_STAT_AREA] > 40 and (cv2.dilate(main,np.ones((9,9),np.uint8)) & (lab==i)).any(): keep |= (lab==i)
    if name in SPIKY:   # isi hanya lubang kecil
        inv = (1-keep).astype(np.uint8); nh, lh, sh, _ = cv2.connectedComponentsWithStats(inv)
        sil = keep.copy()
        for i in range(1,nh):
            x_,y_,w_,h_,a_ = sh[i]
            if a_ < SPIKY[name] and x_>0 and y_>0 and x_+w_<keep.shape[1] and y_+h_<keep.shape[0]: sil[lh==i] = 1
    else:
        cs,_ = cv2.findContours(keep, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        sil = np.zeros_like(keep); cv2.drawContours(sil, cs, -1, 1, -1)
    a = cv2.GaussianBlur(sil.astype(np.float32),(0,0),.9)
    aa = np.maximum(a,1e-3)[...,None]
    col = np.where(a[...,None]>.05, np.clip((c-(1-aa)*paper)/aa,0,255), c)
    ys, xs = np.where(a > .02); bx0, by0, bx1, by1 = xs.min(), ys.min(), xs.max()+1, ys.max()+1
    rgba = np.dstack([col, a*255]).astype(np.uint8)[by0:by1, bx0:bx1]
    img = Image.fromarray(rgba,'RGBA').resize(((bx1-bx0)*2,(by1-by0)*2), Image.LANCZOS)
    img.save(f'{out}/{name}.png', optimize=True)
    meta.append({'id':name,'x':int(x0+bx0),'y':int(y0+by0),'w':int(bx1-bx0),'h':int(by1-by0)})
json.dump(meta, open(f'{out}/flowers.json','w'), indent=1)
print(len(meta))
