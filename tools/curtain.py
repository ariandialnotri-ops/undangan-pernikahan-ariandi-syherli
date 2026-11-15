"""Buat tirai bunga+pohon kiri/kanan (PNG ber-alpha) dari ilustrasi bersih untuk animasi pembuka."""
import sys, numpy as np, cv2
from PIL import Image
base, out = sys.argv[1], sys.argv[2]
im = np.array(Image.open(base).convert('RGB')).astype(np.float32); H, W = im.shape[:2]
paper = np.array([249,242,224],np.float32)
def alpha_of(a):
    d = np.sqrt(((a-paper)**2).sum(-1))
    m = np.clip((d-16)/26,0,1)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9,9),np.uint8))
    return cv2.GaussianBlur(m,(0,0),1.2)
def over(dst_rgb, dst_a, src_rgb, src_a, x, y):
    h, w = src_a.shape; X0, Y0 = max(0,x), max(0,y); X1, Y1 = min(dst_a.shape[1], x+w), min(dst_a.shape[0], y+h)
    if X1<=X0 or Y1<=Y0: return
    s = src_a[Y0-y:Y1-y, X0-x:X1-x][...,None]; c = src_rgb[Y0-y:Y1-y, X0-x:X1-x]
    da = dst_a[Y0:Y1,X0:X1][...,None]
    dst_rgb[Y0:Y1,X0:X1] = c*s + dst_rgb[Y0:Y1,X0:X1]*(1-s)
    dst_a[Y0:Y1,X0:X1] = (s + da*(1-s))[...,0]
def feather(shape):
    h,w = shape; t = np.clip(np.arange(h)/110,0,1); t = t*t*(3-2*t)       # tepi atas tiap rumpun memudar
    b = np.clip((h-np.arange(h))/30,0,1)
    return (t*b)[:,None]*np.ones((1,w))
PW = int(W*0.62)                                    # tiap tirai menutupi 62% lebar → tumpang tindih di tengah
flo = im[985:H, 0:W//2+40]; floA = alpha_of(flo); floA *= feather(floA.shape)     # rumpun bunga kiri
tree = im[0:590, 0:340]; treeA = alpha_of(tree); treeA *= np.clip((590-np.arange(590))/90,0,1)[:,None]   # berhenti di atas atap rumah
treeA *= np.clip((340-np.arange(340))/60,0,1)[None,:]  # pudar di tepi kanan potongan pohon
rgb = np.tile(paper,(H,PW,1)).astype(np.float32); A = np.zeros((H,PW),np.float32)
# lapisan bunga bertumpuk dari bawah ke atas, digeser agar tidak tampak berulang
for (x,y,sc) in [(30,-80,.95),(-50,40,1.0),(150,150,.9),(0,250,1.0),(170,360,.95),(-40,460,1.05),(120,570,.95),(-20,680,1.0),(160,780,.95),(-60,890,1.05),(100,990,1.0)]:
    f = cv2.resize(flo,(0,0),fx=sc,fy=sc); fa = cv2.resize(floA,(0,0),fx=sc,fy=sc)
    over(rgb,A,f,fa,x,y)
over(rgb,A,tree,treeA,0,-40)
# tepi dalam bergerigi alami: pudar di 18% terakhir mengikuti isi
ramp = np.clip((PW-np.arange(PW))/(PW*0.16),0,1)[None,:]
A *= ramp
A = np.clip(A*1.15,0,1)
Lp = np.dstack([rgb, A*255]).clip(0,255).astype(np.uint8)
Image.fromarray(Lp,'RGBA').resize((PW*3//4, H*3//4), Image.LANCZOS).save(f'{out}/curtainL.webp', quality=82)
# tirai kanan: dari rumpun bunga kanan + pohon kanan
flo = im[985:H, W//2-40:W]; floA = alpha_of(flo); floA *= feather(floA.shape)
tree = im[0:680, 500:W]; treeA = alpha_of(tree); treeA *= np.clip((680-np.arange(680))/90,0,1)[:,None]; treeA *= np.clip((np.arange(W-500))/60,0,1)[None,:]
rgb = np.tile(paper,(H,PW,1)).astype(np.float32); A = np.zeros((H,PW),np.float32)
fw = flo.shape[1]
for (x,y,sc) in [(PW-fw-30,-80,.95),(PW-fw+50,40,1.0),(PW-fw-150,150,.9),(PW-fw,250,1.0),(PW-fw-170,360,.95),(PW-fw+40,460,1.05),(PW-fw-120,570,.95),(PW-fw+20,680,1.0),(PW-fw-160,780,.95),(PW-fw+60,890,1.05),(PW-fw-100,990,1.0)]:
    f = cv2.resize(flo,(0,0),fx=sc,fy=sc); fa = cv2.resize(floA,(0,0),fx=sc,fy=sc)
    over(rgb,A,f,fa,x,y)
over(rgb,A,tree,treeA,PW-tree.shape[1],-40)
A *= np.clip(np.arange(PW)/(PW*0.16),0,1)[None,:]
A = np.clip(A*1.15,0,1)
Rp = np.dstack([rgb, A*255]).clip(0,255).astype(np.uint8)
Image.fromarray(Rp,'RGBA').resize((PW*3//4, H*3//4), Image.LANCZOS).save(f'{out}/curtainR.webp', quality=82)
print('ok', PW)
