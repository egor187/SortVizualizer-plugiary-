import random
import math

import pygame


class Drawer:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND = WHITE
    SIDE_PAD = 100
    TOP_PAD = 150
    GRADIENTS = [(128, 128, 128), (160, 160, 160), (192, 192, 192)]
    FONT = pygame.font.SysFont("comicsans", 30)
    LARGE_FONT = pygame.font.SysFont("comicsans", 40)

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sort Visualizer")
        self.set_lst(lst)

    def set_lst(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor(
            (self.height - self.TOP_PAD) / (self.max_val - self.min_val)
        )
        self.start_x = self.SIDE_PAD // 2


def draw_canvas(drawer: Drawer, algo_name, ascending):
    drawer.window.fill(drawer.BACKGROUND)

    title = drawer.LARGE_FONT.render(
        f"{algo_name} - {'Ascending' if ascending else 'Descending'}",
        True,
        drawer.GREEN,
    )
    drawer.window.blit(title, (drawer.width / 3 - title.get_width() / 3, 5))

    controls = drawer.FONT.render(
        "R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending",
        True,
        drawer.BLACK,
    )
    drawer.window.blit(controls, (drawer.width / 2 - controls.get_width() / 2, 45))

    sorting = drawer.FONT.render(
        "I - Insertion Sort | B - Bubble Sort", 1, drawer.BLACK
    )
    drawer.window.blit(sorting, (drawer.width / 2 - sorting.get_width() / 2, 75))

    draw_list(drawer)
    pygame.display.update()


def draw_list(drawer: Drawer, color_positions={}, clear_bg=False):
    lst = drawer.lst

    if clear_bg:
        clear_rect = (
            drawer.SIDE_PAD // 2,
            drawer.TOP_PAD,
            drawer.width - drawer.SIDE_PAD,
            drawer.height - drawer.TOP_PAD,
        )
        pygame.draw.rect(drawer.window, drawer.BACKGROUND, clear_rect)

    for i, v in enumerate(lst):
        x = drawer.start_x + i * drawer.block_width
        y = drawer.height - (v - drawer.min_val) * drawer.block_height

        color = drawer.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(
            drawer.window, color, (x, y, drawer.block_width, drawer.height)
        )
    if clear_bg:
        pygame.display.update()


def generate_list(n, min_val, max_val):
    lst = [random.randint(min_val, max_val) for _ in range(n)]
    return lst


def bubble_sort(drawer, ascending=True):
    lst = drawer.lst
    for i in range(len(lst)):
        for j in range(len(lst) - 1 - i):
            if (lst[j] > lst[j + 1] and ascending) or (
                lst[j] < lst[j + 1] and not ascending
            ):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(drawer, {j: drawer.GREEN, j + 1: drawer.RED}, True)
                yield True
    return lst


def insertion_sort(drawer, ascending=True):
    lst = drawer.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(drawer, {i - 1: drawer.GREEN, i: drawer.RED}, True)
            yield True

    return lst


def merge_sort(drawer, ascending=True):
    lst = drawer.lst

    if len(lst) <= 1:
        return lst

    mid = len(lst) // 2

    left = merge_sort(lst[:mid])
    right = merge_sort(lst[mid:])

    return merge(left, right)


def merge(left_lst: list, right_lst: list) -> list:
    sorted_list = list()
    left_idx = right_idx = 0

    while left_idx < len(left_lst) and right_idx < len(right_lst):

        if left_lst[left_idx] > right_lst[right_idx]:
            sorted_list.append(right_lst[right_idx])
            right_idx += 1
        else:
            sorted_list.append(left_lst[left_idx])
            left_idx += 1

    if left_idx == len(left_lst):
        sorted_list.append(right_lst[right_idx:])
    elif right_idx == len(right_lst):
        sorted_list.append(left_lst[left_idx:])

    return sorted_list



