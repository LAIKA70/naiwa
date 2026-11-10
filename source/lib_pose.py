import bpy, math, mathutils
def prep(rig):
    for b in rig.pose.bones: b.rotation_mode='QUATERNION'
def wrot(rig,name,axis,deg):
    """rotate bone around an ARMATURE-space axis (x=character left, y=back, z=up), relative to rest"""
    pb=rig.pose.bones[name]; B=pb.bone.matrix_local.to_3x3()
    q=mathutils.Quaternion(axis,math.radians(deg))
    loc=(B.inverted()@q.to_matrix()@B).to_quaternion()
    pb.rotation_quaternion=pb.rotation_quaternion@loc
def reset(rig):
    for b in rig.pose.bones: b.rotation_quaternion=(1,0,0,0); b.location=(0,0,0)
