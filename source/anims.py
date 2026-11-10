import bpy, math, sys, mathutils
sys.path.insert(0,'/home/claude/blender'); from lib_pose import *
bpy.ops.wm.open_mainfile(filepath='/home/claude/blender/naiwa_rig.blend')
rig=bpy.data.objects['NaiwaRig']; prep(rig); sc=bpy.context.scene; sc.render.fps=30
X,Y,Z=(1,0,0),(0,1,0),(0,0,1)
bpy.context.view_layer.objects.active=rig
if not rig.animation_data: rig.animation_data_create()
S=math.sin
def pose(ops,rootz=0.0):
    reset(rig)
    for b,ax,d in ops:
        if abs(d)>1e-6: wrot(rig,b,ax,d)
    rig.pose.bones['root'].location=(0,rootz,0)
def key(f):
    for pb in rig.pose.bones:
        pb.keyframe_insert('rotation_quaternion',frame=f)
    rig.pose.bones['root'].keyframe_insert('location',frame=f)
def new_action(name):
    a=bpy.data.actions.new(name); a.use_fake_user=True; rig.animation_data.action=a; return a
def hands_on_belly(k=1):
    return [('upperarm.L',X,-30*k),('upperarm.R',X,-30*k),('upperarm.L',Y,8*k),('upperarm.R',Y,-8*k),
            ('forearm.L',X,-70*k),('forearm.R',X,-70*k),('forearm.L',Z,-25*k),('forearm.R',Z,25*k)]
acts=[]
# ---------------- idle (2s loop) ----------------
acts.append(new_action('idle'))
for f in range(0,61,4):
    t=f/60*2*math.pi
    pose([('chest',X,1.5*S(t)),('head',X,-1.5*S(t)),('upperarm.L',Y,-2-1.5*S(t)),('upperarm.R',Y,2+1.5*S(t)),('pelvis',Y,0.8*S(t))])
    key(f)
# ---------------- walk (24-frame loop) ----------------
acts.append(new_action('walk'))
for f in range(0,25,2):
    p=f/24*2*math.pi; s=S(p); c=math.cos(p)
    ops=[('thigh.L',X,-26*s),('thigh.R',X,26*s),
         ('shin.L',X,max(0,c)*38),('shin.R',X,max(0,-c)*38),
         ('foot.L',X,-max(0,c)*15+8*s),('foot.R',X,-max(0,-c)*15-8*s),
         ('upperarm.L',X,20*s),('upperarm.R',X,-20*s),('forearm.L',X,-12),('forearm.R',X,-12),
         ('pelvis',Y,4*s),('pelvis',Z,-5*s),('chest',X,5),('chest',Z,4*s),('head',Z,-3*s),('head',X,-4)]
    pose(ops,rootz=0.012*abs(c)-0.004)
    key(f)
# ---------------- laugh (6s = 180 frames) ----------------
acts.append(new_action('laugh'))
for f in range(0,181,2):
    t=f/30; sh=S(t*2*math.pi*6)            # 6Hz shake
    if t<0.5:   k=t/0.5; ops=hands_on_belly(k)+[('head',X,-28*k),('chest',X,-8*k)]; rz=0
    elif t<3.0: ops=hands_on_belly()+[('head',X,-30+5*sh),('chest',X,-10+4*sh),('chest',Y,2*sh),('pelvis',Z,2*sh)]; rz=0.006*abs(sh)
    elif t<3.5: k=(t-3)/0.5; ops=hands_on_belly()+[('chest',X,-10+38*k),('head',X,-30+40*k),('thigh.L',X,-14*k),('thigh.R',X,-14*k),('shin.L',X,26*k),('shin.R',X,26*k)]; rz=-0.03*k
    elif t<4.6: ops=hands_on_belly()+[('chest',X,28+5*sh),('head',X,10+6*sh),('thigh.L',X,-14),('thigh.R',X,-14),('shin.L',X,26),('shin.R',X,26),('pelvis',Z,3*sh)]; rz=-0.03+0.006*abs(sh)
    elif t<5.0: k=(t-4.6)/0.4; ops=[('chest',X,28*(1-k)-6*k),('head',X,10*(1-k)-22*k),('upperarm.L',Y,-125*k),('upperarm.R',Y,125*k),('forearm.L',Y,-85*k),('forearm.R',Y,85*k),
                ('thigh.L',X,-14*(1-k)),('thigh.R',X,-14*(1-k)),('shin.L',X,26*(1-k)),('shin.R',X,26*(1-k))]; rz=-0.03*(1-k)
    elif t<5.6: ops=[('chest',X,-6+3*sh),('head',X,-22+4*sh),('upperarm.L',Y,-125),('upperarm.R',Y,125),('forearm.L',Y,-85),('forearm.R',Y,85),('pelvis',Z,4*sh)]; rz=0.005*abs(sh)
    else:       k=(t-5.6)/0.4; ops=[('chest',X,-6*(1-k)),('head',X,-22*(1-k)),('upperarm.L',Y,-125*(1-k)),('upperarm.R',Y,125*(1-k)),('forearm.L',Y,-85*(1-k)),('forearm.R',Y,85*(1-k))]; rz=0
    pose(ops,rz); key(f)
