from classes import *
import cmath

inaccuracy = 1


def nearest_point_object(coordinate: complex, object):
    """ближайшая точка на объекте и расстояние до нее от данной точки"""
    if type(object) == LINE:
        return nearest_point_line(coordinate, object)
    if type(object) == CIRCLE:
        return nearest_point_circle(coordinate, object)


def nearest_point_line(coordinate: complex, line: LINE):
    """ближайшая точка на прямой"""
    z = (line.formula[0].conjugate() * coordinate - line.formula[0] * coordinate.conjugate() -
         line.formula[1]) / (2 * line.formula[0].conjugate())
    return [z, point_belongs_line(z, line)]


def nearest_point_circle(coordinate: complex, circle: CIRCLE):
    """ближайшая точка на окружности"""
    if coordinate == circle.coordinate_centre:
        return [circle.coordinate_centre + circle.radius, True]
    z = sorted(
        intersections_line_circle(LINE(coordinate, circle.coordinate_centre, {"свойств": "нет"}), circle),
        key=lambda x: abs(x[0] - coordinate))[0]
    return z


def intersections_object_object(object_1, object_2):
    """точка пересечения каких-то двух объектов"""
    # дописать
    if type(object_1) == LINE:
        if type(object_2) == LINE:
            return intersections_line_line(object_1, object_2)
        if type(object_2) == CIRCLE:
            return intersections_line_circle(object_1, object_2)
    if type(object_1) == CIRCLE:
        if type(object_2) == LINE:
            return intersections_line_circle(object_2, object_1)
        if type(object_2) == CIRCLE:
            return intersections_circle_circle(object_1, object_2)


def intersections_line_line(line_1: LINE, line_2: LINE):
    """пересечение двух прямых"""
    m_1, c_1 = line_1.formula
    m_2, c_2 = line_2.formula
    if m_2 * m_1.conjugate() - m_1 * m_2.conjugate() != 0:
        z = (c_2 * m_1 - c_1 * m_2) / (m_2 * m_1.conjugate() - m_1 * m_2.conjugate())
    else:
        z = (c_2 * m_1 - c_1 * m_2) * (0 + 100000000j)
    imaginary = False
    if point_belongs_line(z, line_1) and point_belongs_line(z, line_2):
        imaginary = True
    return [[z, imaginary, ""]]  # точка пересечения и ее мнимость


def intersections_line_circle(line: LINE, circle: CIRCLE):
    """пересечение прямой и окружности"""
    m, c, z_0, r_0 = line.formula[0], line.formula[1], circle.coordinate_centre, circle.radius
    D = (m * z_0.conjugate() + m.conjugate() * z_0 + c) ** 2 - 4 * m * m.conjugate() * r_0 ** 2
    z_1 = (-(m * z_0.conjugate() + m.conjugate() * z_0 + c) + D ** 0.5) / (2 * m.conjugate())
    z_2 = (-(m * z_0.conjugate() + m.conjugate() * z_0 + c) - D ** 0.5) / (2 * m.conjugate())
    if r_0 - inaccuracy <= abs(z_1) <= r_0 + inaccuracy and point_belongs_line(z_1 + z_0, line):
        return [[z_1 + z_0, True, difference_point(z_1 + z_0, line) - difference_point(z_2 + z_0, line)],
                [z_2 + z_0, True, difference_point(z_2 + z_0, line) - difference_point(z_1 + z_0, line)]]
    else:
        return [[z_1 + z_0, False, difference_point(z_1 + z_0, line) - difference_point(z_2 + z_0, line)],
                [z_2 + z_0, False, difference_point(z_2 + z_0, line) - difference_point(z_1 + z_0, line)]]


def difference_point(coordinate: complex, line: LINE):
    if ((coordinate - line.X) / (line.Y - line.X)).real < 0:
        return -abs(coordinate - line.X)
    return abs(coordinate - line.X)


def intersections_circle_circle(circle_1: CIRCLE, circle_2: CIRCLE):
    """пересечение окружностей"""
    z_1, r_1 = circle_1.coordinate_centre, circle_1.radius
    z_2, r_2 = circle_2.coordinate_centre, circle_2.radius
    m = z_2 - z_1
    if m == 0:
        return [[z_1, False, 0], [z_1, False, 0]]
    else:
        a = -m.conjugate()
        b = m * m.conjugate() + r_1 ** 2 - r_2 ** 2
        c = -m * r_1 ** 2
        D = b ** 2 - 4 * a * c
        Z_1 = (-b + D ** 0.5) / (2 * a)
        Z_2 = (-b - D ** 0.5) / (2 * a)
        if r_1 - inaccuracy <= abs(Z_1) <= r_1 + inaccuracy:
            return [[Z_1 + z_1, True, cmath.phase((z_1 - z_2) / (Z_1 + z_1 - z_2))],
                    [Z_2 + z_1, True, cmath.phase((z_1 - z_2) / (Z_2 + z_1 - z_2))]]
        else:
            return [[Z_1 + z_1, False, cmath.phase((z_1 - z_2) / (Z_1 + z_1 - z_2))],
                    [Z_2 + z_1, False, cmath.phase((z_1 - z_2) / (Z_2 + z_1 - z_2))]]


