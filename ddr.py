import math
def ddr(map, playerPos, endPos, grid_size):

    final_distance = 0

    cast = False
    mapPos = [playerPos[0]//grid_size - 1, playerPos[1]//grid_size]
    total_distance = math.sqrt((endPos[0] - playerPos[0])**2 + (endPos[1] - playerPos[1])**2)/grid_size
    theta = -1 * math.atan2(endPos[1] - playerPos[1], endPos[0] - playerPos[0])
    xScale, yScale = math.sqrt(1 + (math.tan(theta))**2), math.sqrt(1 + (1 / math.tan(theta))**2)

    if endPos[0] > playerPos[0]:
        xDir = 1
        ax = grid_size - (playerPos[0] - (playerPos[0]//grid_size)*grid_size)
    else:
        xDir = -1
        ax = playerPos[0] - (playerPos[0]//grid_size)*grid_size
    if endPos[1] > playerPos[1]:
        yDir = 1
        ay = grid_size - (playerPos[1] - (playerPos[1]//grid_size)*grid_size)
    else:
        yDir = -1
        ay = playerPos[1] - (playerPos[1]//grid_size)*grid_size
    
    ax /= grid_size
    ay /= grid_size
    xlen, ylen = xScale * ax, yScale * ay

    if map[int(mapPos[0] + mapPos[1] * int(math.sqrt(len(map))))]:
        return .001, 0, 1
    else:
        cast = True
    while cast:
        if xlen <= ylen:
            if len(map) > int((mapPos[0] + xDir) + mapPos[1] * int(math.sqrt(len(map)))):
                if map[int((mapPos[0] + xDir) + mapPos[1] * int(math.sqrt(len(map))))]:
                    return xlen, 0, map[int((mapPos[0] + xDir) + mapPos[1] * int(math.sqrt(len(map))))], (int((mapPos[0] + xDir)), mapPos[1])
                else:
                    mapPos[0] += xDir
                    xlen += xScale
            else:
                return .001, 0, 1, 0
        else:
            if len(map) > int(mapPos[0] + (mapPos[1] + yDir) * int(math.sqrt(len(map)))):
                if map[int(mapPos[0] + (mapPos[1] + yDir) * int(math.sqrt(len(map))))]:
                    return ylen, 1, map[int(mapPos[0] + (mapPos[1] + yDir) * int(math.sqrt(len(map))))], (mapPos[0], int(mapPos[1] + yDir))
                else:
                    mapPos[1] += yDir
                    ylen += yScale
            else:
                return .001, 0, 1, 0

        if xlen >= total_distance and ylen >= total_distance:
            return total_distance, 0, 1, 0

    if xlen <= ylen:
        return xlen, 0, map[int(mapPos[0] + (mapPos[1]) * int(math.sqrt(len(map))))], (int((mapPos[0] + xDir)), mapPos[1])
    return ylen, 1, map[int(mapPos[0] + (mapPos[1]) * int(math.sqrt(len(map))))], (mapPos[0], int(mapPos[1] + yDir))