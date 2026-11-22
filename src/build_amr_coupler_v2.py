"""Parametric AMR auto-coupler V2. Units: mm. Requires CadQuery 2.6+."""
from pathlib import Path
import json, math
import cadquery as cq
from cadquery import exporters

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "v2"
OUT.mkdir(parents=True, exist_ok=True)

P = dict(
    base_l=145.0, base_w=110.0, base_t=10.0, cover_t=5.0,
    striker_d=16.0, neck_d=12.0, head_d=24.0, pin_h=52.0,
    jaw_t=8.0, pivot_d=10.0, mount_d=8.5,
    guide_mouth=82.0, guide_throat=30.0,
    working_load_N=300.0, proof_load_N=1500.0,
)

def box(x,y,z,dx,dy,dz):
    return cq.Workplane("XY").box(dx,dy,dz).translate((x+dx/2,y+dy/2,z+dz/2))

def cyl(x,y,z,d,h):
    return cq.Workplane("XY").center(x,y).circle(d/2).extrude(h).translate((0,0,z))

def base():
    s=box(-95,-55,0,P['base_l'],P['base_w'],P['base_t']).edges('|Z').fillet(5)
    for x in (-82,35):
        for y in (-42,42): s=s.cut(cyl(x,y,-1,P['mount_d'],P['base_t']+2))
    # Drain/debris slots prevent the pin pocket from becoming a dirt trap.
    s=s.cut(box(2,-4,-1,42,8,P['base_t']+2))
    return s

def guide(sign):
    # A replaceable, sacrificial guide rail with a large lateral capture window.
    y0=sign*15; ym=sign*50
    pts=[(-2,y0),(48,ym),(48,sign*55),(-8,sign*22),(-35,sign*22),(-35,y0)]
    return cq.Workplane('XY').polyline(pts).close().extrude(18).translate((0,0,10))

def fixed_socket():
    # Structural towing loads enter this fixed steel block; latch jaws only retain the pin.
    s=box(-8,-25,10,24,50,18).edges('|Z').fillet(4)
    s=s.cut(cyl(10,0,9,P['striker_d']+1.0,20))
    s=s.cut(box(10,-9,9,16,18,20))
    return s

def jaw(sign, opened=False):
    # Symmetric helmet-style pawls. Pin cams both outward during capture.
    pts=[(-28,sign*27),(-5,sign*25),(15,sign*10),(15,sign*2),(-2,sign*7),(-34,sign*16)]
    j=cq.Workplane('XY').polyline(pts).close().extrude(P['jaw_t']).translate((0,0,15))
    j=j.cut(cyl(-22,sign*21,14,P['pivot_d']+0.4,P['jaw_t']+2))
    j=j.cut(cyl(10,0,14,P['neck_d']+0.8,P['jaw_t']+2))
    j=j.cut(cyl(-27,sign*22,14,5.2,P['jaw_t']+2))
    if opened:
        angle=-sign*24
        j=j.rotate((-22,sign*21,0),(-22,sign*21,1),angle)
    return j

def pivot(sign): return cyl(-22,sign*21,10,P['pivot_d'],25)

def release_yoke(opened=False):
    x=-53 if opened else -42
    y=box(x,-34,14,10,68,10).edges('|Z').fillet(4)
    for yy in (-25,25): y=y.cut(cyl(x+5,yy,13,5.2,12))
    return y

def actuator(opened=False):
    body=box(-91,-17,12,36,34,28).edges('|X').fillet(4)
    # Rod position indicates release stroke; actuator never carries tow load.
    rod_end=-48 if opened else -37
    rod=cq.Workplane('YZ').center(0,26).circle(4).extrude(rod_end+55).translate((-55,0,0))
    clevis=box(rod_end-4,-10,17,8,20,18).edges('|Z').fillet(3)
    return body.union(rod).union(clevis)

def link(sign, opened=False):
    # Dog-bone link from common yoke to each independent jaw tail.
    x0=-48 if opened else -37; y0=sign*25
    x1=-27; y1=sign*22
    dx,dy=x1-x0,y1-y0; L=(dx*dx+dy*dy)**0.5; a=math.degrees(math.atan2(dy,dx))
    l=box(0,-4,16,L,8,6).edges('|Z').fillet(3)
    for xx in (0,L): l=l.cut(cyl(xx,0,15,5.2,8))
    return l.rotate((0,0,0),(0,0,1),a).translate((x0,y0,0))

