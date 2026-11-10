import bpy
bpy.ops.wm.open_mainfile(filepath='/home/claude/blender/naiwa_rig.blend')
ob=bpy.data.objects['Naiwa']; G={g.name:g for g in ob.vertex_groups}; idx={g.index:g.name for g in ob.vertex_groups}
def ss(e0,e1,x):
    t=min(1,max(0,(x-e0)/(e1-e0))); return t*t*(3-2*t)
for v in ob.data.vertices:
    z=v.co.z; w={idx[g.group]:g.weight for g in v.groups}; h=w.get('head',0)
    if h<=0: continue
    keep=h*ss(0.72,0.82,z); moved=h-keep
    if moved<1e-4: continue
    if keep>0.002: G['head'].add([v.index],keep,'REPLACE')
    else: G['head'].remove([v.index])
    G['chest'].add([v.index],w.get('chest',0)+moved,'REPLACE')
bpy.ops.wm.save_as_mainfile(filepath='/home/claude/blender/naiwa_rig.blend'); print('ok')
