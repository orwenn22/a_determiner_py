import pyray
import os
from gameobject import portal
from items import spdiamond
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


def parse_map_file(gameplay_state, map_file: str) -> str:
    """
    Parse a specified map file (in maps directory) and put all of its stuff in a gameplay_state
    Return empty string on success, or a string containing the error on failure
    """
    import gameplaystate
    gameplay_state: gameplaystate.GameplayState

    map_init: list = read_map_file(map_file)
    map_image_path = ""
    map_size: pyray.Vector2 = pyray.Vector2(0, 0)
    for line in map_init:
        match line[0]:
            case "camera_center":
                # Specify the position of the camera's center           format : camera_center x y
                m.set_camera_center(pyray.Vector2(float(line[1]), float(line[2])))
            case "bitmap":
                # Image corresponding to the main layer of the map      format : bitmap my_map.png
                map_image_path = line[1]
            case "mapsize":
                # Size of the map in meter                              format : mapsize x y
                map_size = pyray.Vector2(float(line[1]), float(line[2]))
            case "portal":
                # Place a pair of portal                                format : portal x1 y1 x2 y2
                portal.Portal.spawn_portals(gameplay_state.object_manager, float(line[1]), float(line[2]), float(line[3]),
                                            float(line[4]))
            case "portal_gun":
                # Place a portal gun object                             format : portal_gun x y
                gameplay_state.object_manager.add_object(portalgun.PortalGun(float(line[1]), float(line[2])))
            case "trowel":
                # Place a trowel object                                 format : trowel x y
                gameplay_state.object_manager.add_object(trowel.Trowel(float(line[1]), float(line[2])))
            case "spdiamond":
                # Place a skill point diamond                           format : spdiamond x y
                gameplay_state.object_manager.add_object(spdiamond.SPDiamond(float(line[1]), float(line[2])))
            case "blue_start":
                # Define the blue spawn location                        format : blue_start x y w h
                gameplay_state.starts[0] = (float(line[1]), float(line[2]), float(line[3]), float(line[4]))
            case "red_start":
                # Define the red spawn location                         format : red_start x y w h
                gameplay_state.starts[1] = (float(line[1]), float(line[2]), float(line[3]), float(line[4]))
            case "background":
                pass  # we haven't already defined how the background will be placed

    if map_image_path == "":
        return "Image not specified in level file"

    if map_size.x <= 0 or map_size.y <= 0:
        return f"Error while loading map : invalid size {map_size.x} {map_size.y}"

    full_map_image_path = "maps/" + map_image_path
    if not os.path.isfile(full_map_image_path):
        return f"The file " + full_map_image_path + " don't exist"

    # We already checked if the file exists, therefore this shouldn't fail.
    gameplay_state.initialise_terrain(full_map_image_path, map_size.x, map_size.y)
    return ""
