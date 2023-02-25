import bpy
import os
import shutil
import numpy as np

def generate_spritesheet(path, savepath, name):
    bdata = bpy.data
    images = []
    paths = os.listdir(path)
    paths.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    
    #загрузка всех рендеров
    for imgPath in paths:
        fullPath = os.path.join( path, imgPath )
        images.append(bpy.data.images.load(fullPath ))
        
    views = len(images)
    #размер картинки 
    tile_size = images[0].size[0]
    
    new = True
    for img in bdata.images:
        if img.name == name:
            spritesheet = img.copy()
            new = False
    
    #создание новой картинки, общей для всех     
    if new:
        spritesheet = bdata.images.new(name, width = views * tile_size, height = tile_size, alpha = True)
    
    spritesheet.alpha_mode = 'CHANNEL_PACKED'
    
    #трехмерный массив (rgba * 256 * 256views), который дальше будем заполнять
    sb = np.zeros([views * tile_size,tile_size,4], dtype = 'float32')
    
    k = len(images)
    for i in range(k):
        buffer = get_image_buffer(images[i])
        write_tile(buffer, sb, i, (views, 1))
    
    #удаляем одиночные картинки
    for img in images:
        bpy.data.images.remove(img)
        
    # выгружаем данные из заполненного ранее массива
    spritesheet.pixels.foreach_set(sb.swapaxes(0, 1).flatten(order='C'))
        
    shutil.rmtree(path)
    savepath = os.path.join(savepath, name + '.png')
                     
    spritesheet.filepath_raw = savepath
    spritesheet.save()
    return spritesheet


def get_image_buffer(image):
    buffer = np.zeros(len(image.pixels), dtype = 'float32')
    
    #заполняем буфер данными картинки
    image.pixels.foreach_get(buffer)
    #преобразование к трехммерному массиву
    buffer = buffer.reshape([image.size[0], image.size[1], image.channels])
    return buffer

    
def write_tile(buffer, target_buffer, tile, grid:tuple ):
    buffer = buffer.swapaxes(0, 1)
    b_shape = buffer.shape
    tile_x = tile % grid[0]
    tile_y = int(tile / grid[0])
    x_offset = tile_x * b_shape[0]
    y_offset = tile_y * b_shape[1]
    target_buffer[x_offset:x_offset + b_shape[0], y_offset:y_offset + b_shape[1] ] = buffer