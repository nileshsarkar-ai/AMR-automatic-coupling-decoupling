"""Create the verified AMR Coupler V1 engineering specification PDF."""
from pathlib import Path
import json
import imageio.v2 as imageio
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, KeepTogether

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'outputs'/'v1'; WORK=ROOT/'work'/'spec_sheet'; WORK.mkdir(parents=True,exist_ok=True)
PDF=OUT/'AMR_Coupler_V1_Specification.pdf'; manifest=json.loads((OUT/'manifest_v1.json').read_text(encoding='utf-8'))

def frame(video,index,name):
    r=imageio.get_reader(OUT/video); im=Image.fromarray(r.get_data(index)); r.close(); p=WORK/name; im.save(p,quality=94); return p

img_capture=frame('amr_coupler_v1_amr_operation.mp4',125,'capture.jpg')
img_tow=frame('amr_coupler_v1_amr_operation.mp4',275,'tow.jpg')
img_release=frame('amr_coupler_v1_amr_operation.mp4',350,'release.jpg')

NAVY=colors.HexColor('#12324A'); BLUE=colors.HexColor('#1676A3'); CYAN=colors.HexColor('#11A9B8'); ORANGE=colors.HexColor('#F08A24'); LIGHT=colors.HexColor('#EDF3F6'); MID=colors.HexColor('#D7E3E9'); DARK=colors.HexColor('#17242B'); GREEN=colors.HexColor('#2E8B57')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleX',fontName='Helvetica-Bold',fontSize=24,leading=28,textColor=NAVY,spaceAfter=5*mm))
styles.add(ParagraphStyle(name='SubX',fontName='Helvetica',fontSize=10.5,leading=15,textColor=colors.HexColor('#40545F'),spaceAfter=4*mm))
styles.add(ParagraphStyle(name='H1X',fontName='Helvetica-Bold',fontSize=15,leading=19,textColor=NAVY,spaceBefore=3*mm,spaceAfter=2.5*mm))
styles.add(ParagraphStyle(name='H2X',fontName='Helvetica-Bold',fontSize=10.5,leading=13,textColor=BLUE,spaceBefore=2*mm,spaceAfter=1.5*mm))
styles.add(ParagraphStyle(name='BodyX',fontName='Helvetica',fontSize=8.8,leading=12.2,textColor=DARK,spaceAfter=2*mm))
styles.add(ParagraphStyle(name='SmallX',fontName='Helvetica',fontSize=7.4,leading=9.4,textColor=colors.HexColor('#40545F')))
styles.add(ParagraphStyle(name='Callout',fontName='Helvetica-Bold',fontSize=9.2,leading=12,textColor=colors.white,backColor=NAVY,borderPadding=6,spaceAfter=3*mm))

def footer(canvas,doc):
    canvas.saveState(); canvas.setStrokeColor(MID); canvas.line(16*mm,13*mm,194*mm,13*mm)
    canvas.setFont('Helvetica',7); canvas.setFillColor(colors.HexColor('#536772')); canvas.drawString(16*mm,8.5*mm,'AMR Automatic Coupler V1 | Engineering concept specification | 22 November 2026')
    canvas.drawRightString(194*mm,8.5*mm,f'Page {doc.page}'); canvas.restoreState()

def table(data,widths,header=True,font=7.5):
    t=Table(data,colWidths=widths,repeatRows=1 if header else 0,hAlign='LEFT')
    cmd=[('FONTNAME',(0,0),(-1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),font),('LEADING',(0,0),(-1,-1),font+2.5),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('GRID',(0,0),(-1,-1),.35,MID),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]
    if header: cmd += [('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold')]
    for r in range(1 if header else 0,len(data)):
        if r%2==0: cmd.append(('BACKGROUND',(0,r),(-1,r),LIGHT))
    t.setStyle(TableStyle(cmd)); return t

