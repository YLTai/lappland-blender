# Build / download / inspect / revise log

## R1 — clean-room initial build

Started from empty repository files; used all twelve supplied references. Created blade, skewed D-frame/chord, upper shoulder, grip, pair and exports. Commit e1c3d5e1202deb23836d0c606517944d204271e1; Actions 34220927713 failed its strict union check (17 surface components, zero nonmanifold edges). No usable artifact was produced. This failed pass is not counted as an inspected delivery.

## R1.1 — first downloaded inspection artifact

Commit 34ff670bf37e5c7cf506f7c187afdcd4b8cdb39e; Actions 34221348893; artifact 10054104949, 87.7 MB. Downloaded and inspected all fourteen views, with full-size guard/handle details and an actual Blender silhouette aligned over the official concept. Diagnostic metadata explicitly said validation_passed=false.

Union diagnostics showed one real sword (361,952 vertices) and sixteen numerical islands at the blade/root overlap: largest island extent 0.754 mm, others below 0.22 mm. No intentional component was missing or required deletion. Added narrowly bounded numerical-island handling and retained the strict final topology requirement.

Largest geometry errors: guard chord/perimeter too thin and inset; main blade centreline too far right and distal portion too wide; missing wide stepped ricasso; handle spirals projecting as a zigzag instead of crossing. Eleven checked lower-blade scanlines gave mean absolute centreline deviation 5.48 mm, maximum 13.46 mm, and mean width difference 5.36 mm at the chosen image scale. These are projection measurements, not claims of canonical physical accuracy.

## R2 — silhouette and proportion correction, second downloaded artifact

Commit fe995ae718520531d2baa2f846a994a8d7866c32; Actions 34222880433; artifact 10054752382, 89.0 MB. Downloaded, extracted and inspected all fourteen views, full-size guard oblique and tip, and the reference-overlay mask. Independently reloaded both STLs with trimesh and the GLB as a scene.

Moved outer guard endpoints to (540,240)/(549,511), broadened the chord and curved perimeter, independently corrected the opening, and replaced blade stations with the measured concept trace. Added the approximately 50 mm ricasso stepping into the approximately 29–32 mm main blade, plus its inferred 3 mm extra thickness. Rotated the opposing wrap phase by half a turn to create real crossings.

Results: strict build validation passed, one connected component, zero nonmanifold edges, no numerical islands needed removal. Independent STL check confirmed watertight, consistent winding and positive volume; A/B files were identical masters. GLB contained 56 mesh instances and no external dependencies, in metres. On the same eleven lower-blade scanlines, absolute centreline deviation reduced to 1.28 mm (one reference pixel) and width differences to zero at that raster sampling. This shows convergence to the supplied drawing, not sub-millimetre real-world accuracy.

Remaining visible issues: upper shoulder was too uniformly flat rather than grooved, light grip wrapping covered too little of the handle, and the X-aligned nose cap looked pinched in the tip close-up. The former '45' cameras also had shallower actual azimuths.

## R3 — targeted final geometry and inspection-camera refinement

Kept the converged main blade and guard outline. Rebuilt the upper shoulder as a floor plus raised outer lip/inner plate, with a real 1.8 mm recessed channel, on both faces. Increased ivory ribbon width to 7 mm and set pitch to 22 mm to approach the reference's light-dominant crossed grip. Blended the last blade stations into the local normal plane, retaining the nominal 4 mm rounded nose rather than a sheared cap. The pair, guard and tip oblique cameras now have actual 45-degree azimuths; they retain modest elevation to expose the layered depth. No unrelated decoration, skin or alter geometry was introduced.

The workflow generates the complete BLEND/GLB/STL/14-PNG package with strict per-sword topology validation and recorded nominal/measured dimensions. Final artifact inspection is performed on the downloaded outputs, separately from the build's internal checks.
