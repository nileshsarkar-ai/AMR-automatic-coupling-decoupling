from pathlib import Path
import json
import cadquery as cq
import imageio.v2 as imageio
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'outputs'/'v1'; result={}
for state in ('coupled','released'):
    s=cq.importers.importStep(str(OUT/f'amr_coupler_v1_{state}.step')); solids=s.solids().vals()
    assert len(solids)==30 and all(x.isValid() and x.Volume()>0 for x in solids)
    result[state]={'solids':len(solids),'valid':True,'volume_mm3':round(sum(x.Volume() for x in solids),2)}
for key,file,count in [('moving_360','amr_coupler_v1_360.mp4',240),('operation','amr_coupler_v1_amr_operation.mp4',450)]:
    r=imageio.get_reader(OUT/file); m=r.get_meta_data(); n=r.count_frames(); r.close()
    assert n==count and m['fps']==30.0 and m['size']==(1920,1088)
    result[key]={'frames':n,'duration_s':m['duration'],'fps':m['fps'],'size':m['size']}
manifest=json.loads((OUT/'manifest_v1.json').read_text(encoding='utf-8')); assert manifest['version']=='1.0' and len(manifest['payload_profiles'])==3
result['payload_profiles']=list(manifest['payload_profiles'])
pdf=PdfReader(str(OUT/'AMR_Coupler_V1_Specification.pdf')); assert len(pdf.pages)==3
result['specification_pdf']={'pages':len(pdf.pages),'extractable_text_chars':sum(len(p.extract_text() or '') for p in pdf.pages)}
legacy={'amr_coupler_v1_professional_working_demo.mp4'}
result['files']=sorted(str(p.relative_to(ROOT)) for p in OUT.rglob('*') if p.is_file() and p.name not in legacy)
(OUT/'validation_report_v1.json').write_text(json.dumps(result,indent=2),encoding='utf-8'); print(json.dumps(result,indent=2))
