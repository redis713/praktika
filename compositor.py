import bpy
import os
import shutil


def set_compositor(path):
    context = bpy.context
    bops = bpy.ops
    
    names = ['albedo', 'normal', 'emit']
    paths = []
    for name in names:
        namePath = os.path.join(path, name)
        if os.path.exists(namePath):
            shutil.rmtree(namePath)
        os.mkdir(namePath)
        paths.append(namePath)
    
    tree = context.scene.node_tree
    print(paths)
    
    render_layers = tree.nodes.get('Render Layers', None)
    if render_layers is None:
        render_layers = tree.nodes.new('CompositorNodeRLayers')
    
    albedo = tree.nodes.new('CompositorNodeOutputFile')
    albedo.base_path = paths[0]
    
    set_alpha = tree.nodes.new('CompositorNodeSetAlpha')
    tree.links.new(render_layers.outputs['DiffCol'], set_alpha.inputs[0])
    tree.links.new(render_layers.outputs['Alpha'], set_alpha.inputs[1])
    tree.links.new(set_alpha.outputs['Image'], albedo.inputs[0])
    
    normal = tree.nodes.new('CompositorNodeOutputFile')
    normal.base_path = paths[1]
    
    mix = tree.nodes.new('CompositorNodeMixRGB')
    mix.inputs[0].default_value = 0.5
    mix.inputs[1].default_value[0] = 1.0
    mix.inputs[1].default_value[1] = 1.0
    mix.inputs[1].default_value[2] = 1.0
    
    tree.links.new(render_layers.outputs['Normal'], mix.inputs[1])
    
    math_1 = tree.nodes.new('CompositorNodeMath')
    math_1.operation = 'DIVIDE'
    math_1.use_clamp = True
    scale = scale * math.sqrt(1 / 3)
    math_1.inputs[1].default_value = scale * 2
    
    tree.links.new(render_layers.outputs['Depth'], math_1.inputs[0])

    
    set_alpha = tree.nodes.new('CompositorNodeSetAlpha')
        
    tree.links.new(mix.outputs['Image'], set_alpha.inputs[0])
    tree.links.new(math_1.outputs['Value'], set_alpha.inputs[1])
    
    tree.links.new(set_alpha.outputs['Image'], normal.inputs[0])
    
    emit = tree.nodes.new('CompositorNodeOutputFile')
    emit.base_path = paths[2]
    tree.links.new(render_layers.outputs['Emit'], emit.inputs[0])