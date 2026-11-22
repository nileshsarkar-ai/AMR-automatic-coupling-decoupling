# AMR automatic coupler V2

Parametric CAD for a compact AMR-to-trolley automatic coupling. V2 uses a fixed structural load socket, dual spring-closed helmet-style retention jaws, a release-only linear actuator and independent pin/release sensing.

## Build

```powershell
python -m pip install cadquery==2.6.1 vtk==9.3.1 imageio imageio-ffmpeg
python .\src\build_amr_coupler_v2.py
python .\src\render_v2.py
```

Outputs are written under `outputs/v2/`, including coupled and released STEP/STL assemblies, individual part STLs, previews, and the 360-degree MP4.

## Safety

Concept prototype only. The included load calculations are screening estimates, not certification. Complete FEA, tolerance analysis, spring sizing, actuator sizing, guarding, safety-rated controls, fatigue/impact evaluation and physical proof testing before real towing. See `docs/PATENT_DESIGN_AROUND_REVIEW.md` for the preliminary patent-risk screen.
