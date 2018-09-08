def check_collision(item1, item2, CurrentStatus):
    item1_x = item1.get_x() 
    item1_y = item1.get_y() 
    item1_sizex = item1.get_size_x() 
    item1_sizey = item1.get_size_y() 
    item1_minx = item1_x
    item1_maxx = item1_x + item1_sizex
    item1_miny = item1_y
    item1_maxy = item1_y + item1_sizey

    item2_x = item2.get_x() 
    item2_y = item2.get_y() 
    item2_sizex = item2.get_size_x() 
    item2_sizey = item2.get_size_y() 
    item2_minx = item2_x
    item2_maxx = item2_x + item2_sizex
    item2_miny = item2_y
    item2_maxy = item2_y + item2_sizey

    if (item1_minx <= item2_maxx) and (item1_maxx >= item2_minx) and (item1_miny <= item2_maxy) and (item1_maxy >= item2_miny):
        NewStatus = CurrentStatus[0:2] + "_Hit"
        if (item1_minx <= item2_minx):
            item1.set_x(item2_minx - item1_sizex)
        elif (item1_maxx >= item2_maxx):
            item1.set_x(item2_maxx)
        if (item1_miny <= item2_miny):
            item1.set_y(item2_miny - item1_sizey)
        elif (item1_maxy >= item2_maxy):
            item1.set_y(item2_maxy)
        item1.set_v(0, 0)
    else:
        NewStatus = CurrentStatus

    return NewStatus
    

def check_collision_boundaries(item, minx, miny, maxx, maxy, CurrentStatus):
    NewStatus = CurrentStatus
    item_x = item.get_x() 
    item_y = item.get_y() 
    item_sizex = item.get_size_x() 
    item_sizey = item.get_size_y() 
    item_minx = item_x
    item_maxx = item_x + item_sizex
    item_miny = item_y
    item_maxy = item_y + item_sizey
    if (item_minx < minx):
        item.set_x(minx - (item_minx - minx))
        item.set_v(-item.get_vx(), item.get_vy())
        NewStatus = CurrentStatus[0:2] + "_Missed"
    elif (item_maxx > maxx):
        item.set_x(maxx - (item_maxx - maxx))
        item.set_v(-item.get_vx(), item.get_vy())
        NewStatus = CurrentStatus[0:2] + "_Missed"
    if (item_miny < miny):
        item.set_y(miny - (item_miny - miny))
        item.set_v(item.get_vx(), -item.get_vy())
        NewStatus = CurrentStatus[0:2] + "_Missed"
    elif (item_maxy > maxy):
        item.set_y(maxy - (item_maxy - maxy))
        item.set_v(item.get_vx(), -item.get_vy())
        NewStatus = CurrentStatus[0:2] + "_Missed"
    return NewStatus
