"""Potong ranting/dedaunan pohon dari ilustrasi menjadi sprite transparan untuk hiasan tepi halaman."""
import sys, numpy as np, cv2
from PIL import Image
base, out = sys.argv[1], sys.argv[2]
im = np.array(Image.open(base).convert('RGB')).astype(np.float32)
paper = np.array([249,242,224],np.float32)
def sprite(x0,y0,x1,y1, fade_side, name):
    c = im[y0:y1,x0:x1]; h,w = c.shape[:2]
    d = np.sqrt(((c-paper)**2).sum(-1)); a = np.clip((d-14)/30,0,1)
    a = cv2.morphologyEx(a, cv2.MORPH_CLOSE, np.ones((5,5),np.uint8))
    xs = np.arange(w)/w; ys = np.arange(h)/h
    fx = np.clip((1-xs)/.35,0,1) if fade_side=='right' else np.clip(xs/.35,0,1)   # pudar ke arah dalam halaman
    fy = np.clip(ys/.12,0,1) * np.clip((1-ys)/.25,0,1)
    a *= (fx[None,:]**1.2) * fy[:,None]
    a0 = np.clip((d-14)/30,0,1); aa = np.maximum(a0,1e-3)[...,None]
    col = np.where(a0[...,None]>.05, np.clip((c-(1-aa)*paper)/aa,0,255), c)   # warna dari alpha asli; pudar hanya di alpha
    Image.fromarray(np.dstack([col,a*255]).astype(np.uint8),'RGBA').save(f'{out}/{name}.webp', quality=86)
sprite(0,150,250,560,'right','branchL')
sprite(560,140,768,600,'left','branchR')
print('ok')
