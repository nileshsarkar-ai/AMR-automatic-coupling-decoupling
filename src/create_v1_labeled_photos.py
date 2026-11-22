"""Create labeled, repository-ready V1 assembly and parts images."""
from pathlib import Path
import textwrap
import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import vtk
from vtk.util.numpy_support import vtk_to_numpy

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'outputs'/'v1'; PARTS=OUT/'parts'
NAVY=(17,49,72); BLUE=(19,111,154); CYAN=(12,170,184); ORANGE=(240,138,36); BG=(239,244,247)
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
DISPLAY={
 'base':'Receiver base','guide_left':'Left guide wall','guide_right':'Right guide wall','fixed_load_socket':'Fixed load socket',
 'jaw_left':'Left retention jaw','jaw_right':'Right retention jaw','pivot_left':'Left pivot pin','pivot_right':'Right pivot pin',
 'release_yoke':'Release yoke','link_left':'Left release link','link_right':'Right release link','spring_left':'Left return spring',
 'spring_right':'Right return spring','linear_actuator':'Linear release actuator','pin_sensor':'Striker presence sensor','release_sensor':'Yoke-home sensor',
 'top_cover':'Service cover','striker_arm':'Trolley striker arm','wear_insert_left':'Left UHMW guide insert','wear_insert_right':'Right UHMW guide insert',
 'jaw_roller_left':'Left cam roller','jaw_roller_right':'Right cam roller','energy_bumper_left':'Left energy bumper',
 'energy_bumper_right':'Right energy bumper','isolation_front_left':'Front-left isolator','isolation_front_right':'Front-right isolator',
 'isolation_rear_left':'Rear-left isolator','isolation_rear_right':'Rear-right isolator','link_guard_left':'Left linkage guard','link_guard_right':'Right linkage guard'
}

def font(size,bold=False):
    paths=[r'C:\Windows\Fonts\arialbd.ttf' if bold else r'C:\Windows\Fonts\arial.ttf',r'C:\Windows\Fonts\segoeuib.ttf' if bold else r'C:\Windows\Fonts\segoeui.ttf']
    for p in paths:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def actor(name):
    r=vtk.vtkSTLReader(); r.SetFileName(str(PARTS/f'{name}.stl')); r.Update(); m=vtk.vtkPolyDataMapper(); m.SetInputConnection(r.GetOutputPort()); a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetColor(*COL[name]); a.GetProperty().SetInterpolationToPBR(); a.GetProperty().SetMetallic(.25); a.GetProperty().SetRoughness(.36)
    if name=='top_cover': a.GetProperty().SetOpacity(.16)
    elif name in ('link_guard_left','link_guard_right'): a.GetProperty().SetOpacity(.28)
    elif name=='striker_arm': a.GetProperty().SetOpacity(.36)
    return a

def capture(ren,w,h):
    win=vtk.vtkRenderWindow(); win.SetOffScreenRendering(1); win.SetSize(w,h); win.SetMultiSamples(8); win.AddRenderer(ren); win.Render(); c=vtk.vtkWindowToImageFilter(); c.SetInput(win); c.ReadFrontBufferOff(); c.Update(); arr=vtk_to_numpy(c.GetOutput().GetPointData().GetScalars()).reshape(h,w,-1); return Image.fromarray(np.flipud(arr[:,:,:3]))

def project(ren,pt,h):
    ren.SetWorldPoint(pt[0],pt[1],pt[2],1); ren.WorldToDisplay(); x,y,_=ren.GetDisplayPoint(); return (int(x),int(h-y))

