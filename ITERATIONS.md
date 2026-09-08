# Build / download / inspect / revise log

## R1 — from the empty repository

Created the blade, skewed D-frame/chord, layered shoulder, grip, identical second sword and exporters from the twelve supplied images. Commit e1c3d5e1202deb23836d0c606517944d204271e1; Actions 34220927713 failed the strict union test (17 surface components, zero nonmanifold edges). No usable artifact was produced; this was not a completed model.

## R1.1 — diagnostic artifact actually downloaded

Commit 34ff670bf37e5c7cf506f7c187afdcd4b8cdb39e; successful Actions run 34221348893; lappland-build artifact 10054104949. Downloaded the 87.7 MB ZIP and inspected all fourteen PNG views, with full-size guard/handle details and a reference-aligned actual Blender silhouette mask. This diagnostic version was explicitly marked validation_passed=false.

The union diagnostics contained one real sword (361,952 vertices) and sixteen tiny resampling islands at the blade/root overlap: maximum island extent 0.754 mm, others below 0.22 mm. No intentional part needed to be discarded. Final validation must require one component after removing only subvoxel numerical islands.

Largest visible errors: the guard chord and curved perimeter were too thin and inset; the long blade centreline was too far right and its distal portion too wide; the broad stepped ricasso was missing; the two handle spirals projected as a zigzag rather than crossing. On eleven manually checked lower-blade scanlines the actual render differed from the concept trace by a mean 5.48 mm centreline offset (maximum 13.46 mm) and mean 5.36 mm width difference (maximum 10.26 mm), at the chosen reconstruction scale. These are image-projection comparisons, not physical/canonical accuracy measurements.

## R2 — geometry corrections after artifact inspection

Retraced independent outer and inner guard curves: outer endpoints moved from (551,243)/(559,500) to (540,240)/(549,511); the straight chord is now materially wider, with the original skew maintained. Broadened the curved frame and adjusted the opening instead of scaling a torus. Replaced the blade stations with the checked concept silhouette, including a roughly 50 mm-wide root stepping into a roughly 29–32 mm main blade. Aligned station planes to the measured X-section to avoid a false lump at this transition. Added a restrained 3 mm extra root thickness and larger dark root band; preserved the 3.2 mm blunt edge land and rounded 4 mm tip.

Corrected the opposed wrap phase by half a turn so that the two ribbons form the concept's crossed pattern. Restored strict topology validation and enabled narrowly bounded subvoxel island removal only. Darkened the recessed/underwrap materials and lowered exposure to make depth readable, without adding unrelated decoration. The existing workflow is unchanged; model entry errors now exit nonzero.

R2 must be downloaded and inspected before any final acceptance statement is made.
