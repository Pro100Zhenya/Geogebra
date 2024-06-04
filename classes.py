import pygame

class flatness:
    """класс координатной плоскости"""

    def __init__(self):
        self.left_top_coordinate = complex(0, 0)  # координата левого верхнего угла
        self.dimension = 10 ** 5  # размер одного пикселя в координатах\
        self.zoom_constant = 1.6

    def update(self, left_top_coordinate=False, dimension=False):
        """изменение видимой части плоскости"""
        if left_top_coordinate:
            self.left_top_coordinate = left_top_coordinate
        if dimension:
            self.dimension = dimension


class POINT:
    """класс точки"""

    def __init__(self, coordinate, dependencies: dict, colors=(0, 0, 0), visibility="visible", fixity=False,
                 existence=True):
        self.coordinate = coordinate
        self.visibility = visibility
        self.fixity = fixity
        self.existence = existence
        self.colors = colors
        self.dependencies = dependencies  # надо придумать как записывать зависимости


class LINE:
    """класс линии"""

    def __init__(self, X: complex, Y: complex, dependencies: dict, colors=(0, 0, 0), visibility="visible",
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

    def formula_update(self):
        self.formula = [(self.Y - self.X) * complex(0, 1),
                        complex(0, 1) * (self.X * self.Y.conjugate() - self.Y * self.X.conjugate())]


class CIRCLE:
    """класс окружности"""

    def __init__(self, coordinate_centre: complex, radius: float, dependencies: dict, colors=(0, 0, 0),
                 existence=True, visibility="visible"):
        self.coordinate_centre = coordinate_centre
        self.radius = radius
        self.visibility = visibility
        self.existence = existence
        self.colors = colors
        self.dependencies = dependencies  # надо придумать как записывать зависимости


class BUTTON:
    def __init__(self, surface, left_top, right_lower, styles, action, criteria=lambda x: False):
        self.surface = surface
        self.left_top, self.right_lower = left_top, right_lower
        self.regim = "Normal"
        self.styles = styles
        self.action = action
        self.criteria = criteria
        if self.styles[self.regim]["show_photo"]:
            self.photo_surf = pygame.image.load(self.styles[self.regim]["photo"])
            self.photo_surf.set_colorkey((255, 255, 255))
            self.photo_rect = self.photo_surf.get_rect(topleft=self.left_top)
        if self.styles[self.regim]["show_text"]:
            font2 = pygame.font.SysFont('freesanbold.ttf', 16)
            self.img2 = font2.render(self.styles[self.regim]["text"], True, (0, 0, 0))

    def update(self, event):
        if self.left_top[0] <= pygame.mouse.get_pos()[0] <= self.right_lower[0] and \
                self.left_top[1] <= pygame.mouse.get_pos()[1] <= self.right_lower[1]:
            if self.regim == "Normal":
                self.regim = "Hover"
        else:
            if self.regim == "Hover":
                self.regim = "Normal"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.left_top[0] <= event.pos[0] <= self.right_lower[0] and self.left_top[1] <= event.pos[1] <= \
                    self.right_lower[1] and event.button == 1:
                if self.regim != "Active":
                    self.action(self)
                    self.regim = "Active"
                    return True
                else:
                    self.regim = "Hover"
        elif self.criteria(event):
            if self.regim != "Active":
                self.action(self)
                self.regim = "Active"
                return True
            else:
                self.regim = "Hover"
        return False

    def draw(self):
        pygame.draw.rect(self.surface, self.styles[self.regim]["filling"],
                         [self.left_top, [self.right_lower[0] - self.left_top[0],
                                          self.right_lower[1] - self.left_top[1]]],
                         border_radius=self.styles[self.regim]["border_radius"])
        if self.styles[self.regim]["show_photo"]:
            self.surface.blit(self.photo_surf, self.photo_rect)
        if self.styles[self.regim]["show_text"]:
            self.surface.blit(self.img2, self.left_top)

        pygame.draw.rect(self.surface, self.styles[self.regim]["border"],
                         [self.left_top, [self.right_lower[0] - self.left_top[0],
                                          self.right_lower[1] - self.left_top[1]]], width=2,
                         border_radius=self.styles[self.regim]["border_radius"])

    def update_draw(self):
        pygame.draw.rect(self.surface, self.styles[self.regim]["filling"],
                         [self.left_top, [self.right_lower[0] - self.left_top[0],
                                          self.right_lower[1] - self.left_top[1]]],
                         border_radius=self.styles[self.regim]["border_radius"])
        pygame.draw.rect(self.surface, self.styles[self.regim]["border"],
                         [self.left_top, [self.right_lower[0] - self.left_top[0],
                                          self.right_lower[1] - self.left_top[1]]], width=2,
                         border_radius=self.styles[self.regim]["border_radius"])


class LIST_BUTTON:
    def __init__(self, surface, left_top, right_lower, styles):
        self.surface = surface
        self.left_top, self.right_lower = left_top, right_lower
        self.styles = styles
        self.list_button = []

    def add_button(self, components):
        if self.styles["button_alignment"] == "left":
            button = BUTTON(self.surface,
                            [self.left_top[0] + 5 + len(self.list_button) * (self.right_lower[1] - self.left_top[1]),
                             self.left_top[1] + 5], [self.right_lower[1] + self.left_top[0] - self.left_top[1] - 5 +
                                                     len(self.list_button) * (self.right_lower[1] - self.left_top[1]),
                                                     self.right_lower[1] - 5], components[0], components[1],
                            components[2])
        elif self.styles["button_alignment"] == "top":
            button = BUTTON(self.surface,
                            [self.left_top[0] + 5,
                             self.left_top[1] + 5 + len(self.list_button) * (self.right_lower[0] - self.left_top[0])],
                            [self.right_lower[0] - 5,
                             self.left_top[1] - self.left_top[0] + self.right_lower[0] - 5 + len(self.list_button) * (
                                     self.right_lower[0] - self.left_top[0])], components[0], components[1],
                            components[2])
        else:
            button = False
        self.list_button.append(button)
        return button

    def update(self, event):
        for button in self.list_button:
            button.update(event)
        if self.left_top[0] <= pygame.mouse.get_pos()[0] <= self.right_lower[0] and \
                self.left_top[1] <= pygame.mouse.get_pos()[1] <= self.right_lower[1]:
            return True
        else:
            return False

    def draw(self):
        pygame.draw.rect(self.surface, self.styles["filling"], [self.left_top,
                                                                [self.right_lower[0] - self.left_top[0],
                                                                 self.right_lower[1] - self.left_top[1]]],
                         border_radius=self.styles["border_radius"])
        pygame.draw.rect(self.surface, self.styles["border"], [self.left_top, [self.right_lower[0] - self.left_top[0],
                                                                               self.right_lower[1] - self.left_top[1]]],
                         width=2,
                         border_radius=self.styles["border_radius"])
        for button in self.list_button:
            button.draw()

    def update_draw(self):
        for button in self.list_button:
            button.draw()