story=[]
story += [Paragraph('AMR AUTOMATIC COUPLER V1',styles['TitleX']),Paragraph('Fail-safe passive capture, sensor-confirmed towing and powered release for compact indoor autonomous mobile robots.',styles['SubX'])]
hero=Table([[RLImage(str(img_tow),width=118*mm,height=66.9*mm),Paragraph('<b>Release status</b><br/>Engineering concept<br/><br/><b>CAD states</b><br/>Coupled + released<br/><br/><b>Part count</b><br/>30 solids<br/><br/><b>Interface</b><br/>Vertical grooved striker',styles['BodyX'])]],colWidths=[123*mm,55*mm])
hero.setStyle(TableStyle([('BACKGROUND',(1,0),(1,0),LIGHT),('BOX',(0,0),(-1,-1),.5,MID),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(1,0),(1,0),7),('TOPPADDING',(1,0),(1,0),7)])); story += [hero,Spacer(1,4*mm)]
story += [Paragraph('DESIGN INTENT',styles['H1X']),Paragraph('V1 automatically captures a trolley striker as the AMR reverses into the guided receiver. Two spring-closed jaws retain the striker without continuous electrical power. A fixed socket carries towing and braking forces; the actuator is used only to pull a release yoke after the trolley is restrained and the hitch is unloaded.',styles['BodyX'])]
spec=[['Parameter','V1 specification'],['Receiver footprint','145 x 110 mm'],['Receiver structural height','41 mm nominal'],['Mounting holes','4 x 8.5 mm clearance'],['Striker interface','16 mm shank / 12 mm neck / 24 mm head'],['Striker height','52 mm nominal'],['Guide mouth / throat','82 mm / 30 mm'],['Sensors','Striker presence + release-yoke home'],['Release actuation','Linear actuator; release-only load path'],['CAD deliverables','STEP assemblies and individual STL parts']]
story += [table(spec,[60*mm,118*mm])]
story += [Spacer(1,3*mm),Paragraph('Important: dimensions are prototype nominal values in millimetres. Assigning a certified payload rating requires final material, tolerance, fastener, weld, spring, actuator, fatigue and control validation.',styles['Callout']),PageBreak()]

story += [Paragraph('MECHANISM AND OPERATING SEQUENCE',styles['TitleX'])]
imgs=Table([[RLImage(str(img_capture),width=87*mm,height=49.3*mm),RLImage(str(img_release),width=87*mm,height=49.3*mm)],['Passive capture cutaway','Powered release cutaway']],colWidths=[89*mm,89*mm])
imgs.setStyle(TableStyle([('FONTNAME',(0,1),(-1,1),'Helvetica-Bold'),('FONTSIZE',(0,1),(-1,1),8),('TEXTCOLOR',(0,1),(-1,1),NAVY),('ALIGN',(0,1),(-1,1),'CENTER'),('TOPPADDING',(0,1),(-1,1),3)])); story += [imgs,Spacer(1,3*mm)]
seq=[['State','Mechanical action','Control permission'],['1. Align','Tapered, replaceable guide inserts center the striker.','Approach at the selected payload-profile speed.'],['2. Capture','Striker rolls both cam followers outward; return springs close the jaws into the groove.','No close-actuator stroke is required.'],['3. Verify','Presence sensor and yoke-home sensor must both indicate locked.','Towing remains inhibited until both signals agree.'],['4. Tow','Fixed socket transfers longitudinal loads into the receiver base.','Monitor lock state continuously.'],['5. Park','Trolley restraint is applied and hitch load is relieved.','Release command is permitted only when stationary.'],['6. Release','Linear actuator retracts the blue yoke and both links, opening the jaws.','AMR separates only after release confirmation.'],['7. Reset','After clearance, springs restore the capture-ready jaw position.','A failed confirmation stops motion and reports service.']]
seq_wrapped=[seq[0]]+[[Paragraph(c,styles['SmallX']) for c in row] for row in seq[1:]]
story += [table(seq_wrapped,[25*mm,92*mm,61*mm],font=7.1),Spacer(1,3*mm)]
story += [Paragraph('Fail-safe principle',styles['H2X']),Paragraph('Loss of electrical power does not command release. The jaws are spring-biased toward capture, the actuator does not carry tow load, and the fixed socket provides the primary structural bearing surface.',styles['BodyX'])]
story += [Paragraph('Motion evidence',styles['H2X']),Paragraph('The supplied 15-second operation video shows approach, cutaway capture, sensor confirmation, towing, parking, release and separation. The 8-second moving 360-degree video shows locked, release, pin withdrawal, spring reset, recapture and final confirmation.',styles['BodyX']),PageBreak()]

