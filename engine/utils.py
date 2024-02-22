def check_collision_rectangles(rect1: tuple[any, any, any, any], rect2: tuple[any, any, any, any]) -> bool:
    return ((rect1[0] < rect2[0] + rect2[2]) and (rect1[0] + rect1[2] > rect2[0])) and (
        rect1[1] < (rect2[1] + rect2[3]) and (rect1[1] + rect1[3]) > rect2[1])


def check_collision_point_rect(point: tuple[any, any], rectangle: tuple[any, any, any, any]):
    return ((rectangle[0] <= point[0] < rectangle[0] + rectangle[2]) and (rectangle[1] <= point[1] < rectangle[1] + rectangle[3]))
