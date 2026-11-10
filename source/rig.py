import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath='/home/claude/blender/naiwa_clean.blend')
ob=bpy.data.objects['Naiwa']
arm_data=bpy.data.armatures.new('NaiwaRig'); rig=bpy.data.objects.new('NaiwaRig',arm_data)
bpy.context.scene.collection.objects.link(rig); bpy.context.view_layer.objects.active=rig
bpy.ops.object.mode_set(mode='EDIT')
E=arm_data.edit_bones
def bone(name,h,t,parent=None,conn=False,roll=0):
    b=E.new(name); b.head=h; b.tail=t; b.roll=roll
    if parent: b.parent=E[parent]; b.use_connect=conn
    return b
bone('root',(0,0,0),(0,0,0.12))
bone('pelvis',(0,0,0.28),(0,0,0.50),'root')
bone('chest',(0,0,0.50),(0,0,0.76),'pelvis',True)
bone('head',(0,0,0.76),(0,0,1.0),'chest',True)
for s,sx in (('L',1),('R',-1)):
    bone(f'upperarm.{s}',(0.20*sx,0,0.71),(0.24*sx,0,0.52),'chest')
    bone(f'forearm.{s}',(0.24*sx,0,0.52),(0.24*sx,-0.01,0.37),f'upperarm.{s}',True)
    bone(f'hand.{s}',(0.24*sx,-0.01,0.37),(0.235*sx,-0.01,0.29),f'forearm.{s}',True)
    bone(f'thigh.{s}',(0.115*sx,0,0.30),(0.12*sx,0,0.17),'pelvis')
    bone(f'shin.{s}',(0.12*sx,0,0.17),(0.12*sx,0,0.05),f'thigh.{s}',True)
    bone(f'foot.{s}',(0.12*sx,0,0.05),(0.12*sx,-0.11,0.02),f'shin.{s}',True)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); rig.select_set(True); bpy.context.view_layer.objects.active=rig
bpy.ops.object.parent_set(type='ARMATURE_AUTO')
# report unweighted verts
vg=ob.vertex_groups; unw=sum(1 for v in ob.data.vertices if not any(g.weight>0.01 for g in v.groups))
print('groups',len(vg),'unweighted',unw,'of',len(ob.data.vertices))
bpy.ops.wm.save_as_mainfile(filepath='/home/claude/blender/naiwa_rig.blend')
