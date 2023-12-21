import struct
import typing

class Name:
    def __init__(self):
        self.name = None

    def set_name(self, name: str):
        self.name = bytearray()
        for char in name:
            self.name.append(ord(char))
        while len(self.name) < 32:
            self.name.append(0)

    def serialize(self, f):
        f.write(self.name)

class Vertex:
    def __init__(self):
        self.pos = None
        self.normal = None
        self.uv = None

    def set_pos(self, x: float, y: float, z: float):
        self.pos = [x, y, z, 0]

    def set_normal(self, x: float, y: float, z: float):
        self.normal = [x, y, z]

    def set_uv(self, u: float, v: float):
        self.uv = [0, u, 1.0 - v]

    def serialize(self, f):
        f.write(struct.pack("<f", self.pos[0]))
        f.write(struct.pack("<f", self.pos[1]))
        f.write(struct.pack("<f", self.pos[2]))
        f.write(struct.pack("<f", self.pos[3]))
        f.write(struct.pack("<f", self.normal[0]))
        f.write(struct.pack("<f", self.normal[1]))
        f.write(struct.pack("<f", self.normal[2]))
        f.write(struct.pack("<f", self.uv[0]))
        f.write(struct.pack("<f", self.uv[1]))
        f.write(struct.pack("<f", self.uv[2]))

class Triangle:
    def __init__(self):
        self.indices = None

    def set_indices(self, i0: int, i1: int, i2: int):
        self.indices = [i0, i1, i2]

    def serialize(self, f):
        f.write(self.indices[0].to_bytes(2, 'little', signed=False))
        f.write(self.indices[1].to_bytes(2, 'little', signed=False))
        f.write(self.indices[2].to_bytes(2, 'little', signed=False))

class Texture:
    def __init__(self):
        self.name = None

        self.index = -1

    def set_name(self, name: Name):
        self.name = name

    def serialize(self, f):
        self.name.serialize(f)

class Model:
    def __init__(self):
        self.model_name: Name = None
        self.offset = None
        self.unknown1 = [0, 0, 0, 0]  # What do these number mean? rotation perhaps?
        self.nextSiblingModelIndex = -1
        self.prevSiblingModelIndex = -1
        self.parentModelIndex = -1
        self.childModelIndex = -1
        self.tri_num = 0
        self.tri_offset = 0
        self.vert_num = 0
        self.vert_offset = 0
        self.use_tex = 0
        self.render_order = 0  # FIXME: Not really sure if it is render-order or some kind of material index?
        self.unknown2 = [1, 0, 0, 0]  # What do these number mean?

        self.index = -1

    def set_name(self, name: str):
        self.model_name = Name()
        self.model_name.set_name(name)

    def set_offset(self, x: float, y: float, z: float):
        self.offset = [x, y, z]

    def set_model_index(self, next_index, prev_index, parent_index, child_index):
        if next_index is not None:
            self.nextSiblingModelIndex = next_index
        if prev_index is not None:
            self.prevSiblingModelIndex = prev_index
        if parent_index is not None:
            self.parentModelIndex = parent_index
        if child_index is not None:
            self.childModelIndex = child_index

    def set_tri_num_offset(self, num, offset):
        if num is not None:
            self.tri_num = num
        if offset is not None:
            self.tri_offset = offset

    def set_vert_num_offset(self, num, offset):
        if num is not None:
            self.vert_num = num
        if offset is not None:
            self.vert_offset = offset

    def set_use_tex(self, use_tex: bool):
        self.use_tex = 1 if use_tex else 0

    def set_render_order(self, render_order: int):
        self.render_order = render_order

    def serialize(self, f):
        self.model_name.serialize(f)
        f.write(struct.pack("<f", self.offset[0]))
        f.write(struct.pack("<f", self.offset[1]))
        f.write(struct.pack("<f", self.offset[2]))
        f.write(self.unknown1[0].to_bytes(4, 'little', signed=False))
        f.write(self.unknown1[1].to_bytes(4, 'little', signed=False))
        f.write(self.unknown1[2].to_bytes(4, 'little', signed=False))
        f.write(self.unknown1[3].to_bytes(4, 'little', signed=False))
        f.write(self.nextSiblingModelIndex.to_bytes(4, 'little', signed=True))
        f.write(self.prevSiblingModelIndex.to_bytes(4, 'little', signed=True))
        f.write(self.parentModelIndex.to_bytes(4, 'little', signed=True))
        f.write(self.childModelIndex.to_bytes(4, 'little', signed=True))
        f.write(self.tri_num.to_bytes(2, 'little', signed=False))
        f.write(self.tri_offset.to_bytes(2, 'little', signed=False))
        f.write(self.vert_num.to_bytes(2, 'little', signed=False))
        f.write(self.vert_offset.to_bytes(2, 'little', signed=False))
        f.write(self.use_tex.to_bytes(2, 'little', signed=False))
        f.write(self.render_order.to_bytes(2, 'little', signed=False))
        f.write(self.unknown2[0].to_bytes(2, 'little', signed=False))
        f.write(self.unknown2[1].to_bytes(2, 'little', signed=False))
        f.write(self.unknown2[2].to_bytes(2, 'little', signed=False))
        f.write(self.unknown2[3].to_bytes(2, 'little', signed=False))

