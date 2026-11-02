"""Generate responsive SVG diagrams. No external fonts, scripts or raster assets."""
from pathlib import Path
from html import escape
ROOT = Path(__file__).resolve().parents[1]
STYLE = '''
.bg{fill:#0d1424}.panel{fill:#141f34;stroke:#30415b;stroke-width:1}.tile{fill:#1b2b45;stroke:#456080;stroke-width:1}
.title{fill:#f0f6ff;font:700 32px system-ui,sans-serif}.label{fill:#edf4ff;font:600 17px system-ui,sans-serif}
.copy{fill:#b9c9df;font:15px system-ui,sans-serif}.small{fill:#aebfd6;font:13px system-ui,sans-serif}
.kicker{fill:#69dccb;font:600 12px ui-monospace,monospace;letter-spacing:1.4px}.accent{fill:#69dccb}
.wire{fill:none;stroke:#4b6b91;stroke-width:2}.flow{fill:none;stroke:#69dccb;stroke-width:2;stroke-dasharray:5 9;animation:flow 2s linear infinite}
.step{animation:step 8s ease-in-out infinite;animation-delay:var(--delay,0s)}.signal{fill:#69dccb;animation:signal 4s ease-in-out infinite;animation-delay:var(--delay,0s)}
@keyframes flow{to{stroke-dashoffset:-28}}@keyframes step{0%,100%{stroke:#456080}20%,40%{stroke:#69dccb}}
@keyframes signal{0%,100%{opacity:.25}35%,60%{opacity:1}}
@media(prefers-color-scheme:light){.bg{fill:#f4f7fc}.panel{fill:#fff;stroke:#ccd8e8}.tile{fill:#edf3fc;stroke:#a8bad2}.title,.label{fill:#14263f}.copy{fill:#405874}.small{fill:#4c6380}.kicker,.accent{fill:#087f76}.flow{stroke:#087f76}.signal{fill:#087f76}}
@media(prefers-reduced-motion:reduce){.flow,.step,.signal{animation:none}.signal{opacity:1}}
'''
def text(x,y,s,cls='copy',**attrs):
 return f'<text x="{x}" y="{y}" class="{cls}" '+ ' '.join(f'{k}="{v}"' for k,v in attrs.items())+f'>{escape(s)}</text>'
def rect(x,y,w,h,cls='tile',extra=''):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" class="{cls}" {extra}/>'
def wire(d): return f'<path d="{d}" class="wire"/><path d="{d}" class="flow"/>'
def svg(name,w,h,title,desc,body):
 out=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc><style>{STYLE}</style><rect width="{w}" height="{h}" rx="20" class="bg"/>{body}</svg>\n'
 (ROOT/'assets'/name).write_text(out)
def hero(mobile):
 w,h=(360,680) if mobile else (960,350)
 b=text(24 if mobile else 36,38,'KIRILL BAIBAKOV','kicker')
 if mobile:
  b+=text(24,78,'From domain','title')+text(24,117,'to delivery.','title')
  b+=text(24,150,'Full-stack engineer · Go / TypeScript')
 else:
  b+=text(36,87,'From domain to delivery.','title')+text(36,120,'Full-stack engineer · reliable products, clear boundaries, shared state.')
 stages=[('01','Model','Rules + ownership'),('02','Persist','PostgreSQL'),('03','Serve','Go / Node.js'),('04','Interact','React / Next.js'),('05','Deliver','Tests / Docker / CI')]
 for i,(n,title,detail) in enumerate(stages):
  x,y=(24,183+i*91) if mobile else (36+i*180,174)
  cw,ch=(312,72) if mobile else (168,125)
  if i<4:
   b+=wire(f'M{x+156} {y+ch}v19') if mobile else wire(f'M{x+168} {y+62}h12')
  b+=rect(x,y,cw,ch,'tile step',f'style="--delay:{i*1.3}s"')
  b+=text(x+16,y+27,n,'kicker')
  b+=text(x+(54 if mobile else 16),y+(28 if mobile else 65),title,'label')
  b+=text(x+(54 if mobile else 16),y+(52 if mobile else 93),detail,'small')
  b+=f'<circle cx="{x+cw-18}" cy="{y+22}" r="4" class="signal" style="--delay:{i*.7}s"/>'
 svg('engineering-pipeline'+('-mobile' if mobile else '')+'.svg',w,h,'Kirill Baibakov — from domain to delivery','Five connected steps: model, persist, serve, interact, deliver. The mobile layout stacks readable cards vertically.',b)
