"""Targeted interference and clearance audit for functional V1 CAD pairs."""
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
import build_amr_coupler_v1 as model
OUT=ROOT/'outputs'/'v1'

PAIRS={
 'jaw_left__striker_arm':('jaw_left','striker_arm'),
 'jaw_right__striker_arm':('jaw_right','striker_arm'),
 'jaw_left__fixed_socket':('jaw_left','fixed_load_socket'),
 'jaw_right__fixed_socket':('jaw_right','fixed_load_socket'),
 'jaw_left__base':('jaw_left','base'),'jaw_right__base':('jaw_right','base'),
 'jaw_left__jaw_right':('jaw_left','jaw_right'),
 'striker_arm__fixed_socket':('striker_arm','fixed_load_socket'),
 'striker_arm__base':('striker_arm','base'),
 'striker_arm__guide_left':('striker_arm','guide_left'),
 'striker_arm__guide_right':('striker_arm','guide_right'),
 'top_cover__striker_arm':('top_cover','striker_arm'),
}
LIMITS={
 'coupled':{'jaw_left__striker_arm':.35,'jaw_right__striker_arm':.35,'jaw_left__fixed_socket':.9,'jaw_right__fixed_socket':.9,'jaw_left__jaw_right':7.0,'striker_arm__fixed_socket':.45,'striker_arm__base':.45,'top_cover__striker_arm':4.5},
 'released':{'jaw_left__striker_arm':9.0,'jaw_right__striker_arm':9.0,'jaw_left__fixed_socket':.9,'jaw_right__fixed_socket':.9,'jaw_left__jaw_right':20.0,'striker_arm__fixed_socket':.45,'striker_arm__base':.45,'top_cover__striker_arm':4.5},
}
result={'units':'mm','states':{},'excluded_contacts':['link-to-jaw pivot joints','yoke-to-actuator clevis','mounting fasteners and bushings']}
for opened,label in ((False,'coupled'),(True,'released')):
    parts=model.state(opened); rows={}; passed=True
    for key,(a,b) in PAIRS.items():
        overlap=parts[a].val().intersect(parts[b].val()).Volume(); clearance=parts[a].val().distance(parts[b].val()); minimum=LIMITS[label].get(key,0.0)
        ok=overlap<1e-5 and clearance+1e-6>=minimum; passed &= ok
        rows[key]={'overlap_mm3':round(overlap,6),'clearance_mm':round(clearance,3),'minimum_mm':minimum,'pass':ok}
    result['states'][label]={'pass':passed,'pairs':rows}
result['pass']=all(x['pass'] for x in result['states'].values())
assert result['pass'], json.dumps(result,indent=2)
(OUT/'clearance_audit_v1.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
