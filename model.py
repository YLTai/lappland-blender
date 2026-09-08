"""Original Lappland: first visual inspection and union diagnostics.
Run: blender -b --python model.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lappland_geometry import build

CONFIG = {
    'revision': 'r1.1-union-diagnostic',
    'strict_validation': False,
    'reference_mm_per_pixel': 1.2823007845,
    'blade_stations_mm': [
        [8.0,-12.0,33.0],[10.71,-29.20,33.27],[2.35,-124.14,34.53],
        [-8.13,-242.11,34.53],[-22.50,-363.65,34.53],[-39.74,-485.28,34.53],
        [-58.11,-607.52,34.53],[-80.15,-723.00,34.53],[-104.27,-800.96,32.0],
        [-124.2,-837.3,16.0],[-133.1,-852.1,8.0]
    ],
    'blade_thickness_mm': 8.5,
    'blunt_edge_mm': 3.2,
    'spine_land_mm': 4.0,
    'tip_radius_mm': 4.0,
    'guard_outer_beziers_px': [
        [[551,243],[615,239],[669,291],[665,365]],
        [[665,365],[669,446],[622,492],[559,500]]
    ],
    'guard_inner_beziers_px': [
        [[571,260],[620,263],[650,306],[649,368]],
        [[649,368],[651,435],[617,475],[576,483]]
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
    build(CONFIG)
