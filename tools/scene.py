"""Pecah ilustrasi menjadi lapisan pembuka: house.webp (rumah gadang + langit, tanpa pohon & bunga),
treeL.webp, treeR.webp, flowers.webp (PNG/WebP transparan) untuk animasi masuk & ayunan halus."""
import sys, json, numpy as np, cv2
from PIL import Image
base, out = sys.argv[1], sys.argv[2]
im = np.array(Image.open(base).convert('RGB')).astype(np.float32); H, W = im.shape[:2]
paper = np.array([250,244,228],np.float32)
yy, xx = np.mgrid[0:H,0:W].astype(np.float32)
def ss(v,a,b): t=np.clip((v-a)/(b-a),0,1); return t*t*(3-2*t)
d = np.sqrt(((im-paper)**2).sum(-1)); ink = np.clip((d-10)/26,0,1)
ink = cv2.GaussianBlur(cv2.morphologyEx(ink, cv2.MORPH_CLOSE, np.ones((5,5),np.uint8)),(0,0),.8)
# wilayah tiap lapisan (bobot lembut)
flo_top = 1010 - 150*np.clip(np.abs(xx-W/2)/(W/2)-.42,0,1)/.58          # batas atas bunga: 1010 di tengah → 860 di tepi
flo = ss(yy, flo_top-26, flo_top+14)
lim_l = 270 - 130*ss(yy,500,580)                      # di samping rumah gadang, pohon hanya sampai x≈140
tl = (1-ss(xx,lim_l-40,lim_l+30)) * (1-ss(yy,700,790)) * (1-flo)
lim_r = 535 + 135*ss(yy,470,550)
tr = ss(xx,lim_r-30,lim_r+40) * (1-ss(yy,900,990)) * (1-flo)
band = (1-ss(yy,120,150)) * ss(xx,200,250) * (1-ss(xx,540,590))           # pita songket atas tetap di latar
tl *= (1-band); tr *= (1-band)
def save(name, wgt, box, q=84):
    x0,y0,x1,y1 = box; a = (ink*wgt)[y0:y1,x0:x1]; c = im[y0:y1,x0:x1]
    aa = np.maximum(a,1e-3)[...,None]; col = np.where(a[...,None]>.04, np.clip((c-(1-aa)*paper)/aa,0,255), c)
    Image.fromarray(np.dstack([col,a*255]).astype(np.uint8),'RGBA').save(f'{out}/{name}.webp', quality=q, method=6)
    return [x0,y0,x1-x0,y1-y0]
meta = {'treeL':save('treeL',tl,(0,0,330,800)), 'treeR':save('treeR',tr,(480,0,W,1000)), 'flowers':save('flowers',flo,(0,830,W,H),88)}
# latar: rumah gadang saja — pohon & bunga dipudarkan ke warna kertas
flo_in = ss(yy, flo_top+30, flo_top+90)                 # latar baru memudar jauh di dalam wilayah lapisan → tak ada celah terang
keep = 1 - np.clip((np.clip(tl+tr,0,1)-.8)*5 ,0,1) ; keep = np.minimum(keep, 1-flo_in)
keep = cv2.GaussianBlur(keep,(0,0),5)
house = im*keep[...,None] + paper*(1-keep[...,None])
Image.fromarray(house.clip(0,255).astype(np.uint8)).save(f'{out}/house.webp', quality=86, method=6)
json.dump(meta, open(f'{out}/scene.json','w')); print(meta)
