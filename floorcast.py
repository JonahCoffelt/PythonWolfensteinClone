import pygame
import numpy as np 
import wallcolors 

color_scaling = 1.1

def floorcast(win, winSize, resolution, viewFOV, direction, posx, posy, grid_size, floor, vertical_offset):
    vertical_res = int(winSize[1]/(winSize[1]/resolution))//2
    scaling_factor = resolution/np.rad2deg(viewFOV)

    pixel_width = winSize[0]/resolution
    pixel_height = winSize[1]/vertical_res/2
 
    print(vertical_res - int(vertical_offset/pixel_height))
    for x_layer in range(0-resolution//2, resolution//2):
        rot_x = direction + np.deg2rad(x_layer/scaling_factor - viewFOV/2)
        sin, cos, cos2 = np.sin(rot_x),  np.cos(rot_x), np.cos(np.deg2rad(x_layer/scaling_factor - viewFOV/2))

        

        for y_layer in range(int(vertical_offset/pixel_height), vertical_res):
            if vertical_res-y_layer:
                n = (vertical_res/(vertical_res-y_layer))/cos2
            else:
                n = 0
            x, y = posx/grid_size + sin*n, posy/grid_size + cos*n

            if x > 0 and y > 0 and x < 60 and y < 60:
                if floor[int(x) + int(y) * 60]:
                    if int(x)%2 == int(y)%2:
                        #print(y_layer - int(vertical_offset/pixel_height))
                        color = wallcolors.colors[floor[int(x) + int(y) * 60]]
                        pygame.draw.rect(win, (color[0] * (1 - (((y_layer - int(vertical_offset/pixel_height))/color_scaling)/(vertical_res - int(vertical_offset/pixel_height)))) * (1-abs(x_layer/color_scaling)/resolution/2), color[1] * (1-(((y_layer - int(vertical_offset/pixel_height))/color_scaling)/(vertical_res - int(vertical_offset/pixel_height)))) * (1-abs(x_layer/color_scaling)/resolution/2), color[2] * (1-(((y_layer - int(vertical_offset/pixel_height))/color_scaling)/(vertical_res - int(vertical_offset/pixel_height)))) * (1-abs(x_layer/color_scaling)/resolution/2)), (pixel_width * x_layer + winSize[0]/2, winSize[1] - pixel_height * (y_layer) + vertical_offset, pixel_width, pixel_height + 1))
                        #pygame.draw.rect(win, (color[0] * (1 - (((y_layer - int(vertical_offset/pixel_height))/color_scaling)/(vertical_res - int(vertical_offset/pixel_height)))) * (1-abs(x_layer/color_scaling)/resolution/2), color[1] * (1-(((y_layer - int(vertical_offset/pixel_height))/color_scaling)/(vertical_res - int(vertical_offset/pixel_height)))) * (1-abs(x_layer/color_scaling)/resolution/2), color[2] * (1-(((y_layer - int(vertical_offset/pixel_height))/color_scaling)/(vertical_res - int(vertical_offset/pixel_height)))) * (1-abs(x_layer/color_scaling)/resolution/2)), (pixel_width * x_layer + winSize[0]/2, pixel_height * y_layer, pixel_width, pixel_height + 1))
                    else:
                        color = wallcolors.colorsDark[floor[int(x) + int(y) * 60]]
                        pygame.draw.rect(win, (color[0] * (1 - (((y_layer - int(vertical_offset/pixel_height))/color_scaling)/(vertical_res - int(vertical_offset/pixel_height)))) * (1-abs(x_layer/color_scaling)/resolution/2), color[1] * (1-(((y_layer - int(vertical_offset/pixel_height))/color_scaling)/(vertical_res - int(vertical_offset/pixel_height)))) * (1-abs(x_layer/color_scaling)/resolution/2), color[2] * (1-(((y_layer - int(vertical_offset/pixel_height))/color_scaling)/(vertical_res - int(vertical_offset/pixel_height)))) * (1-abs(x_layer/color_scaling)/resolution/2)), (pixel_width * x_layer + winSize[0]/2, winSize[1] - pixel_height * (y_layer) + vertical_offset, pixel_width, pixel_height + 1))
                    #   pygame.draw.rect(win, (color[0] * (1-(y_layer/color_scaling)/vertical_res) * (1-abs(x_layer/color_scaling)/resolution/2), color[1] * (1-(y_layer/color_scaling)/vertical_res) * (1-abs(x_layer/color_scaling)/resolution/2), color[2] * (1-(y_layer/color_scaling)/vertical_res) * (1-abs(x_layer/color_scaling)/resolution/2)), (pixel_width * x_layer + winSize[0]/2, pixel_height * y_layer, pixel_width, pixel_height + 1))
            #if int(x)%2 == int(y)%2:
            #    pygame.draw.rect(win, (35 * (1-(y_layer/color_scaling)/vertical_res) * (1-abs(x_layer/color_scaling)/resolution/2), 15 * (1-(y_layer/color_scaling)/vertical_res) * (1-abs(x_layer/color_scaling)/resolution/2), 200 * (1-(y_layer/color_scaling)/vertical_res) * (1-abs(x_layer/color_scaling)/resolution/2)), (pixel_width * x_layer + winSize[0]/2, winSize[1] - pixel_height * y_layer, pixel_width, pixel_height + 1))
            #    pygame.draw.rect(win, (200 * (1-(y_layer/color_scaling)/vertical_res) * (1-abs(x_layer/color_scaling)/resolution/2), 15 * (1-(y_layer/color_scaling)/vertical_res) * (1-abs(x_layer/color_scaling)/resolution/2), 35 * (1-(y_layer/color_scaling)/vertical_res) * (1-abs(x_layer/color_scaling)/resolution/2)), (pixel_width * x_layer + winSize[0]/2, pixel_height * y_layer, pixel_width, pixel_height + 1))