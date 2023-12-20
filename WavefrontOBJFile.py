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
        f.write(self.indices[0].to_bytes(2, 'little', False))
        f.write(self.indices[1].to_bytes(2, 'little', False))
        f.write(self.indices[2].to_bytes(2, 'little', False))

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
        self.modelName = None
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
        self.modelName = Name()
        self.modelName.set_name(name)

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
        f.write(self.modelName)
        f.write(struct.pack("<f", self.offset[0]))
        f.write(struct.pack("<f", self.offset[1]))
        f.write(struct.pack("<f", self.offset[2]))
        f.write(self.unknown1[0].to_bytes(4, 'little', False))
        f.write(self.unknown1[1].to_bytes(4, 'little', False))
        f.write(self.unknown1[2].to_bytes(4, 'little', False))
        f.write(self.unknown1[3].to_bytes(4, 'little', False))
        f.write(self.nextSiblingModelIndex.to_bytes(4, 'little', True))
        f.write(self.prevSiblingModelIndex.to_bytes(4, 'little', True))
        f.write(self.parentModelIndex.to_bytes(4, 'little', True))
        f.write(self.childModelIndex.to_bytes(4, 'little', True))
        f.write(self.tri_num.to_bytes(2, 'little', False))
        f.write(self.tri_offset.to_bytes(2, 'little', False))
        f.write(self.vert_num.to_bytes(2, 'little', False))
        f.write(self.vert_offset.to_bytes(2, 'little', False))
        f.write(self.use_tex.to_bytes(2, 'little', False))
        f.write(self.render_order.to_bytes(2, 'little', False))
        f.write(self.unknown2[0].to_bytes(2, 'little', False))
        f.write(self.unknown2[1].to_bytes(2, 'little', False))
        f.write(self.unknown2[2].to_bytes(2, 'little', False))
        f.write(self.unknown2[3].to_bytes(2, 'little', False))

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

    def add_material(self, material: Material):
        material.index = self.mat_num
        self.mats.append(material)
        self.mat_num += 1
        return mat.index

    def init_tri_tex_indices(self):
        self.tri_tex_indices = [-1] * self.tri_num

    def bind_model_texture(self, model: Model, texture: Texture):
        if texture is None:
            self.tri_tex_indices[model.tri_offset:model.tri_num] = [-1] * model.tri_num
        else:
            self.tri_tex_indices[model.tri_offset:model.tri_num] = [texture.index] * model.tri_num

    def serialize(self, f):
        f.write(self.vert_num.to_bytes(4, 'little', false))
        f.write(self.tri_num.to_bytes(4, 'little', false))
        f.write(self.tex_num.to_bytes(4, 'little', false))
        f.write(self.model_num.to_bytes(4, 'little', false))
        f.write(self.mat_num.to_bytes(4, 'little', false))
        for v in self.verts:
            v.serialize(f)
        for t in self.tris:
            t.serialize(f)
        for tex in self.texs:
            tex.serialize(f)
        for m in self.models:
            m.serialize(f)
        for i in self.tri_tex_indices:
            f.write(i.to_bytes(1, 'little', true))
        for mat in self.mats:
            mat.serialize(f)

import struct
import typing

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

class Triangle:
    def __init__(self):
        self.indices = None

    def set_indices(self, i0: int, i1: int, i2: int):
        self.indices = [i0, i1, i2]

class Material:
    def __init__(self):
        self.name = None
        self.ambient = None
        self.diffuse = None
        self.specular = None
        self.emissive = None
        self.shininess = None
        self.tex_name = None

        self.index = -1

    def set_name(self, name: str):
        self.name = name

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

    def set_tex_name(self, tex_name: str):
        self.tex_name = tex_name

# Similar to J3DFile.py: class Model.
class Object:
    def __init__(self):
        self.name: str = None
        self.verts: list[Vertex] = []
        self.uvs: list[list[float]] = []
        self.normals: list[list[float]] = []
        self.tris: list[Triangle] = []
        self.mat: Material = None

    def set_name(self, name: str):
        self.name = name

    def add_vert(self, vert: Vertex):
        self.verts.append(vert)

    def add_tri(self, tri: Triangle):
        self.tris.append(tri)

    def set_material(self, mat: Material):
        self.mat = mat

