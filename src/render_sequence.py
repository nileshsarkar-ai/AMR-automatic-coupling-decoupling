"""Animate approach, passive capture, locked tow state, powered release and separation."""
from pathlib import Path
import math
import numpy as np
import imageio.v2 as imageio
import vtk
from vtk.util.numpy_support import vtk_to_numpy

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'outputs'/'v2'; PARTS=OUT/'parts'
COL={
 'base':(0.28,0.31,0.34),'guide_left':(0.48,0.52,0.55),'guide_right':(0.48,0.52,0.55),
 'fixed_load_socket':(0.18,0.20,0.22),'jaw_left':(0.92,0.52,0.08),'jaw_right':(0.92,0.52,0.08),
 'pivot_left':(0.75,0.77,0.80),'pivot_right':(0.75,0.77,0.80),'release_yoke':(0.20,0.45,0.75),
 'link_left':(0.25,0.55,0.82),'link_right':(0.25,0.55,0.82),'spring_left':(0.85,0.85,0.88),
 'spring_right':(0.85,0.85,0.88),'linear_actuator':(0.12,0.25,0.42),'pin_sensor':(0.10,0.70,0.32),
 'release_sensor':(0.10,0.70,0.32),'top_cover':(0.68,0.72,0.75),'striker_arm':(0.55,0.58,0.61)
}

ren=vtk.vtkRenderer(); ren.SetBackground(.94,.93,.90); actors={}
for n,c in COL.items():
    rd=vtk.vtkSTLReader(); rd.SetFileName(str(PARTS/f'{n}.stl')); rd.Update()
    mp=vtk.vtkPolyDataMapper(); mp.SetInputConnection(rd.GetOutputPort())
    ac=vtk.vtkActor(); ac.SetMapper(mp); ac.GetProperty().SetColor(*c)
    ac.GetProperty().SetInterpolationToPBR(); ac.GetProperty().SetMetallic(.25); ac.GetProperty().SetRoughness(.4)
    if n=='top_cover': ac.GetProperty().SetOpacity(.28)
    actors[n]=ac; ren.AddActor(ac)

pl=vtk.vtkPlaneSource(); pl.SetOrigin(-150,-125,-2); pl.SetPoint1(210,-125,-2); pl.SetPoint2(-150,125,-2)
pm=vtk.vtkPolyDataMapper(); pm.SetInputConnection(pl.GetOutputPort()); pa=vtk.vtkActor(); pa.SetMapper(pm)
pa.GetProperty().SetColor(.82,.81,.78); ren.AddActor(pa)

title=vtk.vtkTextActor(); title.SetInput('AUTOMATIC COUPLING SEQUENCE')
title.SetPosition(38,670); title.GetTextProperty().SetFontSize(24); title.GetTextProperty().SetColor(.08,.09,.10); title.GetTextProperty().SetBold(True); ren.AddActor2D(title)
phase=vtk.vtkTextActor(); phase.SetPosition(38,45); phase.GetTextProperty().SetFontSize(26); phase.GetTextProperty().SetColor(.05,.18,.34); phase.GetTextProperty().SetBold(True); ren.AddActor2D(phase)
note=vtk.vtkTextActor(); note.SetPosition(38,17); note.GetTextProperty().SetFontSize(15); note.GetTextProperty().SetColor(.18,.19,.20); ren.AddActor2D(note)

win=vtk.vtkRenderWindow(); win.SetOffScreenRendering(1); win.SetSize(1280,720); win.SetMultiSamples(8); win.AddRenderer(ren)
cam=ren.GetActiveCamera(); cam.SetFocalPoint(10,0,18); cam.SetPosition(205,-225,145); cam.SetViewUp(0,0,1); ren.ResetCameraClippingRange()

def transform_jaw(name, sign, angle):
    t=vtk.vtkTransform(); t.PostMultiply(); t.Translate(22,-sign*21,0); t.RotateZ(-sign*angle); t.Translate(-22,sign*21,0)
    actors[name].SetUserTransform(t)

def set_scene(i):
    # 0-44 approach, 45-74 cam-open/snap, 75-119 locked, 120-149 release, 150-194 withdraw, 195-209 reset.
    dx=0.; angle=0.; yoke=0.
    if i<45:
        q=i/44; dx=75*(1-q); label='1  ALIGN AND APPROACH'; sub='Tapered guides tolerate lateral error; no actuator power is required.'
    elif i<75:
        q=(i-45)/29; dx=5*(1-q); angle=24*math.sin(math.pi*q); label='2  PASSIVE CAPTURE'; sub='The grooved striker cams both spring-loaded jaws outward, then they snap closed.'
    elif i<120:
        label='3  VERIFIED MECHANICAL LOCK'; sub='Fixed socket carries tow load; dual jaws retain the striker after power loss.'
    elif i<150:
        q=(i-120)/29; angle=24*q; yoke=-11*q; label='4  POWERED RELEASE'; sub='Actuator pulls the blue yoke only after trolley restraint and load relief.'
    elif i<195:
        q=(i-150)/44; angle=24; yoke=-11; dx=75*q; label='5  AUTOMATIC SEPARATION'; sub='AMR moves clear while the release yoke holds both jaws open.'
    else:
        q=(i-195)/14; dx=75; angle=24*(1-q); yoke=-11*(1-q); label='6  FAIL-SAFE RESET'; sub='Return springs restore the ready-to-capture state when the actuator relaxes.'
    actors['striker_arm'].SetPosition(dx,0,0)
    transform_jaw('jaw_left',1,angle); transform_jaw('jaw_right',-1,angle)
    actors['release_yoke'].SetPosition(yoke,0,0)
    actors['link_left'].SetPosition(yoke*.65,0,0); actors['link_right'].SetPosition(yoke*.65,0,0)
    phase.SetInput(label); note.SetInput(sub)

def grab():
    win.Render(); c=vtk.vtkWindowToImageFilter(); c.SetInput(win); c.ReadFrontBufferOff(); c.Update()
    a=vtk_to_numpy(c.GetOutput().GetPointData().GetScalars()).reshape(720,1280,-1)
    return np.flipud(a[:,:,:3])

with imageio.get_writer(OUT/'amr_coupler_v2_auto_sequence.mp4',fps=30,codec='libx264',quality=8,
                        output_params=['-pix_fmt','yuv420p','-movflags','+faststart']) as wr:
    for i in range(210): set_scene(i); wr.append_data(grab())
set_scene(90); imageio.imwrite(OUT/'amr_coupler_v2_sequence_preview.png',grab())
print(OUT/'amr_coupler_v2_auto_sequence.mp4')