def spring(sign):
    # Visual/packaging model of independent jaw return spring.
    path=cq.Wire.makeHelix(3.2,20,5)
    prof=cq.Workplane('XZ').center(5,0).circle(0.8)
    s=prof.sweep(path)
    return s.rotate((0,0,0),(0,1,0),90).translate((-48,sign*38,19))

def cover():
    c=box(-92,-52,36,137,104,P['cover_t']).edges('|Z').fillet(5)
    c=c.cut(box(-46,-38,35,72,76,7))
    for x in (-82,35):
        for y in (-42,42): c=c.cut(cyl(x,y,35,P['mount_d'],7))
    return c

def striker():
    arm=box(10,-16,4,115,32,12).edges('|Z').fillet(7)
    shank=cyl(10,0,8,P['striker_d'],P['pin_h'])
    neck=cyl(10,0,23,P['neck_d'],12)
    head=cyl(10,0,34,P['head_d'],8).edges('>Z or <Z').chamfer(2)
    mount=cyl(110,0,3,10.5,14)
    return arm.union(shank).cut(cyl(10,0,23,P['striker_d']+2,12)).union(neck).union(head).cut(mount)

def sensor(name):
    if name=='pin': return box(19,27,12,18,10,18).edges('|X').fillet(2)
    return box(-41,36,14,16,9,15).edges('|X').fillet(2)

COL={
 'base':(0.28,0.31,0.34),'guide_left':(0.48,0.52,0.55),'guide_right':(0.48,0.52,0.55),
 'fixed_load_socket':(0.18,0.20,0.22),'jaw_left':(0.92,0.52,0.08),'jaw_right':(0.92,0.52,0.08),
 'pivot_left':(0.75,0.77,0.80),'pivot_right':(0.75,0.77,0.80),'release_yoke':(0.20,0.45,0.75),
 'link_left':(0.25,0.55,0.82),'link_right':(0.25,0.55,0.82),'spring_left':(0.85,0.85,0.88),
 'spring_right':(0.85,0.85,0.88),'linear_actuator':(0.12,0.25,0.42),'pin_sensor':(0.10,0.70,0.32),
 'release_sensor':(0.10,0.70,0.32),'top_cover':(0.68,0.72,0.75),'striker_arm':(0.55,0.58,0.61)
}

def state(opened=False):
    return {
      'base':base(),'guide_left':guide(1),'guide_right':guide(-1),'fixed_load_socket':fixed_socket(),
      'jaw_left':jaw(1,opened),'jaw_right':jaw(-1,opened),'pivot_left':pivot(1),'pivot_right':pivot(-1),
      'release_yoke':release_yoke(opened),'link_left':link(1,opened),'link_right':link(-1,opened),
      'spring_left':spring(1),'spring_right':spring(-1),'linear_actuator':actuator(opened),
      'pin_sensor':sensor('pin'),'release_sensor':sensor('release'),'top_cover':cover(),'striker_arm':striker()
    }

def export_state(label, parts, export_parts=False):
    assy=cq.Assembly(name=f'AMR_Coupler_V2_{label}')
    for n,s in parts.items(): assy.add(s,name=n,color=cq.Color(*COL[n]))
    assy.save(str(OUT/f'amr_coupler_v2_{label}.step'))
    comp=cq.Compound.makeCompound([s.val() for s in parts.values()])
    exporters.export(comp,str(OUT/f'amr_coupler_v2_{label}.stl'),tolerance=.06,angularTolerance=.12)
    if export_parts:
      d=OUT/'parts'; d.mkdir(exist_ok=True)
      for n,s in parts.items(): exporters.export(s,str(d/f'{n}.stl'),tolerance=.06,angularTolerance=.12)

closed=state(False); opened=state(True)
export_state('coupled',closed,True); export_state('released',opened)

# Conservative first-pass static sizing checks; these do not replace FEA/test.
load=P['proof_load_N']; pin_area=2*math.pi*(P['striker_d']**2)/4
pin_shear=load/pin_area
bearing=load/(P['striker_d']*18)
manifest={
 'version':'2.0','units':'mm','parameters':P,
 'architecture':'Dual spring-closed cam jaws retain a grooved striker; fixed socket carries tow load; actuator pulls a release-only yoke.',
 'states':['coupled','released'],'part_count':len(closed),
 'screening_checks':{'proof_load_N':load,'pin_double_shear_MPa':round(pin_shear,2),'socket_bearing_MPa':round(bearing,2),
   'warning':'Screening arithmetic only. Validate actual material, fasteners, welds, fatigue, impact and geometry with FEA and physical proof testing.'},
 'volumes_mm3':{n:round(s.val().Volume(),2) for n,s in closed.items()}
}
(OUT/'manifest_v2.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))
