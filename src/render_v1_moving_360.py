"""Moving 360-degree cutaway of release, withdrawal, reset and recapture."""
from pathlib import Path
import math
import numpy as np
import imageio.v2 as imageio
import vtk
from vtk.util.numpy_support import vtk_to_numpy

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'outputs'/'v1'; PARTS=OUT/'parts'; W,H=1920,1088
COL={'base':(.25,.29,.32),'guide_left':(.48,.52,.55),'guide_right':(.48,.52,.55),'fixed_load_socket':(.12,.14,.16),'jaw_left':(.96,.55,.06),'jaw_right':(.96,.55,.06),'pivot_left':(.76,.79,.82),'pivot_right':(.76,.79,.82),'release_yoke':(.12,.43,.80),'spring_left':(.86,.88,.90),'spring_right':(.86,.88,.90),'pin_sensor':(.08,.72,.30),'release_sensor':(.08,.72,.30),'top_cover':(.72,.76,.79),'striker_arm':(.56,.59,.62),'wear_insert_left':(.02,.75,.82),'wear_insert_right':(.02,.75,.82),'jaw_roller_left':(.90,.92,.94),'jaw_roller_right':(.90,.92,.94),'energy_bumper_left':(.80,.16,.09),'energy_bumper_right':(.80,.16,.09),'isolation_front_left':(.10,.11,.12),'isolation_front_right':(.10,.11,.12),'isolation_rear_left':(.10,.11,.12),'isolation_rear_right':(.10,.11,.12),'link_guard_left':(.20,.22,.24),'link_guard_right':(.20,.22,.24)}

def load(n,c):
 r=vtk.vtkSTLReader(); r.SetFileName(str(PARTS/f'{n}.stl')); r.Update(); m=vtk.vtkPolyDataMapper(); m.SetInputConnection(r.GetOutputPort()); a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetColor(*c); a.GetProperty().SetInterpolationToPBR(); a.GetProperty().SetMetallic(.28); a.GetProperty().SetRoughness(.34); return a
def cube(center,size,color):
 s=vtk.vtkCubeSource(); s.SetCenter(*center); s.SetXLength(size[0]); s.SetYLength(size[1]); s.SetZLength(size[2]); m=vtk.vtkPolyDataMapper(); m.SetInputConnection(s.GetOutputPort()); a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetColor(*color); return a
def cyl(center,r,h,color,axis='y'):
 s=vtk.vtkCylinderSource(); s.SetCenter(0,0,0); s.SetRadius(r); s.SetHeight(h); s.SetResolution(36); m=vtk.vtkPolyDataMapper(); m.SetInputConnection(s.GetOutputPort()); a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetColor(*color); a.RotateZ(-90); a.SetPosition(*center); return a
def between(p0,p1,r,color):
 d=np.subtract(p1,p0); L=float(np.linalg.norm(d)); mid=np.add(p0,p1)/2; s=vtk.vtkCylinderSource(); s.SetRadius(r); s.SetHeight(L); s.SetResolution(28); m=vtk.vtkPolyDataMapper(); m.SetInputConnection(s.GetOutputPort()); a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetColor(*color); t=vtk.vtkTransform(); t.Translate(*mid); v=d/L; y=np.array([0.,1.,0.]); ax=np.cross(y,v); dot=float(np.clip(np.dot(y,v),-1,1)); ang=math.degrees(math.acos(dot));
 if np.linalg.norm(ax)>1e-8: t.RotateWXYZ(ang,*ax)
 a.SetUserTransform(t); return a
def rot(p,piv,deg):
 a=math.radians(deg); x,y=p[0]-piv[0],p[1]-piv[1]; return (piv[0]+x*math.cos(a)-y*math.sin(a),piv[1]+x*math.sin(a)+y*math.cos(a),p[2])

