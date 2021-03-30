from shaper import ShapeArray, Shape, RelPoints
from drawshapes import write_shapes_to_file, CutLayer, ScoreLayer


def create_single_wall_box(box_dimensions):
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

    safe_wing = height/2 * 0.95
    if wing > safe_wing:
        wing = safe_wing

    shapes = ShapeArray()

    bottom = Shape(
        ((0, 0), (width, 0), (width, depth), (0, depth)),
        closed=True,
        layer=ScoreLayer)

    outer_cut_left = Shape(
        RelPoints([
            (-(width / 2 - thickness), 0),
            (-wing, wing_slope),
            (0, (height - 2*wing_slope)),
            (wing, wing_slope),
            (-(height+thickness), 0),
            (0, depth),  # <-- Middle
            ((height + thickness), 0),
            (-wing, wing_slope),
            (0, (height-2*wing_slope)),
            (wing, wing_slope),
            ((width / 2 - thickness), 0),

        ], mirror=(1, -1)),
        move=((width / 2), -height),
        layer=CutLayer,
    )

    shapes.add_shape(bottom)
    shapes.add_shape(outer_cut_left)
    shapes.add_shape(outer_cut_left.create_internal_line(1, 4, layer=ScoreLayer))
    shapes.add_shape(outer_cut_left.create_internal_line(7, 10, layer=ScoreLayer))
    shapes.add_shape(outer_cut_left.create_internal_line(12, 15, layer=ScoreLayer))
    shapes.add_shape(outer_cut_left.create_internal_line(18, 21, layer=ScoreLayer))

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
    led_d['depth'] = body_d['depth'] + 2*t
    led_d['height'] = box_dimensions['led_height']

    return create_single_wall_box(body_d), create_single_wall_box(led_d)


if __name__ == '__main__':
    dimensions = dict(height=35, width=85, depth=35, led_height=20, thickness=0.7, fold_margin=2, wing_width=10)
    body, led = create_box_with_led(dimensions)
    write_shapes_to_file('body3.dxf', body)
    write_shapes_to_file('body3_led.dxf', led)


