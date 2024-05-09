from classes import *
import cmath


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
        z = (c_2 * m_1 - c_1 * m_2) / (0 + 0.000001j)
    imaginary = False
    if point_belongs_line(z, line_1) and point_belongs_line(z, line_2):
        imaginary = True
    return [[z, imaginary, ""]]  # точка пересечения и ее мнимость


def intersections_line_circle(line: LINE, circle: CIRCLE):
    """пересечение прямой и окружности"""
    inaccuracy = 0.00000001
    m, c, z_0, r_0 = line.formula[0], line.formula[1], circle.coordinate_centre, circle.radius
    D = (m * z_0.conjugate() + m.conjugate() * z_0 + c) ** 2 - 4 * m * m.conjugate() * r_0 ** 2
    z_1 = (-(m * z_0.conjugate() + m.conjugate() * z_0 + c) + D ** 0.5) / (2 * m.conjugate())
    z_2 = (-(m * z_0.conjugate() + m.conjugate() * z_0 + c) - D ** 0.5) / (2 * m.conjugate())
    z = nearest_point_object(z_0, line)[0]
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
    """пересечение прямой и окружности"""
    inaccuracy = 0.00000001
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
    inaccuracy = 0.00000001
    if not abs(z * line.formula[0].conjugate() + z.conjugate() * line.formula[0] + line.formula[1]) <= inaccuracy:
        return False
    if line.type_line == "straight":
        return True
    if line.type_line == "section":
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
            circle.radius = max(abs(
                circle.dependencies["depend_object"][1].coordinate - circle.dependencies["depend_object"][
                    0].coordinate), 0.000001)


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


def right_point(point: POINT, object_1, object_2):
    inaccuracy = 0.00000001
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
    elif point.dependencies["type_dependencies"] == "none":
        if new_coordinate and not point.fixity:
            point.coordinate = new_coordinate
    elif point.dependencies["type_dependencies"] == "belong":
        if new_coordinate and not point.fixity:
            point.coordinate = nearest_point_object(new_coordinate, point.dependencies["depend_object"][0])[0]
        else:
            point.coordinate = nearest_point_object(point.coordinate, point.dependencies["depend_object"][0])[0]


def update_OBJECT(object):
    if type(object) == POINT:
        update_POINT(object)
    if type(object) == CIRCLE:
        update_CIRCLE(object)
    if type(object) == LINE:
        update_LINE(object)
