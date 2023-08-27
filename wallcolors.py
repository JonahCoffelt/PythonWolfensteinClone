from PIL import Image
colors = {
    1 : (90, 90, 90),
    2 : (0, 100, 175),
    3 : (90, 60, 0)
}

colorsDark = {
    1 : (45, 45, 45),
    2 : (0, 50, 90),
    3 : (45, 30, 0)
}


textures = ["wallTestSmall", "StoneTile", "WoodTile"]

colorScale = 2
texture_scale = 16
wall_textures = {}
wall_textures_dark = {}

def read_walls():
    i = 1
    for texture in textures:
        texture_image = Image.open('Images/{}.png'.format(texture))
        texture_pixels = texture_image.load()
        txt = [texture_image.size[0]]
        txt_dark = [texture_image.size[0]]
        for x in range(texture_image.size[0]):
            for y in range(texture_image.size[0]):
                txt.append(texture_pixels[y,x])
                txt_dark.append((texture_pixels[y,x][0]/colorScale, texture_pixels[y,x][1]/colorScale, texture_pixels[y,x][2]/colorScale, texture_pixels[y,x][3]/colorScale))
        
        wall_textures[i] = txt
        wall_textures_dark[i] = txt_dark

        i+=1
    print(wall_textures[3])



def get_wall():

    wall = []
    wallDark = []

    wallimage = Image.open('Images/wallTestSmall.png')
    wallPixels = wallimage.load()

    for x in range(wallimage.size[0]):
        for y in range(wallimage.size[0]):
            wall.append(wallPixels[y,x])
            #wallDark = wall
            wallDark.append((wallPixels[y,x][0]/colorScale, wallPixels[y,x][1]/colorScale, wallPixels[y,x][2]/colorScale, wallPixels[y,x][3]/colorScale))

    return wall, wallDark, wallimage.size[0]

read_walls()