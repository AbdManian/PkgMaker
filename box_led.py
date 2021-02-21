from shaper import ShapeArray
from drawshapes import write_shapes_to_file


def create_double_wall_box(box_dimentions):
    """
    width, depth, height, thickness

    :param box_dimention:
    :return:
    """

    shapes = ShapeArray()

    b1 = shapes.add(
        ((0, 0), (30, 0), (30, 20), (0, 20)),
        closed=True
    )

    b2 = shapes.add(
        ((0, 0), )
    )

    return shapes


shapes = create_double_wall_box(dict())

write_shapes_to_file('sample.dxf', shapes)

