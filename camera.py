import bpy
import math

def rotate():
    # Get the active object
    obj = bpy.context.active_object

    # Get the object's mesh data
    mesh = obj.data

    # Get the object's global transformation matrix
    matrix = obj.matrix_world

    # Get the bounding box of the object's geometry in global space
    bbox = [matrix @ mathutils.Vector(b) for b in obj.bound_box]
    x_min = min(bbox, key=lambda v: v[0])[0]
    x_max = max(bbox, key=lambda v: v[0])[0]
    y_min = min(bbox, key=lambda v: v[1])[1]
    y_max = max(bbox, key=lambda v: v[1])[1]
    z_min = min(bbox, key=lambda v: v[2])[2]
    z_max = max(bbox, key=lambda v: v[2])[2]
    
    x_m = (x_min + x_max) / 2.0
    y_m = (y_min + y_max) / 2.0
    z_m = (z_min + z_max) / 2.0
    
    x_s = x_max - x_m
    y_s = y_max - y_m
    z_s = z_max - z_m
    
    scale = max(x_s, max(y_s, z_s))
    
    scale = math.sqrt(scale**2 * 3)
    
    print(scale)
    
    # Calculate the center of the bounding box
    center = mathutils.Vector((x_m, y_m, z_m))

    # Print the center coordinates
    print(center)
    
    bpy.context.scene.cursor.location = center
    
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    
    ortho_scale = scale * 2
    
    cam = bpy.data.cameras.new("OrthoCam")
    cam_ob = bpy.data.objects.new("OrthoCam", cam)

    # Set the camera type to orthographic and set the scale
    cam.type = 'ORTHO'
    cam.ortho_scale = ortho_scale

    # Add the camera to the scene and make it the active camera
    bpy.context.scene.collection.objects.link(cam_ob)
    bpy.context.scene.camera = cam_ob

    # Add a "Track To" constraint to the camera
    track_to = cam_ob.constraints.new('TRACK_TO')
    track_to.target = bpy.context.active_object
    

    # Create a new mesh data for the UV sphere
    mesh = bpy.data.meshes.new("UV Sphere")

    # Set the radius of the sphere
    sphere_radius = 1

    # Create the UV sphere
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=4, radius=sphere_radius * scale)
    bm.to_mesh(mesh)
    bm.free()
    
    verts = [v.co + center for v in mesh.vertices]
    
    def angle_to_y(v):
        return v[2]
    
    verts.sort(key=angle_to_y)
    
    verts_count = len(verts)
    
    for i in range(verts_count):
        for j in range(verts_count - 1):
            if verts[j][2] == verts[j+1][2]:
                vec1 = verts[j] - center
                vec1.z = 0
                vec1.normalize()
                vec2 = verts[j+1] - center
                vec2.z = 0
                vec2.normalize()
                if vec1.angle((0,1,0)) < vec2.angle((0,1,0)):
                    verts[j], verts[j+1] = verts[j+1], verts[j]
    
    
    verts.reverse()         
    
    for i in range(verts_count):
        cam_ob.location = verts[i]
        print(verts[i])