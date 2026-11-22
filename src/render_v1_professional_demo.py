"""Professional 1080p AMR coupling demonstration with coherent mechanism motion."""
from pathlib import Path
import math
import numpy as np
import imageio.v2 as imageio
import vtk
from vtk.util.numpy_support import vtk_to_numpy

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'outputs'/'v1'; PARTS=OUT/'parts'
W,H,FPS=1920,1088,30
COL={
 'base':(.25,.29,.32),'guide_left':(.48,.52,.55),'guide_right':(.48,.52,.55),'fixed_load_socket':(.12,.14,.16),
 'jaw_left':(.96,.55,.06),'jaw_right':(.96,.55,.06),'pivot_left':(.76,.79,.82),'pivot_right':(.76,.79,.82),
 'release_yoke':(.12,.43,.80),'link_left':(.22,.60,.92),'link_right':(.22,.60,.92),'spring_left':(.86,.88,.90),
 'spring_right':(.86,.88,.90),'linear_actuator':(.08,.22,.38),'pin_sensor':(.08,.72,.30),'release_sensor':(.08,.72,.30),
 'top_cover':(.72,.76,.79),'striker_arm':(.56,.59,.62),'wear_insert_left':(.02,.75,.82),'wear_insert_right':(.02,.75,.82),
 'jaw_roller_left':(.90,.92,.94),'jaw_roller_right':(.90,.92,.94),'energy_bumper_left':(.80,.16,.09),
 'energy_bumper_right':(.80,.16,.09),'isolation_front_left':(.10,.11,.12),'isolation_front_right':(.10,.11,.12),
 'isolation_rear_left':(.10,.11,.12),'isolation_rear_right':(.10,.11,.12),'link_guard_left':(.20,.22,.24),'link_guard_right':(.20,.22,.24)
}

def stl_actor(name,color):
    r=vtk.vtkSTLReader(); r.SetFileName(str(PARTS/f'{name}.stl')); r.Update(); m=vtk.vtkPolyDataMapper(); m.SetInputConnection(r.GetOutputPort())
    a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetColor(*color); a.GetProperty().SetInterpolationToPBR(); a.GetProperty().SetMetallic(.28); a.GetProperty().SetRoughness(.34); return a

def cube(center,size,color,opacity=1):
    s=vtk.vtkCubeSource(); s.SetCenter(*center); s.SetXLength(size[0]); s.SetYLength(size[1]); s.SetZLength(size[2]); m=vtk.vtkPolyDataMapper(); m.SetInputConnection(s.GetOutputPort())
    a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetColor(*color); a.GetProperty().SetOpacity(opacity); a.GetProperty().SetInterpolationToPBR(); a.GetProperty().SetRoughness(.42); return a

def cylinder(center,radius,height,color,axis='z'):
    s=vtk.vtkCylinderSource(); s.SetCenter(0,0,0); s.SetRadius(radius); s.SetHeight(height); s.SetResolution(48); m=vtk.vtkPolyDataMapper(); m.SetInputConnection(s.GetOutputPort())
    a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetColor(*color); a.GetProperty().SetInterpolationToPBR(); a.GetProperty().SetRoughness(.38)
    if axis=='x': a.RotateZ(-90)
    elif axis=='z': a.RotateX(90)
    a.SetPosition(*center)
    return a

def rounded_body(center,size,color):
    # Central box plus end cylinders gives a clean industrial rounded AMR footprint.
    x,y,z=center; lx,ly,lz=size; parts=[cube(center,(lx-ly,ly,lz),color)]
    for sx in (-1,1): parts.append(cylinder((x+sx*(lx-ly)/2,y,z),ly/2,lz,color,'z'))
    return parts

def actor_between(p0,p1,r,color):
    line=np.subtract(p1,p0); L=float(np.linalg.norm(line)); mid=np.add(p0,p1)/2
    s=vtk.vtkCylinderSource(); s.SetRadius(r); s.SetHeight(L); s.SetResolution(28); m=vtk.vtkPolyDataMapper(); m.SetInputConnection(s.GetOutputPort()); a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetColor(*color)
    t=vtk.vtkTransform(); t.Translate(*mid); y=np.array([0.,1.,0.]); v=line/L; axis=np.cross(y,v); dot=float(np.clip(np.dot(y,v),-1,1)); angle=math.degrees(math.acos(dot))
    if np.linalg.norm(axis)>1e-8: t.RotateWXYZ(angle,*axis)
    elif dot<0: t.RotateX(180)
    a.SetUserTransform(t); return a