story += [Paragraph('PAYLOAD CONFIGURATION AND QUALIFICATION',styles['TitleX'])]
profiles=[['Profile','Example payload','Design tow force','Screening proof load','Final 50 mm speed','Suggested actuator']]
for key,label in [('light_10kg','Light'),('standard_50kg','Standard'),('heavy_150kg','Heavy')]:
    p=manifest['payload_profiles'][key]; profiles.append([label,f"{p['payload_kg']} kg",f"{p['tow_design_N']} N",f"{p['proof_N']:,} N",f"{p['approach_mm_s']} mm/s",f">= {p['actuator_N']} N"])
story += [table(profiles,[25*mm,26*mm,30*mm,34*mm,34*mm,29*mm],font=7.2),Spacer(1,3*mm)]
story += [Paragraph('Payload mass is not hitch force',styles['Callout']),Paragraph('The final load case must include total trolley mass, acceleration and emergency braking, floor gradient, rolling resistance, caster scrub, floor joints, obstacle impact, misalignment and duty cycle. The three profiles are engineering starting points and are not certified capacities.',styles['BodyX'])]
materials=[['Subsystem','Recommended prototype construction','Wear-control feature'],['Fixed socket / striker','Hardened or ground steel','Replaceable bearing surface; deburr groove'],['Jaws / pivots','Heat-treated steel with sealed bushings','Rolling cam followers and dry-film lubricant'],['Guide inserts','UHMW-PE or acetal','Replace at 1 mm local wear'],['Bumpers / isolators','Oil-resistant polyurethane','Absorbs capture over-travel and vibration'],['Cover / guards','Formed aluminium or steel','Non-structural, service-removable'],['Fasteners','Property class selected by final load case','Positive locking and witness marks']]
story += [Paragraph('Materials and wear control',styles['H1X']),table(materials,[38*mm,77*mm,63*mm],font=7.2)]
maint=[['Interval / trigger','Required check'],['Each startup','Verify both sensors, guard condition and clear receiver path.'],['Initially every 10,000 cycles','Inspect guide inserts, cam rollers, pivots, springs and striker groove; refine interval using measured wear.'],['After collision or overload','Remove from service; inspect structure and fasteners; repeat proof test.'],['At 1 mm guide wear','Replace polymer insert and inspect striker alignment.'],['Any binding, excess play or cracking','Stop operation and replace affected component before return to service.']]
story += [Paragraph('Inspection and maintenance',styles['H1X']),table(maint,[48*mm,130*mm],font=7.4)]
story += [Paragraph('Required before production use',styles['H1X']),Paragraph('Complete tolerance stack-up; spring and actuator sizing; contact and structural FEA; fastener and weld calculations; fatigue and impact assessment; electrical and functional-safety analysis; guarding review; contamination testing; and instrumented physical tests for misalignment, power loss, false lock, blocked release, slope, caster transients and maximum braking.',styles['BodyX'])]
story += [Paragraph('Patent status',styles['H2X']),Paragraph('A preliminary design-around review is included in the repository. It is not a freedom-to-operate opinion and does not establish non-infringement or patentability. Obtain a jurisdiction-specific claim chart before manufacture or sale.',styles['SmallX'])]

doc=SimpleDocTemplate(str(PDF),pagesize=A4,rightMargin=16*mm,leftMargin=16*mm,topMargin=15*mm,bottomMargin=18*mm,title='AMR Automatic Coupler V1 Specification',author='Engineering concept package')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(PDF)
