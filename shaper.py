class Shape:
    def __init__(self, points, closed=False, scale=(1, 1), move=(0, 0), layer=0):
        self.points = points
        self.closed = closed
        self.scale = scale
        self.move = move
        self.layer = layer
        self.calc_points = self.calc_absolute_points()

    def calc_absolute_points(self):
        res = []
        scale_x, scale_y = self.scale
        move_x, move_y = self.move
        for x, y in self.points:
            new_x = scale_x * x
            new_y = scale_y * y

            new_x += move_x
            new_y += move_y

            res.append((new_x, new_y))
        return res

    def get_bound_box(self):
        x_list = [x for x,y in self.calc_points]
        y_list = [y for x,y in self.calc_points]
        return min(x_list), min(y_list), max(x_list), max(y_list)

    def get_anchor(self, anchor="center-center"):
        anchor = anchor + "-center"
        anchor_x, anchor_y = anchor.split("-")[:2]

        x_min, y_min, x_max, y_max = self.get_bound_box()

        x_center = (x_min + x_max)/2
        y_center = (y_min + y_max)/2

        x_selector = dict(left=x_min, center=x_center, right=x_max)
        y_selector = dict(up=y_max, center=y_center, down=y_min)
        return x_selector[anchor_x], y_selector[anchor_y]

    def move_to(self, new_position=(0, 0)):
        self.move = new_position
        self.calc_points = self.calc_absolute_points()

    def align_to(self, reference, position="center-center"):
        self.move_to(reference.get_anchor(position))

    def get_lines(self):
        ret = []
        prv_point = self.calc_points[0]

        for point in self.calc_points[1:]:
            ret.append((prv_point, point))
            prv_point = point
        if self.closed:
            ret.append((prv_point, self.calc_points[0]))

        return ret


class ShapeArray:
    def __init__(self):
        self.shapes = []

    def add(self, *args, **kwargs):
        x = Shape(*args, **kwargs)
        self.shapes.append(x)
        return x
