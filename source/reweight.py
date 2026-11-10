import bpy, numpy as np, mathutils
bpy.ops.wm.open_mainfile(filepath='/home/claude/blender/naiwa_rig.blend')
ob=bpy.data.objects['Naiwa']; rig=bpy.data.objects['NaiwaRig']
G={g.name:g for g in ob.vertex_groups}
armb={'L':['upperarm.L','forearm.L','hand.L'],'R':['upperarm.R','forearm.R','hand.R']}
allarm=sum(armb.values(),[])
def ss(e0,e1,x):
    t=np.clip((x-e0)/(e1-e0),0,1); return t*t*(3-2*t)
seg={b.name:(np.array(b.head_local),np.array(b.tail_local)) for b in rig.data.bones}
def segd(p,a,b):
    ab=b-a; t=np.clip(np.dot(p-a,ab)/np.dot(ab,ab),0,1); return np.linalg.norm(a+ab*t-p)
idx={g.index:g.name for g in ob.vertex_groups}
import collections
me=ob.data; VV=np.array([v.co[:] for v in me.vertices]); nb=collections.defaultdict(list)
for e in me.edges: a,b=e.vertices; nb[a].append(b); nb[b].append(a)
island=set()
for sx in (1,-1):
    seed=int(np.argmin(np.linalg.norm(VV-np.array([0.24*sx,-0.05,0.33]),axis=1))); seen={seed}; q=[seed]
    while q:
        u=q.pop()
        for w2 in nb[u]:
            if w2 not in seen and VV[w2,2]<0.43: seen.add(w2); q.append(w2)
    island|=seen
for v in ob.data.vertices:
    x,y,z=v.co; ax=abs(x); side='L' if x>0 else 'R'
    m=ss(0.185,0.215,ax)*ss(0.24,0.27,z)*ss(0.79,0.69,z)
    if v.index in island or (ax>0.185 and 0.27<z<0.42): m=1.0
    w={idx[g.group]:g.weight for g in v.groups}
    body={k:val for k,val in w.items() if k not in allarm}
    s=sum(body.values())
    if s<1e-4:
        body={'chest':1.0} if z>0.5 else {'pelvis':1.0}; s=1
    body={k:val/s*(1-m) for k,val in body.items()}
    p=np.array(v.co[:])
    d=np.array([segd(p,*seg[b]) for b in armb[side]]); aw=np.exp(-d/0.025); aw/=aw.sum()
    new=dict(body)
    for b,a in zip(armb[side],aw): new[b]=new.get(b,0)+m*a
    for k in w: G[k].remove([v.index])
    for k,val in new.items():
        if val>0.002: G[k].add([v.index],val,'REPLACE')
bpy.ops.wm.save_as_mainfile(filepath='/home/claude/blender/naiwa_rig.blend'); print('ok')