def box(x,y,w,label,detail=None):
 return rect(x,y,w,48 if detail is None else 64)+text(x+w/2,y+26,label,'label',**{'text-anchor':'middle'})+(text(x+w/2,y+49,detail,'small',**{'text-anchor':'middle'}) if detail else '')
def highlights(mobile):
 w,h=(360,1550) if mobile else (960,1024)
 b=text(24 if mobile else 36,38,'ENGINEERING IN PRACTICE','kicker')
 b+=text(24 if mobile else 36,77,'Decisions that hold up.','label' if mobile else 'title')
 panels=[('01 / SHARED MODEL','One model. Two views.',['Metric domain data drives both','the 2D plan and the 3D scene.','Geometry stays consistent.']),('02 / REALTIME RULES','The server decides.',['Validate input and commit once.','Clients receive shared state;','retries do not duplicate results.']),('03 / VERSIONED CONTENT','Edit without disruption.',['The library can move to v2.','An assigned lesson or homework','keeps its original v1 snapshot.']),('04 / RELEASE RECOVERY','Ship with a way back.',['Checks, backup, release, health.','If the app fails its health check,','restore the previous release.'])]
 for i,(tag,title,lines) in enumerate(panels):
  x,y=(16,100+i*358) if mobile else (24,112+i*226)
  pw,ph=(328,340) if mobile else (912,210)
  b+=rect(x,y,pw,ph,'panel')+text(x+18,y+27,tag,'kicker')
  tx,ty=(x+18,y+211) if mobile else (x+474,y+65)
  b+=text(tx,ty,title,'label')
  for j,l in enumerate(lines):b+=text(tx,ty+28+j*22,l,'copy')
  dx,dy=x+18,y+50
  if i==0:
   b+=box(dx,dy+39,120,'Domain','x / y / z')
   b+=wire(f'M{dx+120} {dy+71}h22v-45h14M{dx+142} {dy+71}v40h14')
   b+=box(dx+156,dy,132,'2D plan')+box(dx+156,dy+86,132,'3D scene')
   b+=f'<circle cx="{dx+142}" cy="{dy+71}" r="5" class="signal"/>'
  elif i==1:
   b+=box(dx,dy,125,'Input #42')+box(dx+162,dy,126,'Validate')+wire(f'M{dx+125} {dy+24}h37')
   b+=wire(f'M{dx+225} {dy+48}v25h-80')+box(dx+62,dy+77,226,'Commit once','shared state → clients')
  elif i==2:
   b+=box(dx,dy,125,'Library v2')+box(dx+164,dy,124,'New work')+wire(f'M{dx+125} {dy+24}h39')
   b+=box(dx,dy+84,125,'Lesson v1')+box(dx+164,dy+84,124,'HW v1')
   b+=text(dx+144,dy+73,'SNAPSHOTS','kicker',**{'text-anchor':'middle'})
  else:
   for k,label in enumerate(['Checks','Backup','Release']):
    b+=box(dx+k*99,dy,90,label)
    if k<2:b+=wire(f'M{dx+k*99+90} {dy+24}h9')
   b+=wire(f'M{dx+243} {dy+48}v31')+box(dx+174,dy+85,114,'Health')
   b+=wire(f'M{dx+174} {dy+109}H{dx+118}')+box(dx,dy+85,118,'Rollback')
 svg('engineering-decisions'+('-mobile' if mobile else '')+'.svg',w,h,'Engineering decisions — shared models, server rules, snapshots and recovery','Four animated diagrams show shared 2D/3D data, authoritative realtime state, immutable assignment snapshots, and checked releases with recovery. All labels stay visible, including with reduced motion.',b)
for mobile in (False,True): hero(mobile);highlights(mobile)
