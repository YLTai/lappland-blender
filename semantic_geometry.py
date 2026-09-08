"""Analytic part grammar for the original Lappland props.

The guard is a concentric HALF annulus, not a traced projected ellipse.
All positions below are millimetres. The diameter beam occupies only its
own half-plane, so two real guard meshes can close into one circle without
overlapping beams. No pixel-coordinate silhouettes are used in this module.
"""
import math
import json
import bpy
from mathutils import Matrix, Vector
import lappland_geometry as G


def smoothstep(a, b, x):
    t=max(0.0,min(1.0,(x-a)/(b-a)))
    return t*t*(3-2*t)


def blade_sections(cfg):
    """A swept broad flat, wide root, shoulder transition and rounded nose.
    Sampling only tessellates these dimensional laws; samples are not a trace.
    """
    sections=[]
    for i in range(161):
        t=i/160
        z=-cfg['blade_neck_z_mm']-cfg['blade_body_span_mm']*t
        x=-(cfg['sweep_linear_mm']*t+cfg['sweep_quadratic_mm']*t*t+
            cfg['sweep_nose_mm']*t**16)
        base=cfg['blade_main_width_mm']
        root=(1-smoothstep(0.163,0.177,t))*smoothstep(0,0.022,t)
        width=base+(cfg['blade_root_width_mm']-base)*root
        # Root widens principally on the spine side; the opposite edge is continuous.
        x+=(width-base)*0.5
        taper=smoothstep(0.835,1.0,t)
        width=width*(1-taper)+2*cfg['tip_radius_mm']*taper
        sections.append([x,z,width])
    return sections


def basis(cfg):
    angle=math.radians(cfg['diameter_to_blade_angle_deg'])
    d=Vector((math.sin(angle),-math.cos(angle)))
    n=Vector((math.cos(angle),math.sin(angle)))
    return Vector(cfg['guard_center_xz_mm']),d,n


def analytic_guard(cfg):
    center,d,n=basis(cfg)
    radius=cfg['guard_outer_radius_mm']
    inner=radius-cfg['guard_radial_width_mm']
    depth=cfg['guard_core_depth_mm']
    lift=cfg['guard_rail_lift_mm']
    samples=180

    def point(u,v):
        return tuple(center+d*u+n*v)

    def arc(r,start=0.0,stop=math.pi,count=samples):
        return [point(-r*math.cos(start+(stop-start)*i/count),
                       r*math.sin(start+(stop-start)*i/count)) for i in range(count+1)]

    def arc_part(name,ro,ri,thick,y=0,mat='frame',stop=math.pi):
        return G.strip(name,arc(ro,stop=stop),arc(ri,stop=stop),thick,y,mat,0.55)

    def beam_part(name,lo,hi,thick,y=0,mat='frame'):
        # Disk clipped by 0 <= n <= beam_width. The end caps follow the SAME circle.
        vals=[lo+(hi-lo)*i/24 for i in range(25)]
        outer=[point(math.sqrt(radius*radius-v*v),v) for v in vals]
        inside=[point(-math.sqrt(radius*radius-v*v),v) for v in vals]
        return G.strip(name,outer,inside,thick,y,mat,0.55)

    arc_part('Guard | exact 180 degree annular core',radius,inner,depth)
    beam_part('Guard | half-plane diameter beam',0,cfg['diameter_beam_width_mm'],depth)
    top=depth/2+lift-0.4
    stop=math.radians(cfg['shoulder_arc_deg'])
    for side in (-1,1):
        y=side*(depth/2+lift/2-0.4)
        arc_part(f'Guard | concentric outer rail {side}',radius,radius-4,lift,y,'silver')
        arc_part(f'Guard | concentric inner rail {side}',inner+4,inner,lift,y,'rim')
        beam_part(f'Guard | diameter outer rail {side}',0,3.8,lift,y,'silver')
        w=cfg['diameter_beam_width_mm']
        beam_part(f'Guard | diameter inner rail {side}',w-3.8,w,lift,y,'rim')
        # Upper shoulder remains INSIDE the common radius. It cannot spoil circle closure.
        floor_bottom=top-0.8
        floor_top=top+1.8
        cap_top=top+3.6
        arc_part(f'Guard | shoulder recessed floor {side}',radius,inner-3,
                 floor_top-floor_bottom,side*(floor_top+floor_bottom)/2,'frame',stop)
        for label,ro,ri in [('outer shoulder lip',radius,radius-4),
                           ('inner shoulder plate',inner+9,inner-3)]:
            arc_part(f'Guard | {label} {side}',ro,ri,cap_top-floor_top+0.6,
                     side*(cap_top+floor_top-0.6)/2,'silver',stop)
        for k,u in enumerate((-radius+22,radius-22)):
            p=point(u,2.4)
            G.pin(f'Guard | captive diameter pin {side} {k}',
                  (p[0],side*(top+0.1),p[1]),1.65,1.6,'spine')
    cfg['guard_actual_shoulder_depth_mm']=2*(top+3.6)
    cfg['guard_actual_rail_depth_mm']=2*top
    return arc(radius),arc(inner)


