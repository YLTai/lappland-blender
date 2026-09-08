"""Headless inspection renderer for original five-star Lappland props.
Run after model.py: blender -b --python render.py
"""
import bpy
import json
import hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'
RENDERS=ROOT/'renders'
RENDERS.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'lappland_original_pair.blend'))
scene=bpy.context.scene
scene.render.engine='CYCLES'
scene.cycles.device='CPU'
scene.cycles.samples=16
scene.cycles.use_denoising=True
scene.cycles.max_bounces=4
scene.cycles.diffuse_bounces=2
scene.cycles.glossy_bounces=2
scene.render.image_settings.file_format='PNG'
scene.render.image_settings.color_mode='RGBA'
scene.render.film_transparent=False
scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'
scene.view_settings.exposure=-0.45
scene.world.use_nodes=True
background=scene.world.node_tree.nodes.get('Background')
background.inputs['Color'].default_value=(0.11,0.13,0.16,1)
background.inputs['Strength'].default_value=0.65
studio=bpy.data.collections.new('STUDIO | cameras and lights only')
scene.collection.children.link(studio)
annotations=bpy.data.collections.new('STUDIO | screen captions')
scene.collection.children.link(annotations)


def area(name,location,target,energy,size):
    data=bpy.data.lights.new(name,'AREA')
    data.energy=energy
    data.shape='DISK'
    data.size=size
    ob=bpy.data.objects.new(name,data)
    studio.objects.link(ob)
    ob.location=location
    ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
    return ob


area('Key | large frontal softbox',(-1.4,-1.8,1.4),(0,0,-0.25),250,1.6)
area('Fill | blade planes',(1.1,-0.8,-0.25),(0,0,-0.3),120,1.4)
area('Rim | back rim',(0.5,1.2,0.8),(0,0,-0.25),320,1.1)
area('Lower fill',(-0.9,0.6,-1.0),(0,0,-0.5),100,0.9)
camera_data=bpy.data.cameras.new('Inspection Camera')
camera=bpy.data.objects.new('Inspection Camera',camera_data)
studio.objects.link(camera)
scene.camera=camera
camera_data.type='ORTHO'
camera_data.lens=65
camera_data.clip_start=0.01
camera_data.clip_end=30
caption_mat=bpy.data.materials.new('Caption | neutral white')
caption_mat.use_nodes=True
nodes=caption_mat.node_tree.nodes
nodes.clear()
em=nodes.new('ShaderNodeEmission')
em.inputs['Color'].default_value=(0.75,0.81,0.86,1)
em.inputs['Strength'].default_value=1.0
output=nodes.new('ShaderNodeOutputMaterial')
caption_mat.node_tree.links.new(em.outputs[0],output.inputs[0])


def text(name,body,loc,size):
    data=bpy.data.curves.new(name,'FONT')
    data.body=body
    data.size=size
    data.extrude=0
    ob=bpy.data.objects.new(name,data)
    annotations.objects.link(ob)
    data.materials.append(caption_mat)
    ob.parent=camera
    ob.location=loc
    return ob


header=text('Title','',(0,0,-0.3),0.02)
footer=text('Notes','',(0,0,-0.3),0.012)
col_b=bpy.data.collections['SWORD_B | same design / shared meshes']
AX=-0.22
views=[
    ('01_pair_front','PAIR / FRONT',(0,-3,-0.325),(0,0,-0.325),1.26,(1500,1750),True,
     'Original five-star Lappland | identical full-size masters | blunt cosplay reference'),
    ('02_front','A / FRONT ORTHOGRAPHIC',(AX,-3,-0.325),(AX,0,-0.325),1.23,(1000,1800),False,
     'Metres in BLEND / GLB | millimetres in STL | nominal overall length approximately 1067 mm'),
    ('03_back','A / BACK ORTHOGRAPHIC',(AX,3,-0.325),(AX,0,-0.325),1.23,(1000,1800),False,
     'Reverse-face channel and shoulder stack are inferred; silhouette follows the concept sheet'),
    ('04_side','A / RIGHT SIDE',(AX+3,0,-0.325),(AX,0,-0.325),1.23,(800,1800),False,
     'Main blade 8.5 mm | thicker ricasso | nominal blunt land 3.2 mm | guard core 12 mm'),
    ('05_top','A / TOP',(AX,0,3),(AX,0,-0.12),0.48,(1700,1000),False,
     'Top down the handle axis: guard layers, grip oval, root collar and blade thickness'),
    ('06_pair_45','PAIR / 45 DEGREE AZIMUTH',(2.0,-2.0,0.45),(0,0,-0.325),1.30,(1600,1750),True,
     'Same master in both hands; no alter or outfit-specific redesign'),
    ('07_guard_front','GUARD / FRONT',(AX+0.02,-2,-0.17),(AX+0.02,0,-0.17),0.43,(1550,1750),False,
     'Closed skewed D-profile | straight chord | grooved shoulder clamp | recessed perimeter channel'),
    ('08_guard_back','GUARD / BACK',(AX+0.02,2,-0.17),(AX+0.02,0,-0.17),0.43,(1550,1750),False,
     'Back-face relief is a restrained inference; no unsupported extra rings or quillons'),
    ('09_guard_45','GUARD / 45 DEGREE AZIMUTH',(AX+1.01,-1.0,0.18),(AX+0.01,0,-0.15),0.47,(1750,1750),False,
     'Raised lips, a recessed shoulder floor and a darker core are separate geometric levels'),
    ('10_guard_side','GUARD / SIDE',(AX+2,0,-0.15),(AX,0,-0.15),0.45,(1100,1750),False,
     'Core 12 mm | perimeter layers 17.5 mm | shoulder stack 24.3 mm | inferred depths'),
    ('11_tip_front','BLADE TIP / FRONT',(AX-0.10,-1,-0.76),(AX-0.10,0,-0.76),0.26,(1400,1700),False,
     'Final cap aligned to the local blade axis: nominal 4 mm plan radius, not a sharpened point'),
    ('12_tip_45','BLADE TIP / 45 DEGREE AZIMUTH',(AX+0.395,-0.5,-0.58),(AX-0.105,0,-0.76),0.26,(1500,1700),False,
     'Rounded cap and finite edge land; not designed for sharpening or metal fabrication'),
    ('13_grip','GRIP / THREE-QUARTER',(AX+0.35,-1,0.28),(AX,0,0.10),0.29,(1400,1700),False,
     'Ivory body / dark crossed seams, 2.2 mm wide | concept-sheet pattern | dark rounded pommel')
]
records=[]
for name,title,location,target,scale,size,pair,note in views:
    col_b.hide_render=not pair
    camera.location=location
    camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
    camera_data.ortho_scale=scale
    scene.render.resolution_x,scene.render.resolution_y=size
    aspect=size[0]/size[1]
    half_w=scale/2 if aspect>=1 else scale*aspect/2
    half_h=scale/(2*aspect) if aspect>=1 else scale/2
    header.data.body='LAPPLAND   /   '+title
    header.data.size=scale*0.017
    header.location=(-half_w+scale*0.032,half_h-scale*0.050,-0.3)
    footer.data.body=note
    footer.data.size=scale*0.0092
    footer.location=(-half_w+scale*0.032,-half_h+scale*0.026,-0.3)
    if len(note)*footer.data.size*0.55>half_w*1.87:
        footer.data.size=half_w*1.87/(len(note)*0.55)
    scene.render.filepath=str(RENDERS/(name+'.png'))
    bpy.context.view_layer.update()
    records.append({'file':name+'.png','camera_location':list(camera.location),
        'camera_rotation':list(camera.rotation_euler),'target':target,'ortho_scale':scale,'resolution':size})
    bpy.ops.render.render(write_still=True)

