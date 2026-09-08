# Lappland / original five-star twin swords

Clean-room Blender Python reconstruction from the user's original/E2/The Young Fang reference archive. **Not** Elegant Menace or Lappland the Decadenza.

Run the existing Blender Build workflow, or run Blender 4.2.1 locally:

```sh
blender -b --python model.py
blender -b --python render.py
```

The workflow uploads `output/` and `renders/` as **lappland-build**. The deliverable includes an editable BLEND, pair GLB, two individual watertight millimetre STLs plus a pair STL, a measured validation manifest, source scripts, and front/back/side/top/three-quarter/guard/tip/grip inspection PNGs. STL is explicitly millimetres; GLB and Blender use metres.

`model.py` contains the scale, trace and construction parameters. `lappland_geometry.py` contains the from-scratch bpy mesh builders; `render.py` is the headless inspection renderer. See `REFERENCE_NOTES.md` for the twelve-reference inventory, scale assumptions, precedence and inferred backside structures. See `ITERATIONS.md` for the actual revision log.

Safe cosplay appearance reference only: finite blunt edge lands and rounded tips; no sharpened weapon construction. Use lightweight compliant materials and follow venue requirements. The full-size reconstruction is not a certified official dimensional replica or an impact-safe fabrication kit.
