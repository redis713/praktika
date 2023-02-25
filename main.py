import bpy
from bpy.types import Operator, Panel, PropertyGroup
from bpy.utils import register_class, unregister_class
from bpy.props import IntProperty, BoolProperty, EnumProperty, PointerProperty


class Doppelganger(Operator):
    bl_idname = 'object.doppelganger'
    bl_label = 'Start'
    
    resolution = None
    samples = None
    gensave = None
    
    def structure(self, context):
        props = context.scene.doppelganger
        self.resolution = props.resolution
        self.samples = props.samples
        self.gensave = props.gensave


    def go(self):
        print(self.resolution)
        print(self.samples)


    def execute(self, context):
        self.structure(context)
        build_dg(context)
        #testbox()
        return {'FINISHED'}


class DoppelgangerProps(PropertyGroup):
    resolution : IntProperty(
        name = 'Resolution',
        default = 256,
        min = 8,
        max = 32,
        subtype = 'FACTOR'
    )
    samples : IntProperty(
        name = 'Samples',
        default = 8,
        min = 8,
        max = 32,
        subtype = 'FACTOR'
    )
    gensave : BoolProperty(
        name = 'Auto',
        default = True
    )
    quality: EnumProperty(
        items = [('0', '6 Views', "Render 6 different angles of the selected objects"), 
        ('1', '26 Views', "Render 26 different angles of the selected objects"), 
        ('2', '62 Views', "Render 62 different angles of the selected objects")],
        name = 'View count', 
        default = 1
    )
    
class OBJECT_PT_DoppelgangerPanel(Panel):
    bl_label = 'MyDoppelganger'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MyDoppelganger'
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.doppelganger
        col = layout.column()
        col.prop(props, 'resolution')
        col.prop(props, 'samples')
        col.prop(props, 'quality')
        col.prop(props, 'gensave')
        row = layout.row()
        row.operator('object.doppelganger')
        
 
 
 classes = [
    DoppelgangerProps,
    Doppelganger,
    OBJECT_PT_DoppelgangerPanel
]

def register():
    for cl in classes:
        register_class(cl)
    bpy.types.Scene.doppelganger = PointerProperty(type = DoppelgangerProps)

def unregister():
    for cl in reversed(classes):
        unregister_class(cl)
        
if __name__ == '__main__':
    register()