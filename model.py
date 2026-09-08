"""Original Lappland / semantic part reconstruction / Blender 4.2.1.

The active design has no image-pixel control points. It uses a half-annulus,
its diameter beam, concentric relief, a swept blunt blade and an oval grip.
"""
import bpy
import sys
import os
import json
import shutil
import traceback
from pathlib import Path

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import lappland_geometry as G
from semantic_geometry import analytic_guard,blade_sections,add_circle_proof

CONFIG={
    'revision':'r5-semantic-half-circle-constraint',
    'strict_validation':True,
    'remove_subvoxel_islands':True,
    'guard_outer_radius_mm':175.0,
    'guard_radial_width_mm':25.0,
    'guard_center_xz_mm':[-14.0,-185.0],
    'diameter_to_blade_angle_deg':30.0,
    'diameter_beam_width_mm':18.0,
    'guard_core_depth_mm':12.0,
    'guard_rail_lift_mm':3.0,
    'shoulder_arc_deg':65.0,
    'shoulder_recess_mm':1.8,
    'blade_neck_z_mm':12.0,
    'blade_body_span_mm':855.0,
    'sweep_linear_mm':86.0,
    'sweep_quadratic_mm':18.0,
    'sweep_nose_mm':32.0,
    'blade_main_width_mm':31.5,
    'blade_root_width_mm':50.0,
    'blade_thickness_mm':8.5,
    'ricasso_extra_thickness_mm':3.0,
    'ricasso_broad_end':0.12,
    'edge_bevel_fraction':0.12,
    'blunt_edge_mm':3.2,
    'spine_land_mm':4.0,
    'tip_radius_mm':4.0,
    'round_tip_axis':True,
    'section_plane_x':True,
    'grip_end_mm':202.0,
    'wrap_pitch_mm':22.0,
    'wrap_width_mm':2.2,
    'stl_voxel_mm':0.70,
    'grip_pattern':'ivory oval body / dark crossed seams / dark rounded pommel',
    'reference_policy':'official geometry and user circle constraint first; no projected contour tracing',
}
CONFIG['blade_stations_mm']=blade_sections(CONFIG)


def finish_and_record():
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH':
            continue
        if ob.name.startswith('Grip | oval charcoal underwrap'):
            ob.data.materials[0]=bpy.data.materials['wrap']
            ob.name=ob.name.replace('oval charcoal underwrap','ivory oval body')
        elif ob.name.startswith('Grip | ivory crossed ribbon'):
            ob.data.materials[0]=bpy.data.materials['leather']
            ob.name=ob.name.replace('ivory crossed ribbon','dark crossed seam')
        elif ob.name.startswith('Grip | rounded pommel cap'):
            ob.data.materials[0]=bpy.data.materials['spine']
    output=ROOT/'output'
    bpy.ops.object.select_all(action='DESELECT')
    for name in ('SWORD_A | original master','SWORD_B | same design / shared meshes'):
        for ob in bpy.data.collections[name].objects:
            ob.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(output/'lappland_original_pair.glb'),
        export_format='GLB',use_selection=True,export_apply=True,export_yup=True)
    proof=add_circle_proof(CONFIG,output)
    manifest=json.loads((output/'model_manifest.json').read_text())
    manifest.update({
        'source_commit':os.environ.get('GITHUB_SHA','local'),
        'workflow_run_id':os.environ.get('GITHUB_RUN_ID','local'),
        'guard_geometry':'concentric 180-degree annulus + half-plane diameter beam',
        'guard_outer_diameter_mm':2*CONFIG['guard_outer_radius_mm'],
        'guard_inner_diameter_mm':2*(CONFIG['guard_outer_radius_mm']-CONFIG['guard_radial_width_mm']),
        'guard_rail_face_to_face_mm':CONFIG['guard_actual_rail_depth_mm'],
        'guard_shoulder_face_to_face_mm':CONFIG['guard_actual_shoulder_depth_mm'],
        'grip_pattern':CONFIG['grip_pattern'],
        'circle_pair_validation_passed':proof['passed'],
        'active_model_contains_pixel_trace':False,
        'third_party_mesh_imported':False,
        'pair_relation':'Congruent swords; their guard frames are complementary half-circles in the supplied proof pose.'
    })
    manifest['reference_limitations'].append(
        'Circle closure is a user-specified geometric constraint. The proof shows only the guard frames, '
        'not an invented latch or a collision-free assembly of the complete swords.')
    (output/'model_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    old=output/'reference_profile.json'
    if old.exists():
        old.rename(output/'analytic_guard_profile.json')
    sources=output/'source'
    for name in ('semantic_geometry.py','reference_probe.py','README.md','REFERENCE_NOTES.md','ITERATIONS.md'):
        if (ROOT/name).exists():
            shutil.copy2(ROOT/name,sources/name)
    bpy.context.scene['guard_design']='two 180 degree half annuli / common radius / non-overlapping half-plane beams'
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.wm.save_as_mainfile(filepath=str(output/'lappland_original_pair.blend'))
    print('LAPPLAND_SEMANTIC_VALIDATION '+json.dumps(manifest))


if __name__=='__main__':
    try:
        G.guard=analytic_guard
        G.build(CONFIG)
        finish_and_record()
        from reference_probe import probe
        probe(ROOT/'output')
    except Exception:
        traceback.print_exc()
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(1)
