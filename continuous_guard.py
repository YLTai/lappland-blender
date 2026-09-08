"""One-piece D-section guard bodies with continuous, non-overlapping rails.

A D contour is an exact circular arc clipped by a straight half-plane.
Nested D contours describe a frame with a hole. Extruding that frame creates
one closed solid containing both the half-annulus and diameter beam. There
are no coplanar arc/beam faces and no Boolean or render-offset workaround.
"""
import math
from mathutils import Vector
import lappland_geometry as G
from semantic_geometry import basis


def continuous_guard(cfg):
    center,d,n=basis(cfg)
    R=cfg['guard_outer_radius_mm']
    ri=R-cfg['guard_radial_width_mm']
    width=cfg['diameter_beam_width_mm']
    depth=cfg['guard_core_depth_mm']
    lift=cfg['guard_rail_lift_mm']
    count=180

    def point(u,v):
        return tuple(center+d*u+n*v)

    def d_contour(radius,cut):
        assert 0<=cut<radius
        start=math.asin(cut/radius)
        stop=math.pi-start
        return [point(-radius*math.cos(start+(stop-start)*i/count),
                       radius*math.sin(start+(stop-start)*i/count)) for i in range(count+1)]

    def frame(name,ro,co,rin,cin,thick,y,mat):
        assert ro>rin and cin>co
        outside=d_contour(ro,co)
        inside=d_contour(rin,cin)
        vertices=[]
        for a,b in zip(outside,inside):
            vertices.extend([(a[0],y-thick/2,a[1]),(b[0],y-thick/2,b[1]),
                             (b[0],y+thick/2,b[1]),(a[0],y+thick/2,a[1])])
        faces=[]
        # Close the final section to the first: this is the actual diameter beam,
        # not another overlapping box. The interior D loop remains a true hole.
        for i in range(len(outside)):
            k=(i+1)%len(outside)
            for j in range(4):
                faces.append((4*i+j,4*i+(j+1)%4,4*k+(j+1)%4,4*k+j))
        return G.mesh(name,vertices,faces,(mat,),bevel=0.55)

    def arc(radius,stop=math.pi):
        return [point(-radius*math.cos(stop*i/count),radius*math.sin(stop*i/count))
                for i in range(count+1)]

    def arc_plate(name,ro,rin,thick,y,mat,stop):
        return G.strip(name,arc(ro,stop),arc(rin,stop),thick,y,mat,0.55)

    frame('Guard | exact 180 degree annular core + diameter beam',R,0,ri,width,depth,0,'frame')
    top=depth/2+lift-0.4
    shoulder_stop=math.radians(cfg['shoulder_arc_deg'])
    for side in (-1,1):
        y=side*(depth/2+lift/2-0.4)
        # Two nested closed D-shaped rails. Their rings and straight portions
        # cannot cross: each is a single continuous boundary offset.
        frame(f'Guard | continuous outer D rail {side}',R,0,R-4,4,lift,y,'silver')
        frame(f'Guard | continuous inner D rail {side}',ri+4,width-4,ri,width,lift,y,'rim')
        floor_bottom=top-0.8
        floor_top=top+1.8
        cap_top=top+3.6
        arc_plate(f'Guard | shoulder recessed floor {side}',R,ri-3,
                  floor_top-floor_bottom,side*(floor_top+floor_bottom)/2,'frame',shoulder_stop)
        for label,ro,rin in [('outer shoulder lip',R,R-4),('inner shoulder plate',ri+9,ri-3)]:
            arc_plate(f'Guard | {label} {side}',ro,rin,cap_top-floor_top+0.6,
                      side*(cap_top+floor_top-0.6)/2,'silver',shoulder_stop)
        for k,u in enumerate((-R+22,R-22)):
            p=point(u,2.4)
            G.pin(f'Guard | captive diameter pin {side} {k}',
                  (p[0],side*(top+0.1),p[1]),1.65,1.6,'spine')
    cfg['guard_actual_shoulder_depth_mm']=2*(top+3.6)
    cfg['guard_actual_rail_depth_mm']=2*top
    cfg['same_layer_guard_joints']='single closed D-contour solids; no overlapping arc/beam faces'
    return arc(R),arc(ri)
