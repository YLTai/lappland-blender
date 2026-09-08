"""Clean-room original Lappland cosplay geometry; all builder arguments are mm."""
import bpy
import bmesh
import math
import json
import struct
import shutil
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parent
ASSETS = []
COL = None
MATS = {}
S = 0.001


def material(name, rgb, metallic=0.0, roughness=0.4):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*rgb, 1)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*rgb, 1)
    p.inputs['Metallic'].default_value = metallic
    p.inputs['Roughness'].default_value = roughness
    return m


def mesh(name, vertices, faces, material_names=('frame',), indices=None, bevel=0.0):
    data = bpy.data.meshes.new(name)
    data.from_pydata([(x*S, y*S, z*S) for x, y, z in vertices], [], faces)
    data.update()
    bm = bmesh.new()
    bm.from_mesh(data)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(data)
    bm.free()
    ob = bpy.data.objects.new(name, data)
    COL.objects.link(ob)
    for key in material_names:
        data.materials.append(MATS[key])
    if indices is not None:
        for p, i in zip(data.polygons, indices):
            p.material_index = i
    if bevel > 0:
        mod = ob.modifiers.new('Soft prop edges', 'BEVEL')
        mod.width = bevel*S
        mod.segments = 3
        mod.limit_method = 'ANGLE'
        mod.angle_limit = 0.35
        mod.harden_normals = True
        norm = ob.modifiers.new('Face normals', 'WEIGHTED_NORMAL')
        norm.keep_sharp = True
        norm.weight = 30
    ASSETS.append(ob)
    return ob


def strip(name, outside, inside, depth, y=0.0, mat='frame', bevel=0.5):
    assert len(outside) == len(inside)
    verts = []
    for a, b in zip(outside, inside):
        verts.extend([(a[0], y-depth/2, a[1]), (b[0], y-depth/2, b[1]),
                      (b[0], y+depth/2, b[1]), (a[0], y+depth/2, a[1])])
    faces = [(3, 2, 1, 0)]
    for i in range(len(outside)-1):
        for j in range(4):
            a, b = 4*i+j, 4*i+(j+1)%4
            faces.append((a, b, b+4, a+4))
    k = 4*(len(outside)-1)
    faces.append(tuple(k+j for j in range(4)))
    return mesh(name, verts, faces, (mat,), bevel=bevel)


