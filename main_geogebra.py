import pygame
from pygame.locals import *
from pygame import gfxdraw
from classes import *
from functions import *

pygame.init()

width, height = (600, 600)  # ширина,высота экрана
window = pygame.display.set_mode((width, height))
window.fill((255, 255, 255))


def check_short(x):
    if -32700 < x < 32700:
        return True
    return False


def draw_circle(surface, coord, radius, filling: bool, color):
    """рисует круг"""

    x, y = coord
    if check_short(x) and check_short(y) and check_short(radius):
        gfxdraw.aacircle(surface, x, y, radius, color)
        if filling:
            gfxdraw.filled_circle(surface, x, y, radius, color)


def aaline_mod(surface, line: LINE, color, thickness=1, type_line="straight"):
    if type_line == "straight":
        if line.formula[0].real == 0 or abs(line.formula[0].imag / line.formula[0].real) > 1:
            line_left = LINE(
                complex_plane.left_top_coordinate - (3 + thickness) * complex_plane.dimension,
                complex_plane.left_top_coordinate - (3 + thickness) * (1 + 1j) * complex_plane.dimension,
                {"свойств": "нет"})
            line_right = LINE(
                complex_plane.left_top_coordinate + (width + 3 + thickness) * complex_plane.dimension,
                complex_plane.left_top_coordinate + (width + 3 + thickness) * (1 + 1j) * complex_plane.dimension,
                {"свойств": "нет"})
            start_pos = intersections_line_line(line, line_left)[0][0]
            end_pos = intersections_line_line(line, line_right)[0][0]
            for i in range(thickness):
                pygame.draw.aaline(surface, color, list(
                    map(round, flatness_display(start_pos + (-1) ** i * complex_plane.dimension * i // 2))), list(
                    map(round, flatness_display(end_pos + (-1) ** i * complex_plane.dimension * i // 2))))

        elif abs(line.formula[0].imag / line.formula[0].real) <= 1:
            line_lower = LINE(
                complex_plane.left_top_coordinate + (height + 3 + thickness) * (0 + 1j) * complex_plane.dimension,
                complex_plane.left_top_coordinate + (height + 3 + thickness) * (1 + 1j) * complex_plane.dimension,
                {"свойств": "нет"})
            line_upper = LINE(
                complex_plane.left_top_coordinate - (3 + thickness) * (0 + 1j) * complex_plane.dimension,
                complex_plane.left_top_coordinate - (3 + thickness) * (1 + 1j) * complex_plane.dimension,
                {"свойств": "нет"})
            start_pos = intersections_line_line(line, line_lower)[0][0]
            end_pos = intersections_line_line(line, line_upper)[0][0]
            for i in range(thickness):
                pygame.draw.aaline(surface, color, list(
                    map(round, flatness_display(start_pos + (-1) ** i * complex_plane.dimension * i // 2))), list(
                    map(round, flatness_display(end_pos + (-1) ** i * complex_plane.dimension * i // 2))))


def display_flatness(coordinates: list):
    """переводит координаты с экрана на плоскость"""
    coordinates = complex(coordinates[0], coordinates[1])
    return complex_plane.left_top_coordinate + complex_plane.dimension * coordinates


def flatness_display(coordinates: complex):
    """переводит координаты с плоскости на экран"""
    coordinates = (coordinates - complex_plane.left_top_coordinate) / complex_plane.dimension
    return [coordinates.real, coordinates.imag]


def changing_mod(event):
    """меняет нынешний мод в программе"""

    global mod_program
    withdrawal_special()
    if event == pygame.K_5:
        mod_program = "POINT"
    elif event == pygame.K_6:
        mod_program = "LINE"
    elif event == pygame.K_1:
        mod_program = "ZOOM"
    elif event == pygame.K_7:
        mod_program = "CIRCLE"
    elif event == pygame.K_2:
        mod_program = "MOVING_OBJECT"
    elif event == pygame.K_3:
        mod_program = "DELETION"
    elif event == pygame.K_4:
        mod_program = "VISIBLE/INVISIBLE"


def position_point(coordinates: complex, consider_point=True, consider_intersections=True, consider_object=True):
    """вычисляет положение точки (с учетом пересечений и принадлежностей)"""
    point = False
    inaccuracy_POINT = 16  # в пикселях
    if consider_point and not point:
        for object in objects:
            if object.visibility != "invisible" or mod_program == "VISIBLE/INVISIBLE":
                if type(object) == POINT:
                    if not point:
                        if abs(object.coordinate - coordinates) <= (inaccuracy_POINT * complex_plane.dimension):
                            point = object
                    else:
                        if abs(object.coordinate - coordinates) <= abs(point.coordinate - coordinates):
                            point = object
    if not point and consider_intersections:
        for i in range(len(objects)):
            for j in range(i + 1, len(objects)):
                if (objects[i].visibility != "invisible" and objects[
                    j].visibility != "invisible") or mod_program == "VISIBLE/INVISIBLE":
                    if type(objects[i]) != POINT and type(objects[j]) != POINT:
                        z = intersections_object_object(objects[i], objects[j])
                        for Z in z:
                            if not point:
                                if abs(Z[0] - coordinates) <= (inaccuracy_POINT * complex_plane.dimension) and Z[1]:
                                    point = POINT(Z[0], {"type_dependencies": "intersection",
                                                         "depend_object": [objects[i], objects[j]],
                                                         "additional_restrictions": [Z[2]]}, fixity=True)
                            else:
                                if abs(Z[0] - coordinates) <= abs(point.coordinate - coordinates) and Z[1]:
                                    point = POINT(Z[0], {"type_dependencies": "intersection",
                                                         "depend_object": [objects[i], objects[j]],
                                                         "additional_restrictions": [Z[2]]}, fixity=True)

    if not point and consider_object:
        for i in range(len(objects)):
            if objects[i].visibility != "invisible" or mod_program == "VISIBLE/INVISIBLE":
                if type(objects[i]) != POINT:
                    z = nearest_point_object(coordinates, objects[i])
                    if not point:
                        if abs(z[0] - coordinates) <= (inaccuracy_POINT * complex_plane.dimension) and z[1]:
                            point = POINT(z[0], {"type_dependencies": "belong",
                                                 "depend_object": [objects[i]],
                                                 "additional_restrictions": []})
                    else:
                        if abs(z[0] - coordinates) <= abs(point.coordinate - coordinates) and z[1]:
                            point = POINT(z[0], {"type_dependencies": "belong",
                                                 "depend_object": [objects[i]],
                                                 "additional_restrictions": []})
    if not point:
        point = POINT(coordinates, {"type_dependencies": "none",
                                    "depend_object": [],
                                    "additional_restrictions": []})
    return point


def mod_point(event_mousebuttondown):
    """действия при моде - точка"""
    withdrawal_special()
    coordinates = display_flatness(event_mousebuttondown.pos)
    point = position_point(coordinates)
    if point in objects:
        point.visibility = "special"
    else:
        objects.append(point)
    # дописать если вернется точка


def mod_line(event_mousebuttondown):
    """действия при моде - линия"""
    if not temporary_objects:
        coordinates = display_flatness(event_mousebuttondown.pos)
        point = position_point(coordinates)
        point.visibility = "special"
        temporary_objects.append(point)
    else:
        coordinates = display_flatness(event_mousebuttondown.pos)
        coordinates = position_point(coordinates)
        if coordinates.coordinate != temporary_objects[0].coordinate:
            temporary_objects.append(coordinates)
        if len(temporary_objects) == 2:
            for object in temporary_objects:
                if object not in objects:
                    objects.append(object)
            objects.append(
                LINE(temporary_objects[0].coordinate, temporary_objects[1].coordinate,
                     {"type_dependencies": "two_points", "depend_object": [temporary_objects[0], temporary_objects[1]],
                      "additional_restrictions": []}))
            withdrawal_special()


def mod_zoom(event_mousebuttondown):
    """мод изменения ..."""  # забыл слово
    if event_mousebuttondown.type == MOUSEBUTTONDOWN:
        if event.button == 1:  # левая кнопка мыши
            if complex_plane.dimension > 1 / 10 ** 4:
                complex_plane.update(
                    left_top_coordinate=complex_plane.left_top_coordinate + (
                            1 - 1 / complex_plane.zoom_constant) * complex(
                        event_mousebuttondown.pos[0], event_mousebuttondown.pos[1]) * complex_plane.dimension,
                    dimension=complex_plane.dimension / complex_plane.zoom_constant)
        if event.button == 3:  # правая кнопка мыши
            if complex_plane.dimension < 10 ** 4:
                complex_plane.update(
                    left_top_coordinate=complex_plane.left_top_coordinate - (complex_plane.zoom_constant - 1) * complex(
                        event_mousebuttondown.pos[0], event_mousebuttondown.pos[1]) * complex_plane.dimension,
                    dimension=complex_plane.dimension * complex_plane.zoom_constant)


def mod_zoom_moving():
    if pygame.mouse.get_pos()[0] <= 20 or width - 20 <= pygame.mouse.get_pos()[0] or pygame.mouse.get_pos()[1] <= 20 or \
            height - 20 <= pygame.mouse.get_pos()[1]:
        if pygame.mouse.get_pos()[0] <= 20:
            complex_plane.left_top_coordinate -= 3 * complex_plane.dimension
        elif width - 20 <= pygame.mouse.get_pos()[0]:
            complex_plane.left_top_coordinate += 3 * complex_plane.dimension
        elif pygame.mouse.get_pos()[1] <= 20:
            complex_plane.left_top_coordinate -= complex(0, 3 * complex_plane.dimension)
        elif height - 20 <= pygame.mouse.get_pos()[1]:
            complex_plane.left_top_coordinate += complex(0, 3 * complex_plane.dimension)


def mod_circle(event_mousebuttondown):
    if not temporary_objects:
        coordinates = display_flatness(event_mousebuttondown.pos)
        point = position_point(coordinates)
        point.visibility = "special"
        temporary_objects.append(point)
    else:
        coordinates = display_flatness(event_mousebuttondown.pos)
        coordinates = position_point(coordinates)
        if coordinates.coordinate != temporary_objects[0].coordinate:
            temporary_objects.append(coordinates)
        if len(temporary_objects) == 2:
            for object in temporary_objects:
                if object not in objects:
                    objects.append(object)
            objects.append(
                CIRCLE(temporary_objects[0].coordinate,
                       abs(temporary_objects[0].coordinate - temporary_objects[1].coordinate),
                       {"type_dependencies": "two_points",
                        "depend_object": [temporary_objects[0], temporary_objects[1]],
                        "additional_restrictions": []}))
            withdrawal_special()


def deleting_objects_list(objests, key=lambda x: False):
    objests_1 = []
    for object in objests:
        if not key(object):
            objests_1.append(object)
    return objests_1


def withdrawal_special():
    """убирает все выделения с объектов"""
    global temporary_objects, objects
    for object in objects:
        if object.visibility == "special":
            object.visibility = "visible"
    temporary_objects = []
    objects = deleting_objects_list(objects, key=lambda x: x.existence == "death")


def mod_moving_object(event_mousebuttondown):
    if not temporary_objects:
        if event_mousebuttondown.type == MOUSEBUTTONDOWN:
            if event_mousebuttondown.button == 1:
                coordinates = display_flatness(event_mousebuttondown.pos)
                point = position_point(coordinates, consider_intersections=False, consider_object=False)
                if point in objects:
                    point.visibility = "special"
                    temporary_objects.append(point)
    else:
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            update_POINT(temporary_objects[0], new_coordinate=display_flatness(event_mousebuttondown.pos))
            for object in objects:
                update_OBJECT(object)
        else:
            withdrawal_special()


def mod_deletion(event_mousebuttondown):
    coordinates = display_flatness(event_mousebuttondown.pos)
    point = position_point(coordinates)
    if point in objects:
        point.existence = "death"
    elif point.dependencies["depend_object"]:
        point.dependencies["depend_object"][0].existence = "death"
    for object in objects:
        update_OBJECT(object)
    withdrawal_special()


def mod_visible_invisible(event_mousebuttondown):
    coordinates = display_flatness(event_mousebuttondown.pos)
    point = position_point(coordinates)
    if point in objects:
        if point.visibility == "visible":
            point.visibility = "invisible"
        else:
            point.visibility = "visible"
    elif point.dependencies["depend_object"]:
        if point.dependencies["depend_object"][0].visibility == "visible":
            point.dependencies["depend_object"][0].visibility = "invisible"
        else:
            point.dependencies["depend_object"][0].visibility = "visible"
    withdrawal_special()


def distribution_mod_event(event_mousebuttondown):
    """распределение по запуску функции опредленного мода"""
    if mod_program == "POINT":
        if event_mousebuttondown.type == MOUSEBUTTONDOWN:
            mod_point(event_mousebuttondown)
    elif mod_program == "LINE":
        if event_mousebuttondown.type == MOUSEBUTTONDOWN:
            mod_line(event_mousebuttondown)
    elif mod_program == "ZOOM":
        mod_zoom(event_mousebuttondown)
    elif mod_program == "CIRCLE":
        if event_mousebuttondown.type == MOUSEBUTTONDOWN:
            mod_circle(event_mousebuttondown)
    elif mod_program == "MOVING_OBJECT":
        mod_moving_object(event_mousebuttondown)
    elif mod_program == "DELETION":
        if event_mousebuttondown.type == MOUSEBUTTONDOWN:
            mod_deletion(event_mousebuttondown)
    elif mod_program == "VISIBLE/INVISIBLE":
        if event_mousebuttondown.type == MOUSEBUTTONDOWN:
            mod_visible_invisible(event_mousebuttondown)


def distribution_mod_not_event():
    if mod_program == "ZOOM":
        mod_zoom_moving()


def draw_POINT(object: POINT):
    """прорисовка точки"""
    if object.visibility == "visible":
        if object.existence:
            if not object.fixity:
                draw_circle(window,
                            list(map(round, flatness_display(object.coordinate))), 4, True,
                            (int(object.colors[0] / 3), int(object.colors[1] / 3), int(object.colors[2] / 3)))
            else:
                draw_circle(window,
                            list(map(round, flatness_display(object.coordinate))), 3, True,
                            (object.colors[0] // 3, object.colors[1] // 3, object.colors[2] // 3))
    elif object.visibility == "special":
        if object.existence:
            if not object.fixity:
                draw_circle(window,
                            list(map(round, flatness_display(object.coordinate))), 4, True,
                            (int(object.colors[0] / 3.5), int(object.colors[1] / 3.5), int(object.colors[2] / 3.5)))
                draw_circle(window,
                            list(map(round, flatness_display(object.coordinate))), 7, False,
                            (int(object.colors[0] / 3.5), int(object.colors[1] / 3.5), int(object.colors[2] / 3.5)))
            else:
                draw_circle(window,
                            list(map(round, flatness_display(object.coordinate))), 3, True,
                            (int(object.colors[0] / 3.5), int(object.colors[1] / 3.5), int(object.colors[2] / 3.5)))
                draw_circle(window,
                            list(map(round, flatness_display(object.coordinate))), 6, False,
                            (int(object.colors[0] / 3.5), int(object.colors[1] / 3.5), int(object.colors[2] / 3.5)))
    elif object.visibility == "invisible" and mod_program == "VISIBLE/INVISIBLE":
        if object.existence:
            if not object.fixity:
                draw_circle(window,
                            list(map(round, flatness_display(object.coordinate))), 4, True,
                            (int(object.colors[0] / 1.7), int(object.colors[1] / 1.7), int(object.colors[2] / 1.7)))
            else:
                draw_circle(window,
                            list(map(round, flatness_display(object.coordinate))), 3, True,
                            (int(object.colors[0] / 1.7), int(object.colors[1] / 1.7), int(object.colors[2] / 1.7)))


def draw_LINE(object: LINE):
    """прорисовка прямой"""
    if object.visibility == "visible":
        if object.existence:
            aaline_mod(window, object,
                       (int(object.colors[0] / 3.5), int(object.colors[1] / 3.5), int(object.colors[2] / 3.5)),
                       thickness=1)
    elif object.visibility == "invisible" and mod_program == "VISIBLE/INVISIBLE":
        if object.existence:
            aaline_mod(window, object,
                       (int(object.colors[0] / 1.7), int(object.colors[1] / 1.7), int(object.colors[2] / 1.7)),
                       thickness=1)


def draw_CIRCLE(object: CIRCLE):
    """прорисовка окружности"""
    if object.visibility == "visible":
        if object.existence:
            draw_circle(window, list(map(round, flatness_display(object.coordinate_centre))),
                        round(object.radius / complex_plane.dimension), False,
                        (int(object.colors[0] / 3.5), int(object.colors[1] / 3.5), int(object.colors[2] / 3.5)))
    elif object.visibility == "invisible" and mod_program == "VISIBLE/INVISIBLE":
        if object.existence:
            draw_circle(window, list(map(round, flatness_display(object.coordinate_centre))),
                        round(object.radius / complex_plane.dimension), False,
                        (int(object.colors[0] / 1.7), int(object.colors[1] / 1.7), int(object.colors[2] / 1.7)))


def rendering():
    """отрисовывает заданные объекты"""
    # прописать функции отрисовки каждого объекта по отдельности
    for object in objects + temporary_objects:
        if type(object) == POINT:
            draw_POINT(object)
        if type(object) == LINE:
            draw_LINE(object)
        if type(object) == CIRCLE:
            draw_CIRCLE(object)


if __name__ == '__main__':
    pygame.init()
    main_run = True

    mod_program = "POINT"
    complex_plane = flatness()
    objects = []  # все объекты в порядке сохдания
    temporary_objects = []  # временные объекты

    while main_run:
        fps = 60
        clock = pygame.time.Clock()
        running = True
        while running:
            distribution_mod_not_event()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    main_run = False
                elif event.type == pygame.KEYDOWN:
                    changing_mod(event.key)
                else:  # event.type == MOUSEBUTTONDOWN:
                    distribution_mod_event(event)

            window.fill((255, 255, 255))

            # добавить отрисовку
            rendering()

            text = mod_program
            text = pygame.font.Font(pygame.font.match_font("arial"), 14).render(text, 1, (100, 0, 0))
            window.blit(text, text.get_rect(topright=(595, 5)))

            pygame.display.flip()
            # if clock.get_fps()<300:
            #     print(clock.get_fps())
            clock.tick(fps)
pygame.quit()
