from .stream import Stream
from .utils import get_color

def parse_model(filepath):
    with open(filepath, "rb") as f:
        data = f.read()

    stream = Stream(data)
    
    vertex_count = stream.read_u_short()
    face_count = stream.read_u_short()
    
    vertices = []
    for _ in range(vertex_count):
        x = stream.read_int()
        y = stream.read_int()
        z = stream.read_int()
        stream.read_int()

        new_x = x
        new_y = z
        new_z = -y
        vertices.append((new_x * 100, new_y * 100, new_z * 100))

    face_vert_cnt, texture_front, texture_back, face_colors, face_texture, face_shade = [], [], [], [], [], []

    for _ in range(face_count):
        face_vert_cnt.append(stream.read_int())
        front, back, shade = stream.read_int(), stream.read_int(), stream.read_int()

        texture_front.append(front)
        texture_back.append(back)
        face_shade.append(shade)

        if front < 0 or back < 0:  # RGB color face
            color = get_color(front if front < 0 else back)
            texture = None
        else:
            texture = back if front == 32767 else front
            color = None

        face_colors.append(color)
        face_texture.append(texture)

    faces = [[stream.read_int() for _ in range(face_vert_cnt[i])] for i in range(face_count)]

    return {
        "vertices": vertices,
        "faces": faces,
        "face_colors": face_colors,
        "face_texture": face_texture,
        "face_properties": {
            "face_vert_cnt": face_vert_cnt,
            "texture_front": texture_front,
            "texture_back": texture_back,
            "face_shade": face_shade,
        },
    }
