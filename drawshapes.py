import ezdxf
import collections

CutLayer = 1
ScoreLayer = 0


def drawshapes(shapes, model_space, layer_dict):
    for shape in shapes.shapes:
        layer = shape.layer
        for line in shape.get_lines():
            model_space.add_line(
                line[0], line[1],
                dxfattribs=layer_dict[layer])
    return model_space


def create_dxf_doc_modelspace():
    doc = ezdxf.new(dxfversion='R2010')
    doc.layers.new(name='CutLayer', dxfattribs={'color': 7})
    doc.layers.new(name='Score', dxfattribs={'color': 1})

    layer_dict = collections.defaultdict(lambda: {'layer': 'Score'})
    layer_dict[1] = {'layer': 'CutLayer'}

    return doc, layer_dict


def write_shapes_to_file(filename, shapes):
    doc, layers = create_dxf_doc_modelspace()
    msp = doc.modelspace()
    drawshapes(shapes, msp, layers)
    doc.saveas(filename)
