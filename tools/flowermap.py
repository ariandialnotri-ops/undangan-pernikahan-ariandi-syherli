"""Peta gerak per-bunga: setiap bunga + tangkainya punya titik pangkal (akar) sendiri.
Keluaran flowermap.png (768x1376, RGB; semua pangkal di tepi bawah):
  R = x pangkal / 768, G = bobot gerak (0 di pangkal -> 1 di kepala bunga, memudar di tepi),
  B = nomor bunga (untuk fase)."""
import sys, json, numpy as np, cv2
from PIL import Image
base, fldir, out = sys.argv[1], sys.argv[2], sys.argv[3]
im = np.array(Image.open(base).convert('RGB')); H, W = im.shape[:2]
meta = {e['id']:e for e in json.load(open(f'{fldir}/flowers.json'))}
# tangkai: titik dari kepala bunga turun ke pangkal (koordinat ilustrasi)
STEM = {
 'jahe-merah':     [(160,1100),(152,1200),(146,1376)],
 'anggrek-1':      [(250,1110),(244,1240),(232,1376)],
 'kuncup-anggrek': [(300,1075),(262,1120),(244,1240),(232,1376)],
 'anggrek-2':      [(172,1190),(178,1290),(184,1376)],
 'anggrek-merah':  [(252,1255),(242,1320),(238,1376)],
 'anggrek-3':      [(116,1300),(124,1340),(128,1376)],
 'lili-pink-2':    [(320,1350),(328,1376)],
 'heliconia-1':    [(682,1150),(684,1260),(680,1376)],
 'heliconia-2':    [(392,1240),(392,1310),(390,1376)],
 'terompet':       [(552,1138),(574,1196),(588,1250),(592,1376)],
 'mawar-pink':     [(632,1182),(642,1230),(646,1376)],
 'lili-pink-1':    [(460,1262),(448,1320),(440,1376)],
 'mawar-liar':     [(612,1298),(604,1340),(600,1376)],
 'mawar-merah-1':  [(694,1244),(698,1310),(702,1376)],
 'mawar-merah-2':  [(694,1348),(696,1376)],
 'lili-putih':     [(430,1360),(426,1376)],
}
ids = [k for k in STEM if k in meta]
N = len(ids); masks = np.zeros((N,H,W),np.uint8); roots=[]; tops=[]
for i,k in enumerate(ids):
    e = meta[k]; a = np.array(Image.open(f'{fldir}/{k}.png').convert('RGBA'))[...,3]
    a = cv2.resize(a,(e['w'],e['h']),interpolation=cv2.INTER_AREA) > 60
    y0,x0 = e['y'],e['x']; hh,ww = a.shape; masks[i,y0:y0+hh,x0:x0+ww] |= a[:H-y0,:W-x0].astype(np.uint8)
    pts = np.array(STEM[k],np.int32); cv2.polylines(masks[i],[pts],False,1,thickness=7)
    roots.append(STEM[k][-1]); tops.append(e['y'])
dist = np.stack([cv2.distanceTransform((1-m).astype(np.uint8),cv2.DIST_L2,5) for m in masks])
order = np.argsort(dist,axis=0); d1 = np.take_along_axis(dist,order[:1],0)[0]; d2 = np.take_along_axis(dist,order[1:2],0)[0] if N>1 else d1+99
own = order[0]
feather = np.clip((14-d1)/8,0,1) * np.clip((d2-d1)/7,0,1)
yy = np.mgrid[0:H,0:W][0].astype(np.float32)
rx = np.array([r[0] for r in roots],np.float32)[own]; ry = np.array([r[1] for r in roots],np.float32)[own]; top = np.array(tops,np.float32)[own]
bend = np.clip((ry-yy)/np.maximum(ry-top,1),0,1)**1.25
w = feather*bend
R = rx/W*255; G = w*255; B = (own+1)*(255//(N+1)); A = (ry-860)/(H-860)*255
mp = np.dstack([R,G,B]).clip(0,255).astype(np.uint8); mp[w<=0.003] = 0
Image.fromarray(mp,'RGB').save(out, optimize=True)
prev = (np.dstack([w*255, (own*37%255)*(w>0), np.zeros_like(w)])).astype(np.uint8)
Image.fromarray(prev).resize((W//2,H//2)).save(out.replace('.png','_preview.png'))
print(N, 'flowers')