def point_belongs_line(z: complex, line: LINE):
    """проверяет принадлежит ли точка какой-то части прямой"""
    if not abs(z * line.formula[0].conjugate() + z.conjugate() * line.formula[0] + line.formula[1]) \
           / (2 * abs(line.formula[0])) <= inaccuracy:
        return False
    if line.type_line == "straight":
        return True
    if line.type_line == "segment":
        if min(line.X.real, line.Y.real) <= z.real <= max(line.X.real, line.Y.real) and min(line.X.imag, line.Y.imag) \
                <= z.imag <= max(line.X.imag, line.Y.imag):
            return True
        return False


def update_CIRCLE(circle: CIRCLE):
    """изменение свойств объекта"""
    # dependencies = {"type_dependencies": "...", "depend_object": [], "additional_restrictions": [],"fixity":"..."}
    for object in circle.dependencies["depend_object"]:
        if object.existence == "death":
            circle.existence = object.existence
    if circle.existence != "death":
        circle.existence = True
        for object in circle.dependencies["depend_object"]:
            if not object.existence:
                circle.existence = False
    if circle.dependencies["type_dependencies"] == "two_points":
        if circle.existence != "death" and circle.existence:
            circle.coordinate_centre = circle.dependencies["depend_object"][0].coordinate
            circle.radius = max(abs(circle.dependencies["depend_object"][1].coordinate -
                                    circle.dependencies["depend_object"][0].coordinate), 0.000001)
    elif circle.dependencies["type_dependencies"] == "circle_tree_points":
        if circle.existence != "death" and circle.existence:
            point_1, point_2, point_3 = circle.dependencies["depend_object"]
            if point_1.coordinate != point_2.coordinate and point_2.coordinate != point_3.coordinate and \
                    point_3.coordinate != point_1.coordinate:
                circle_components = circle_tree_points(point_1, point_2, point_3)
                circle.coordinate_centre = circle_components[0]
                circle.radius = circle_components[1]


def update_LINE(line: LINE):
    """изменение свойств объекта"""
    # dependencies = {"type_dependencies": "...", "depend_object":[],"additional_restrictions":[]}
    for object in line.dependencies["depend_object"]:
        if object.existence == "death":
            line.existence = object.existence
    if line.existence != "death":
        line.existence = True
        for object in line.dependencies["depend_object"]:
            if not object.existence:
                line.existence = False
    if line.dependencies["type_dependencies"] == "two_points":
        if line.existence != "death" and line.existence:
            line.X = line.dependencies["depend_object"][0].coordinate
            if line.X != line.dependencies["depend_object"][1].coordinate:
                line.Y = line.dependencies["depend_object"][1].coordinate
            line.formula = [(line.Y - line.X) * complex(0, 1),
                            complex(0, 1) * (line.X * line.Y.conjugate() - line.Y * line.X.conjugate())]
    elif line.dependencies["type_dependencies"] == "perpendicular_line":
        if line.existence != "death" and line.existence:
            line_components = perpendicular_line(line.dependencies["depend_object"][0],
                                                 line.dependencies["depend_object"][1])
            line.X = line_components[0]
            line.Y = line_components[1]
            line.formula_update()
    elif line.dependencies["type_dependencies"] == "middle_line":
        if line.existence != "death" and line.existence:
            line_components = middle_line(line.dependencies["depend_object"][0], line.dependencies["depend_object"][1])
            line.X = line_components[0]
            if line.X != line.dependencies["depend_object"][1].coordinate:
                line.Y = line_components[1]
            line.formula_update()
    elif line.dependencies["type_dependencies"] == "bisector":
        if line.existence != "death" and line.existence:
            point_1, point_2, point_3 = line.dependencies["depend_object"]
            if point_1.coordinate != point_2.coordinate and point_2.coordinate != point_3.coordinate:
                line_components = bisector(point_1, point_2, point_3)
                line.X = line_components[0]
                line.Y = line_components[1]
                line.formula_update()
    elif line.dependencies["type_dependencies"] == "tangents":
        if line.existence != "death" and line.existence:
            point, circle = line.dependencies["depend_object"]
            lines_components = tangents(point, circle)
            if lines_components[0][2]["additional_restrictions"][0] * line.dependencies["additional_restrictions"][
                0] >= 0:
                lines_components = lines_components[0]
            else:
                lines_components = lines_components[1]
            line.X = lines_components[0]
            line.Y = lines_components[1]
            line.existence = lines_components[3]
            line.formula_update()
    elif line.dependencies["type_dependencies"] == "parallel_line":
        if line.existence != "death" and line.existence:
            line_components = parallel_line(line.dependencies["depend_object"][0],
                                            line.dependencies["depend_object"][1])
            line.X = line_components[0]
            line.Y = line_components[1]
            line.formula_update()


