"""Pecah ilustrasi menjadi: base.webp (burung/kupu dihapus), wind.png (peta angin R=pohon, G=bunga), sprite *.webp beralpha bersih."""
import sys, json, numpy as np, cv2
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
im = np.array(Image.open(src).convert('RGB')); H, W = im.shape[:2]
f = im.astype(np.float32)
SPR = {'hb1':(250,135,320,200),'bf2':(474,152,542,214),'bf3':(165,265,242,340),'bd4':(555,405,615,460),'hb5':(85,590,165,665),
       'hb6':(598,545,685,625),'bf7':(100,710,165,770),'bf8':(30,735,105,792),'bf9':(636,690,676,740),'bf11':(560,995,605,1035),
       'hb13':(410,1022,515,1078),'bf14':(540,325,565,360)}
# sprite yang menempel ke dedaunan dibiarkan diam di latar (tidak dipisah)
EXPORT = {'bf2','bf3','bf7','bf9'}   # hanya kupu-kupu yang dipakai; semua burung & kupu dihapus dari latar
# area di dalam kotak sprite yang bukan bagian tubuh burung/kupu (daun, ranting) — koordinat lokal
EXCL = {'hb1':[[(0,0),(14,0),(14,65),(0,65)]], 'hb5':[[(0,38),(30,75),(0,75)],[(0,0),(16,0),(16,10),(0,10)]], 'hb13':[[(0,49),(105,49),(105,56),(0,56)]],
        'bf7':[[(0,52),(65,52),(65,60),(0,60)]]}
STRICT = {'bf7':55,'bf3':45}
inpaint = np.zeros((H,W),np.uint8); meta = {'W':W,'H':H,'sprites':{}}
for k,(x0,y0,x1,y1) in SPR.items():
    c = f[y0:y1,x0:x1]; c8 = im[y0:y1,x0:x1]
    L = cv2.cvtColor(c8, cv2.COLOR_RGB2GRAY).astype(np.float32); hsv = cv2.cvtColor(c8, cv2.COLOR_RGB2HSV)
    border = np.concatenate([c[0],c[-1],c[:,0],c[:,-1]]); paper = np.median(border,axis=0)
    bgL = np.percentile(np.concatenate([L[0],L[-1],L[:,0],L[:,-1]]),70)
    core = ((L < bgL-STRICT.get(k,38)) | ((hsv[...,1]>70) & (L<225))).astype(np.uint8)
    core = cv2.morphologyEx(core, cv2.MORPH_CLOSE, np.ones((5,5),np.uint8))
    cs,_ = cv2.findContours(core, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    sil = np.zeros_like(core)
    if cs:
        cs = sorted(cs, key=cv2.contourArea, reverse=True); big = cv2.contourArea(cs[0])
        cv2.drawContours(sil, [q for q in cs if cv2.contourArea(q) > big*.08], -1, 1, -1)
    for poly in EXCL.get(k,[]): cv2.fillPoly(sil, [np.array(poly,np.int32)], 0)
    n_, lab_, st_, _ = cv2.connectedComponentsWithStats(sil)
    if n_>1: sil = (lab_==1+np.argmax(st_[1:,cv2.CC_STAT_AREA])).astype(np.uint8)
    sil_d = cv2.dilate(sil, np.ones((3,3),np.uint8)).astype(np.float32)
    # alpha lembut: jarak warna dari kertas, dibatasi siluet; bagian dalam siluet tetap penuh
    d = np.sqrt(((c-paper)**2).sum(-1))
    soft = np.clip((d-14)/36,0,1)
    inner = cv2.erode(sil, np.ones((5,5),np.uint8)).astype(np.float32)
    a = np.maximum(soft, inner) * sil_d
    a = cv2.GaussianBlur(a,(3,3),0)
    # hilangkan halo krem: un-premultiply terhadap warna kertas
    aa = np.maximum(a,1e-3)[...,None]
    col = np.clip((c - (1-aa)*paper)/aa, 0, 255)
    col = np.where(a[...,None]>0.02, col, c)
    rgba = np.dstack([col, a*255]).astype(np.uint8)
    # 2x untuk ketajaman
    if k in EXPORT:
        img = Image.fromarray(rgba,'RGBA').resize(((x1-x0)*2,(y1-y0)*2), Image.LANCZOS)
        img.save(f'{out}/{k}.webp', quality=92)
        meta['sprites'][k] = [x0,y0,x1-x0,y1-y0]
    full = np.zeros((H,W),np.uint8); full[y0:y1,x0:x1] = sil
    inpaint |= cv2.dilate(full, np.ones((9,9),np.uint8))
# sisa burung/kupu kecil yang tidak dijadikan sprite
for (x0,y0,x1,y1) in [(100,895,142,948),(150,1040,218,1100),(648,848,712,892),(430,1060,505,1112),(30,770,110,815),(60,770,100,800)]:
    c8 = im[y0:y1,x0:x1]; L = cv2.cvtColor(c8, cv2.COLOR_RGB2GRAY).astype(np.float32)
    bg = np.percentile(np.concatenate([L[0],L[-1],L[:,0],L[:,-1]]),70)
    m = (L < bg-30).astype(np.uint8); m = cv2.dilate(m, np.ones((7,7),np.uint8))
    inpaint[y0:y1,x0:x1] |= m
clean = cv2.cvtColor(cv2.inpaint(cv2.cvtColor(im,cv2.COLOR_RGB2BGR), inpaint, 7, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB)
Image.fromarray(clean).save(f'{out}/base.webp', quality=88)
# ---- peta angin ----
cf = clean.astype(np.float32)
paper = np.array([249,242,224],np.float32)
nonpaper = (np.sqrt(((cf-paper)**2).sum(-1)) > 22).astype(np.float32)
yy, xx = np.mgrid[0:H,0:W]
def smooth(v,a,b): t=np.clip((v-a)/(b-a),0,1); return t*t*(3-2*t)
tree = np.maximum(smooth(-xx,-330,-250)*smooth(-yy,-800,-700), smooth(xx,470,540)*smooth(-yy,-1010,-900))
tree *= smooth(yy,100,170) + (1-smooth(xx,40,90)) * (1-smooth(yy,100,170))  # pita songket diam, kecuali tepi kiri yg tertutup pohon
tree *= (1 - smooth(xx,700,740)*(1-smooth(yy,100,170))*0)  # (placeholder, tidak mengubah)
house = smooth(xx,140,190)*(1-smooth(xx,630,680))*smooth(yy,560,600)*(1-smooth(yy,960,1000))
flower = smooth(yy,880,960)
R = nonpaper*tree*(1-house); G = nonpaper*flower*(1-house*.7)
R = cv2.GaussianBlur(R,(0,0),7); G = cv2.GaussianBlur(G,(0,0),7)
wind = np.dstack([R*255, G*255, np.zeros_like(R)]).clip(0,255).astype(np.uint8)
Image.fromarray(wind).resize((W//2,H//2), Image.BILINEAR).save(f'{out}/wind.png')
json.dump(meta, open(f'{out}/meta.json','w')); print(json.dumps(meta))
