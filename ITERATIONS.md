# Build / inspect / revise log

## R1 — initial official-silhouette reconstruction

Created from empty files and all twelve supplied images. Traced the curved blade and skewed D-frame, added bilateral channel relief, upper clamp, root and grip, identical second master, GLB/STL export and fourteen inspection views.

Actions run 34220927713 reached the geometry check and exposed 17 disconnected voxel surface components (zero nonmanifold edges). No artifact was produced. This is a failed validation pass, not a successful delivery.

## R1.1 — diagnostic export

Added per-component bounds/count reporting and a clearly marked diagnostic-only non-strict export switch, without changing the silhouette. This permits the first multi-view artifact to be inspected while diagnosing the voxel islands. Final delivery must restore strict validation and pass the single-component check.
