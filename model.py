"""Original five-star Lappland: full-size blunt cosplay reconstruction.
Run: blender -b --python model.py
All parameters are millimetres unless explicitly marked px.
"""
import sys
import os
import traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lappland_geometry import build

CONFIG = {
    'revision': 'r2-official-profile-and-crosswrap',
    'strict_validation': True,
    'remove_subvoxel_islands': True,
    'reference_mm_per_pixel': 1.2823007845,
    'section_plane_x': True,
    'blade_stations_mm': [
        [-0.641,-12.823,30.775],[-1.923,-28.211,48.727],[-2.565,-51.292,50.010],
        [-5.129,-76.938,50.010],[-6.412,-102.584,50.010],[-8.335,-128.230,48.727],
        [-10.258,-162.852,47.445],[-19.235,-171.828,29.493],[-20.517,-192.345,29.493],
        [-21.799,-217.991,29.493],[-28.211,-282.106,29.493],[-35.904,-346.221,29.493],
        [-42.957,-410.336,30.775],[-50.010,-474.451,32.058],[-57.704,-538.566,32.058],
        [-66.680,-602.681,29.493],[-76.297,-666.796,28.211],[-86.555,-730.911,28.211],
        [-92.967,-762.969,28.211],[-102.584,-795.026,24.364],[-109.637,-814.261,23.081],
        [-119.254,-833.496,16.670],[-126.948,-846.319,11.541],[-132.700,-851.700,8.000]
    ],
    'blade_thickness_mm': 8.5,
    'ricasso_extra_thickness_mm': 3.0,
    'ricasso_broad_end': 0.12,
    'edge_bevel_fraction': 0.12,
    'blunt_edge_mm': 3.2,
    'spine_land_mm': 4.0,
    'tip_radius_mm': 4.0,
    'guard_outer_beziers_px': [
        [[540,240],[584.91,219.31],[661.14,250],[670,366]],
        [[670,366],[669.18,409.45],[655.23,504.96],[549,511]]
    ],
    'guard_inner_beziers_px': [
        [[570,253],[602.47,260],[639.38,280],[644,371]],
        [[644,371],[644.33,455.10],[590,477.34],[576,480]]
    ],
    'guard_core_depth_mm': 12.0,
    'guard_rail_lift_mm': 3.0,
    'shoulder_arc_fraction': 0.37,
    'grip_end_mm': 202.0,
    'wrap_pitch_mm': 25.5,
    'wrap_width_mm': 3.4,
    'stl_voxel_mm': 0.70,
}

if __name__ == '__main__':
    try:
        build(CONFIG)
    except Exception:
        traceback.print_exc()
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(1)
