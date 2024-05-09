class flatness:
    """класс координатной плоскости"""

    def __init__(self):
        self.left_top_coordinate = complex(0, 0)  # координата левого верхнего угла
        self.dimension = 1  # размер одного пикселя в координатах\
        self.zoom_constant = 1.6

    def update(self, left_top_coordinate=False, dimension=False):
        """изменение видимой части плоскости"""
        if left_top_coordinate:
            self.left_top_coordinate = left_top_coordinate
        if dimension:
            self.dimension = dimension


class POINT:
    """класс точки"""

    def __init__(self, coordinate, dependencies: dict, colors=(255,255,255), visibility="visible", fixity=False,
                 existence=True):
        self.coordinate = coordinate
        self.visibility = visibility
        self.fixity=fixity
        self.existence = existence
        self.colors = colors
        self.dependencies = dependencies  # надо придумать как записывать зависимости


class LINE:
    """класс линии"""

    def __init__(self, X: complex, Y: complex, dependencies: dict, colors=(255, 255, 255), visibility="visible",
                 existence=True, type_line="straight"):
        self.X = X
        self.Y = Y
        self.visibility = visibility  # тип отрисовки и в каком сосотояние находится объект
        self.existence = existence
        self.colors = colors
        self.dependencies = dependencies  # надо придумать как записывать зависимости
        self.type_line = type_line  # линия,отрезок, луч...
        # формула прямой на комплексной плоскости приведенного вида
        self.formula = [(Y - X) * complex(0, 1), complex(0, 1) * (X * Y.conjugate() - Y * X.conjugate())]


class CIRCLE:
    """класс окружности"""

    def __init__(self, coordinate_centre: complex, radius: float, dependencies: dict, colors=(255, 255, 255),
                 existence=True, visibility="visible"):
        self.coordinate_centre = coordinate_centre
        self.radius = radius
        self.visibility = visibility
        self.existence=existence
        self.colors = colors
        self.dependencies = dependencies  # надо придумать как записывать зависимости
