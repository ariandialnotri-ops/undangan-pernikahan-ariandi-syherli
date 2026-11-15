import sys, json, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
src, out = sys.argv[1], sys.argv[2]
im = np.array(Image.open(src).convert('RGB'))
H, W = im.shape[:2]
SPR = {'hb1':(250,135,320,200),'bf2':(474,152,542,214),'bf3':(165,265,242,340),'bd4':(555,405,615,460),'hb5':(85,590,165,665),
       'hb6':(598,545,685,625),'bf7':(100,710,165,770),'bf8':(30,735,105,800),'bf9':(636,690,676,740),'bf11':(560,995,605,1035),
       'hb13':(410,1022,515,1090),'bf14':(540,325,565,360)}
inpaint_mask = np.zeros((H,W),np.uint8); meta = {'W':W,'H':H,'sprites':{},'layers':{}}
for k,(x0,y0,x1,y1) in SPR.items():
    c = im[y0:y1, x0:x1]
    hsv = cv2.cvtColor(c, cv2.COLOR_RGB2HSV); L = cv2.cvtColor(c, cv2.COLOR_RGB2GRAY).astype(int)
    border = np.concatenate([L[0],L[-1],L[:,0],L[:,-1]]); bgL = np.percentile(border,70)
    m = ((L < bgL-38) | ((hsv[...,1]>70) & (L<225))).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5,5),np.uint8))
    cs,_ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if cs:
        cs = sorted(cs, key=cv2.contourArea, reverse=True); big = cv2.contourArea(cs[0])
        m = np.zeros_like(m); cv2.drawContours(m, [q for q in cs if cv2.contourArea(q) > big*.08], -1, 1, -1)
    m = cv2.dilate(m, np.ones((3,3),np.uint8))
    full = np.zeros((H,W),np.uint8); full[y0:y1,x0:x1] = m
    inpaint_mask |= cv2.dilate(full, np.ones((7,7),np.uint8))
    a = cv2.GaussianBlur(m.astype(np.float32)*255,(3,3),0).clip(0,255).astype(np.uint8)
    rgba = np.dstack([im[y0:y1,x0:x1], a])
    Image.fromarray(rgba,'RGBA').save(f'{out}/{k}.webp', quality=90)
    meta['sprites'][k] = [x0,y0,x1-x0,y1-y0]
clean = cv2.inpaint(cv2.cvtColor(im,cv2.COLOR_RGB2BGR), inpaint_mask, 6, cv2.INPAINT_TELEA)
clean = cv2.cvtColor(clean, cv2.COLOR_BGR2RGB)
Image.fromarray(clean).save(f'{out}/base.webp', quality=82)
LAY = {
 'treeL':[(0,0),(232,0),(300,160),(270,330),(230,560),(210,720),(0,740)],
 'treeR':[(548,0),(768,0),(768,960),(690,960),(630,720),(560,520),(520,260),(530,120)],
 'flL':[(0,870),(300,960),(330,1376),(0,1376)],
 'flM':[(230,1030),(560,1030),(560,1376),(230,1376)],
 'flR':[(470,930),(768,900),(768,1376),(470,1376)],
}
for k,poly in LAY.items():
    mask = Image.new('L',(W,H),0); ImageDraw.Draw(mask).polygon(poly, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(14))
    xs=[p[0] for p in poly]; ys=[p[1] for p in poly]
    x0,y0,x1,y1 = max(0,min(xs)-20),max(0,min(ys)-20),min(W,max(xs)+20),min(H,max(ys)+20)
    rgba = Image.fromarray(clean).convert('RGBA'); rgba.putalpha(mask)
    rgba.crop((x0,y0,x1,y1)).save(f'{out}/{k}.webp', quality=82)
    meta['layers'][k] = [x0,y0,x1-x0,y1-y0]
# pita songket untuk kepala bagian
Image.fromarray(clean).crop((232,0,560,142)).save(f'{out}/band.webp', quality=85)
json.dump(meta, open(f'{out}/meta.json','w'))
print(json.dumps(meta))
