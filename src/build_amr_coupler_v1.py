"""V1 production-candidate payload-optimized AMR coupler."""
from pathlib import Path
import json, math, sys
import cadquery as cq
from cadquery import exporters

ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
import build_amr_coupler_v2 as core
OUT=ROOT/'outputs'/'v1'; OUT.mkdir(parents=True,exist_ok=True)

PROFILES={
 'light_10kg':dict(payload_kg=10,tow_design_N=80,proof_N=400,approach_mm_s=70,actuator_N=80),
 'standard_50kg':dict(payload_kg=50,tow_design_N=250,proof_N=1250,approach_mm_s=55,actuator_N=120),
 'heavy_150kg':dict(payload_kg=150,tow_design_N=600,proof_N=3000,approach_mm_s=35,actuator_N=180),
}

def box(x,y,z,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz).translate((x+dx/2,y+dy/2,z+dz/2))
def cyl(x,y,z,d,h): return cq.Workplane('XY').center(x,y).circle(d/2).extrude(h).translate((0,0,z))

def wear_insert(sign):
    # Replaceable UHMW-PE insert protects the metal guide and lowers entry friction/noise.
    pts=[(5,sign*18),(45,sign*48),(45,sign*52),(1,sign*22)]
    return cq.Workplane('XY').polyline(pts).close().extrude(5).translate((0,0,23))

def jaw_roller(sign):
    # Hardened rolling cam makes striker entry rolling rather than sliding contact.
    return cyl(12,sign*8,20,8,10).cut(cyl(12,sign*8,19,3,12))

def energy_bumper(sign):
    # Elastomer bumper limits jaw over-travel and absorbs capture impact.
    return box(-8,sign*27,20,16,6,10).edges('|Z').fillet(2)

def isolation_bushing(x,y):
    # Replaceable elastomer sleeve for limited high-frequency shock isolation.
    return cyl(x,y,0,14,10).cut(cyl(x,y,-1,8.5,12))

def guard():
    # Shields links and springs while leaving the pin path unobstructed.
    g=box(-92,-51,10,58,18,27).edges('|Z').fillet(4)
    return g.cut(box(-86,-48,15,45,14,16))

ADD_COL={
 'wear_insert_left':(0.10,0.72,0.78),'wear_insert_right':(0.10,0.72,0.78),
 'jaw_roller_left':(0.88,0.90,0.92),'jaw_roller_right':(0.88,0.90,0.92),
 'energy_bumper_left':(0.78,0.18,0.12),'energy_bumper_right':(0.78,0.18,0.12),
 'isolation_front_left':(0.15,0.15,0.16),'isolation_front_right':(0.15,0.15,0.16),
 'isolation_rear_left':(0.15,0.15,0.16),'isolation_rear_right':(0.15,0.15,0.16),
 'link_guard_left':(0.22,0.24,0.27),'link_guard_right':(0.22,0.24,0.27),
}

def state(opened=False):
    p=core.state(opened)
    p.update({
      'wear_insert_left':wear_insert(1),'wear_insert_right':wear_insert(-1),
      'jaw_roller_left':jaw_roller(1),'jaw_roller_right':jaw_roller(-1),
      'energy_bumper_left':energy_bumper(1),'energy_bumper_right':energy_bumper(-1),
      'isolation_front_left':isolation_bushing(35,42),'isolation_front_right':isolation_bushing(35,-42),
      'isolation_rear_left':isolation_bushing(-82,42),'isolation_rear_right':isolation_bushing(-82,-42),
      'link_guard_left':guard(),'link_guard_right':guard().mirror('XZ'),
    })
    return p

COL={**core.COL,**ADD_COL}

def export_state(label,parts,individual=False):
    assy=cq.Assembly(name=f'AMR_Coupler_V1_{label}')
    for n,s in parts.items(): assy.add(s,name=n,color=cq.Color(*COL[n]))
    assy.save(str(OUT/f'amr_coupler_v1_{label}.step'))
    exporters.export(cq.Compound.makeCompound([s.val() for s in parts.values()]),str(OUT/f'amr_coupler_v1_{label}.stl'),tolerance=.07,angularTolerance=.14)
    if individual:
        d=OUT/'parts'; d.mkdir(exist_ok=True)
        for n,s in parts.items(): exporters.export(s,str(d/f'{n}.stl'),tolerance=.07,angularTolerance=.14)

closed=state(False); released=state(True); export_state('coupled',closed,True); export_state('released',released)

checks={}
for name,p in PROFILES.items():
    pin_shear=p['proof_N']/(2*math.pi*16**2/4)
    socket_bearing=p['proof_N']/(16*18)
    capture_time=50/p['approach_mm_s']
    checks[name]={**p,'nominal_pin_double_shear_MPa':round(pin_shear,2),'nominal_socket_bearing_MPa':round(socket_bearing,2),
                  'last_50mm_approach_time_s':round(capture_time,2)}
manifest={
 'version':'1.0','release_name':'V1','units':'mm','part_count':len(closed),'payload_profiles':checks,
 'wear_reduction':['replaceable UHMW-PE guide inserts','rolling jaw cam followers','elastomer over-travel bumpers','replaceable isolation bushings','debris drain slot'],
 'cycle_optimization':['passive capture requires no actuator stroke','dual-state sensing permits immediate lock confirmation','release-only actuator is outside tow load path','profile-specific final approach speed'],
 'safety_note':'Profiles are engineering inputs, not certified payload ratings. Validate full trolley mass, floor slope, caster shock, fatigue, welds, fasteners, spring life and controls.'
}
(OUT/'manifest_v1.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))