def right_point(point: POINT, object_1, object_2):
    possible_point = intersections_object_object(object_1, object_2)
    if type(object_1) == LINE:
        if type(object_2) == LINE:
            return possible_point[0]
        if type(object_2) == CIRCLE:
            common_point = False
            for point_check in object_1.dependencies["depend_object"]:
                if object_2 in point_check.dependencies["depend_object"] or point_check == \
                        object_2.dependencies["depend_object"][1]:
                    common_point = point_check
            point_check = object_2.dependencies["depend_object"][1]
            if object_1 in point_check.dependencies["depend_object"]:
                common_point = point_check
            if common_point:
                if abs(common_point.coordinate - possible_point[0][0]) <= inaccuracy:
                    return possible_point[1]
                return possible_point[0]
            else:
                if point.dependencies["additional_restrictions"][0] * (
                        difference_point(possible_point[0][0], object_1) - difference_point(possible_point[1][0],
                                                                                            object_1)) >= 0:
                    return possible_point[0]
                return possible_point[1]
    if type(object_1) == CIRCLE:
        if type(object_2) == LINE:
            common_point = False
            for point_check in object_2.dependencies["depend_object"]:
                if object_1 in point_check.dependencies["depend_object"] or point_check == \
                        object_1.dependencies["depend_object"][1]:
                    common_point = point_check
            point_check = object_1.dependencies["depend_object"][1]
            if object_2 in point_check.dependencies["depend_object"]:
                common_point = point_check
            if common_point:
                if abs(common_point.coordinate - possible_point[0][0]) <= inaccuracy:
                    return possible_point[1]
                return possible_point[0]
            else:
                if point.dependencies["additional_restrictions"][0] * (
                        difference_point(possible_point[0][0], object_2) - difference_point(possible_point[1][0],
                                                                                            object_2)) >= 0:
                    return possible_point[0]
                return possible_point[1]
        if type(object_2) == CIRCLE:
            common_point = False
            # for point_check in object_2.dependencies["depend_object"][1]:
            point_check = object_2.dependencies["depend_object"][1]
            if object_1 in point_check.dependencies["depend_object"] or point_check == \
                    object_1.dependencies["depend_object"][1]:
                common_point = point_check
            # for point_check in object_1.dependencies["depend_object"][1]:
            point_check = object_1.dependencies["depend_object"][1]
            if object_2 in point_check.dependencies["depend_object"] or point_check == \
                    object_2.dependencies["depend_object"][1]:
                common_point = point_check
            if common_point:
                if abs(common_point.coordinate - possible_point[0][0]) <= inaccuracy:
                    return possible_point[1]
                return possible_point[0]
            else:
                if point.dependencies["additional_restrictions"][0] * cmath.phase(
                        (object_1.coordinate_centre - object_2.coordinate_centre) / (
                                possible_point[0][0] - object_2.coordinate_centre)) >= 0:
                    return possible_point[0]
                return possible_point[1]