def ease(q): return q*q*(3-2*q)
def lerp(a,b,q): return a+(b-a)*ease(max(0,min(1,q)))

ren=vtk.vtkRenderer(); ren.SetGradientBackground(True); ren.SetBackground(.72,.82,.90); ren.SetBackground2(.96,.97,.98)
win=vtk.vtkRenderWindow(); win.SetOffScreenRendering(1); win.SetSize(W,H); win.SetMultiSamples(8); win.AddRenderer(ren)

# Warehouse floor, safe travel lane and shelving.
ren.AddActor(cube((-80,0,-8),(1250,620,12),(.46,.48,.49)))
for y in (-92,92): ren.AddActor(cube((-80,y,-1),(1150,8,2),(.95,.72,.06)))
for y in (-270,270):
    for x in (-420,-140,140,420):
        ren.AddActor(cube((x,y,90),(12,52,180),(.18,.22,.25)))
    for z in (30,90,150): ren.AddActor(cube((0,y,z),(900,45,8),(.26,.30,.34)))
    for x in (-350,-210,-70,70,210,350):
        ren.AddActor(cube((x,y,z if False else 46),(105,38,42),(.62,.40,.18)))

# Real coupling CAD. Guards and top cover stay transparent during close-ups.
parts={}
for n,c in COL.items():
    if n in ('linear_actuator','link_left','link_right'): continue
    a=stl_actor(n,c); parts[n]=a; ren.AddActor(a)
parts['top_cover'].GetProperty().SetOpacity(.18)
parts['link_guard_left'].GetProperty().SetOpacity(.34); parts['link_guard_right'].GetProperty().SetOpacity(.34)

# AMR industrial body, bumper, lid, lidar, status light, wheels and sensors.
amr=[]; amr += rounded_body((-190,0,60),(190,128,76),(.72,.76,.79)); amr += rounded_body((-190,0,34),(205,138,25),(.08,.11,.14))
amr += [cube((-195,0,103),(120,88,10),(.20,.24,.28)),cylinder((-205,0,122),18,30,(.06,.08,.10)),cylinder((-205,0,140),8,7,(.12,.82,.34))]
amr += [cube((-105,-36,54),(8,22,14),(.03,.30,.45)),cube((-105,36,54),(8,22,14),(.03,.30,.45))]
amr_wheels=[]
for x in (-220,-155):
    for y in (-62,62): amr_wheels.append(cylinder((x,y,25),21,13,(.035,.04,.045),'y'))
amr += amr_wheels
for a in amr: ren.AddActor(a)

# Trolley with tray, rails, four casters and visible payload boxes.
trolley=[cube((205,0,66),(155,118,12),(.50,.54,.57)),cube((205,-55,86),(155,7,34),(.38,.42,.45)),cube((205,55,86),(155,7,34),(.38,.42,.45)),cube((275,0,86),(7,110,34),(.38,.42,.45)),
         cube((130,0,45),(12,48,34),(.32,.35,.38))]
for x in (145,265):
    for y in (-48,48):
        trolley += [cube((x,y,34),(9,9,34),(.45,.48,.50)),cylinder((x,y,14),15,9,(.05,.055,.06),'y')]
trolley += [cube((175,-22,103),(58,48,58),(.72,.43,.16)),cube((230,20,100),(48,42,50),(.16,.42,.72)),cube((238,-27,91),(35,30,30),(.78,.68,.15))]
for a in trolley: ren.AddActor(a)

# Replace the merged actuator with an explicitly animated body, rod and clevis.
act_body=cube((-73,0,26),(36,34,28),(.08,.22,.38)); act_rod=cylinder((-47,0,26),4,22,(.82,.84,.86),'x'); act_clevis=cube((-36,0,26),(9,20,18),(.30,.35,.39))
for a in (act_body,act_rod,act_clevis): ren.AddActor(a)
dynamic_links=[]

