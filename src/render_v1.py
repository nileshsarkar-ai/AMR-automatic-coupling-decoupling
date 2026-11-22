"""Render V1 turntable and zoom-out AMR/trolley operating demonstration."""
from pathlib import Path
import math
import numpy as np
import imageio.v2 as imageio
import vtk
from vtk.util.numpy_support import vtk_to_numpy

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'outputs'/'v1'; PARTS=OUT/'parts'
COL={
 'base':(.28,.31,.34),'guide_left':(.48,.52,.55),'guide_right':(.48,.52,.55),'fixed_load_socket':(.18,.20,.22),
 'jaw_left':(.92,.52,.08),'jaw_right':(.92,.52,.08),'pivot_left':(.75,.77,.80),'pivot_right':(.75,.77,.80),
 'release_yoke':(.20,.45,.75),'link_left':(.25,.55,.82),'link_right':(.25,.55,.82),'spring_left':(.85,.85,.88),
 'spring_right':(.85,.85,.88),'linear_actuator':(.12,.25,.42),'pin_sensor':(.10,.70,.32),'release_sensor':(.10,.70,.32),
 'top_cover':(.68,.72,.75),'striker_arm':(.55,.58,.61),'wear_insert_left':(.10,.72,.78),'wear_insert_right':(.10,.72,.78),
 'jaw_roller_left':(.88,.90,.92),'jaw_roller_right':(.88,.90,.92),'energy_bumper_left':(.78,.18,.12),
 'energy_bumper_right':(.78,.18,.12),'isolation_front_left':(.15,.15,.16),'isolation_front_right':(.15,.15,.16),
 'isolation_rear_left':(.15,.15,.16),'isolation_rear_right':(.15,.15,.16),'link_guard_left':(.22,.24,.27),'link_guard_right':(.22,.24,.27)
}

def part_actor(n,c):
    rd=vtk.vtkSTLReader(); rd.SetFileName(str(PARTS/f'{n}.stl')); rd.Update(); mp=vtk.vtkPolyDataMapper(); mp.SetInputConnection(rd.GetOutputPort())
    a=vtk.vtkActor(); a.SetMapper(mp); a.GetProperty().SetColor(*c); a.GetProperty().SetInterpolationToPBR(); a.GetProperty().SetMetallic(.25); a.GetProperty().SetRoughness(.4)
    if n=='top_cover': a.GetProperty().SetOpacity(.25)
    return a

def cube(center,size,color,rounded=False):
    s=vtk.vtkCubeSource(); s.SetCenter(*center); s.SetXLength(size[0]); s.SetYLength(size[1]); s.SetZLength(size[2]); m=vtk.vtkPolyDataMapper(); m.SetInputConnection(s.GetOutputPort())
    a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetColor(*color); a.GetProperty().SetInterpolationToPBR(); a.GetProperty().SetRoughness(.42); return a

def wheel(center):
    s=vtk.vtkCylinderSource(); s.SetCenter(*center); s.SetRadius(17); s.SetHeight(10); s.SetResolution(40); m=vtk.vtkPolyDataMapper(); m.SetInputConnection(s.GetOutputPort())
    a=vtk.vtkActor(); a.SetMapper(m); a.RotateX(90); a.GetProperty().SetColor(.05,.06,.07); return a

def setup(parts_only=False):
    ren=vtk.vtkRenderer(); ren.SetBackground(.93,.94,.95); actors={}
    for n,c in COL.items(): actors[n]=part_actor(n,c); ren.AddActor(actors[n])
    amr=[]; trolley=[]
    if not parts_only:
        amr += [cube((-180,0,55),(170,120,85),(.62,.66,.69)),cube((-190,0,101),(120,85,8),(.18,.22,.25))]
        for y in (-48,48): amr.append(wheel((-175,y,18)))
        trolley += [cube((195,0,63),(145,115,12),(.48,.50,.52)),cube((195,0,76),(135,105,12),(.68,.70,.71))]
        for x in (150,240):
            for y in (-45,45): trolley.append(wheel((x,y,25)))
        trolley += [cube((175,-18,104),(48,42,44),(.72,.43,.15)),cube((223,20,100),(42,38,36),(.18,.45,.70)),cube((220,-22,92),(30,28,20),(.70,.68,.20))]
        for a in amr+trolley: ren.AddActor(a)
    ground=cube((20,0,-6),(600,300,8),(.78,.79,.78)); ren.AddActor(ground)
    win=vtk.vtkRenderWindow(); win.SetOffScreenRendering(1); win.SetSize(1280,720); win.SetMultiSamples(8); win.AddRenderer(ren)
    return ren,win,actors,amr,trolley

