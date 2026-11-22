# V1 payload, cycle-time and wear optimization

V1 is the public production-candidate release. It uses a fail-safe dual-jaw core with replaceable low-friction guide inserts, rolling jaw cam followers, elastomer over-travel bumpers, isolation bushings and link guards. The fixed socket remains the towing load path; the actuator performs release only.

## Payload profiles

| Profile | Example payload | Design tow force | Screening proof load | Final 50 mm approach | Suggested actuator |
|---|---:|---:|---:|---:|---:|
| Light | 10 kg | 80 N | 400 N | 70 mm/s | >=80 N |
| Standard | 50 kg | 250 N | 1,250 N | 55 mm/s | >=120 N |
| Heavy | 150 kg | 600 N | 3,000 N | 35 mm/s | >=180 N |

Payload mass is not the same as hitch force. Final sizing must include trolley mass, acceleration/deceleration, floor slope, rolling resistance, caster scrub, obstacle impact and duty cycle. These profiles are configuration starting points, not rated capacities.

## Efficiency and cycle time

- Passive capture eliminates an actuator-close step. The AMR reverses through the guide and confirms two sensors before towing.
- Only the final 50 mm uses the reduced profile speed; the remaining approach can use the AMR's normal safe docking speed.
- Presence and yoke-home sensors distinguish captured, locked, release-commanded and clear states without time-only delays.
- Release begins only after trolley restraint and hitch-load relief, which reduces actuator force and jaw galling.
- A retry should back off 80 mm and re-approach once; repeated failure should stop and request service.

## Wear-control materials

- Fixed socket and striker: hardened/ground steel or through-hardened replaceable bushing at the bearing surface.
- Jaw and pivot: heat-treated steel with dry-film lubricant or sealed bushings.
- Guide inserts: replaceable UHMW-PE or acetal; countersunk fasteners should remain outside the pin path.
- Bumpers and isolation sleeves: oil-resistant polyurethane selected for temperature and cycle life.
- Cover and guards: aluminum or formed steel; do not use covers as structural load members.

## Maintenance targets

- Inspect and clean daily in dirty environments; verify both sensors at startup.
- Inspect guide inserts, jaw rollers and striker groove every 10,000 cycles initially; adjust interval from measured wear.
- Replace any insert at 1 mm local wear, any roller with binding/play, or any striker showing burrs/cracks.
- Proof-test after a collision, overload or structural repair.

## Required qualification

Complete tolerance stack-up, actuator/spring calculations, FEA with contact, fatigue assessment, emergency-stop/control risk analysis and instrumented physical testing. Test misalignment, power loss, false lock, blocked release, slope, caster transients, contamination and maximum braking before assigning a payload rating.