# On-screen UI.
panel=cube((0,0,0),(1,1,1),(0,0,0)) # unused 3D placeholder keeps helper set compact
title=vtk.vtkTextActor(); title.SetPosition(58,1000); title.GetTextProperty().SetFontSize(34); title.GetTextProperty().SetBold(True); title.GetTextProperty().SetColor(.04,.08,.12); title.GetTextProperty().SetBackgroundColor(.96,.97,.98); title.GetTextProperty().SetBackgroundOpacity(.82); ren.AddActor2D(title)
subtitle=vtk.vtkTextActor(); subtitle.SetPosition(60,62); subtitle.GetTextProperty().SetFontSize(23); subtitle.GetTextProperty().SetColor(.03,.12,.20); subtitle.GetTextProperty().SetBackgroundColor(.96,.97,.98); subtitle.GetTextProperty().SetBackgroundOpacity(.82); ren.AddActor2D(subtitle)
state=vtk.vtkTextActor(); state.SetPosition(1570,1005); state.GetTextProperty().SetFontSize(25); state.GetTextProperty().SetBold(True); state.GetTextProperty().SetBackgroundColor(.96,.97,.98); state.GetTextProperty().SetBackgroundOpacity(.82); ren.AddActor2D(state)

# Static receiver parts translate with the AMR. The jaw/roller pairs, release
# yoke and striker are transformed separately below and must not receive the
# group translation a second time.
dynamic_names={'striker_arm','jaw_left','jaw_right','jaw_roller_left','jaw_roller_right','release_yoke'}
receiver_names=[n for n in parts if n not in dynamic_names]; receiver=[parts[n] for n in receiver_names]
cam=ren.GetActiveCamera(); cam.SetViewUp(0,0,1)

def rotpt(p,pivot,deg):
    a=math.radians(deg); x,y=p[0]-pivot[0],p[1]-pivot[1]; return (pivot[0]+x*math.cos(a)-y*math.sin(a),pivot[1]+x*math.sin(a)+y*math.cos(a),p[2])

def set_jaw(actor_name,roller_name,sign,ang,rx):
    # Match CAD opening direction and move roller rigidly with the jaw.
    pivot=(-22,sign*21,0); deg=sign*ang
    t=vtk.vtkTransform(); t.PostMultiply(); t.Translate(-pivot[0],-pivot[1],0); t.RotateZ(deg); t.Translate(pivot[0]+rx,pivot[1],0)
    parts[actor_name].SetUserTransform(t); parts[roller_name].SetUserTransform(t)

def update_links(rx,open_q):
    global dynamic_links
    for a in dynamic_links: ren.RemoveActor(a)
    dynamic_links=[]; yoke_x=-37-11*open_q
    for sign in (1,-1):
        tail=rotpt((-27,sign*22,25),(-22,sign*21,25),sign*24*open_q); tail=(tail[0]+rx,tail[1],tail[2])
        yp=(yoke_x+rx,sign*25,25); a=actor_between(yp,tail,3.2,(.22,.60,.92)); dynamic_links.append(a); ren.AddActor(a)

def group_position(group,x):
    for a in group: a.SetPosition(x,0,0)

def set_camera(pos,focal): cam.SetPosition(*pos); cam.SetFocalPoint(*focal); ren.ResetCameraClippingRange()

def grab():
    win.Render(); c=vtk.vtkWindowToImageFilter(); c.SetInput(win); c.ReadFrontBufferOff(); c.Update(); a=vtk_to_numpy(c.GetOutput().GetPointData().GetScalars()).reshape(H,W,-1); return np.flipud(a[:,:,:3])