class WavefrontOBJFile:
    def __init__(self):
        self.objects: list[Object] = []
        self.mats: list[Material] = []

    def get_mat_by_name(self, name: str):
        for mat in self.mats:
            if mat.name == name:
                return mat
        return None

    @staticmethod
    def load_material_library(path: str) -> list[Material]:
        f = open(path, 'r')
        lines: list[str] = f.readlines()
        lines = [line.strip() for line in lines]
        f.close()

        results = []
        cur_mat: Material = None
        for line in lines:
            if line.startswith("#"):
                continue
            if line.startswith("newmtl "):
                cur_mat = Material()
                cur_mat.set_name(line[7:])
                results.append(cur_mat)
            elif line.startswith("Ns "):
                cur_mat.set_shininess(float(line[3:]))
            elif line.startswith("Ka "):
                components = line.split(' ')
                cur_mat.set_ambient_color(float(components[1]), float(components[2]), float(components[3]), float(components[4]) if len(components) == 5 else 1.0)
            elif line.startswith("Kd "):
                components = line.split(' ')
                cur_mat.set_diffuse_color(float(components[1]), float(components[2]), float(components[3]), float(components[4]) if len(components) == 5 else 1.0)
            elif line.startswith("Ks "):
                components = line.split(' ')
                cur_mat.set_specular_color(float(components[1]), float(components[2]), float(components[3]), float(components[4]) if len(components) == 5 else 1.0)
            elif line.startswith("Ke "):
                components = line.split(' ')
                cur_mat.set_emissive_color(float(components[1]), float(components[2]), float(components[3]), float(components[4]) if len(components) == 5 else 1.0)
            elif line.startswith("d "):
                opaque = float(line[2:])
                cur_mat.set_ambient_color(cur_mat.ambient[0], cur_mat.ambient[1], cur_mat.ambient[2], cur_mat.ambient[3] * opaque)
                cur_mat.set_diffuse_color(cur_mat.diffuse[0], cur_mat.diffuse[1], cur_mat.diffuse[2], cur_mat.diffuse[3] * opaque)
                cur_mat.set_specular_color(cur_mat.specular[0], cur_mat.specular[1], cur_mat.specular[2], cur_mat.specular[3] * opaque)
                cur_mat.set_emissive_color(cur_mat.emissive[0], cur_mat.emissive[1], cur_mat.emissive[2], cur_mat.emissive[3] * opaque)
            elif line.startswith("Tr "):
                opaque = 1.0 - float(line[3:])
                cur_mat.set_ambient_color(cur_mat.ambient[0], cur_mat.ambient[1], cur_mat.ambient[2], cur_mat.ambient[3] * opaque)
                cur_mat.set_diffuse_color(cur_mat.diffuse[0], cur_mat.diffuse[1], cur_mat.diffuse[2], cur_mat.diffuse[3] * opaque)
                cur_mat.set_specular_color(cur_mat.specular[0], cur_mat.specular[1], cur_mat.specular[2], cur_mat.specular[3] * opaque)
                cur_mat.set_emissive_color(cur_mat.emissive[0], cur_mat.emissive[1], cur_mat.emissive[2], cur_mat.emissive[3] * opaque)
            elif line.startswith("Ni "):
                # Index of refraction
                pass
            elif line.startswith("illum "):
                # Illumination model
                pass
            elif line.startswith("map_Kd "):
                cur_mat.set_tex_name(line[7:])

        return results

    def load_file(self, path: str):
        f = open(path, 'r')
        lines: list[str] = f.readlines()
        lines = [line.strip() for line in lines]
        f.close()

        cur_obj: Object = None
        for line in lines:
            if line.startswith("#"):
                continue
            if line.startswith("mtllib "):
                loaded_mats = self.load_material_library(path[0:path.rfind('\\')] + "\\" + line[7:])
                for loaded_mat in loaded_mats:
                    loaded_mat.index = len(self.mats)
                    self.mats.append(loaded_mat)
            elif line.startswith("o "):
                cur_obj = Object()
                cur_obj.set_name(line[2:])
                self.objects.append(cur_obj)
            elif line.startswith("v "):
                components = line.split(' ')
                cur_vert = Vertex()
                cur_vert.set_pos(float(components[1]), float(components[2]), float(components[3]))
                cur_obj.add_vert(cur_vert)
            elif line.startswith("vt "):
                components = line.split(' ')
                cur_obj.uvs.append([float(components[1]), float(components[2])])
            elif line.startswith("vn "):
                components = line.split(' ')
                cur_obj.normals.append([float(components[1]), float(components[2]), float(components[3])])
            elif line.startswith("usemtl "):
                cur_obj.set_material(self.get_mat_by_name(line[7:]))
            elif line.startswith("s "):
                pass
            elif line.startswith("f "):
                components = line.split(' ')
                v1_components = components[1].split('/')
                v2_components = components[2].split('/')
                v3_components = components[3].split('/')
                v1_vert = int(v1_components[0]) - 1
                v1_uv = int(v1_components[1]) - 1
                v1_normal = int(v1_components[2]) - 1
                v2_vert = int(v2_components[0]) - 1
                v2_uv = int(v2_components[1]) - 1
                v2_normal = int(v2_components[2]) - 1
                v3_vert = int(v3_components[0]) - 1
                v3_uv = int(v3_components[1]) - 1
                v3_normal = int(v3_components[2]) - 1
                cur_obj.verts[v1_vert].set_uv(cur_obj.uvs[v1_uv][0], cur_obj.uvs[v1_uv][1])
                cur_obj.verts[v1_vert].set_normal(cur_obj.normals[v1_normal][0], cur_obj.normals[v1_normal][1], cur_obj.normals[v1_normal][2])
                cur_obj.verts[v2_vert].set_uv(cur_obj.uvs[v2_uv][0], cur_obj.uvs[v2_uv][1])
                cur_obj.verts[v2_vert].set_normal(cur_obj.normals[v2_normal][0], cur_obj.normals[v2_normal][1], cur_obj.normals[v2_normal][2])
                cur_obj.verts[v3_vert].set_uv(cur_obj.uvs[v3_uv][0], cur_obj.uvs[v3_uv][1])
                cur_obj.verts[v3_vert].set_normal(cur_obj.normals[v3_normal][0], cur_obj.normals[v3_normal][1], cur_obj.normals[v3_normal][2])
                tri = Triangle()
                tri.set_indices(v1_vert, v2_vert, v3_vert)
                cur_obj.tris.append(tri)