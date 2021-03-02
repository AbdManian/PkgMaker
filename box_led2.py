from shaper import ShapeArray, Shape, RelPoints
from drawshapes import write_shapes_to_file, CutLayer, ScoreLayer


def create_double_wall_box(box_dimensions):
    """
    width, depth, height, thickness,
    fold_margin, wing_width

    returns ShapeArray
    """

    width = box_dimensions['width']
    height = box_dimensions['height']
    depth = box_dimensions['depth']
    thickness = box_dimensions['thickness']
    fold_margin = box_dimensions['fold_margin']
    wing = box_dimensions['wing_width']
    wing_slope = fold_margin * 2
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

    outer_cut_left = Shape(
        RelPoints([
            (-(width / 2 - thickness - wing_slope), 0),
            (-wing_slope, wing),
            (0, height - thickness),
            (-(internal_wing + thickness), 0),
            (0, height),
            (internal_wing, 0),
            (-(2 * height - thickness), 0),
            (-wing, wing_slope),
            (0, depth - 2 * wing_slope),  # <--
            (wing, wing_slope),
            ((2 * height - thickness), 0),
            (-internal_wing, 0),
            (0, height ),
            ((internal_wing + thickness), 0),
            (0, height - thickness),
            (wing_slope, wing),
            ((width / 2 - thickness - wing_slope), 0),

        ], mirror=(1, -1)),
        move=(width / 2, -(height * 2 - thickness + wing)),
        layer=CutLayer,
    )

    score1 = Shape(
        RelPoints([
            (0, depth),
        ]),
        layer=ScoreLayer,
    )

    shapes.add_shape(bottom)
    shapes.add_shape(outer_cut_left)

    w_wall.align_to(bottom, position='left-up', move=(thickness, 0))
    shapes.add_shape(w_wall)

    w_wall.align_to(bottom, position='left-down', move=(thickness, 0), scale=(1, -1))
    shapes.add_shape(w_wall)

    shapes.add_shape(outer_cut_left.create_internal_line(2, layer=ScoreLayer))
    shapes.add_shape(outer_cut_left.create_internal_line(15, layer=ScoreLayer))

    score1.align_to(bottom, position='left-down', move=(-height, 0))
    shapes.add_shape(score1)
    score1.align_to(bottom, position='left-down', move=(-(2*height-thickness), 0))
    shapes.add_shape(score1)

    score1.align_to(bottom, position='right-down', move=(height, 0))
    shapes.add_shape(score1)
    score1.align_to(bottom, position='right-down', move=((2*height-thickness), 0))
    shapes.add_shape(score1)

    return shapes


def create_box_with_led(box_dimensions):
    """
    width, height, depth, led_height,
    thickness, fold_margin, wing_width
    """

    t = box_dimensions['thickness']

    body_d = dict(box_dimensions)
    led_d = dict(box_dimensions)

    led_d['width'] = body_d['width'] + 4*t
    led_d['depth'] = body_d['depth'] + 4*t
    led_d['height'] = box_dimensions['led_height']

    return create_double_wall_box(body_d), create_double_wall_box(led_d)


if __name__ == '__main__':
    dimensions = dict(height=35, width=85, depth=35, led_height=20, thickness=0.7, fold_margin=2, wing_width=10)
    body, led = create_box_with_led(dimensions)
    write_shapes_to_file('body2.dxf', body)
    write_shapes_to_file('led2.dxf', led)


