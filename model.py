"""Original five-star Lappland: full-size blunt cosplay reconstruction.
Run: blender -b --python model.py
Parameters are millimetres unless marked px. Geometry is built first;
reference-specific grip colours are assigned as an explicit finishing pass.
"""
import sys
import os
import json
import traceback
from pathlib import Path
import bpy

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from lappland_geometry import build

CONFIG = {
    'revision': 'r4-final-original-grip-pattern',
    'strict_validation': True,
    'remove_subvoxel_islands': True,
    'reference_mm_per_pixel': 1.2823007845,
    'section_plane_x': True,
    'round_tip_axis': True,
    'shoulder_recess_mm': 1.8,
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
    'wrap_pitch_mm': 22.0,
    'wrap_width_mm': 2.2,
    'grip_pattern': 'ivory body / dark crossed seams / dark pommel',
    'stl_voxel_mm': 0.70,
}


def finish_grip_materials():
    """Match the concept's light tiles/dark seams, not generic dark katana diamonds.

    No vertex coordinates are changed here: the thin seam geometry was already
    built and included in the validated STL. A/B meshes share their materials.
    """
    counts = {'body':0, 'seams':0, 'pommel':0}
    for ob in list(bpy.context.scene.objects):
        if ob.type != 'MESH':
            continue
        if ob.name.startswith('Grip | oval charcoal underwrap'):
            ob.data.materials[0] = bpy.data.materials['wrap']
            ob.name = ob.name.replace('oval charcoal underwrap','ivory oval body')
            counts['body'] += 1
        elif ob.name.startswith('Grip | ivory crossed ribbon'):
            ob.data.materials[0] = bpy.data.materials['leather']
            ob.name = ob.name.replace('ivory crossed ribbon','dark crossed seam')
            counts['seams'] += 1
        elif ob.name.startswith('Grip | rounded pommel cap'):
            ob.data.materials[0] = bpy.data.materials['spine']
            counts['pommel'] += 1
    assert counts == {'body':2,'seams':4,'pommel':2}, counts
    # The hidden STL master is a neutral geometry check, not a second paint scheme.
    for ob in bpy.data.collections['EXPORT_SOLIDS | hidden / millimetre STL source'].objects:
        if ob.type == 'MESH':
            ob.data.materials.clear()
            ob.data.materials.append(bpy.data.materials['frame'])
            for polygon in ob.data.polygons:
                polygon.material_index = 0
    bpy.ops.object.select_all(action='DESELECT')
    for name in ('SWORD_A | original master','SWORD_B | same design / shared meshes'):
        for ob in bpy.data.collections[name].objects:
            if ob.type == 'MESH':
                ob.select_set(True)
    bpy.context.scene['grip_pattern'] = CONFIG['grip_pattern']
    output = ROOT/'output'
    bpy.ops.export_scene.gltf(filepath=str(output/'lappland_original_pair.glb'),
        export_format='GLB',use_selection=True,export_apply=True,export_yup=True)
    path = output/'model_manifest.json'
    manifest = json.loads(path.read_text(encoding='utf-8'))
    manifest.update({'grip_pattern':CONFIG['grip_pattern'], 'grip_style_object_counts':counts,
        'source_commit':os.environ.get('GITHUB_SHA','local'),
        'workflow_run_id':os.environ.get('GITHUB_RUN_ID','local')})
    manifest['reference_limitations'].append(
        'Dark grip seams are represented by shallow solid bands. Their exact relief is inferred; '
        'the light body/dark lattice follows the concept drawing rather than generic katana wrapping.')
    path.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    bpy.ops.wm.save_as_mainfile(filepath=str(output/'lappland_original_pair.blend'))
    print('LAPPLAND_FINAL_STYLE '+json.dumps(manifest))


if __name__ == '__main__':
    try:
        build(CONFIG)
        finish_grip_materials()
    except Exception:
        traceback.print_exc()
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(1)