def add_circle_proof(cfg, output):
    """Duplicate the ACTUAL guard components, not a substitute illustration.
    This verifies the two guard frames, not an invented whole-sword locking joint.
    """
    center,d,n=basis(cfg)
    scene=bpy.context.scene
    collection=bpy.data.collections.new('PAIR_PROOF | two actual guards / closed circle')
    scene.collection.children.link(collection)
    roots=[]
    source=[ob for ob in G.ASSETS if ob.name.startswith('Guard |')]
    assert source
    for half in (0,1):
        root=bpy.data.objects.new('Circle half '+('A' if half==0 else 'B'),None)
        collection.objects.link(root)
        matrix=Matrix.Identity(4) if half==0 else Matrix.Rotation(math.pi,4,'Y')
        matrix.translation=Vector((-center.x/1000,0,-center.y/1000)) if half==0 else Vector((center.x/1000,0,center.y/1000))
        root.matrix_world=matrix
        roots.append(root)
        for original in source:
            ob=original.copy()
            ob.data=original.data
            ob.name=('Proof A | ' if half==0 else 'Proof B | ')+original.name
            collection.objects.link(ob)
            ob.parent=root
            ob.matrix_basis=Matrix.Identity(4)
            ob.color=(0.18,0.42,0.68,1) if half==0 else (0.85,0.52,0.18,1)
            ob['source_component']=original.name
    bpy.context.view_layer.update()
    dg=bpy.context.evaluated_depsgraph_get()
    metrics=[]
    for half,root in enumerate(roots):
        vertices=[]
        for ob in root.children:
            ev=ob.evaluated_get(dg)
            data=ev.to_mesh()
            vertices.extend([ob.matrix_world@v.co*1000 for v in data.vertices])
            ev.to_mesh_clear()
        radial=[math.hypot(p.x,p.z) for p in vertices]
        signed=[p.x*n.x+p.z*n.y for p in vertices]
        intrusion=max(0,-min(signed)) if half==0 else max(0,max(signed))
        metrics.append({'half':'AB'[half],'evaluated_vertices':len(vertices),
                        'max_radius_mm':max(radial),'opposite_half_plane_intrusion_mm':intrusion})
        assert max(radial)<=cfg['guard_outer_radius_mm']+0.015,metrics
        assert intrusion<0.015,metrics
    R=cfg['guard_outer_radius_mm']
    endpoint_error=0.0
    for v in (-d*R,d*R):
        pa=Vector((center.x+v.x,0,center.y+v.y))/1000
        pb=Vector((center.x-v.x,0,center.y-v.y))/1000
        error=(roots[0].matrix_world@pa-roots[1].matrix_world@pb).length*1000
        endpoint_error=max(endpoint_error,error)
    assert endpoint_error<0.015
    report={'constraint':'two congruent concentric 180-degree guard frames close into one circle',
        'source':'the same meshes used on the delivered swords; no replacement proxy rings',
        'diameter_mm':2*R,'inner_diameter_mm':2*(R-cfg['guard_radial_width_mm']),
        'sweep_per_half_deg':180,'diameter_to_blade_angle_deg':cfg['diameter_to_blade_angle_deg'],
        'endpoint_coincidence_error_mm':endpoint_error,'evaluated_mesh_tests':metrics,
        'nonoverlap_basis':'A occupies n>=0 and B occupies n<=0; beams meet at the diameter boundary only.',
        'scope_limit':'Guard-frame geometry check. No magnet, latch or collision-free whole-sword assembly is claimed.',
        'passed':True}
    (output/'circle_pair_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    bpy.ops.object.select_all(action='DESELECT')
    for ob in collection.objects:
        ob.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(output/'lappland_guard_circle_proof.glb'),
        export_format='GLB',use_selection=True,export_apply=True,export_yup=True)
    collection.hide_render=True
    collection.hide_viewport=True
    return report
