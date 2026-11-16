"""Warnai ulang aset versi 1 ke palet putih · hitam · emas · bunga merah.
Kertas → putih, pohon/rumah/daun → tinta abu-hitam, pita songket → emas, kelopak → merah, inti bunga → emas."""
import sys, glob, numpy as np, cv2
from PIL import Image
A = sys.argv[1]
PAPER = np.array([250,244,228],np.float32)
def recolor(rgb, white_balance, band_rows=0, flowers=True, band_terracotta_only=False):
    f = rgb.astype(np.float32)
    if white_balance: f = np.clip(f * (255/PAPER), 0, 255)
    u8 = f.astype(np.uint8); hsv = cv2.cvtColor(u8, cv2.COLOR_RGB2HSV).astype(np.float32); h,s,v = hsv[...,0],hsv[...,1],hsv[...,2]
    grey = cv2.cvtColor(u8, cv2.COLOR_RGB2GRAY).astype(np.float32)
    ink = np.clip((grey-128)*1.22+128 - 6, 0, 255)                       # tinta abu-hitam, sedikit lebih kontras
    out = np.dstack([ink,ink,ink])
    if flowers:
        petal = (((h<=13)|(h>=150)) & (s>38) & (v>60)).astype(np.float32)      # merah / pink / jingga-merah
        if band_rows: petal[:band_rows+6] = 0                          # pita songket bukan bunga
        petal = cv2.GaussianBlur(petal,(0,0),1.0)
        gold  = cv2.GaussianBlur(((h>13)&(h<32)&(s>95)&(v>140)).astype(np.float32),(0,0),.8)   # inti kuning
        ps = np.clip(s*1.7+70,0,255); pv = np.clip(v*.92 - (255-s)*.16,0,255)
        red = cv2.cvtColor(np.dstack([np.full_like(h,177),ps,pv]).astype(np.uint8), cv2.COLOR_HSV2RGB).astype(np.float32)
        gd  = cv2.cvtColor(np.dstack([np.full_like(h,21),np.clip(s*.9,0,255),v]).astype(np.uint8), cv2.COLOR_HSV2RGB).astype(np.float32)
        out = out*(1-petal[...,None]) + red*petal[...,None]
        out = out*(1-gold[...,None]) + gd*gold[...,None]
    if band_rows:                                                        # pita songket → emas
        g = grey[:band_rows]/255.; lo = np.array([120,88,28],np.float32); hi = np.array([247,232,190],np.float32)
        gb = lo + (hi-lo)*np.clip((g-.25)/.6,0,1)[...,None]
        m = np.clip((235-grey[:band_rows])/30,0,1)[...,None] * np.clip((band_rows-np.arange(band_rows))/14,0,1)[:,None,None]
        if band_terracotta_only:   # lapisan pohon: hanya bagian pita (terakota) yang jadi emas, daun tetap abu
            t = cv2.GaussianBlur((((h<=16)|(h>=160)) & (s>70)).astype(np.float32),(0,0),1.2)[:band_rows]; m = m*t[...,None]
        out[:band_rows] = out[:band_rows]*(1-m) + gb*m
    return out.clip(0,255).astype(np.uint8)
def do(path, white_balance=False, band=0, flowers=True, q=86, tonly=False):
    im = Image.open(path); has_a = im.mode in ('RGBA','LA','P') and 'A' in im.convert('RGBA').getbands()
    rgba = np.array(im.convert('RGBA')); rgb = recolor(rgba[...,:3], white_balance, int(band*rgba.shape[0]), flowers, tonly)
    if has_a and rgba[...,3].min() < 255: Image.fromarray(np.dstack([rgb,rgba[...,3]]),'RGBA').save(path, quality=q, method=6)
    else: Image.fromarray(rgb).save(path, quality=q, method=6)
do(f'{A}/base.webp', True, band=.108)
do(f'{A}/house.webp', True, band=.108, flowers=False)
do(f'{A}/treeL.webp', band=.19, tonly=True); do(f'{A}/treeR.webp', band=.152, tonly=True)
do(f'{A}/flowers.webp', q=88)
for p in glob.glob(f'{A}/flowers/*.webp'): do(p, q=90)
for p in glob.glob(f'{A}/bf*.webp'): do(p, flowers=False)
print('ok')