def grab(win):
    win.Render(); c=vtk.vtkWindowToImageFilter(); c.SetInput(win); c.ReadFrontBufferOff(); c.Update(); a=vtk_to_numpy(c.GetOutput().GetPointData().GetScalars()).reshape(720,1280,-1)
    return np.flipud(a[:,:,:3])

# Final-version 360-degree video.
ren,win,actors,_,_=setup(True); cam=ren.GetActiveCamera(); cam.SetFocalPoint(0,0,20); cam.SetPosition(205,-225,150); cam.SetViewUp(0,0,1); ren.ResetCameraClippingRange()
imageio.imwrite(OUT/'amr_coupler_v1_preview.png',grab(win))
with imageio.get_writer(OUT/'amr_coupler_v1_360.mp4',fps=30,codec='libx264',quality=8,output_params=['-pix_fmt','yuv420p','-movflags','+faststart']) as w:
    for _ in range(180): w.append_data(grab(win)); cam.Azimuth(2); ren.ResetCameraClippingRange()

# Operational video: mechanism close-up -> zoom out -> tow loaded trolley -> release.
ren,win,actors,amr,trolley=setup(False); cam=ren.GetActiveCamera(); cam.SetViewUp(0,0,1)
title=vtk.vtkTextActor(); title.SetPosition(35,665); title.GetTextProperty().SetFontSize(24); title.GetTextProperty().SetBold(True); title.GetTextProperty().SetColor(.05,.08,.12); ren.AddActor2D(title)
sub=vtk.vtkTextActor(); sub.SetPosition(35,30); sub.GetTextProperty().SetFontSize(17); sub.GetTextProperty().SetColor(.06,.18,.32); ren.AddActor2D(sub)
receiver_names=[n for n in actors if n!='striker_arm']; receiver=[actors[n] for n in receiver_names]

def jaw_t(name,sign,angle,dx):
    t=vtk.vtkTransform(); t.PostMultiply(); t.Translate(22,-sign*21,0); t.RotateZ(-sign*angle); t.Translate(-22,sign*21,0); t.Translate(dx,0,0); actors[name].SetUserTransform(t)

with imageio.get_writer(OUT/'amr_coupler_v1_amr_operation.mp4',fps=30,codec='libx264',quality=8,output_params=['-pix_fmt','yuv420p','-movflags','+faststart']) as w:
  for i in range(300):
    angle=0; rx=tx=0; striker_extra=0
    if i<60:
      q=i/59; striker_extra=55*(1-q); angle=24*math.sin(math.pi*q)
      cam.SetPosition(165,-185,190); cam.SetFocalPoint(0,0,20); title.SetInput('1  LOW-IMPACT PASSIVE CAPTURE'); sub.SetInput('Striker cams both rolling jaws open; springs snap them closed without actuator power.')
    elif i<120:
      q=(i-60)/59; cam.SetPosition(170-30*q,-170-330*q,130+170*q); cam.SetFocalPoint(-5+20*q,0,30+25*q); title.SetInput('2  ZOOM OUT: AMR + LOADED TROLLEY'); sub.SetInput('Fixed socket carries towing load; sensors authorize motion only after full lock.')
    elif i<200:
      q=(i-120)/79; rx=tx=-85*q; cam.SetPosition(140-85*q,-500,300); cam.SetFocalPoint(15-85*q,0,55); title.SetInput('3  EFFICIENT AUTOMATIC TOWING'); sub.SetInput('Profile-specific acceleration and final approach speed minimize cycle time and impact.')
    elif i<235:
      q=(i-200)/34; rx=tx=-85; angle=24*q; title.SetInput('4  PARK, UNLOAD HITCH, POWER RELEASE'); sub.SetInput('Trolley restraint is applied before the actuator pulls the release yoke.')
    else:
      q=(i-235)/64; tx=-85; rx=-85-100*q; angle=24; title.SetInput('5  VERIFIED DECOUPLING'); sub.SetInput('AMR separates; trolley and payload remain parked. Springs reset after clearance.')
    for a in amr+trolley: a.SetVisibility(i>=60)
    for a in amr+receiver: a.SetPosition(rx,0,0)
    for a in trolley: a.SetPosition(tx,0,0)
    actors['striker_arm'].SetPosition(tx+striker_extra,0,0)
    jaw_t('jaw_left',1,angle,rx); jaw_t('jaw_right',-1,angle,rx)
    actors['release_yoke'].SetPosition(rx-11*(angle/24 if angle else 0),0,0)
    ren.ResetCameraClippingRange(); w.append_data(grab(win))
print(OUT/'amr_coupler_v1_amr_operation.mp4')
