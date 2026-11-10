import bpy, math, mathutils
bpy.ops.wm.open_mainfile(filepath='/home/claude/blender/naiwa_rig.blend')
ob=bpy.data.objects['Naiwa']; rig=bpy.data.objects['NaiwaRig']
# give stray verts to nearest bone
bones=[(b.name,rig.matrix_world@b.head_local,rig.matrix_world@b.tail_local) for b in rig.data.bones]
def segd(p,a,b):
    ab=b-a; t=max(0,min(1,(p-a).dot(ab)/ab.length_squared)); return (a+ab*t-p).length
n=0
for v in ob.data.vertices:
    if not any(g.weight>0.01 for g in v.groups):
        p=ob.matrix_world@v.co; nm=min(bones,key=lambda b:segd(p,b[1],b[2]))[0]
        ob.vertex_groups[nm].add([v.index],1.0,'REPLACE'); n+=1
print('fixed',n)
bpy.ops.wm.save_as_mainfile(filepath='/home/claude/blender/naiwa_rig.blend')
P=rig.pose.bones
P['upperarm.L'].rotation_mode=P['upperarm.R'].rotation_mode='XYZ'
P['upperarm.L'].rotation_euler=(0,math.radians(-70),0) if False else (0,0,0)
import sys
