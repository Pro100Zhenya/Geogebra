from pygame.locals import *
from pygame import gfxdraw
from functions import *
from test_button import *

pygame.init()

width, height = (1000, 700)  # ширина,высота экрана
window = pygame.display.set_mode((width, height))
window.fill((255, 255, 255))


def check_short(x):
    if -32700 < x < 32700:
        return True
    return False


def draw_circle(surface, coord, radius, filling: bool, color, thickness=1):
    """рисует круг"""

    x, y = coord
    for i in range(thickness):
        if check_short(x) and check_short(y) and check_short(radius):
            gfxdraw.aacircle(surface, x, y, radius + (-1) ** i * (i // 2), color)
    if filling:
        gfxdraw.filled_circle(surface, x, y, radius, color)


def aaline_mod(surface, line: LINE, color, thickness=1):
    if line.type_line == "straight":
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
    if line.type_line == "segment":
        for i in range(thickness):
            pygame.draw.aaline(surface, color, list(
                map(round, flatness_display(line.X + (-1) ** i * complex_plane.dimension * i // 2))), list(
                map(round, flatness_display(line.Y + (-1) ** i * complex_plane.dimension * i // 2))))


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
    elif event == pygame.K_8:
        mod_program = "MIDDLE_POINT"
    elif event == pygame.K_9:
        mod_program = "PERPENDICULAR_LINE"
    elif event == pygame.K_q:
        mod_program = "MIDDLE_LINE"


def position_point(coordinates: complex, consider_point=True, consider_intersections=True, consider_object=True):
    """вычисляет положение точки (с учетом пересечений и принадлежностей)"""
    point = False
    inaccuracy_POINT = 16  # в пикселях
    if consider_point and not point:
        for object in objects:
            if object.visibility != "invisible" or mod_program == "VISIBLE_INVISIBLE":
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
                if (objects[i].visibility != "invisible" and objects[j].visibility != "invisible") \
                        or mod_program == "VISIBLE_INVISIBLE":
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
            if objects[i].visibility != "invisible" or mod_program == "VISIBLE_INVISIBLE":
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


def mod_segment(event_mousebuttondown):
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
                      "additional_restrictions": []}, type_line="segment"))
            withdrawal_special()


def mod_zoom(event_mousebuttondown):
    """мод изменения ..."""  # забыл слово
    if event_mousebuttondown.type == MOUSEBUTTONDOWN:
        if event.button == 1:  # левая кнопка мыши
            if complex_plane.dimension > 10:
                complex_plane.update(
                    left_top_coordinate=complex_plane.left_top_coordinate + (
                            1 - 1 / complex_plane.zoom_constant) * complex(
                        event_mousebuttondown.pos[0], event_mousebuttondown.pos[1]) * complex_plane.dimension,
                    dimension=complex_plane.dimension / complex_plane.zoom_constant)
        if event.button == 3:  # правая кнопка мыши
            if complex_plane.dimension < 10 ** 5:
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


def mod_middle_point(event_mousebuttondown):
    if not temporary_objects:
        coordinates = display_flatness(event_mousebuttondown.pos)
        point = position_point(coordinates)
        point.visibility = "special"
        temporary_objects.append(point)
    else:
        coordinates = display_flatness(event_mousebuttondown.pos)
        point = position_point(coordinates)
        if point.coordinate != temporary_objects[0].coordinate:
            temporary_objects.append(point)
        if len(temporary_objects) == 2:
            for object in temporary_objects:
                if object not in objects:
                    objects.append(object)
            point_components = middle_point(temporary_objects[0], temporary_objects[1])
            objects.append(
                POINT(point_components[0], point_components[1], fixity=True))
            withdrawal_special()


def mod_perpendicular_line(event_mousebuttondown):
    if not temporary_objects:
        coordinates = display_flatness(event_mousebuttondown.pos)
        point = position_point(coordinates)
        point.visibility = "special"
        temporary_objects.append(point)
    else:
        coordinates = display_flatness(event_mousebuttondown.pos)
        point = position_point(coordinates, consider_point=False, consider_intersections=False)
        if point.dependencies["depend_object"] and type(point.dependencies["depend_object"][0]) == LINE:
            temporary_objects.append(point.dependencies["depend_object"][0])
        if len(temporary_objects) == 2:
            for object in temporary_objects:
                if object not in objects:
                    objects.append(object)
            line_components = perpendicular_line(temporary_objects[0], temporary_objects[1])
            objects.append(LINE(line_components[0], line_components[1], line_components[2]))
            withdrawal_special()


def mod_middle_line(event_mousebuttondown):
    if not temporary_objects:
        coordinates = display_flatness(event_mousebuttondown.pos)
        point = position_point(coordinates)
        point.visibility = "special"
        temporary_objects.append(point)
    else:
        coordinates = display_flatness(event_mousebuttondown.pos)
        point = position_point(coordinates)
        if point.coordinate != temporary_objects[0].coordinate:
            temporary_objects.append(point)
        if len(temporary_objects) == 2:
            for object in temporary_objects:
                if object not in objects:
                    objects.append(object)
            line_components = middle_line(temporary_objects[0], temporary_objects[1])
            objects.append(LINE(line_components[0], line_components[1], line_components[2]))
            withdrawal_special()


def mod_circle_tree_points(event_mousebuttondown):
    if len(temporary_objects) < 3:
        flag_add = True
        coordinates = display_flatness(event_mousebuttondown.pos)
        point = position_point(coordinates)
        for object in temporary_objects:
            if object.coordinate == point.coordinate:
                flag_add = False
                break
        if flag_add:
            point.visibility = "special"
            temporary_objects.append(point)
    if len(temporary_objects) == 3:
        for object in temporary_objects:
            if object not in objects:
                objects.append(object)
        circle_components = circle_tree_points(temporary_objects[0], temporary_objects[1], temporary_objects[2])
        objects.append(CIRCLE(circle_components[0], circle_components[1], circle_components[2]))
        withdrawal_special()


def mod_bisector(event_mousebuttondown):
    if len(temporary_objects) < 3:
        coordinates = display_flatness(event_mousebuttondown.pos)
        point = position_point(coordinates)
        if len(temporary_objects) == 0 or temporary_objects[-1].coordinate != point.coordinate:
            point.visibility = "special"
            temporary_objects.append(point)
    if len(temporary_objects) == 3:
        for object in temporary_objects:
            if object not in objects:
                objects.append(object)
        line_components = bisector(temporary_objects[0], temporary_objects[1], temporary_objects[2])
        objects.append(LINE(line_components[0], line_components[1], line_components[2]))
        withdrawal_special()


def mod_tangents(event_mousebuttondown):
    if not temporary_objects:
        coordinates = display_flatness(event_mousebuttondown.pos)
        point = position_point(coordinates)
        point.visibility = "special"
        temporary_objects.append(point)
    else:
        coordinates = display_flatness(event_mousebuttondown.pos)
        point = position_point(coordinates, consider_point=False, consider_intersections=False)
        if point.dependencies["depend_object"] and type(point.dependencies["depend_object"][0]) == CIRCLE:
            temporary_objects.append(point.dependencies["depend_object"][0])
        if len(temporary_objects) == 2:
            for object in temporary_objects:
                if object not in objects:
                    objects.append(object)
            lines_components = tangents(temporary_objects[0], temporary_objects[1])
            objects.append(LINE(lines_components[0][0], lines_components[0][1], lines_components[0][2],
                                existence=lines_components[0][3]))
            objects.append(LINE(lines_components[1][0], lines_components[1][1], lines_components[1][2],
                                existence=lines_components[1][3]))
            withdrawal_special()


def mod_parallel_line(event_mousebuttondown):
    if not temporary_objects:
        coordinates = display_flatness(event_mousebuttondown.pos)
        point = position_point(coordinates)
        point.visibility = "special"
        temporary_objects.append(point)
    else:
        coordinates = display_flatness(event_mousebuttondown.pos)
        point = position_point(coordinates, consider_point=False, consider_intersections=False)
        if point.dependencies["depend_object"] and type(point.dependencies["depend_object"][0]) == LINE:
            temporary_objects.append(point.dependencies["depend_object"][0])
        if len(temporary_objects) == 2:
            for object in temporary_objects:
                if object not in objects:
                    objects.append(object)
            line_components = parallel_line(temporary_objects[0], temporary_objects[1])
            objects.append(LINE(line_components[0], line_components[1], line_components[2]))
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
    elif mod_program == "VISIBLE_INVISIBLE":
        if event_mousebuttondown.type == MOUSEBUTTONDOWN:
            mod_visible_invisible(event_mousebuttondown)
    elif mod_program == "MIDDLE_POINT":
        if event_mousebuttondown.type == MOUSEBUTTONDOWN:
            mod_middle_point(event_mousebuttondown)
    elif mod_program == "PERPENDICULAR_LINE":
        if event_mousebuttondown.type == MOUSEBUTTONDOWN:
            mod_perpendicular_line(event_mousebuttondown)
    elif mod_program == "MIDDLE_LINE":
        if event_mousebuttondown.type == MOUSEBUTTONDOWN:
            mod_middle_line(event_mousebuttondown)
    elif mod_program == "CIRCLE_THREE_POINTS":
        if event_mousebuttondown.type == MOUSEBUTTONDOWN:
            mod_circle_tree_points(event_mousebuttondown)
    elif mod_program == "BISECTOR":
        if event_mousebuttondown.type == MOUSEBUTTONDOWN:
            mod_bisector(event_mousebuttondown)
    elif mod_program == "TANGENTS":
        if event_mousebuttondown.type == MOUSEBUTTONDOWN:
            mod_tangents(event_mousebuttondown)
    elif mod_program == "PARALLEL_LINE":
        if event_mousebuttondown.type == MOUSEBUTTONDOWN:
            mod_parallel_line(event_mousebuttondown)
    elif mod_program == "SEGMENT":
        if event_mousebuttondown.type == MOUSEBUTTONDOWN:
            mod_segment(event_mousebuttondown)


def distribution_mod_not_event():
    if mod_program == "ZOOM":
        mod_zoom_moving()


def brightness_change(color, n: float):
    """измененение цвета"""
    return (round(255 - (255 - color[0]) / n), round(255 - (255 - color[1]) / n), round(255 - (255 - color[2]) / n))


def draw_POINT(object: POINT):
    """прорисовка точки"""
    if object.visibility == "visible":
        if object.existence:
            if not object.fixity:
                draw_circle(window,
                            list(map(round, flatness_display(object.coordinate))), 4, True,
                            brightness_change(object.colors, 1))
            else:
                draw_circle(window,
                            list(map(round, flatness_display(object.coordinate))), 3, True,
                            brightness_change(object.colors, 1))
    elif object.visibility == "special":
        if object.existence:
            if not object.fixity:
                draw_circle(window,
                            list(map(round, flatness_display(object.coordinate))), 4, True,
                            brightness_change(object.colors, 1))
                draw_circle(window,
                            list(map(round, flatness_display(object.coordinate))), 7, False,
                            brightness_change(object.colors, 1))
            else:
                draw_circle(window,
                            list(map(round, flatness_display(object.coordinate))), 3, True,
                            brightness_change(object.colors, 1))
                draw_circle(window,
                            list(map(round, flatness_display(object.coordinate))), 6, False,
                            brightness_change(object.colors, 1))
    elif object.visibility == "invisible" and mod_program == "VISIBLE_INVISIBLE":
        if object.existence:
            if not object.fixity:
                draw_circle(window,
                            list(map(round, flatness_display(object.coordinate))), 4, True,
                            brightness_change(object.colors, 3))
            else:
                draw_circle(window,
                            list(map(round, flatness_display(object.coordinate))), 3, True,
                            brightness_change(object.colors, 3))


def draw_LINE(object: LINE):
    """прорисовка прямой"""
    if object.visibility == "visible":
        if object.existence:
            aaline_mod(window, object,
                       brightness_change(object.colors, 1),
                       thickness=1)
    elif object.visibility == "special":
        if object.existence:
            aaline_mod(window, object,
                       brightness_change(object.colors, 1),
                       thickness=3)
    elif object.visibility == "invisible" and mod_program == "VISIBLE_INVISIBLE":
        if object.existence:
            aaline_mod(window, object,
                       brightness_change(object.colors, 3),
                       thickness=1)


def draw_CIRCLE(object: CIRCLE):
    """прорисовка окружности"""
    if object.visibility == "visible":
        if object.existence:
            draw_circle(window, list(map(round, flatness_display(object.coordinate_centre))),
                        round(object.radius / complex_plane.dimension), False,
                        brightness_change(object.colors, 1), thickness=1)
    elif object.visibility == "special":
        if object.existence:
            draw_circle(window, list(map(round, flatness_display(object.coordinate_centre))),
                        round(object.radius / complex_plane.dimension), False,
                        brightness_change(object.colors, 1), thickness=2)
    elif object.visibility == "invisible" and mod_program == "VISIBLE_INVISIBLE":
        if object.existence:
            draw_circle(window, list(map(round, flatness_display(object.coordinate_centre))),
                        round(object.radius / complex_plane.dimension), False,
                        brightness_change(object.colors, 3), thickness=1)


def creating_window():
    """отвечает за дизайн приложения"""

    construction_name_buttons = ["POINT", "LINE", "CIRCLE", "SEGMENT", "MIDDLE_POINT", "PERPENDICULAR_LINE",
                                 "PARALLEL_LINE", "MIDDLE_LINE", "CIRCLE_THREE_POINTS", "BISECTOR", "TANGENTS"]
    edit_name_buttons = ["MOVING_OBJECT", "ZOOM", "VISIBLE_INVISIBLE", "DELETION", "VISUAL"]
    construction_button = LIST_BUTTON(window, (0, 0), [width, 50],
                                      {"filling": (255, 255, 255), "border": (99, 99, 99), "border_radius": 4,
                                       "button_alignment": "left"})
    edit_button = LIST_BUTTON(window, (width - 50, 150), [width, 400],
                              {"filling": (255, 255, 255), "border": (99, 99, 99), "border_radius": 4,
                               "button_alignment": "top"})
    all_graphics_components.append(construction_button)
    all_graphics_components.append(edit_button)

    def action(self: BUTTON):
        global mod_program
        withdrawal_special()
        mod_program = self.styles[self.regim]["text"]
        for button in list_working_buttons:
            if button.regim == "Active":
                if button.left_top[0] <= pygame.mouse.get_pos()[0] <= button.right_lower[0] and \
                        button.left_top[1] <= pygame.mouse.get_pos()[1] <= button.right_lower[1]:
                    button.regim = "Hover"
                else:
                    button.regim = "Normal"

    for button in construction_name_buttons:
        styles_button = {
            "Normal": {"filling": (255, 255, 255), "border": (110, 110, 110), "border_radius": 4, "text": button,
                       "show_text": False, "photo": f"image_button/{button}.png", "show_photo": True},
            "Hover": {"filling": (255, 255, 255), "border": (142, 142, 255), "border_radius": 4, "text": button,
                      "show_text": False, "photo": f"image_button/{button}.png", "show_photo": True},
            "Active": {"filling": (255, 255, 255), "border": (80, 80, 255), "border_radius": 4, "text": button,
                       "show_text": False, "photo": f"image_button/{button}.png", "show_photo": True}}
        list_working_buttons.append(construction_button.add_button([styles_button, action, lambda x: False]))
    for button in edit_name_buttons:
        styles_button = {
            "Normal": {"filling": (255, 255, 255), "border": (110, 110, 110), "border_radius": 4, "text": button,
                       "show_text": False, "photo": f"image_button/{button}.png", "show_photo": True},
            "Hover": {"filling": (255, 255, 255), "border": (142, 142, 255), "border_radius": 4, "text": button,
                      "show_text": False, "photo": f"image_button/{button}.png", "show_photo": True},
            "Active": {"filling": (255, 255, 255), "border": (80, 80, 255), "border_radius": 4, "text": button,
                       "show_text": False, "photo": f"image_button/{button}.png", "show_photo": True}}
        list_working_buttons.append(edit_button.add_button([styles_button, action, lambda x: False]))


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

    list_working_buttons = []
    all_graphics_components = []
    working_buttons_surf = pygame.Surface((width, height))
    creating_window()
    for list_button in all_graphics_components:
        list_button.draw()

    while main_run:
        fps = 500
        clock = pygame.time.Clock()
        running = True
        while running:
            distribution_mod_not_event()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    main_run = False
                elif not any([list_button.update(event) for list_button in all_graphics_components]):
                    if event.type == pygame.KEYDOWN:
                        pass
                    else:
                        distribution_mod_event(event)

            window.fill((255, 255, 255))

            # добавить отрисовку
            rendering()

            for list_button in all_graphics_components:
                list_button.draw()

            pygame.display.flip()
            clock.tick()
pygame.quit()
