# AMR automatic coupler V1

Parametric CAD for a compact AMR-to-trolley automatic coupling. V1 uses a fixed structural load socket, dual spring-closed helmet-style retention jaws, a release-only linear actuator, independent pin/release sensing, replaceable wear inserts, rolling cam followers and payload profiles.

## Build

```powershell
python -m pip install cadquery==2.6.1 vtk==9.3.1 imageio imageio-ffmpeg
python .\src\build_amr_coupler_v1.py
python .\src\render_v1.py
python .\src\validate_v1.py
```

Outputs are written under `outputs/v1/`, including coupled and released STEP/STL assemblies, 30 individual part STLs, a 360-degree MP4, and a working AMR/payload coupling and decoupling MP4.

The operation video starts with the actual jaw and striker movement, zooms out to the AMR towing a loaded trolley, and shows parking, powered release and physical separation. It is a kinematic engineering demonstration; final spring rates, actuator stroke/force and control timing must be established by test.

## Safety

Concept prototype only. The included load calculations are screening estimates, not certification. Complete FEA, tolerance analysis, spring sizing, actuator sizing, guarding, safety-rated controls, fatigue/impact evaluation and physical proof testing before real towing. See `docs/PATENT_DESIGN_AROUND_REVIEW.md` for the preliminary patent-risk screen.
