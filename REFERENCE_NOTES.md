# Original Lappland — reference ledger

This is a clean-room reconstruction begun at the empty repository skeleton. No earlier implementation or external 3D asset has been consulted. The supplied archive contains 12 images. Only the original five-star operator, E2 and The Young Fang are in scope; Elegant Menace and Lappland the Decadenza are excluded.

## Priority and what was actually read

1. `Lappland_Concept_Art.png` (763 x 816): primary silhouette authority. The isolated sword establishes the long narrow curving blade, an unusually large skewed D-shaped frame *below* the grip rather than a conventional symmetric crossguard, the straight chord, the layered upper shoulder, crossed light grip wrapping and pommel. It is a drawing, not a dimensioned engineering orthographic projection.
2. `The_Young_Fang.png` (511 x 511): checks that the two swords belong to the same design family and confirms the dark/light blade faces and the skewed guard/chord relationship. Debris, white cloth and composition are not blade geometry.
3. `Lappland.png` (890 x 1221): original official standing art, checks the pair, blade-to-body scale and the two-handed presentation. Perspective and foreshortening prevent direct dimension recovery.
4. `Lappland_Elite_2.png` (2048 x 2048): checks both grips/guards and the long single-edged-looking curved silhouette; effects and occlusion are not reconstructed.
5. `05_apex_front.jpg`: overall silhouette/scale secondary check.
6. `06_apex_back.jpg`: reverse guard and spatial orientation check.
7. `07_apex_back2.jpg`: backside chord and handle relation check.
8. `08_apex_3q.jpg`: three-quarter blade/guard relationship.
9. `09_apex_upper.jpg`: upper-body grip and sword-root details.
10. `10_apex_scale.jpg`: coarse full-figure proportion only; no stated weapon dimension is inferred from a figure photograph.
11. `11_apex_guard_side.jpg`: guard depth and inner opening, secondary only.
12. `12_apex_weapon_closeup.jpg`: raised shoulder plate, recessed perimeter channel, root collar and the substantial guard cross-section. This supports layering but does not override the concept silhouette.

## Reproducible trace and scale

The concept sheet's grip axis runs approximately from pixel (624,253), the root, to (702,109), the pommel. An initial chosen root-to-pommel scale of 210 mm gives 1.2823007845 mm/pixel. Local +Z points toward the pommel. Local X is across the broad blade and Y is thickness. The origin is the grip/root junction. All script inputs are millimetres; Blender coordinates and GLB are metres. STL stores literal millimetres.

The front reference trace is encoded as paired cubic curves in `model.py`. The outer arc starts near (551,243), passes around (665,365) and ends near (559,500). The chord closes it. The inner opening is separately traced, rather than generated as a circular torus. Blade stations follow the gradual leftward sweep and the narrow almost-constant width before the final nose.

## Explicit assumptions

No official weapon length or thickness is printed in the supplied references. The roughly 1.07 m overall length is a full-size cosplay scale choice, not a verified canonical measurement. The broad blade face and dull bevel are modelled, but the land stays 3.2 mm thick and the tip has a 4 mm planar radius. Guard core depth, reverse-face channels, exact rail heights, cap/lug construction and small fastener positions are restrained reconstructions based on the concept layering and APEX oblique views. They are not official dimensions.

The two swords share one full-size geometric master. Apparent dark/silver differences are treated as facing/lighting rather than evidence for unequal-length blades or a different guard. No unsupported extra quillons, serrations, wolf heads, spikes, internal mechanisms or alter-specific ornaments are added. The long loose carry strap on the concept sheet is excluded from the rigid prop, as are module background debris and E2 visual effects.

## Prop use

This is an appearance reference for lightweight, compliant cosplay construction. A blunt rigid print can still injure; this model is not certified impact-safe or venue-approved. Do not sharpen it, add a cutting insert or use it as a real weapon. Whole STLs are supplied as continuous reference solids, not a printer-specific split/connector kit.
