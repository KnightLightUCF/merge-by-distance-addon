import bpy
import bmesh


#Bster's Functions

def merge_vertices_with_distance(obj_name, merge_distance):
    obj = bpy.data.objects[obj_name]
    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    bpy.ops.mesh.remove_doubles(threshold=merge_distance)

    bpy.ops.object.mode_set(mode='OBJECT')

def calculate_vertex_count_with_merge_distance(obj_name, merge_distance):
    obj = bpy.data.objects[obj_name]

    # Create a copy of the mesh
    mesh = obj.data.copy()
    bm = bmesh.new()
    bm.from_mesh(mesh)

    # Merge vertices using the specified merge distance
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=merge_distance)

    # Calculate the resulting vertex count
    vertex_count = len(bm.verts)
    
    bm.free()
    return vertex_count

def guess_number(desired_number):
    lower_bound = 0.001
    upper_bound = 10
    guess = 0
    guess_count = 0

    while guess_count < 200:  # Maximum of 20 guesses
        guess = (lower_bound + upper_bound) / 2
        guess = round(guess, 3)  # Round guess to 3 decimal places
        guess_count += 1

        vertex_count = calculate_vertex_count_with_merge_distance(object_name, guess)
        if vertex_count == desired_number:
            return {"guess": guess, "guesses": guess_count, "vertices": vertex_count, "result": "exact"}
        elif vertex_count > desired_number:
            lower_bound = guess + 0.001
        elif vertex_count <= desired_number and vertex_count >= (desired_number - 2):
            return {"guess": guess, "guesses": guess_count, "vertices": vertex_count, "result": "close enough"}
        else:
            upper_bound = guess - 0.001

    return {"guess": guess, "guesses": guess_count, "vertices": vertex_count, "result": "not found"}


#Michael's Functions




####---------- MAIN ------------####

#Michael's Code - User Interface

    #Creating AutoMerge Operator
class MESH_OT_automerge_dist(bpy.types.Operator):
    """Automates the Merge-by-Distance process"""
    bl_idname = 'mesh.automerge_dist'
    bl_label = "AutoMergeByDist"
    bl_options = {'REGISTER','UNDO'}

    #Checks that the correct area is selected, Allows operator to be detectable
    @classmethod
    def poll(cls,context):
        return context.area.type == 'VIEW_3D'

        #code which is run when operator is called
    def execute(self, context):
        #Bster's Code - Script
        object_name = "ROCKET-V1"  # Replace with your object name
        desired_number = 300
        result = guess_number(desired_number)

        if result["result"] == "close enough":
             merge_vertices_with_distance(object_name, result["guess"])

        message = "Resulting Vertex Count: {}".format(result)
        bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text=message), title="Vertex Count", icon='INFO')

        

    #creating AutoMerge Panel Button
    class VIEW3D_PT_automerge_dist(bpy.types.Panel):
        bl_space_type = 'View 3D'
        bl_region_type = 'UI'
        bl_category = "AutoMergeDist"
        bl_label = "Select Object"
        
        #Necessary for button to visually exist
        def draw(self, context):
            self.layout.operator()

def register():
    bpy.utils.register_class(MESH_OT_automerge_dist)
   # bpy.utils.register_class(VIEW3D_PT_automerge_dist)
def unregister():
    bpy.utils.unregister_class(MESH_OT_automerge_dist)   
   # bpy.utils.unregister_class(VIEW3D_PT_automerge_dist) 

if __name__ == '__main__':
    register()