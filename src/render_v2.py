"""Render colored V2 preview and a 360-degree MP4 turntable."""
from pathlib import Path
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

ren=vtk.vtkRenderer(); ren.SetBackground(0.94,0.93,0.90); ren.SetUseDepthPeeling(True)
for n,c in COL.items():
    rd=vtk.vtkSTLReader(); rd.SetFileName(str(PARTS/f'{n}.stl')); rd.Update()
    mp=vtk.vtkPolyDataMapper(); mp.SetInputConnection(rd.GetOutputPort())
    ac=vtk.vtkActor(); ac.SetMapper(mp); ac.GetProperty().SetColor(*c)
    ac.GetProperty().SetInterpolationToPBR(); ac.GetProperty().SetMetallic(.28); ac.GetProperty().SetRoughness(.38)
    if n=='top_cover': ac.GetProperty().SetOpacity(.38)
    ren.AddActor(ac)

# Ground plane improves depth perception.
pl=vtk.vtkPlaneSource(); pl.SetOrigin(-150,-120,-2); pl.SetPoint1(180,-120,-2); pl.SetPoint2(-150,120,-2)
pm=vtk.vtkPolyDataMapper(); pm.SetInputConnection(pl.GetOutputPort()); pa=vtk.vtkActor(); pa.SetMapper(pm)
pa.GetProperty().SetColor(.82,.81,.78); pa.GetProperty().SetRoughness(.8); ren.AddActor(pa)

win=vtk.vtkRenderWindow(); win.SetOffScreenRendering(1); win.SetSize(1280,720); win.SetMultiSamples(8); win.AddRenderer(ren)
ren.ResetCamera(); cam=ren.GetActiveCamera(); cam.SetFocalPoint(5,0,18); cam.SetPosition(190,-210,150); cam.SetViewUp(0,0,1)
ren.ResetCameraClippingRange()

def frame():
    win.Render(); cap=vtk.vtkWindowToImageFilter(); cap.SetInput(win); cap.ReadFrontBufferOff(); cap.Update()
    im=vtk_to_numpy(cap.GetOutput().GetPointData().GetScalars())
    im=im.reshape(720,1280,-1); return np.flipud(im[:,:,:3])

img=frame(); imageio.imwrite(OUT/'amr_coupler_v2_preview.png',img)
with imageio.get_writer(OUT/'amr_coupler_v2_360.mp4',fps=30,codec='libx264',quality=8,
                        output_params=['-pix_fmt','yuv420p','-movflags','+faststart']) as wr:
    for _ in range(180):
        wr.append_data(frame()); cam.Azimuth(2); ren.ResetCameraClippingRange()
print(OUT/'amr_coupler_v2_360.mp4')