def update_POINT(point: POINT, new_coordinate=False):
    """изменение свойств объекта"""
    # dependencies = {"type_dependencies": "...", "depend_object":[],"additional_restrictions":[]}
    for object in point.dependencies["depend_object"]:
        if object.existence == "death":
            point.existence = "death"
    if point.existence != "death":
        point.existence = True
        for object in point.dependencies["depend_object"]:
            if not object.existence:
                point.existence = False
    if point.dependencies["type_dependencies"] == "intersection":
        if point.existence != "death" and point.existence:
            possible_point = right_point(point, point.dependencies["depend_object"][0],
                                         point.dependencies["depend_object"][1])
            point.coordinate = possible_point[0]
            if not possible_point[1]:
                point.existence = False
    elif point.dependencies["type_dependencies"] == "middle_point":
        if point.existence != "death" and point.existence:
            point.coordinate = (point.dependencies["depend_object"][0].coordinate +
                                point.dependencies["depend_object"][1].coordinate) / 2
    elif point.dependencies["type_dependencies"] == "none":
        if new_coordinate and not point.fixity:
            point.coordinate = new_coordinate
    elif point.dependencies["type_dependencies"] == "belong":
        if new_coordinate and not point.fixity:
            if type(point.dependencies["depend_object"][0]) == LINE:
                point.existence = point_belongs_line(
                    nearest_point_object(new_coordinate, point.dependencies["depend_object"][0])[0],
                    point.dependencies["depend_object"][0])
            point.coordinate = nearest_point_object(new_coordinate, point.dependencies["depend_object"][0])[0]
        else:
            if type(point.dependencies["depend_object"][0]) == LINE:
                point.existence = point_belongs_line(
                    nearest_point_object(point.coordinate, point.dependencies["depend_object"][0])[0],
                    point.dependencies["depend_object"][0])
            point.coordinate = nearest_point_object(point.coordinate, point.dependencies["depend_object"][0])[0]


def update_OBJECT(object):
    if type(object) == POINT:
        update_POINT(object)
    if type(object) == CIRCLE:
        update_CIRCLE(object)
    if type(object) == LINE:
        update_LINE(object)


def middle_line(point_1: POINT, point_2: POINT):
    return [(point_1.coordinate + point_2.coordinate) / 2,
            (point_1.coordinate + point_2.coordinate) / 2 - (point_1.coordinate - point_2.coordinate) * complex(0, 1),
            {"type_dependencies": "middle_line", "depend_object": [point_1, point_2], "additional_restrictions": []}]


def perpendicular_line(point: POINT, line: LINE):
    return [point.coordinate, point.coordinate - line.formula[0],
            {"type_dependencies": "perpendicular_line", "depend_object": [point, line], "additional_restrictions": []}]


def middle_point(point_1: POINT, point_2: POINT):
    return [(point_1.coordinate + point_2.coordinate) / 2,
            {"type_dependencies": "middle_point", "depend_object": [point_1, point_2], "additional_restrictions": []}]


def circle_tree_points(point_1: POINT, point_2: POINT, point_3: POINT):
    middle_line_12 = middle_line(point_1, point_2)
    middle_line_12 = LINE(middle_line_12[0], middle_line_12[1], middle_line_12[2])
    middle_line_23 = middle_line(point_2, point_3)
    middle_line_23 = LINE(middle_line_23[0], middle_line_23[1], middle_line_23[2])
    coordinate_centre = intersections_object_object(middle_line_12, middle_line_23)[0][0]
    return [coordinate_centre, abs(coordinate_centre - point_1.coordinate),
            {"type_dependencies": "circle_tree_points", "depend_object": [point_1, point_2, point_3],
             "additional_restrictions": []}]


def bisector(point_1: POINT, point_2: POINT, point_3: POINT):
    direction_bisector = cmath.sqrt(
        (point_1.coordinate - point_2.coordinate) * (point_3.coordinate - point_2.coordinate))
    return [point_2.coordinate, point_2.coordinate + direction_bisector,
            {"type_dependencies": "bisector", "depend_object": [point_1, point_2, point_3],
             "additional_restrictions": []}]


def tangents(point: POINT, circle: CIRCLE):
    points = intersections_object_object(CIRCLE((point.coordinate + circle.coordinate_centre) / 2,
                                                abs((point.coordinate - circle.coordinate_centre) / 2), {}), circle)
    if -inaccuracy <= abs(point.coordinate - circle.coordinate_centre) - circle.radius <= inaccuracy:
        points[0][0] = perpendicular_line(point, LINE(point.coordinate, circle.coordinate_centre, {}))[1]
        points[1][0] = perpendicular_line(point, LINE(point.coordinate, circle.coordinate_centre, {}))[1]
        points[0][1] = True
        points[1][1] = True
    return [[point.coordinate, points[0][0],
             {"type_dependencies": "tangents", "depend_object": [point, circle],
              "additional_restrictions": [points[0][2]]}, points[0][1]],
            [point.coordinate, points[1][0], {"type_dependencies": "tangents", "depend_object": [point, circle],
                                              "additional_restrictions": [points[1][2]]}, points[1][1]]]


def parallel_line(point: POINT, line: LINE):
    return [point.coordinate, point.coordinate - line.formula[0] * complex(0, 1),
            {"type_dependencies": "parallel_line", "depend_object": [point, line], "additional_restrictions": []}]
