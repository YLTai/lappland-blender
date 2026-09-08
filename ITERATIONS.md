# Clean-room build / download / inspect / revise record

No earlier implementation or third-party 3D asset was read or restored. The starting model.py and render.py were empty. All twelve user images are inventoried in REFERENCE_NOTES.md.

## R1 — initial build, failed validation

Commit e1c3d5e1202deb23836d0c606517944d204271e1; Actions 34220927713. Built blade, D-frame/chord, shoulder, grip, pair and exports. Strict union validation found 17 components and zero nonmanifold edges. No usable artifact was produced. This is recorded as a failed build, not a completed deliverable.

## R1.1 — first downloaded artifact

Commit 34ff670bf37e5c7cf506f7c187afdcd4b8cdb39e; Actions 34221348893; artifact 10054104949 (87.7 MB). Downloaded, extracted and inspected all fourteen views, full-size guard/grip details, and the actual Blender mask aligned with the concept sheet. Diagnostic metadata explicitly said validation_passed=false.

The 17 components were one real sword (361,952 vertices) plus sixteen numerical islands at the blade/root overlap. The largest island extent was 0.754 mm; the others were below 0.22 mm. Added narrowly bounded subvoxel handling, not blanket deletion of real parts.

Largest errors: guard chord/perimeter too thin and inset, blade centreline too far right and distal blade too wide, absent broad stepped ricasso, grip spirals reading as a zigzag. Eleven checked lower-blade scanlines gave mean absolute centre deviation 5.48 mm (maximum 13.46 mm), mean width difference 5.36 mm. These values use the chosen image-to-prop scale; they are not official physical tolerances.

## R2 — official silhouette/proportion correction

Commit fe995ae718520531d2baa2f846a994a8d7866c32; Actions 34222880433; downloaded artifact 10054752382 (89.0 MB). Inspected all fourteen views, enlarged guard/tip renders and the reference overlay. Independently reloaded A/B STL and GLB.

Retraced outer guard endpoints to (540,240)/(549,511), widened the chord/perimeter and independently corrected the opening. Replaced blade stations from the concept trace, including a roughly 50 mm root stepping into the roughly 29–32 mm main blade. Added an inferred 3 mm root-thickness increase. Opposed wrap phase was corrected to create crossings.

Strict and independent validation passed: one component per sword, zero nonmanifold edges, consistent winding, positive volume, watertight STLs, identical A/B masters, metre GLB without external dependencies. No numerical islands needed removal. The same eleven scanlines reduced to 1.28 mm absolute centre deviation (one source pixel), with zero width difference at that raster sampling. Remaining problems were a flat shoulder cap, insufficient light grip coverage, a sheared/pinched-looking nose cap, and oblique cameras that were not literally 45 degrees.

## R3 — shoulder layers and genuinely rounded nose

Commit b5db1d404cce90b049d68f061f310c60db9354f8; Actions 34224349165; downloaded artifact 10055262883 (90.5 MB). Inspected the complete fourteen-view contact sheet, reference overlay and grip/tip details; independently revalidated the exported files.

Preserved the converged blade and guard outline. Added a real 1.8 mm shoulder recess between raised lips, rotated the final nose sections into the local normal plane for a nominal 4 mm rounded cap, and changed pair/guard/tip cameras to actual 45-degree azimuths. The broader 7 mm light wrap improved coverage but still resembled generic white katana wrapping over dark diamonds, rather than the concept's predominantly light grip with dark intersecting seam lines.

Validation again passed with no islands removed: one component, zero nonmanifold edges, 797,948 triangles per sword. Dimensions were 1066.62 x 286.76 x 31.60 mm (length x width x depth). The eleven blade scanlines gave mean centre deviation 1.17 mm, maximum 1.28 mm, mean width difference 0.23 mm. The deliberately rounded last few millimetres are a safety adaptation, not an attempt to copy a sharp point.

## R4 — final original-grip correction

The enlarged concept grip was checked against R3's actual close-up. Changed the pattern to an ivory oval body with dark crossed seams, seam width 2.2 mm and pitch 22 mm, and a dark rounded pommel. This does not borrow a different character/outfit design. The seam bands retain shallow relief as an explicit reconstruction assumption.

Geometry remains generated and validated before material assignment. model.py now performs a named, checked grip-material finishing pass, re-exports GLB and BLEND, and records the actual GitHub source commit/run in the manifest. No vertices change in that finishing pass, so STL and editable geometry remain consistent. The converged blade, guard, recessed shoulder, blunt edge and rounded nose are unchanged. All fourteen views are regenerated, and render.py writes SHA-256 checksums for the actual final model files and PNGs.

Build-time validation is distinct from the subsequent download inspection. The final downloaded artifact and independent checks are the acceptance evidence; a successful Actions status alone is not sufficient.