def label(draw,anchor,box,text):
    x,y=box; f=font(24,True); wrapped='\n'.join(textwrap.wrap(text,22)); bb=draw.multiline_textbbox((0,0),wrapped,font=f,spacing=4); bw=bb[2]-bb[0]+28; bh=bb[3]-bb[1]+22
    edge=(x+bw if x<anchor[0] else x,y+bh//2); draw.line([anchor,edge],fill=BLUE,width=4); draw.ellipse((anchor[0]-6,anchor[1]-6,anchor[0]+6,anchor[1]+6),fill=ORANGE,outline='white',width=2); draw.rounded_rectangle((x,y,x+bw,y+bh),radius=10,fill=(255,255,255),outline=NAVY,width=3); draw.multiline_text((x+14,y+10),wrapped,font=f,fill=NAVY,spacing=4)

# 1. Major-component assembly overview.
W,H=1800,1100; ren=vtk.vtkRenderer(); ren.SetGradientBackground(True); ren.SetBackground(.82,.88,.92); ren.SetBackground2(.97,.98,.99)
for n in COL: ren.AddActor(actor(n))
cam=ren.GetActiveCamera(); cam.SetFocalPoint(-5,0,24); cam.SetPosition(220,-275,190); cam.SetViewUp(0,0,1); ren.ResetCameraClippingRange(); im=capture(ren,W,H); d=ImageDraw.Draw(im)
d.rounded_rectangle((35,25,1765,100),radius=16,fill=(255,255,255),outline=NAVY,width=3); d.text((65,42),'AMR AUTOMATIC COUPLER V1 - LABELED ASSEMBLY',font=font(34,True),fill=NAVY)
callouts=[
 ((1485,585),(40,145),'Trolley striker arm'),((940,640),(40,285),'Replaceable guide inserts'),((655,455),(40,425),'Release-only linear actuator'),((850,485),(40,565),'Blue release yoke'),
 ((865,455),(1310,145),'Grooved vertical striker'),((905,545),(1310,285),'Dual spring-closed jaws'),((1000,535),(1310,425),'Fixed structural load socket'),((1125,555),(1310,565),'Green lock sensor'),
 ((980,590),(1310,705),'Jaw pivot and cam roller'),((640,555),(40,705),'Independent return springs')]
for anchor,boxp,text in callouts: label(d,anchor,boxp,text)
d.text((55,1035),'Transparent cover and drawbar reveal the load path and moving latch components.',font=font(21),fill=(55,75,86)); im.save(OUT/'AMR_Coupler_V1_Labeled_Assembly.png',quality=96)

# 2. All 30 individual parts, each rendered and named.
cols,rows,cw,ch=5,6,360,260; sheet=Image.new('RGB',(cols*cw,rows*ch+100),BG); sd=ImageDraw.Draw(sheet); sd.rectangle((0,0,cols*cw,100),fill=NAVY); sd.text((40,25),'AMR COUPLER V1 - 30 PART COMPONENT CATALOG',font=font(34,True),fill='white')
for i,n in enumerate(COL):
    rr=vtk.vtkRenderer(); rr.SetBackground(1,1,1); a=actor(n); a.GetProperty().SetOpacity(1); rr.AddActor(a); rr.ResetCamera(); cc=rr.GetActiveCamera(); cc.Azimuth(30); cc.Elevation(24); cc.Zoom(1.05); rr.ResetCameraClippingRange(); thumb=capture(rr,cw-20,ch-55); x=(i%cols)*cw+10; y=100+(i//cols)*ch+8; sheet.paste(thumb,(x,y)); sd.rounded_rectangle((x,y+ch-48,x+cw-20,y+ch-12),radius=8,fill=(232,240,244),outline=(190,208,216),width=2); name=DISPLAY[n]; tw=sd.textbbox((0,0),name,font=font(18,True))[2]; sd.text((x+(cw-20-tw)//2,y+ch-40),name,font=font(18,True),fill=NAVY)
sheet.save(OUT/'AMR_Coupler_V1_Labeled_Parts_Catalog.png',quality=96)

# 3. System-level photo from the verified operation video.
rd=imageio.get_reader(OUT/'amr_coupler_v1_amr_operation.mp4'); sysim=Image.fromarray(rd.get_data(275)); rd.close(); sd=ImageDraw.Draw(sysim); sd.rounded_rectangle((35,28,1885,105),radius=16,fill=(255,255,255),outline=NAVY,width=3); sd.text((65,45),'V1 INSTALLED ON AMR - LOADED TROLLEY TOWING',font=font(34,True),fill=NAVY)
system_labels=[((520,610),(55,170),'Compact indoor AMR'),((1030,610),(65,320),'Automatic coupler receiver'),((1255,520),(1410,190),'Trolley striker interface'),((1550,385),(1435,340),'Payload on trolley'),((1530,650),(1435,490),'Four-caster trolley'),((820,820),(55,470),'Marked docking / travel lane')]
for anchor,boxp,text in system_labels: label(sd,anchor,boxp,text)
sysim.save(OUT/'AMR_Coupler_V1_Labeled_AMR_System.png',quality=96)
print('Created 3 labeled PNG files in',OUT)
