import bpy, mathutils
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath='trellis_raw.glb')
ob=[o for o in bpy.context.scene.objects if o.type=='MESH'][0]
for o in list(bpy.context.scene.objects):
    if o!=ob and o.type=='EMPTY':
        ob.parent=None
bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); bpy.context.view_layer.objects.active=ob
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
for o in list(bpy.context.scene.objects):
    if o!=ob: bpy.data.objects.remove(o)
ob.name='Naiwa'; ob.data.name='NaiwaMesh'
# merge duplicate verts, decimate
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.remove_doubles(threshold=0.0005); bpy.ops.object.mode_set(mode='OBJECT')
d=ob.modifiers.new('dec','DECIMATE'); d.ratio=18000/len(ob.data.polygons); bpy.ops.object.modifier_apply(modifier='dec')
bpy.ops.object.shade_smooth()
# feet on ground, centred
zs=[ (ob.matrix_world@v.co).z for v in ob.data.vertices]; xs=[v.co.x for v in ob.data.vertices]; ys=[v.co.y for v in ob.data.vertices]
off=mathutils.Vector((-(max(xs)+min(xs))/2,-(max(ys)+min(ys))/2,-min(zs)))
for v in ob.data.vertices: v.co+=off
# warmer texture
img=bpy.data.images['Image_0']; img.filepath='/home/claude/blender/tex_0_warm.png'; img.source='FILE'; img.reload(); img.pack()
for i in bpy.data.images:
    if not i.packed_file: i.pack()
print('faces',len(ob.data.polygons),'height',round(ob.dimensions.z,3))
bpy.ops.wm.save_as_mainfile(filepath='/home/claude/blender/naiwa_clean.blend')
