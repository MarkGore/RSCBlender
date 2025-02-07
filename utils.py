def get_color(rsc_color):
    rsc_color = -1 - rsc_color
    r = (rsc_color >> 10 & 31) * 8 / 255
    g = (rsc_color >> 5 & 31) * 8 / 255
    b = (rsc_color & 31) * 8 / 255
    return (r, g, b, 1.0)

def get_rs_color(material):
    color = material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value[:3]
    r, g, b = [int(c * 255) for c in color]
    return -((((r // 8) & 0x1f) << 10) | (((g // 8) & 0x1f) << 5) | ((b // 8) & 0x1f)) - 1
