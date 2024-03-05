import pyray
import terrain
from objects import portal
import items.portalgun as portalgun
import items.trowel as trowel
from engine import metrics as m


def read_map_file(map_name: str) -> list:
    """

    :param map_name: the name of the file containing the map layout (only include the txt file name but remind to put it in maps)
    """
    map_name = "maps/" + map_name
    map_list = []
    with open(map_name, "r") as map_file:
        line = map_file.readline().split()
        while line:
            map_list.append(line)
            line = map_file.readline().split()
    return map_list


def parse_map_file(gameplay_state, map_file: str):
    import gameplaystate
    gameplay_state: gameplaystate.GameplayState

    map_init: list = read_map_file(map_file)
    map_image = ""
    map_size: pyray.Vector2 = pyray.Vector2(0, 0)
    for line in map_init:
        match line[0]:
            # Put the cam at the center of the world
            case "camera_center":
                m.set_camera_center(pyray.Vector2(float(line[1]), float(line[2])))
            case "map":
                map_image = line[1]
            case "mapsize":
                map_size = pyray.Vector2(float(line[1]), float(line[2]))
            case "portal":
                portal.Portal.spawn_portals(gameplay_state.object_manager, float(line[1]), float(line[2]), float(line[3]),
                                            float(line[4]))
            case "portal_gun":
                gameplay_state.object_manager.add_object(portalgun.PortalGun(float(line[1]), float(line[2])))
            case "trowel":
                gameplay_state.object_manager.add_object(trowel.Trowel(float(line[1]), float(line[2])))
            case "blue_start":
                gameplay_state.blue_start: tuple[float, float, float, float] = (
                float(line[1]), float(line[2]), float(line[3]), float(line[4]))
            case "red_start":
                gameplay_state.red_start: tuple[float, float, float, float] = (
                float(line[1]), float(line[2]), float(line[3]), float(line[4]))
            case "background":
                pass  # we haven't already defined how the background will be placed

    if map_image == "":
        assert "Image not specified in level file"

    if map_size.x != 0 and map_size.y != 0:
        gameplay_state.t = terrain.Terrain(map_image, map_size)
    else:
        assert f"Error while loading map : invalid size {map_size.x} {map_size.y}"
