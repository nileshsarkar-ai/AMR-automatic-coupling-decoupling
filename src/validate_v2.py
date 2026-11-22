"""Re-import deliverables and run basic geometric/media checks."""
from pathlib import Path
import json
import cadquery as cq
import imageio.v2 as imageio

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'outputs'/'v2'
results={}
for name in ('coupled','released'):
    p=OUT/f'amr_coupler_v2_{name}.step'
    model=cq.importers.importStep(str(p)); solids=model.solids().vals()
    assert len(solids)==18, (name,len(solids))
    assert all(s.isValid() and s.Volume()>0 for s in solids)
    results[name]={'solids':len(solids),'valid':True,'volume_mm3':round(sum(s.Volume() for s in solids),2)}

vid=OUT/'amr_coupler_v2_360.mp4'; rd=imageio.get_reader(vid); meta=rd.get_meta_data()
frames=rd.count_frames(); rd.close()
assert frames==180, frames
assert round(meta['duration'],1)==6.0, meta
results['video']={'frames':frames,'fps':meta['fps'],'duration_s':meta['duration'],'size':meta['size']}
results['files_checked']=sorted(str(p.relative_to(ROOT)) for p in OUT.rglob('*') if p.is_file())
(OUT/'validation_report.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
