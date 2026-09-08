"""Reproducible multiview inspection, including actual guard-circle closure.
The second Blender scene contains copies of the delivered guard meshes,
not an ideal-circle drawing substituted for the parts.
"""
import bpy
import json
import math
import hashlib
import os
import sys
import traceback
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'
RENDERS=ROOT/'renders'


def main():
    RENDERS.mkdir(exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(OUT/'lappland_original_pair.blend'))
    scene=bpy.context.scene
    scene.name='Original Lappland | twin props'
    manifest=json.loads((OUT/'model_manifest.json').read_text())
    cfg=json.loads((OUT/'design_parameters.json').read_text())
    scene.render.engine='CYCLES'
    scene.cycles.device='CPU'
    scene.cycles.samples=16
    scene.cycles.use_denoising=True
    scene.cycles.max_bounces=4
    scene.cycles.diffuse_bounces=2
    scene.cycles.glossy_bounces=2
    scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGBA'
    scene.render.resolution_percentage=100
    scene.view_settings.view_transform='AgX'
    scene.view_settings.exposure=-0.45
    scene.world.use_nodes=True
    bg=scene.world.node_tree.nodes.get('Background')
    bg.inputs['Color'].default_value=(0.11,0.13,0.16,1)
    bg.inputs['Strength'].default_value=0.65
    studio=bpy.data.collections.new('STUDIO | inspect cameras and lights')
    scene.collection.children.link(studio)
    captions=bpy.data.collections.new('STUDIO | inspection captions')
    scene.collection.children.link(captions)

    def area(name,pos,power,size):
        data=bpy.data.lights.new(name,'AREA')
        data.energy=power
        data.shape='DISK'
        data.size=size
        ob=bpy.data.objects.new(name,data)
        studio.objects.link(ob)
        ob.location=pos
        ob.rotation_euler=(Vector((0,0,-0.25))-ob.location).to_track_quat('-Z','Y').to_euler()
    area('Key',(-1.4,-1.8,1.4),250,1.6)
    area('Fill',(1.1,-0.8,-0.25),120,1.4)
    area('Rim',(0.5,1.2,0.8),320,1.1)
    area('Lower fill',(-0.9,0.6,-1),100,0.9)
    mat=bpy.data.materials.new('Caption emission')
    mat.use_nodes=True
    nodes=mat.node_tree.nodes
    nodes.clear()
    em=nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value=(0.75,0.81,0.86,1)
    output=nodes.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(em.outputs[0],output.inputs[0])
    texts=[]
    for name in ('Title','Dimensions and assumptions'):
        data=bpy.data.curves.new(name,'FONT')
        ob=bpy.data.objects.new(name,data)
        captions.objects.link(ob)
        data.materials.append(mat)
        texts.append(ob)
    records=[]
    cameras={}

    def render_view(active,name,title,pos,target,scale,size,note):
        camera_data=bpy.data.cameras.new(name)
        camera_data.type='ORTHO'
        camera_data.ortho_scale=scale
        camera_data.clip_start=0.01
        camera_data.clip_end=30
        camera=bpy.data.objects.new(name,camera_data)
        studio.objects.link(camera)
        camera.location=pos
        camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
        active.camera=camera
        active.render.resolution_x,active.render.resolution_y=size
        active.render.resolution_percentage=100
        active.render.image_settings.file_format='PNG'
        active.render.image_settings.color_mode='RGBA'
        aspect=size[0]/size[1]
        half_w=scale/2 if aspect>=1 else scale*aspect/2
        half_h=scale/(2*aspect) if aspect>=1 else scale/2
        for ob in texts:
            ob.parent=camera
            ob.rotation_euler=(0,0,0)
        texts[0].data.body='LAPPLAND  /  '+title
        texts[0].data.size=min(scale*0.017,half_w*1.85/(max(1,len(texts[0].data.body))*0.60))
        texts[0].location=(-half_w+scale*0.03,half_h-scale*0.05,-0.3)
        texts[1].data.body=note
        texts[1].data.size=min(scale*0.0092,half_w*1.85/(max(1,len(note))*0.55))
        texts[1].location=(-half_w+scale*0.03,-half_h+scale*0.026,-0.3)
        active.render.filepath=str(RENDERS/(name+'.png'))
        bpy.context.view_layer.update()
        bpy.ops.render.render(write_still=True,scene=active.name)
        records.append({'file':name+'.png','scene':active.name,'location':pos,
                        'target':target,'ortho_scale':scale,'resolution':size})
        cameras[name]=camera

    ax=-0.22
    col_b=bpy.data.collections['SWORD_B | same design / shared meshes']
    length=manifest['dimensions_xyz_mm'][2]
    views=[
        ('01_pair_front','PAIR / FRONT',(0,-3,-0.33),(0,0,-0.33),1.28,(1500,1750),True,
         'Original five-star design | two congruent props | parametric part geometry'),
        ('02_front','A / FRONT',(ax,-3,-0.33),(ax,0,-0.33),1.25,(1000,1800),False,
         f'Overall measured length {length:.1f} mm | STL millimetres / GLB metres'),
        ('03_back','A / BACK',(ax,3,-0.33),(ax,0,-0.33),1.25,(1000,1800),False,
         'Reverse relief is inferred; concentric radii and the half-circle constraint remain exact'),
        ('04_side','A / SIDE',(ax+3,0,-0.33),(ax,0,-0.33),1.25,(800,1800),False,
         'Main section 8.5 mm / root 11.5 mm nominal | edge land 3.2 mm'),
        ('05_top','A / TOP',(ax,0,3),(ax,0,-0.12),0.49,(1700,1000),False,
         'Grip oval, broad-flat blade and real guard-layer thicknesses'),
        ('06_pair_45','PAIR / 45 DEGREE',(2,-2,0.45),(0,0,-0.33),1.32,(1600,1750),True,
         'Same master in both hands | no skin or alter-specific components'),
        ('07_guard_front','HALF-CIRCLE GUARD / FRONT',(ax+0.02,-2,-0.18),(ax+0.02,0,-0.18),0.44,(1550,1750),False,
         'R175 outer / R150 inner | exactly 180 degrees | diameter beam at 30 degrees to blade'),
        ('08_guard_back','HALF-CIRCLE GUARD / BACK',(ax+0.02,2,-0.18),(ax+0.02,0,-0.18),0.44,(1550,1750),False,
         'Concentric rails and recessed shoulder; backside detail is an explicit inference'),
        ('09_guard_45','GUARD / 45 DEGREE',(ax+1.01,-1,0.18),(ax+0.01,0,-0.15),0.49,(1750,1750),False,
         'Annular core + diameter beam + raised lips + recessed upper shoulder'),
        ('10_guard_side','GUARD / SIDE',(ax+2,0,-0.17),(ax,0,-0.17),0.47,(1100,1750),False,
         'Core 12 mm | rail stack 17.2 mm | shoulder stack 24.4 mm'),
        ('11_tip_front','ROUNDED TIP / FRONT',(ax-0.10,-1,-0.775),(ax-0.10,0,-0.775),0.26,(1400,1700),False,
         'Swept blade with finite edge land and nominal 4 mm round nose'),
        ('12_tip_45','ROUNDED TIP / 45 DEGREE',(ax+0.395,-0.5,-0.59),(ax-0.105,0,-0.775),0.26,(1500,1700),False,
         'Rounded cap follows the local blade axis; not a sharpened cutting point'),
        ('13_grip','GRIP / THREE-QUARTER',(ax+0.35,-1,0.28),(ax,0,0.10),0.29,(1400,1700),False,
         'Ivory oval body / dark crossed seams / dark rounded pommel')
    ]
    for name,title,pos,target,scale,size,pair,note in views:
        col_b.hide_render=not pair
        render_view(scene,name,title,pos,target,scale,size,note)
    col_b.hide_render=True
    captions.hide_render=True
    scene.render.engine='BLENDER_WORKBENCH'
    scene.display.shading.light='FLAT'
    scene.display.shading.color_type='SINGLE'
    scene.display.shading.single_color=(0,0,0)
    scene.display.shading.background_type='WORLD'
    scene.display.shading.show_shadows=False
    scene.display.shading.show_cavity=False
    scene.display.shading.show_specular_highlight=False
    scene.world.color=(1,1,1)
    scene.view_settings.view_transform='Standard'
    scene.view_settings.exposure=0
    render_view(scene,'14_outline_mask','OUTLINE',(ax,-3,-0.33),(ax,0,-0.33),1.22,(900,1800),'')

    # Separate native scene: ONLY the actual paired guard frames, no intersecting full swords.
    proof_collection=bpy.data.collections['PAIR_PROOF | two actual guards / closed circle']
    scene.collection.children.unlink(proof_collection)
    proof=bpy.data.scenes.new('Guard closure | actual mesh pair | diameter 350 mm')
    proof.collection.children.link(proof_collection)
    proof.collection.children.link(studio)
    proof.collection.children.link(captions)
    proof_collection.hide_render=False
    proof_collection.hide_viewport=False
    proof.world=scene.world.copy()
    proof.world.color=(0.07,0.085,0.105)
    proof.render.engine='BLENDER_WORKBENCH'
    proof.display.shading.light='STUDIO'
    proof.display.shading.color_type='OBJECT'
    proof.display.shading.background_type='WORLD'
    proof.display.shading.show_shadows=False
    proof.display.shading.show_cavity=True
    proof.display.shading.cavity_type='BOTH'
    proof.display.shading.show_specular_highlight=True
    proof.view_settings.view_transform='Standard'
    proof.view_settings.exposure=0
    bpy.context.window.scene=proof
    captions.hide_render=False
    render_view(proof,'15_guard_circle_front','TWO GUARDS / ONE CIRCLE',(0,-2,0),(0,0,0),0.46,(1750,1750),
                'Actual A/B guard meshes | diameter 350 mm | complementary half-planes | no proxy rings')
    render_view(proof,'16_guard_circle_45','CIRCLE CLOSURE / 45 DEGREE',(1,-1,0.35),(0,0,0),0.48,(1750,1750),
                'Same thickness plane; diameter beams abut instead of occupying the same volume')
    beta=math.radians(cfg['diameter_to_blade_angle_deg'])
    tip=(-cfg['guard_outer_radius_mm']*math.sin(beta)/1000,0,
          cfg['guard_outer_radius_mm']*math.cos(beta)/1000)
    render_view(proof,'17_guard_circle_seam','DIAMETER END / JOINT CHECK',(tip[0],-1,tip[2]),tip,0.105,(1500,1500),
                'Rounded seam edges; guard-frame test only, not a whole-sword locking mechanism')
    proof.camera=cameras['15_guard_circle_front']
    captions.hide_render=True
    bpy.context.window.scene=scene
    scene.render.engine='CYCLES'
    scene.view_settings.view_transform='AgX'
    scene.view_settings.exposure=-0.45
    scene.world.color=(0.11,0.13,0.16)
    col_b.hide_render=False
    scene.camera=cameras['06_pair_45']
    scene.render.resolution_x=1600
    scene.render.resolution_y=1750
    scene.render.filepath=str(RENDERS/'06_pair_45.png')
    (OUT/'render_views.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'lappland_original_pair.blend'))
    for backup in OUT.glob('*.blend1'):
        backup.unlink()
    required=[OUT/'lappland_original_pair.blend',OUT/'lappland_original_pair.glb',
              OUT/'lappland_sword_A_mm.stl',OUT/'lappland_sword_B_mm.stl',OUT/'lappland_pair_mm.stl',
              OUT/'lappland_guard_circle_proof.glb']
    assert all(p.exists() and p.stat().st_size>1000 for p in required)
    assert len(list(RENDERS.glob('*.png')))>=17
    checksums=[]
    for path in required+sorted(RENDERS.glob('*.png')):
        h=hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda:stream.read(1048576),b''):
                h.update(chunk)
        checksums.append(h.hexdigest()+'  '+str(path.relative_to(ROOT)))
    (OUT/'SHA256SUMS.txt').write_text('\n'.join(checksums)+'\n',encoding='utf-8')
    print('LAPPLAND_RENDER_COMPLETE: 17 actual inspection renders, two Blender scenes, model files and checksums')


if __name__=='__main__':
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(1)
