# AMR coupler V2 - preliminary design-around review

Date reviewed: 22 November 2026. This is an engineering risk screen, not a legal opinion, patentability conclusion, or freedom-to-operate clearance.

## V2 architecture

The V2 receiver uses two symmetric, independently spring-closed cam jaws around a grooved vertical striker. A fixed U-shaped socket carries towing and braking loads. A linear actuator pulls a transverse release yoke that opens the jaws; it does not hold the hitch closed and is not in the towing load path. Loss of electrical power leaves the jaws mechanically retained. Two sensors separately indicate striker presence and release-yoke home position.

## Claim-oriented design choices

| Reference | Relevant claim theme | V2 distinction | Residual risk |
|---|---|---|---|
| WO2022027141A1 | Pintle hitch movable portion, actuator/hitch linkage, actuator linkage to mounting plate, resilient member; actuator holds open/closed | No pintle hook; two passive cam jaws; actuator is release-only and does not hold closed or carry load | Medium. Dependent and method claims plus national claims require professional charting. |
| US20260014823A1 | AMR, funnel-guided pin, jaw/electromechanical latch, sensing and automatic release | Fixed socket carries load; dual grooved-pin retention jaws and release yoke differ from illustrated single jaw/lever arrangement | High. The published claims and prosecution history must be charted; broad functional overlap remains. |
| WO2023043676A1 / US11987084B2 family | Guided receiver, latch, hook sensing and actuator states | Separate presence and yoke-home sensing; no hook; actuator has no intermediate load-holding state | Medium. Active granted claims must be compared jurisdiction by jurisdiction. |
| US10168711B2 | Powered cart latch and brake release coordination | V2 CAD has no trolley brake-release linkage | Lower for this feature, but other claims still require review. |
| US20210017007A1 family | AGV hitch with powered positioning/sensing | V2 receiver is chassis-fixed; no vertical/lateral powered hitch positioning | Lower for powered positioning claims; generic hitch claims remain relevant. |

## Conclusions and required next step

The design deliberately avoids the specific actuator-held movable pintle architecture and powered floating-positioner architecture. It does not avoid the crowded broad concept of funnel-guided pin capture, sensing, and powered release. No statement that the product "does not violate patents" is supportable from this limited search. Before manufacture or sale, counsel should run current Indian InPASS and target-market register searches, identify live national-family claims, inspect prosecution amendments, and prepare an element-by-element claim chart against the final production design.

Do not describe V1 as patented, patentable, cleared, or non-infringing.

## V1 independent-claim risk matrix

This matrix compares the public V1 release, despite the older V2 wording elsewhere in this historical review. A patent claim is normally infringed literally only if every required element is present; equivalents, claim construction, prosecution history, national amendments and indirect infringement still require legal analysis.

| Family / independent claim | Required combination relevant here | V1 comparison | Preliminary literal-overlap risk |
|---|---|---|---|
| ATI US20260014823A1 claim 1 (pending US publication) | Top plate with integrated manual release handle; bottom plate; electromechanical pin jaw with inbuilt motor pushing a lever to open/close a claw; pin sensor plus impact sensor plus current/load sensing; microcontroller; funnel plates ending in a pin notch; trolley link with Z-axis pivot | V1 has no integrated top-plate release handle, no inbuilt latch motor, no actuator-close function, no specified impact/current/load sensor suite, and no Z-pivot trolley link. It uses an external release-only yoke, dual spring-closed jaws and a separate fixed load socket. | Reduced against the complete published combination, but not cleared. Pending claims may change. |
| ATI US20260014823A1 claims 6 and 9 | Specific LiDAR/depth-camera approach plus multiple confirmation sensors; motor/lever claw release | V1 CAD does not specify that sensor-fusion method and does not use an inbuilt motor that opens and closes a single claw. | Reduced for the published method wording; control implementation must preserve the distinction. |
| AIS WO2022027141A1 claim 1 | Mounting plate, pintle hitch movable portion, actuator, hitch linkage, actuator linkage to mounting plate and resilient member biasing the pintle closed | V1 has no pintle hitch and no actuator linkage holding a movable pintle. It uses two passive retention jaws around a grooved vertical striker; a fixed socket carries towing load. | Reduced. The listed PCT record is ceased, but disclosure remains prior art and national rights must be checked. |
| Crown WO2023043676A1 / US11987084B2 family | Receiving member, latch, sensors and an actuator commanded among retracted, intermediate and extended positions | V1 specifies two endpoint release states, a pin rather than a cart hook, and no intermediate actuator load-holding state. | Medium. Live national claims and continuations require jurisdiction-specific charting. |
| Tractonomy US11919155B2 claim 1 | At least two robot arms; each arm has a gripper hand with at least two grippers biased open; a movable latch locks those grippers closed | V1 has one fixed receiver, two jaws biased closed, no two robot arms and no secondary latch locking the jaws. | Lower for claim 1's complete structure. |
| Omron US10168711B2 independent claims | Sensor-directed gross/fine cart alignment followed by latching, transport and unlatching; some claims add motorized hook/brake interaction | V1 mechanical CAD does not define the claimed two-stage sensing method, V-shaped cart-recognition geometry, motorized pulling hook or cart-brake release. | Mechanical overlap appears lower; AMR navigation/control software still requires separate review. |
| USPS US20210017007A1 / US11708252B2 family | Hitch with powered vertical and/or lateral positioning, sensing and control | V1 receiver is chassis-fixed and has no powered vertical or lateral positioning axes. | Lower for claims requiring powered positioning. |

## Design controls that preserve the intended distinctions

- Keep the actuator release-only. Do not use actuator force to hold the jaws closed during towing.
- Keep the fixed socket as the primary longitudinal load path; the jaws provide retention rather than the main towing bearing surface.
- Do not implement a three-position actuator controller unless the Crown family has been professionally cleared for the target country.
- Avoid an integrated top-plate manual handle matching the ATI claim wording. A required service override should be separately guarded and legally reviewed.
- Do not add a two-arm, two-gripper architecture or a secondary latch that locks normally-open grippers closed.
- Treat navigation, vision, sensor fusion and trolley-brake control as separate patent-review workstreams; the present CAD review does not clear software methods.

## What can and cannot be claimed

The engineering combination is differentiated from the specific independent-claim structures reviewed above. The broad idea of an AMR automatically capturing, towing and releasing a cart is not unique. This review cannot establish worldwide novelty, patentability or freedom to operate. Only a current search of the intended countries, legal-status verification and an attorney-prepared claim chart against the final manufactured product can support a clearance opinion.

## Sources reviewed

- WO2022027141A1: https://patents.google.com/patent/WO2022027141A1/en
- US20260014823A1: https://patents.google.com/patent/US20260014823A1/en
- WO2023043676A1: https://patents.google.com/patent/WO2023043676A1/en
- US10168711B2: https://patents.google.com/patent/US10168711B2/en
- US20210017007A1 and granted family member US11708252B2: https://patents.google.com/patent/US20210017007A1/en

Patent status and claim scope can change. The linked records are research inputs, not substitutes for official national registers.