# ---------------- battle (12.7s = 381 frames) ----------------
acts.append(new_action('battle'))
def stance(k):
    return [('thigh.L',Y,-22*k),('thigh.R',Y,22*k),('thigh.L',X,-18*k),('thigh.R',X,-18*k),
            ('shin.L',Y,20*k),('shin.R',Y,-20*k),('shin.L',X,32*k),('shin.R',X,32*k),('foot.L',X,-12*k),('foot.R',X,-12*k)]
def push(side,k):   # side 'L' or 'R' palm push forward, other fist at chest
    o='R' if side=='L' else 'L'; sg=1 if side=='L' else -1
    return [(f'upperarm.{side}',X,-85*k),(f'upperarm.{side}',Y,-15*sg*k),(f'forearm.{side}',X,-8*k),(f'hand.{side}',X,40*k),
            (f'upperarm.{o}',X,-45*k),(f'forearm.{o}',X,-95*k),(f'forearm.{o}',Z,30*sg*k),('chest',Z,-14*sg*k),('head',Z,10*sg*k)]
for f in range(0,382,2):
    t=f/30
    if t<2.5:   k=min(1,t/0.4); ops=hands_on_belly(k)+[('chest',X,22*k+2*S(t*5)),('head',X,18*k)]; rz=-0.01*k
    elif t<3.1: k=(t-2.5)/0.6; ops=hands_on_belly(1-k)+[('chest',X,22*(1-k)-6*k),('head',X,18*(1-k)-8*k)]+stance(k)+push('L',k); rz=-0.01*(1-k)-0.045*k
    elif t<11.2:
        seg=int((t-3.1)//2); f2=((t-3.1)%2)/2; side='L' if seg%2==0 else 'R'
        thr=min(1,f2/0.08) if seg>0 else 1
        prev='R' if side=='L' else 'L'
        if seg>0 and f2<0.08: ops=stance(1)+[(b,a,d*(1-thr)) for b,a,d in push(prev,1)]+[(b,a,d*thr) for b,a,d in push(side,1)]
        else: ops=stance(1)+push(side,1)
        ops+=[('chest',X,-6+1.5*S(t*2.2)),('head',X,-8)]
        rz=-0.045+0.004*S(t*2.2)
    else:       k=min(1,(t-11.2)/0.6); ops=[(b,a,d*(1-k)) for b,a,d in stance(1)+push('R',1)]; rz=-0.045*(1-k)
    pose(ops,rz); key(f)
rig.animation_data.action=acts[0]
# make sure every action is exported: park each on its own NLA track
for a in acts:
    tr=rig.animation_data.nla_tracks.new(); tr.name=a.name; st=tr.strips.new(a.name,int(a.frame_range[0]),a); tr.mute=True
rig.animation_data.action=None
reset(rig)
print('actions',[ (a.name,a.frame_range[:]) for a in acts])
bpy.ops.wm.save_as_mainfile(filepath='/home/claude/blender/naiwa_anim.blend')