ren=vtk.vtkRenderer(); ren.SetGradientBackground(True); ren.SetBackground(.66,.76,.84); ren.SetBackground2(.96,.97,.98); win=vtk.vtkRenderWindow(); win.SetOffScreenRendering(1); win.SetSize(W,H); win.SetMultiSamples(8); win.AddRenderer(ren)
parts={}
for n,c in COL.items(): parts[n]=load(n,c); ren.AddActor(parts[n])
parts['top_cover'].GetProperty().SetOpacity(.15); parts['link_guard_left'].GetProperty().SetOpacity(.25); parts['link_guard_right'].GetProperty().SetOpacity(.25); parts['striker_arm'].GetProperty().SetOpacity(.28)
ren.AddActor(cube((0,0,-7),(360,260,10),(.52,.54,.55)))
body=cube((-73,0,26),(36,34,28),(.08,.22,.38)); rod=cyl((-47,0,26),4,22,(.84,.86,.88)); clevis=cube((-36,0,26),(9,20,18),(.30,.35,.39)); ren.AddActor(body); ren.AddActor(rod); ren.AddActor(clevis)
links=[]; cam=ren.GetActiveCamera(); cam.SetFocalPoint(-5,0,22); cam.SetPosition(220,-260,175); cam.SetViewUp(0,0,1)
title=vtk.vtkTextActor(); title.SetPosition(58,1005); title.GetTextProperty().SetFontSize(34); title.GetTextProperty().SetBold(True); title.GetTextProperty().SetColor(.04,.08,.12); title.GetTextProperty().SetBackgroundColor(.96,.97,.98); title.GetTextProperty().SetBackgroundOpacity(.82); ren.AddActor2D(title)
sub=vtk.vtkTextActor(); sub.SetPosition(60,60); sub.GetTextProperty().SetFontSize(23); sub.GetTextProperty().SetColor(.03,.12,.20); sub.GetTextProperty().SetBackgroundColor(.96,.97,.98); sub.GetTextProperty().SetBackgroundOpacity(.82); ren.AddActor2D(sub)

def jaw(n,rn,sign,q):
 piv=(-22,sign*21,0); t=vtk.vtkTransform(); t.PostMultiply(); t.Translate(-piv[0],-piv[1],0); t.RotateZ(sign*24*q); t.Translate(*piv); parts[n].SetUserTransform(t); parts[rn].SetUserTransform(t)
def grab():
 win.Render(); c=vtk.vtkWindowToImageFilter(); c.SetInput(win); c.ReadFrontBufferOff(); c.Update(); a=vtk_to_numpy(c.GetOutput().GetPointData().GetScalars()).reshape(H,W,-1); return np.flipud(a[:,:,:3])

with imageio.get_writer(OUT/'amr_coupler_v1_360.mp4',fps=30,codec='libx264',quality=9,output_params=['-pix_fmt','yuv420p','-movflags','+faststart']) as wr:
 for i in range(240):
  for a in links: ren.RemoveActor(a)
  links=[]; q=0.; pinx=0.
  if i<45: title.SetInput('LOCKED'); sub.SetInput('Dual jaws retain the grooved striker; fixed socket carries towing load.')
  elif i<90: q=(i-45)/44; title.SetInput('POWERED RELEASE'); sub.SetInput('Blue yoke retracts both moving links and opens the orange jaws.')
  elif i<135: q=1; pinx=75*(i-90)/44; title.SetInput('PIN WITHDRAWAL'); sub.SetInput('AMR separates while the restrained trolley striker clears the receiver.')
  elif i<165: q=1-(i-135)/29; pinx=75; title.SetInput('SPRING RESET'); sub.SetInput('Jaws return to their fail-safe capture position after clearance.')
  elif i<225:
   z=(i-165)/59; pinx=75*(1-z); q=math.sin(math.pi*z); title.SetInput('AUTOMATIC RECAPTURE'); sub.SetInput('Incoming pin cams the jaws open; springs close them into the groove.')
  else: title.SetInput('LOCK CONFIRMED'); sub.SetInput('Presence sensor turns green and towing can begin.')
  parts['striker_arm'].SetPosition(pinx,0,0); jaw('jaw_left','jaw_roller_left',1,q); jaw('jaw_right','jaw_roller_right',-1,q); parts['release_yoke'].SetPosition(-11*q,0,0); rod.SetPosition(-7*q,0,0); clevis.SetPosition(-11*q,0,0)
  yx=-37-11*q
  for sign in (1,-1):
   tail=rot((-27,sign*22,25),(-22,sign*21,25),sign*24*q); a=between((yx,sign*25,25),tail,3.2,(.22,.60,.92)); links.append(a); ren.AddActor(a)
  parts['pin_sensor'].GetProperty().SetColor(*((.08,.82,.25) if i<45 or i>=225 else (.86,.12,.08)))
  cam.Azimuth(1.5); ren.ResetCameraClippingRange(); wr.append_data(grab())
print(OUT/'amr_coupler_v1_360.mp4')
