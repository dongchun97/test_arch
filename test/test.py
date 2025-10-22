import bpy,bmesh


bm=bmesh.new()

circle_vert = bmesh.ops.create_circle(bm, segments=8, radius=1.0)["verts"][0]

circle_vert.co.z+=1

mesh=bpy.data.meshes.new("TestMesh")
bm.to_mesh(mesh)
bm.free()

obj=bpy.data.objects.new("TestObject",mesh)
bpy.context.collection.objects.link(obj)