VIDEO=OUT/'amr_coupler_v1_amr_operation.mp4'
with imageio.get_writer(VIDEO,fps=FPS,codec='libx264',quality=9,output_params=['-pix_fmt','yuv420p','-movflags','+faststart']) as wr:
  for i in range(450):
    rx=0.; tx=0.; open_q=0.; sensor_locked=False; body_alpha=1.; phase=''
    if i<75: # wide approach, stop 40 mm before capture
        q=i/74; rx=lerp(-180,-40,q); set_camera((60,-560,420),(20,0,48)); title.SetInput('AUTONOMOUS APPROACH'); subtitle.SetInput('AMR reverses inside the marked docking lane at controlled speed.'); phase='ALIGNING'
    elif i<165: # cutaway final capture
        q=(i-75)/89; rx=lerp(-40,0,q); open_q=math.sin(math.pi*q); sensor_locked=q>.82; body_alpha=.16
        set_camera((170,-205,185),(0,0,24)); title.SetInput('CUTAWAY: PASSIVE MECHANICAL CAPTURE'); subtitle.SetInput('Striker rolls both jaws outward; return springs snap them into the groove.'); phase='CAPTURING' if not sensor_locked else 'LOCKED'
    elif i<225: # verify and zoom out
        q=(i-165)/59; sensor_locked=True; body_alpha=lerp(.16,1,q); set_camera((lerp(170,40,q),lerp(-205,-560,q),lerp(185,420,q)),(lerp(0,20,q),0,lerp(24,48,q)))
        title.SetInput('DUAL-SENSOR LOCK CONFIRMED'); subtitle.SetInput('Fixed socket carries tow load. Actuator remains unloaded and unpowered.'); phase='READY TO TOW'
    elif i<330: # tow whole train through aisle
        q=(i-225)/104; rx=tx=lerp(0,-360,q); sensor_locked=True; set_camera((40+rx,-560,420),(20+rx,0,48)); title.SetInput('TOWING LOADED TROLLEY'); subtitle.SetInput('AMR, coupler and payload move as one locked system through the warehouse.'); phase='TOWING'
    elif i<390: # park and release closeup
        q=(i-330)/59; rx=tx=-360; open_q=ease(q); sensor_locked=False; body_alpha=.18; set_camera((-190,-205,185),(-360,0,24)); title.SetInput('PARK, UNLOAD AND POWERED RELEASE'); subtitle.SetInput('Release yoke retracts both links only after the trolley is restrained.'); phase='RELEASING'
    else: # physical separation and reset
        q=(i-390)/59; tx=-360; rx=lerp(-360,-500,q); open_q=1 if q<.7 else 1-(q-.7)/.3; body_alpha=lerp(.18,1,q)
        set_camera((-210,-560,400),(-315,0,48)); title.SetInput('DECOUPLED AND READY'); subtitle.SetInput('AMR drives clear; trolley remains parked and jaws return to capture position.'); phase='CLEAR'

    # Position AMR/receiver and trolley/striker groups.
    group_position(amr,rx); group_position(receiver,rx); group_position(trolley,tx); parts['striker_arm'].SetPosition(tx,0,0)
    for a in amr: a.GetProperty().SetOpacity(body_alpha)
    for n in ('top_cover','link_guard_left','link_guard_right'): parts[n].GetProperty().SetOpacity(.12 if body_alpha<.5 else (.18 if n=='top_cover' else .34))
    parts['striker_arm'].GetProperty().SetOpacity(.28 if body_alpha<.5 else 1.0)
    # Coherent latch, yoke, links and actuator rod motion.
    set_jaw('jaw_left','jaw_roller_left',1,24*open_q,rx); set_jaw('jaw_right','jaw_roller_right',-1,24*open_q,rx)
    parts['release_yoke'].SetPosition(rx-11*open_q,0,0); update_links(rx,open_q)
    act_body.SetPosition(rx,0,0); act_rod.SetPosition(rx-7*open_q,0,0); act_clevis.SetPosition(rx-11*open_q,0,0)
    parts['pin_sensor'].GetProperty().SetColor(*((.08,.82,.25) if sensor_locked else (.86,.12,.08)))
    state.SetInput('STATUS: '+phase); state.GetTextProperty().SetColor(*((.04,.55,.16) if phase in ('LOCKED','READY TO TOW','TOWING','CLEAR') else (.82,.34,.03)))
    wr.append_data(grab())

print(VIDEO)