def box(name, center, size, mat='frame', bevel=0.6):
    x, y, z = center
    a, b, c = (v/2 for v in size)
    verts = [(x+sx*a,y+sy*b,z+sz*c) for sx,sy,sz in
             [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),
              (-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
    faces = [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    return mesh(name, verts, faces, (mat,), bevel=bevel)


def cubic(cp, t):
    return tuple((1-t)**3*cp[0][i]+3*t*(1-t)**2*cp[1][i]+
                 3*t*t*(1-t)*cp[2][i]+t**3*cp[3][i] for i in range(2))


def interpolate(a, b, t):
    return tuple(x*(1-t)+y*t for x, y in zip(a, b))


def trace_to_mm(p, cfg):
    dx, dy = p[0]-624.0, p[1]-253.0
    scale = cfg['reference_mm_per_pixel']
    return ((dx*0.879291967+dy*0.476283149)*scale,
            -(-dx*0.476283149+dy*0.879291967)*scale)


def catmull(points, steps=16):
    result = []
    for i in range(len(points)-1):
        p0, p1 = points[max(0,i-1)], points[i]
        p2, p3 = points[i+1], points[min(len(points)-1,i+2)]
        for j in range(steps):
            t = j/steps
            result.append(tuple(0.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+
                                    (-a+3*b-3*c+d)*t*t*t)
                                for a,b,c,d in zip(p0,p1,p2,p3)))
    result.append(tuple(points[-1]))
    return result


def blade(cfg):
    pts = catmull(cfg['blade_stations_mm'], 18)
    verts, faces, mats, tangents = [], [], [], []
    face_mats = [1,0,2,2,2,0,1,1]
    for i, (x,z,w) in enumerate(pts):
        a, b = pts[max(0,i-1)], pts[min(len(pts)-1,i+1)]
        tangent = Vector((b[0]-a[0], b[1]-a[1])).normalized()
        normal = Vector((1.0, 0.0)) if cfg.get('section_plane_x', False) else Vector((-tangent.y, tangent.x))
        tangents.append(tangent)
        progress = max(0.0, min(1.0, (-z-12)/(abs(pts[-1][1])-12)))
        thickness = cfg['blade_thickness_mm']*(1-0.32*progress**3)
        root_blend = max(0.0, min(1.0, (185+z)/30))
        thickness += cfg.get('ricasso_extra_thickness_mm', 0.0)*root_blend
        broad_end = 0.40-(0.40-cfg.get('ricasso_broad_end',0.40))*root_blend
        edge_end = -0.5+cfg.get('edge_bevel_fraction',0.25)
        edge, spine = cfg['blunt_edge_mm'], cfg['spine_land_mm']
        profile = [(-0.5,-edge/2),(edge_end,-thickness/2),(broad_end,-thickness/2),
                   (0.5,-spine/2),(0.5,spine/2),(broad_end,thickness/2),
                   (edge_end,thickness/2),(-0.5,edge/2)]
        w = max(2*cfg['tip_radius_mm'], w)
        for u,y in profile:
            verts.append((x+normal.x*u*w, y, z+normal.y*u*w))
    faces.append(tuple(reversed(range(8))))
    mats.append(2)
    for i in range(len(pts)-1):
        for j in range(8):
            faces.append((i*8+j,i*8+(j+1)%8,(i+1)*8+(j+1)%8,(i+1)*8+j))
            mats.append(face_mats[j])
    center = Vector((pts[-1][0], pts[-1][1]))
    tangent = tangents[-1]
    last_ring = verts[-8:]
    ring_start = len(verts)-8
    for k in range(1,9):
        angle = (math.pi/2)*k/9
        c = center+tangent*cfg['tip_radius_mm']*math.sin(angle)
        shrink = math.cos(angle)
        new_start = len(verts)
        for vx,vy,vz in last_ring:
            delta = Vector((vx,vz))-center
            verts.append((c.x+delta.x*shrink,vy*shrink,c.y+delta.y*shrink))
        for j in range(8):
            faces.append((ring_start+j,ring_start+(j+1)%8,new_start+(j+1)%8,new_start+j))
            mats.append(face_mats[j])
        ring_start = new_start
    tip = center+tangent*cfg['tip_radius_mm']
    tip_index = len(verts)
    verts.append((tip.x,0,tip.y))
    for j in range(8):
        faces.append((ring_start+j,ring_start+(j+1)%8,tip_index))
        mats.append(face_mats[j])
    return mesh('Blade | curved broad flat and blunt land', verts, faces,
                ('blade','silver','spine'), mats, bevel=0.45)


def guard(cfg):
    raw_o, raw_i = [], []
    for outer, inner in zip(cfg['guard_outer_beziers_px'],cfg['guard_inner_beziers_px']):
        for j in range(65):
            if raw_o and j == 0:
                continue
            raw_o.append(cubic(outer,j/64))
            raw_i.append(cubic(inner,j/64))
    out, ins = [trace_to_mm(p,cfg) for p in raw_o], [trace_to_mm(p,cfg) for p in raw_i]
    depth, lift = cfg['guard_core_depth_mm'], cfg['guard_rail_lift_mm']
    strip('Guard | continuous D arc core',out,ins,depth,mat='frame',bevel=0.65)
    chord_o, chord_i = [out[0],out[-1]], [ins[0],ins[-1]]
    strip('Guard | skewed straight chord',chord_o,chord_i,depth,mat='frame',bevel=0.65)
    for side in (-1,1):
        y = side*(depth/2+lift/2-0.25)
        for label,lo,hi,mat in [('outer lip',0.02,0.24,'silver'),('inner lip',0.78,0.98,'rim')]:
            a = [interpolate(o,i,lo) for o,i in zip(out,ins)]
            b = [interpolate(o,i,hi) for o,i in zip(out,ins)]
            strip(f'Guard | {label} | face {side}',a,b,lift,y,mat,0.35)
            a = [interpolate(o,i,lo) for o,i in zip(chord_o,chord_i)]
            b = [interpolate(o,i,hi) for o,i in zip(chord_o,chord_i)]
            strip(f'Chord | {label} | face {side}',a,b,lift,y,mat,0.35)
        end = int(len(out)*cfg['shoulder_arc_fraction'])
        cap_o = [interpolate(o,i,-0.055) for o,i in zip(out[:end],ins[:end])]
        cap_i = [interpolate(o,i,1.055) for o,i in zip(out[:end],ins[:end])]
        strip(f'Guard | raised shoulder clamp | face {side}',cap_o,cap_i,
              3.8,side*(depth/2+lift+1.25),'silver',0.65)
        for frac in (0.055,0.94):
            po = interpolate(chord_o[0],chord_o[1],frac)
            pi = interpolate(chord_i[0],chord_i[1],frac)
            p = interpolate(po,pi,0.15)
            pin(f'Chord | captive rounded pin {side} {frac}',
                (p[0],side*(depth/2+lift+0.05),p[1]),2.1,1.6,'spine')
    return out, ins


def pin(name,center,radius,depth,mat):
    x,y,z = center
    n, verts = 20, []
    for yy in (y-depth/2,y+depth/2):
        for j in range(n):
            a=2*math.pi*j/n
            verts.append((x+radius*math.cos(a),yy,z+radius*math.sin(a)))
    faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]
    faces += [(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
    return mesh(name,verts,faces,(mat,),bevel=0.3)


def oval_loft(name,sections,mat,bevel=0.4):
    n, verts = 48, []
    for z,rx,ry in sections:
        for j in range(n):
            a=2*math.pi*j/n
            verts.append((rx*math.cos(a),ry*math.sin(a),z))
    faces=[tuple(reversed(range(n)))]
    for k in range(len(sections)-1):
        faces.extend([(k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j) for j in range(n)])
    faces.append(tuple((len(sections)-1)*n+j for j in range(n)))
    return mesh(name,verts,faces,(mat,),bevel=bevel)


def grip(cfg):
    end = cfg['grip_end_mm']
    oval_loft('Grip | oval charcoal underwrap',[(0,13.5,10.8),(18,14,11.1),
              (end*0.5,13.4,10.7),(end-10,11.4,9.5),(end,11.1,9.3)],'leather')
    pitch, width = cfg['wrap_pitch_mm'],cfg['wrap_width_mm']
    for direction in (-1,1):
        verts=[]
        z0,z1=11,end-6
        count=int((z1-z0)/pitch*96)
        for i in range(count+1):
            z=z0+(z1-z0)*i/count
            angle=direction*2*math.pi*(z-z0)/pitch + (math.pi if direction < 0 else 0.0)
            taper=z/end
            rx, ry = 14.0-2.7*taper*taper, 11.1-1.7*taper*taper
            lift=0.7+0.22*direction*math.cos(2*angle)
            for dz,dr in [(-width/2,-0.85),(width/2,-0.85),(width/2,lift),(-width/2,lift)]:
                verts.append(((rx+dr)*math.cos(angle),(ry+dr)*math.sin(angle),z+dz))
        faces=[(3,2,1,0)]
        for i in range(count):
            for j in range(4):
                faces.append((4*i+j,4*i+(j+1)%4,4*(i+1)+(j+1)%4,4*(i+1)+j))
        faces.append(tuple(4*count+j for j in range(4)))
        mesh(f'Grip | ivory crossed ribbon {direction}',verts,faces,('wrap',),bevel=0.16)
    oval_loft('Grip | root ferrule',[(-4,15.1,12.4),(8,15.1,12.4),(10,14,11.5)],'spine',0.7)
    oval_loft('Grip | rounded pommel cap',[(end-3,12,10),(end+5,12,10),(end+8,9.5,8)],'silver',0.8)
    verts=[]
    rings,sides=48,10
    for j in range(rings):
        a=2*math.pi*j/rings
        center=Vector((12+5*math.cos(a),0,end+0.5+7*math.sin(a)))
        normal=Vector((math.cos(a),0,math.sin(a))).normalized()
        for k in range(sides):
            b=2*math.pi*k/sides
            v=center+normal*(1.6*math.cos(b))+Vector((0,1.6*math.sin(b),0))
            verts.append(tuple(v))
    faces=[(j*sides+k,j*sides+(k+1)%sides,((j+1)%rings)*sides+(k+1)%sides,((j+1)%rings)*sides+k)
           for j in range(rings) for k in range(sides)]
    mesh('Pommel | closed lanyard lug',verts,faces,('spine',))
    box('Blade root | rounded collar',(2,0,-9),(30,27,25),'spine',1.3)
    for side in (-1,1):
        box(f'Blade root | shoulder pad {side}',(3,side*14,-13),(23,3.6,19),'silver',0.8)


def components_of(bm):
    unseen = set(bm.verts)
    groups = []
    while unseen:
        seed = unseen.pop()
        group, todo = {seed}, [seed]
        while todo:
            current = todo.pop()
            for edge in current.link_edges:
                other = edge.other_vert(current)
                if other in unseen:
                    unseen.remove(other)
                    group.add(other)
                    todo.append(other)
        groups.append(group)
    return sorted(groups,key=len,reverse=True)


def solid_union(cfg, output):
    bpy.context.view_layer.update()
    dg=bpy.context.evaluated_depsgraph_get()
    temp=[]
    for original in ASSETS:
        data=bpy.data.meshes.new_from_object(original.evaluated_get(dg),depsgraph=dg)
        ob=bpy.data.objects.new('Temporary union part',data)
        bpy.context.scene.collection.objects.link(ob)
        temp.append(ob)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in temp:
        ob.select_set(True)
    bpy.context.view_layer.objects.active=temp[0]
    bpy.ops.object.join()
    ob=bpy.context.object
    ob.name='EXPORT | prop master union'
    mod=ob.modifiers.new('Closed prop union at specified tolerance','REMESH')
    mod.mode='VOXEL'
    mod.voxel_size=cfg['stl_voxel_mm']*S
    mod.use_smooth_shade=False
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bm=bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    groups=components_of(bm)
    component_report=[]
    for group in groups:
        bounds=[[min(v.co[i] for v in group)*1000,max(v.co[i] for v in group)*1000] for i in range(3)]
        component_report.append({'vertices':len(group),'bounds_xyz_mm':bounds})
    print('UNION_COMPONENT_REPORT '+json.dumps(component_report))
    (output/'union_diagnostics.json').write_text(json.dumps(component_report,indent=2),encoding='utf-8')
    removed=0
    if cfg.get('remove_subvoxel_islands',False):
        for group in groups[1:]:
            extent=max(max(v.co[i] for v in group)-min(v.co[i] for v in group) for i in range(3))
            if extent <= cfg['stl_voxel_mm']*S*2.1:
                bmesh.ops.delete(bm,geom=list(group),context='VERTS')
                removed+=1
        groups=components_of(bm)
    nonmanifold=sum(not e.is_manifold for e in bm.edges)
    volume=abs(bm.calc_volume(signed=True))*1e9
    bm.to_mesh(ob.data)
    bm.free()
    valid=nonmanifold==0 and len(groups)==1
    if not valid and cfg.get('strict_validation',True):
        raise RuntimeError(f'STL union failed: {nonmanifold} nonmanifold edges; {len(groups)} components')
    ob.data.calc_loop_triangles()
    triangles=list(ob.data.loop_triangles)
    def write_stl(path,offsets):
        with path.open('wb') as stream:
            stream.write(b'Lappland ORIGINAL | BLUNT COSPLAY REFERENCE | units mm'.ljust(80,b' '))
            stream.write(struct.pack('<I',len(triangles)*len(offsets)))
            for dx in offsets:
                for tri in triangles:
                    coords=[]
                    for index in tri.vertices:
                        p=ob.data.vertices[index].co
                        coords.extend((p.x*1000+dx,p.y*1000,p.z*1000))
                    stream.write(struct.pack('<12fH',*tri.normal,*coords,0))
    write_stl(output/'lappland_sword_A_mm.stl',[0])
    write_stl(output/'lappland_sword_B_mm.stl',[0])
    write_stl(output/'lappland_pair_mm.stl',[-220,220])
    coords=[v.co*1000 for v in ob.data.vertices]
    bounds=[[min(v[i] for v in coords),max(v[i] for v in coords)] for i in range(3)]
    stats={'units':'mm','validation_passed':valid,'nonmanifold_edges':nonmanifold,
           'connected_components_per_sword':len(groups),'removed_subvoxel_islands':removed,
           'triangles_per_sword':len(triangles),'volume_mm3':volume,'bounds_xyz_mm':bounds,
           'dimensions_xyz_mm':[b-a for a,b in bounds],'stl_union_voxel_mm':cfg['stl_voxel_mm'],
           'pair_relation':'Two copies of one master, not a newly mirrored or short-sword design.'}
    hidden=bpy.data.collections.new('EXPORT_SOLIDS | hidden / millimetre STL source')
    bpy.context.scene.collection.children.link(hidden)
    for collection in list(ob.users_collection):
        collection.objects.unlink(ob)
    hidden.objects.link(ob)
    hidden.hide_render=True
    hidden.hide_viewport=True
    ob.hide_render=True
    return stats


def build(cfg):
    global COL
    ASSETS.clear()
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    scene=bpy.context.scene
    scene.unit_settings.system='METRIC'
    scene.unit_settings.length_unit='MILLIMETERS'
    scene.unit_settings.scale_length=1.0
    scene['design_scope']='Original five-star Lappland / E2 / The Young Fang only'
    scene['revision']=cfg['revision']
    scene['safety']='Blunt main edge land and rounded tip; not an impact-safe certification.'
    for name,rgb,metal,rough in [
        ('frame',(0.026,0.032,0.042),0.40,0.38),('rim',(0.13,0.16,0.20),0.60,0.33),
        ('blade',(0.25,0.29,0.34),0.72,0.28),('silver',(0.57,0.62,0.68),0.78,0.27),
        ('spine',(0.012,0.016,0.022),0.30,0.40),('leather',(0.008,0.010,0.015),0.0,0.72),
        ('wrap',(0.69,0.69,0.65),0.0,0.76)]:
        MATS[name]=material(name,rgb,metal,rough)
    COL=bpy.data.collections.new('SWORD_A | original master')
    scene.collection.children.link(COL)
    blade(cfg)
    outline,inner=guard(cfg)
    grip(cfg)
    output=ROOT/'output'
    output.mkdir(exist_ok=True)
    stats=solid_union(cfg,output)
    root_a=bpy.data.objects.new('Sword_A',None)
    COL.objects.link(root_a)
    for ob in ASSETS:
        ob.parent=root_a
    root_a.location.x=-0.22
    col_b=bpy.data.collections.new('SWORD_B | same design / shared meshes')
    scene.collection.children.link(col_b)
    root_b=bpy.data.objects.new('Sword_B',None)
    col_b.objects.link(root_b)
    root_b.location.x=0.22
    objects_b=[]
    for original in ASSETS:
        copy=original.copy()
        copy.data=original.data
        copy.name=original.name+' | B'
        col_b.objects.link(copy)
        copy.parent=root_b
        objects_b.append(copy)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in ASSETS+objects_b:
        ob.select_set(True)
    bpy.context.view_layer.objects.active=ASSETS[0]
    bpy.ops.export_scene.gltf(filepath=str(output/'lappland_original_pair.glb'),
        export_format='GLB',use_selection=True,export_apply=True,export_yup=True)
    stats.update({'revision':cfg['revision'],'nominal_handle_including_pommel_mm':cfg['grip_end_mm']+8,
        'blade_main_max_section_mm':cfg['blade_thickness_mm'],
        'ricasso_nominal_max_section_mm':cfg['blade_thickness_mm']+cfg.get('ricasso_extra_thickness_mm',0),
        'nominal_blunt_main_edge_land_mm':cfg['blunt_edge_mm'],
        'tip_plan_radius_mm':cfg['tip_radius_mm'],'guard_core_depth_mm':cfg['guard_core_depth_mm']})
    stats['reference_limitations']=[
        'No dimensioned official orthographic blueprint was supplied; life-size scale is an explicit reconstruction choice.',
        'Guard depth, reverse-face channels, clamp stack and small cap details are inferred from concept layering and APEX oblique views.',
        'Both swords use one geometric master. Dark/light illustration areas are not treated as alternate forms.',
        'The long carrying strap and module-background debris/effects are not part of the rigid sword geometry.',
        'The STL union is resampled at the recorded voxel tolerance; BLEND retains the individual original surfaces.'
    ]
    (output/'model_manifest.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
    (output/'design_parameters.json').write_text(json.dumps(cfg,indent=2),encoding='utf-8')
    (output/'reference_profile.json').write_text(json.dumps({'outer_xz_mm':outline,'inner_xz_mm':inner},indent=2),encoding='utf-8')
    (output/'README.txt').write_text(
        'LAPPLAND / ORIGINAL FIVE-STAR / BLUNT COSPLAY REFERENCE\n\n'
        'Editable components: lappland_original_pair.blend. GLB uses metres; STL numbers use millimetres.\n'
        'A and B are the same full-size master. The pair STL contains two copies.\n'
        'Check model_manifest.json for measured bounds and validation_passed before fabrication.\n'
        'A visible broad bevel is aesthetic and terminates in a blunt land. Do not sharpen or make a metal weapon.\n'
        'Choose lightweight compliant materials, cover the tip, and obtain venue approval. A rigid print can still injure.\n'
        'No official engineering dimensions or hidden mechanisms are claimed. Parameters and assumptions are supplied.\n',encoding='utf-8')
    sources=output/'source'
    sources.mkdir(exist_ok=True)
    for filename in ('model.py','render.py','lappland_geometry.py','REFERENCE_NOTES.md','ITERATIONS.md'):
        if (ROOT/filename).exists():
            shutil.copy2(ROOT/filename,sources/filename)
    bpy.ops.wm.save_as_mainfile(filepath=str(output/'lappland_original_pair.blend'))
    print('LAPPLAND_VALIDATION '+json.dumps(stats))
