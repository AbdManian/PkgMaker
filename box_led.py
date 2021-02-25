from shaper import ShapeArray, Shape, RelPoints
from drawshapes import write_shapes_to_file, CutLayer, ScoreLayer


def create_double_wall_box(box_dimentions):
    """
    width, depth, height, thickness,
    fold_margin, wing_width

    :param box_dimention:
    :return:
    """

    width = box_dimentions['width']
    height = box_dimentions['height']
    depth = box_dimentions['depth']
    thickness = box_dimentions['thickness']
    fold_margin = box_dimentions['fold_margin']
    wing = box_dimentions['wing_width']

    internal_wing = depth / 2 - 2*fold_margin

    shapes = ShapeArray()

    bottom = Shape(
        ((0, 0), (width, 0), (width, depth), (0, depth)),
        closed=True,
        layer=ScoreLayer)

    w_wall = Shape(
        ((0, 0), (0, height), (width-2*thickness, height), (width-2*thickness, 0)),
        layer=ScoreLayer
    )

    d_wall = Shape(
        RelPoints([
            (-height, 0),
            (0, fold_margin),
            (-(height-thickness), 0),
            (-wing, 2*fold_margin),
            (0, depth - 2*(2*fold_margin + fold_margin)),
            (wing, 2*fold_margin),
            (height-thickness, 0),
            (0, fold_margin),
            (height, 0)
        ]),
        layer=CutLayer
    )

    w_wing_wall = Shape (
        RelPoints([
            (0, fold_margin),
            (-internal_wing, 0),
            (0, height - 2*fold_margin),
            (internal_wing, 0),
            (0, fold_margin),

            (fold_margin, 0),
            (0, height - thickness),
            (2*fold_margin, wing),
            (width - 2*(thickness+3*fold_margin), 0),  # <----
            (2*fold_margin, -wing),
            (0, -(height - thickness)),
            (fold_margin, 0),

            (0, -fold_margin),
            (internal_wing, 0),
            (0, -(height - 2*fold_margin)),
            (-internal_wing, 0),
            (0, -fold_margin)

        ]),
        layer=CutLayer
    )

    shapes.add_shape(bottom)

    w_wall.align_to(bottom, position='left-up', move=(thickness, 0))
    shapes.add_shape(w_wall)

    w_wall.align_to(bottom, position='left-down', move=(thickness, 0), scale=(1, -1))
    shapes.add_shape(w_wall)

    shapes.add_shape(d_wall)

    shapes.add_shape(d_wall.align_to(bottom, position='right-down', scale=(-1, 1)))

    shapes.add_shape(w_wing_wall.align_to(bottom, position='left-up', move=(thickness, 0)))

    #shapes.add_shape(w_wall.align_to(bottom, position='left-up', move=(thickness, 0)))


    return shapes


if __name__ == '__main__':
    dimentions = dict(height=50, width=135, depth=45, thickness=0.7, fold_margin=2, wing_width=10)
    shapes = create_double_wall_box(dimentions)
    write_shapes_to_file('sample.dxf', shapes)

