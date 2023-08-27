import pygame, math, json
import numpy as np
from player import Player
from wallcolors import colors, colorsDark, get_wall, read_walls, wall_textures, wall_textures_dark
import ddr, floorcast

clock = pygame.time.Clock()

winSize = (1500, 1000)
win = pygame.display.set_mode(winSize, pygame.RESIZABLE)

run = True
mouseMvt = True
pygame.mouse.set_visible(False)
pygame.init()

map = []
map_size = 60
grid_size = winSize[0]//map_size

viewDistance = 2000
resolution = winSize[0]//10
viewFOV = np.deg2rad(75)
color_scaling = 6

vrot_limit = 1.5

read_walls()

floor = [0, 1, 0,
         1, 1, 1,
         0, 1, 0]

playerCharacter = Player(grid_size)

def create_empty_map():
    for y in range(map_size):
        for x in range(map_size):
            map.append(0)

def display_map():
    for y in range(map_size):
        for x in range(map_size):
            if map[x + y*map_size - 1]:
                pygame.draw.rect(win, colors[map[x + y*map_size - 1]], (x*grid_size, y*grid_size, grid_size - 1, grid_size - 1))  

def draw():
    win.fill("black")

    vertical_offset = int(playerCharacter.vrot * winSize[1]/2 + playerCharacter.height)

    if mouseMvt:
        floorcast.floorcast(win, winSize, resolution//1, viewFOV, playerCharacter.direction, playerCharacter.x, playerCharacter.y, grid_size, floor, vertical_offset)
        ray_direction = playerCharacter.direction - viewFOV/2
        ray_step = viewFOV/resolution
        for ray in range(resolution):
            endPoint = (playerCharacter.x + viewDistance * math.sin(ray_direction), playerCharacter.y + viewDistance * math.cos(ray_direction))
            distance, side, clr, colPoint = ddr.ddr(map, (playerCharacter.x, playerCharacter.y), (endPoint[0], endPoint[1]), grid_size)
            
            theta = -1 * math.atan2(endPoint[1] - playerCharacter.y, endPoint[0] - playerCharacter.x) + math.pi/2
            colision = ((playerCharacter.x + (distance*grid_size) * math.sin(theta))/grid_size, (playerCharacter.y + (distance*grid_size) * math.cos(theta))/grid_size)
    
            if (distance+1) < viewDistance/grid_size:
                da = abs(playerCharacter.direction - ray_direction)
                distance  *= np.cos(da)
                #print(distance)
                lineHeight = winSize[1]/distance + abs(resolution/2 - ray)/resolution * 50
                if side:
                    for pixel in range(wall_textures[clr][0]):
                        texture_point = ((int(colision[0]*wall_textures[clr][0]))%wall_textures[clr][0]) + (wall_textures[clr][0]-pixel - 1)*wall_textures[clr][0] + 1
                        color = wall_textures[clr][texture_point]
                        if distance > color_scaling:
                            pygame.draw.rect(win, (color[0]/(distance/color_scaling), color[1]/(distance/color_scaling), color[2]/(distance/color_scaling)), ((winSize[0]/resolution)*ray, winSize[1]/2 - lineHeight/2 + lineHeight/wall_textures[clr][0]*(wall_textures[clr][0] - pixel - 1) + vertical_offset, int(winSize[0]/resolution), lineHeight/wall_textures[clr][0] + 1))
                            pygame.draw.rect(win, (color[0]/(distance/color_scaling), color[1]/(distance/color_scaling), color[2]/(distance/color_scaling)), ((winSize[0]/resolution)*ray, winSize[1]/2 - lineHeight/2 + lineHeight/wall_textures[clr][0]*(wall_textures[clr][0] - pixel - 1) + vertical_offset - lineHeight, int(winSize[0]/resolution), lineHeight/wall_textures[clr][0] + 1))
                        else:
                            pygame.draw.rect(win, wall_textures[clr][texture_point], ((winSize[0]/resolution)*ray, winSize[1]/2 - lineHeight/2 + lineHeight/wall_textures[clr][0]*(wall_textures[clr][0] - pixel - 1) + vertical_offset, int(winSize[0]/resolution), lineHeight/wall_textures[clr][0] + 1))
                            pygame.draw.rect(win, wall_textures[clr][texture_point], ((winSize[0]/resolution)*ray, winSize[1]/2 - lineHeight/2 + lineHeight/wall_textures[clr][0]*(wall_textures[clr][0] - pixel - 1) + vertical_offset - lineHeight, int(winSize[0]/resolution), lineHeight/wall_textures[clr][0] + 1))
                else:
                    for pixel in range(wall_textures[clr][0]):
                        texture_point = ((int(colision[1]*wall_textures_dark[clr][0]))%wall_textures_dark[clr][0]) + (wall_textures_dark[clr][0]-pixel - 1)*wall_textures_dark[clr][0] + 1
                        color = wall_textures_dark[clr][texture_point]
                        if distance > color_scaling:
                            pygame.draw.rect(win, (color[0]/(distance/color_scaling), color[1]/(distance/color_scaling), color[2]/(distance/color_scaling)), ((winSize[0]/resolution)*ray, winSize[1]/2 - lineHeight/2 + lineHeight/wall_textures_dark[clr][0]*(wall_textures_dark[clr][0] - pixel - 1) + vertical_offset, int(winSize[0]/resolution), lineHeight/wall_textures_dark[clr][0] + 1))
                            pygame.draw.rect(win, (color[0]/(distance/color_scaling), color[1]/(distance/color_scaling), color[2]/(distance/color_scaling)), ((winSize[0]/resolution)*ray, winSize[1]/2 - lineHeight/2 + lineHeight/wall_textures_dark[clr][0]*(wall_textures_dark[clr][0] - pixel - 1) + vertical_offset - lineHeight, int(winSize[0]/resolution), lineHeight/wall_textures_dark[clr][0] + 1))
                        else:
                            pygame.draw.rect(win, wall_textures_dark[clr][texture_point], ((winSize[0]/resolution)*ray, winSize[1]/2 - lineHeight/2 + lineHeight/wall_textures_dark[clr][0]*(wall_textures_dark[clr][0] - pixel - 1) + vertical_offset, int(winSize[0]/resolution), lineHeight/wall_textures_dark[clr][0] + 1))
                            pygame.draw.rect(win, wall_textures_dark[clr][texture_point], ((winSize[0]/resolution)*ray, winSize[1]/2 - lineHeight/2 + lineHeight/wall_textures_dark[clr][0]*(wall_textures_dark[clr][0] - pixel - 1) + vertical_offset - lineHeight, int(winSize[0]/resolution), lineHeight/wall_textures_dark[clr][0] + 1))

            ray_direction += ray_step
    
        pygame.draw.circle(win, (255, 255, 255), (winSize[0]/2, winSize[1]/2), 5)
    else:
        display_map()

    pygame.display.flip()

def update():
    draw()

#create_empty_map()

with open('Maps/save.json', 'r') as openfile:
    map = json.load(openfile)

with open('Maps/floor.json', 'r') as openfile:
    floor = json.load(openfile)

while run:
    dt = clock.tick()

    mouseX, mouseY = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
        if event.type == pygame.MOUSEMOTION:
            if mouseMvt:
                pygame.mouse.set_pos([winSize[0]/2, winSize[1]/2])
                pos=event.pos 
                playerCharacter.direction -= (winSize[0]/2 - pos[0])/750
                playerCharacter.vrot += (winSize[1]/2 - pos[1])/250
                if playerCharacter.vrot > vrot_limit:
                    playerCharacter.vrot = vrot_limit
                elif playerCharacter.vrot < -vrot_limit:
                    playerCharacter.vrot = -vrot_limit
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        projectedY = playerCharacter.y + playerCharacter.speed * math.cos(playerCharacter.direction) * dt
        projectedX = playerCharacter.x + playerCharacter.speed * math.sin(playerCharacter.direction) * dt
        if projectedY > 0 and projectedY < grid_size * map_size - grid_size:
            if not map[int((playerCharacter.x - grid_size/3)//grid_size + (projectedY//grid_size)*map_size) - 1] and not map[int((playerCharacter.x + grid_size/3)//grid_size + (projectedY//grid_size)*map_size) - 1]:
                playerCharacter.y = projectedY
        if projectedX > 0 and projectedX < grid_size * map_size - grid_size:
            if not map[int((projectedX - grid_size/3)//grid_size + (playerCharacter.y//grid_size)*map_size) - 1] and not map[int((projectedX + grid_size/3)//grid_size + (playerCharacter.y//grid_size)*map_size) - 1]:
                playerCharacter.x = projectedX
    if keys[pygame.K_s]:
        projectedY = playerCharacter.y - playerCharacter.speed * math.cos(playerCharacter.direction) * dt
        projectedX = playerCharacter.x - playerCharacter.speed * math.sin(playerCharacter.direction) * dt
        if projectedY > 0 and projectedY < grid_size * map_size - grid_size:
            if not map[int((playerCharacter.x - grid_size/3)//grid_size + (projectedY//grid_size)*map_size) - 1] and not map[int((playerCharacter.x + grid_size/3)//grid_size + (projectedY//grid_size)*map_size) - 1]:
                playerCharacter.y = projectedY
        if projectedX > 0 and projectedX < grid_size * map_size - grid_size:
            if not map[int((projectedX - grid_size/3)//grid_size + (playerCharacter.y//grid_size)*map_size) - 1] and not map[int((projectedX + grid_size/3)//grid_size + (playerCharacter.y//grid_size)*map_size) - 1]:
                playerCharacter.x = projectedX
    if keys[pygame.K_d]:
        projectedY = playerCharacter.y - playerCharacter.speed * math.sin(playerCharacter.direction) * dt
        projectedX = playerCharacter.x + playerCharacter.speed * math.cos(playerCharacter.direction) * dt
        if projectedY > 0 and projectedY < grid_size * map_size - grid_size:
            if not map[int((playerCharacter.x - grid_size/3)//grid_size + (projectedY//grid_size)*map_size) - 1] and not map[int((playerCharacter.x + grid_size/3)//grid_size + (projectedY//grid_size)*map_size) - 1]:
                playerCharacter.y = projectedY
        if projectedX > 0 and projectedX < grid_size * map_size - grid_size:
            if not map[int((projectedX - grid_size/3)//grid_size + (playerCharacter.y//grid_size)*map_size) - 1] and not map[int((projectedX + grid_size/3)//grid_size + (playerCharacter.y//grid_size)*map_size) - 1]:
                playerCharacter.x = projectedX
    if keys[pygame.K_a]:
        projectedY = playerCharacter.y + playerCharacter.speed * math.sin(playerCharacter.direction) * dt
        projectedX = playerCharacter.x - playerCharacter.speed * math.cos(playerCharacter.direction) * dt
        if projectedY > 0 and projectedY < grid_size * map_size - grid_size:
            if not map[int((playerCharacter.x - grid_size/3)//grid_size + (projectedY//grid_size)*map_size) - 1] and not map[int((playerCharacter.x + grid_size/3)//grid_size + (projectedY//grid_size)*map_size) - 1]:
                playerCharacter.y = projectedY
        if projectedX > 0 and projectedX < grid_size * map_size - grid_size:
            if not map[int((projectedX - grid_size/3)//grid_size + (playerCharacter.y//grid_size)*map_size) - 1] and not map[int((projectedX + grid_size/3)//grid_size + (playerCharacter.y//grid_size)*map_size) - 1]:
                playerCharacter.x = projectedX
    
    if keys[pygame.K_LEFT]:
        playerCharacter.direction -= playerCharacter.turnSpeed * dt
    if keys[pygame.K_RIGHT]:
        playerCharacter.direction += playerCharacter.turnSpeed * dt
    if keys[pygame.K_UP]:
        if playerCharacter.vrot < .8:
            playerCharacter.vrot += playerCharacter.turnSpeed * dt/5
    if keys[pygame.K_DOWN]:
        if playerCharacter.vrot > -.8:
            playerCharacter.vrot -= playerCharacter.turnSpeed * dt/5
    #if keys[pygame.K_SPACE]:
    #    playerCharacter.height += playerCharacter.speed * dt
    #if keys[pygame.K_LSHIFT]:
    #    playerCharacter.height -= playerCharacter.speed * dt
        
    if keys[pygame.K_ESCAPE]:
        mouseMvt = False
        pygame.mouse.set_visible(True)
    
    if not mouseMvt:
        if keys[pygame.K_1]:
            mouse_gridX, mouse_gridY = int(mouseX/grid_size), int(mouseY/grid_size)
            map[mouse_gridX + mouse_gridY*map_size - 1] = 1
        if keys[pygame.K_2]:
            mouse_gridX, mouse_gridY = int(mouseX/grid_size), int(mouseY/grid_size)
            map[mouse_gridX + mouse_gridY*map_size - 1] = 2
        if keys[pygame.K_3]:
            mouse_gridX, mouse_gridY = int(mouseX/grid_size), int(mouseY/grid_size)
            map[mouse_gridX + mouse_gridY*map_size - 1] = 3
        if pygame.mouse.get_pressed()[0]:
            mouse_gridX, mouse_gridY = int(mouseX/grid_size), int(mouseY/grid_size)
            map[mouse_gridX + mouse_gridY*map_size - 1] = 1
        if pygame.mouse.get_pressed()[2]:
            mouse_gridX, mouse_gridY = int(mouseX/grid_size), int(mouseY/grid_size)
            map[mouse_gridX + mouse_gridY*map_size - 1] = 0
        if keys[pygame.K_s]:
            json_object = json.dumps(map, indent=4)
            with open("Maps/floor.json", "w") as outfile:
                outfile.write(json_object)

    update()