class Material:
    def __init__(self):
        self.ambient = None
        self.diffuse = None
        self.specular = None
        self.emissive = None
        self.shininess = None

        self.index = -1

    def set_ambient_color(self, r: float, g: float, b: float, a: float):
        self.ambient = [r, g, b, a]

    def set_diffuse_color(self, r: float, g: float, b: float, a: float):
        self.diffuse = [r, g, b, a]

    def set_specular_color(self, r: float, g: float, b: float, a: float):
        self.specular = [r, g, b, a]

    def set_emissive_color(self, r: float, g: float, b: float, a: float):
        self.emissive = [r, g, b, a]

    def set_shininess(self, shininess: float):
        self.shininess = shininess

    def serialize(self, f):
        f.write(struct.pack("<f", self.ambient[0]))
        f.write(struct.pack("<f", self.ambient[1]))
        f.write(struct.pack("<f", self.ambient[2]))
        f.write(struct.pack("<f", self.ambient[3]))
        f.write(struct.pack("<f", self.diffuse[0]))
        f.write(struct.pack("<f", self.diffuse[1]))
        f.write(struct.pack("<f", self.diffuse[2]))
        f.write(struct.pack("<f", self.diffuse[3]))
        f.write(struct.pack("<f", self.specular[0]))
        f.write(struct.pack("<f", self.specular[1]))
        f.write(struct.pack("<f", self.specular[2]))
        f.write(struct.pack("<f", self.specular[3]))
        f.write(struct.pack("<f", self.emissive[0]))
        f.write(struct.pack("<f", self.emissive[1]))
        f.write(struct.pack("<f", self.emissive[2]))
        f.write(struct.pack("<f", self.emissive[3]))
        f.write(struct.pack("<f", self.shininess))

class J3DFile:
    def __init__(self):
        self.vert_num = 0
        self.tri_num = 0
        self.tex_num = 0
        self.model_num = 0
        self.mat_num = 0
        self.verts: list[Vertex] = []
        self.tris: list[Triangle] = []
        self.texs: list[Texture] = []
        self.models: list[Model] = []
        self.tri_tex_indices: list[int] = []  # FIXME: Need to double-check if it's texture index or material index?
        self.mats: list[Material] = []

    def add_model(self, model: Model, verts: list[Vertex], tris: list[Triangle]):
        model.tri_num = len(tris)
        model.vert_num = len(verts)
        model.tri_offset = self.tri_num
        model.vert_offset = self.vert_num
        model.index = self.model_num
        self.tris.extend(tris)
        self.verts.extend(verts)
        self.tri_num += len(tris)
        self.vert_num += len(verts)
        self.models.append(model)
        self.model_num += 1
        return model.index

    def add_texture(self, name: str):
        if name.lower().endswith(".bmp"):
            name_without_extension = name[:-4]
            existing_tex = self.get_tex_by_name(name_without_extension)
            if existing_tex is not None:
                return existing_tex.index
            tex_name = Name()
            tex_name.set_name(name_without_extension)
            tex = Texture()
            tex.set_name(tex_name)
            tex.index = self.tex_num
            self.texs.append(tex)
            self.tex_num += 1
            return tex.index
        else:
            print("Only BMP format is supported for textures.")
            return -1

    def get_tex_by_name(self, tex_name: str):
        test_name = Name()
        test_name.set_name(tex_name)
        for tex in self.texs:
            if tex.name.name == test_name.name:
                return tex
        return None

    def add_material(self, material: Material):
        material.index = self.mat_num
        self.mats.append(material)
        self.mat_num += 1
        return material.index

    def init_tri_tex_indices(self):
        self.tri_tex_indices = [-1] * self.tri_num

    def bind_model_texture(self, model: Model, texture: Texture):
        if texture is None:
            self.tri_tex_indices[model.tri_offset:model.tri_num] = [-1] * model.tri_num
        else:
            self.tri_tex_indices[model.tri_offset:model.tri_num] = [texture.index] * model.tri_num

    def serialize(self, f):
        f.write(self.vert_num.to_bytes(4, 'little', signed=False))
        f.write(self.tri_num.to_bytes(4, 'little', signed=False))
        f.write(self.tex_num.to_bytes(4, 'little', signed=False))
        f.write(self.model_num.to_bytes(4, 'little', signed=False))
        f.write(self.mat_num.to_bytes(4, 'little', signed=False))
        for v in self.verts:
            v.serialize(f)
        for t in self.tris:
            t.serialize(f)
        for tex in self.texs:
            tex.serialize(f)
        for m in self.models:
            m.serialize(f)
        for i in self.tri_tex_indices:
            f.write(i.to_bytes(1, 'little', signed=True))
        for mat in self.mats:
            mat.serialize(f)
