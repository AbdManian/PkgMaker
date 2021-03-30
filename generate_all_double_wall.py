from box_led2 import write_shapes_to_file, create_box_with_led

boxes = [
    dict(name="bird02"   , width=120, depth=50 , height=50, led_height=20),
    dict(name="bird3x"   , width=95 , depth=105, height=40, led_height=20),
    dict(name="bird01_02", width=120, depth=60 , height=50, led_height=20),
    dict(name="bird01"   , width=95 , depth=40 , height=40, led_height=20),
]

thickness, fold_margin, wing_width = 0.7, 2, 10

for x in boxes:
    file_base = x["name"]
    sizes = dict(thickness=0.7, fold_margin=2, wing_width=10)
    sizes.update(x)

    body_file = f"box_{file_base}_body.dxf"
    led_file = f"box_{file_base}_led.dxf"

    body, led = create_box_with_led(sizes)
    write_shapes_to_file(body_file, body)
    write_shapes_to_file(led_file, led)