# Flat mask permits comparison without a material/lighting bias.
col_b.hide_render=True
annotations.hide_render=True
camera.location=(AX,-3,-0.325)
camera.rotation_euler=(Vector((AX,0,-0.325))-camera.location).to_track_quat('-Z','Y').to_euler()
camera_data.ortho_scale=1.18
scene.render.resolution_x=900
scene.render.resolution_y=1800
scene.render.engine='BLENDER_WORKBENCH'
scene.display.shading.light='FLAT'
scene.display.shading.color_type='SINGLE'
scene.display.shading.single_color=(0,0,0)
scene.display.shading.background_type='WORLD'
scene.world.color=(1,1,1)
scene.display.shading.show_shadows=False
scene.display.shading.show_cavity=False
scene.display.shading.show_specular_highlight=False
scene.view_settings.view_transform='Standard'
scene.view_settings.exposure=0
scene.render.filepath=str(RENDERS/'14_outline_mask.png')
bpy.ops.render.render(write_still=True)
bpy.context.view_layer.update()
anchors={}
for label,p in {'origin':[AX,0,0],'handle_end':[AX,0,0.21],
                'blade_tip_reference':[AX-0.13544,0,-0.85649]}.items():
    q=world_to_camera_view(scene,camera,Vector(p))
    anchors[label]=[q.x*900,(1-q.y)*1800]
(OUT/'render_views.json').write_text(json.dumps({'views':records,'mask_anchors_px':anchors},indent=2),encoding='utf-8')

scene.render.engine='CYCLES'
scene.view_settings.view_transform='AgX'
scene.view_settings.exposure=-0.45
col_b.hide_render=False
annotations.hide_render=True
camera.location=(2.0,-2.0,0.45)
camera.rotation_euler=(Vector((0,0,-0.325))-camera.location).to_track_quat('-Z','Y').to_euler()
camera_data.ortho_scale=1.30
scene.render.resolution_x=1600
scene.render.resolution_y=1750
scene.world.color=(0.11,0.13,0.16)
scene.render.filepath=str(RENDERS/'06_pair_45.png')
scene.render.image_settings.color_mode='RGBA'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'lappland_original_pair.blend'))
for backup in OUT.glob('*.blend1'):
    backup.unlink()
required=[OUT/'lappland_original_pair.blend',OUT/'lappland_original_pair.glb',
          OUT/'lappland_sword_A_mm.stl',OUT/'lappland_sword_B_mm.stl',OUT/'lappland_pair_mm.stl']
assert all(p.exists() and p.stat().st_size>1000 for p in required)
assert len(list(RENDERS.glob('*.png')))>=14
checksums=[]
for path in required+sorted(RENDERS.glob('*.png')):
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):
            digest.update(chunk)
    checksums.append(digest.hexdigest()+'  '+str(path.relative_to(ROOT)))
(OUT/'SHA256SUMS.txt').write_text('\n'.join(checksums)+'\n',encoding='utf-8')
print('LAPPLAND_RENDER_COMPLETE: 14 inspection PNGs, required formats and checksums')
