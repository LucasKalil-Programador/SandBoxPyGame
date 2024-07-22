import random
from enum import Enum
import pygame
import numpy as np
from numba import njit


class Types(Enum):
    BG = (0, 0, 0, 0, 0)
    SAND = (203, 189, 147, 1, 0)
    WATER = (28, 163, 236, 2, 0)
    STONE = (115, 112, 112, 3, 0)
    VACUUM = (20, 20, 20, 4, 0)
    CLONER = (108, 60, 12, 5, 0)


@njit
def run_physics(data, size):
    if random.random() > 0.5:
        data = data[::-1]

    for x in range(len(data)):
        skip_y = False
        for y in range(len(data[x])):
            if skip_y or y + 1 >= size[1]:
                skip_y = False
            elif data[x, y, 3] == Types.SAND.value[3]:
                skip_y = sand_physics(data, size, x, y)
            elif data[x, y, 3] == Types.WATER.value[3]:
                skip_y = water_physics(data, size, x, y)
            elif data[x, y, 3] == Types.VACUUM.value[3]:
                skip_y = vacuum_physics(data, size, x, y)
            elif data[x, y, 3] == Types.CLONER.value[3]:
                skip_y = cloner_physics(data, size, x, y)


@njit
def cloner_physics(data, size, x, y):
    adjacent = ((x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1))
    type_id = data[x, y, 4]
    for adj_x, adj_y in adjacent:
        if adj_x < 0 or adj_y < 0 or adj_x >= size[0] or adj_y >= size[1]:
            continue
        if type_id == Types.BG.value[3]:
            if data[adj_x, adj_y, 3] not in (Types.CLONER.value[3], Types.BG.value[3], Types.VACUUM.value[3]):
                data[x, y, 4] = data[adj_x, adj_y, 3]
        else:
            if data[adj_x, adj_y, 3] == Types.BG.value[3]:
                type_b = Types.BG
                if data[x, y, 4] == Types.SAND.value[3]:
                    type_b = Types.SAND
                elif data[x, y, 4] == Types.WATER.value[3]:
                    type_b = Types.WATER
                elif data[x, y, 4] == Types.STONE.value[3]:
                    type_b = Types.STONE

                if type_b.value[3] in (Types.SAND.value[3], Types.WATER.value[3], Types.STONE.value[3]):
                    spawn_pixel(data, adj_x, adj_y, color=type_b.value, cmod=10)
                elif type_b.value[3] in (Types.BG.value[3], Types.VACUUM.value[3], Types.CLONER.value[3]):
                    spawn_pixel(data, adj_x, adj_y, color=type_b.value)
    return False


@njit
def vacuum_physics(data, size, x, y):
    adjacent = ((x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1))
    for adj_x, adj_y in adjacent:
        if adj_x < 0 or adj_y < 0 or adj_x >= size[0] or adj_y >= size[1]:
            continue
        if data[adj_x, adj_y, 3] not in (Types.VACUUM.value[3], Types.BG.value[3]):
            spawn_pixel(data, adj_x, adj_y, color=Types.BG.value)
    return False


@njit
def sand_physics(data, size, x, y):
    # region Gravity
    if data[x, y + 1, 3] == Types.BG.value[3]:
        data[x, y + 1] = data[x, y]
        data[x, y] = Types.BG.value
        return True
    # endregion Gravity
    # region Drop down left or right
    random_side = -1 if random.random() > 0.5 else 1
    if x + random_side < 0 or x + random_side >= size[0]:
        random_side *= -1

    if data[x + random_side, y + 1, 3] in (Types.BG.value[3], Types.WATER.value[3]):
        data[x + random_side, y + 1], data[x, y] = data[x, y], data[x + random_side, y + 1].copy()
        return False

    random_side *= -1
    if x + random_side < 0 or x + random_side >= size[0]:
        return False

    if data[x + random_side * -1, y + 1, 3] in (Types.BG.value[3], Types.WATER.value[3]):
        data[x + random_side * -1, y + 1], data[x, y] = data[x, y], data[x + random_side * -1, y + 1].copy()
        return False
    # endregion Drop down left or right
    return False


@njit
def water_physics(data, size, x, y):
    # region Gravity
    if data[x, y + 1, 3] == Types.BG.value[3]:
        data[x, y + 1], data[x, y] = data[x, y], Types.BG.value
        return True
    # endregion Gravity
    # region Drop down left or Right
    random_side = -1 if random.random() > 0.5 else 1
    if x + random_side < 0 or x + random_side >= size[0]:
        random_side *= -1

    if data[x + random_side, y + 1, 3] == Types.BG.value[3]:
        data[x + random_side, y + 1], data[x, y] = data[x, y], Types.BG.value
        return False
    # endregion Drop down left or Right
    # region Sand fall over water
    if y - 1 > 0 and data[x, y - 1, 3] == Types.SAND.value[3]:
        data[x, y - 1], data[x, y] = data[x, y], data[x, y - 1].copy()
        return True
    # endregion Sand fall over water
    # region Moving horizontal
    max_steps = size[0]
    if data[x, y + 1][3] != Types.BG.value[3]:
        for new_x in range(x + 1, min(x + max_steps, size[0])):
            if data[new_x, y, 3] == Types.BG.value[3]:
                if data[new_x, y + 1, 3] == Types.BG.value[3]:
                    data[new_x, y], data[x, y] = data[x, y], Types.BG.value
                    return False
            else:
                break
        for new_x in range(x - 1, max(x - max_steps, 0), -1):
            if data[new_x, y, 3] == Types.BG.value[3]:
                if data[new_x, y + 1, 3] == Types.BG.value[3]:
                    data[new_x, y], data[x, y] = data[x, y], Types.BG.value
                    return False
            else:
                break
    # endregion Moving horizontal
    return False


@njit
def spawn_pixel(data, x, y, color=Types.BG.value, cmod=0):
    color = (color[0] + random.randint(-cmod, cmod),
             color[1] + random.randint(-cmod, cmod),
             color[2] + random.randint(-cmod, cmod),
             color[3], color[4])
    data[x, y] = color


@njit
def spawn(data, size, center, radius, type_b=Types.BG):
    for x in range(center[0] - radius, center[0] + radius):
        for y in range(center[1] - radius, center[1] + radius):
            if y < 0 or x < 0 or y >= size[1] or x >= size[0]:
                continue

            if (y - center[1]) ** 2 + (x - center[0]) ** 2 <= radius ** 2 and data[x, y, 3] != type_b.value[3]:
                if type_b.value[3] in (Types.SAND.value[3], Types.WATER.value[3], Types.STONE.value[3]):
                    spawn_pixel(data, x, y, color=type_b.value, cmod=10)
                elif type_b.value[3] in (Types.BG.value[3], Types.VACUUM.value[3], Types.CLONER.value[3]):
                    spawn_pixel(data, x, y, color=type_b.value)


class SandBox:
    def __init__(self, size: tuple[int, int]):
        self.__size = size
        self.__data: np.ndarray = np.empty(0)
        self.reset()
        self.__surface = pygame.Surface(size)
        self.update_surface()

    def spawn(self, center, radius, type_b=Types.BG):
        spawn(self.__data, self.__size, center, radius, type_b)

    def run_physics(self):
        run_physics(self.__data, self.__size)

    def reset(self):
        self.__data = np.full((self.__size[0], self.__size[1], 5), Types.BG.value, dtype=np.uint8)

    def update_surface(self):
        pygame.surfarray.blit_array(self.__surface, self.__data[:, :, :3])

    def get_surface(self):
        self.update_surface()
        return self.__surface
