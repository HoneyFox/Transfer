import struct
import typing

class Vertex:
    def __init__(self):
        self.pos = None
        self.normal = None
        self.uv = None

    def set_pos(self, x: float, y: float, z: float):
        self.pos = [x, y, z]

    def set_normal(self, x: float, y: float, z: float):
        self.normal = [x, y, z]

    def set_uv(self, u: float, v: float):
        self.uv = [u, v]

class Triangle:
    def __init__(self):
        self.indices = None

    def set_indices(self, i0: int, i1: int, i2: int):
        self.indices = [i0, i1, i2]

class Material:
    def __init__(self):
        self.name = None
        self.ambient = [0, 0, 0, 0]
        self.diffuse = [0, 0, 0, 0]
        self.specular = [0, 0, 0, 0]
        self.emissive = [0, 0, 0, 0]
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
        self.tris: list[Triangle] = []
        self.mat: Material = None

        self.positions: list[list[float]] = []
        self.uvs: list[list[float]] = []
        self.normals: list[list[float]] = []

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

    @staticmethod
    def finish_obj(obj: Object, used_positions: int, used_uvs: int, used_normals: int, vert_set: set[tuple[int, int, int]], tri_list):
        # Generate verts based on vert_set
        sorted_verts = {}  # Record distinct verts' index for usage from triangles.
        for vert in vert_set:
            sorted_verts[vert] = len(sorted_verts)
            new_vert = Vertex()
            # obj only stores its own vertex data so the index starts from 0, but tri stores global index.
            new_vert.set_pos(obj.positions[vert[0] - used_positions][0], obj.positions[vert[0] - used_positions][1], obj.positions[vert[0] - used_positions][2])
            new_vert.set_uv(obj.uvs[vert[1] - used_uvs][0], obj.uvs[vert[1] - used_uvs][1])
            new_vert.set_normal(obj.normals[vert[2] - used_normals][0], obj.normals[vert[2] - used_normals][1], obj.normals[vert[2] - used_normals][2])
            obj.add_vert(new_vert)
        for tri in tri_list:
            new_tri = Triangle()
            new_tri.set_indices(sorted_verts[tri[0]], sorted_verts[tri[1]], sorted_verts[tri[2]])
            obj.add_tri(new_tri)

    def load_file(self, path: str):
        f = open(path, 'r')
        lines: list[str] = f.readlines()
        lines = [line.strip() for line in lines]
        f.close()

        cur_obj: Object = None

        vert_set: set[tuple[int, int, int]] = set()
        tri_list = []

        used_positions = 0
        used_uvs = 0
        used_normals = 0
        used_tris = 0

        for line in lines:
            if line.startswith("#"):
                continue
            if line.startswith("mtllib "):
                loaded_mats = self.load_material_library(path[0:path.rfind('\\')] + "\\" + line[7:])
                for loaded_mat in loaded_mats:
                    loaded_mat.index = len(self.mats)
                    self.mats.append(loaded_mat)
            elif line.startswith("o "):
                # Previous Object should be finished before continuing to the next Object.
                if cur_obj is not None:
                    WavefrontOBJFile.finish_obj(cur_obj, used_positions, used_uvs, used_normals, vert_set, tri_list)
                    self.objects.append(cur_obj)
                    used_positions += len(cur_obj.positions)
                    used_uvs += len(cur_obj.uvs)
                    used_normals += len(cur_obj.normals)
                    used_tris += len(cur_obj.tris)
                    vert_set.clear()
                    tri_list.clear()
                cur_obj = Object()
                obj_name = line[2:]
                underscore = obj_name.rfind('_')
                if underscore >= 0:
                    obj_name = obj_name[0:underscore]
                cur_obj.set_name(obj_name)
            elif line.startswith("v "):
                components = line.split(' ')
                cur_obj.positions.append([float(components[1]), float(components[2]), float(components[3])])
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
                v1_pos = int(v1_components[0]) - 1
                v1_uv = int(v1_components[1]) - 1
                v1_normal = int(v1_components[2]) - 1
                v2_pos = int(v2_components[0]) - 1
                v2_uv = int(v2_components[1]) - 1
                v2_normal = int(v2_components[2]) - 1
                v3_pos = int(v3_components[0]) - 1
                v3_uv = int(v3_components[1]) - 1
                v3_normal = int(v3_components[2]) - 1
                vert_set.add((v1_pos, v1_uv, v1_normal))
                vert_set.add((v2_pos, v2_uv, v2_normal))
                vert_set.add((v3_pos, v3_uv, v3_normal))
                tri_list.append(((v1_pos, v1_uv, v1_normal), (v2_pos, v2_uv, v2_normal), (v3_pos, v3_uv, v3_normal)))

        # when reaching the end of file, the last Object should be finished too.
        if cur_obj is not None:
            WavefrontOBJFile.finish_obj(cur_obj, used_positions, used_uvs, used_normals, vert_set, tri_list)
            self.objects.append(cur_obj)
            used_positions += len(cur_obj.positions)
            used_uvs += len(cur_obj.uvs)
            used_normals += len(cur_obj.normals)
            used_tris += len(cur_obj.tris)
            vert_set.clear()
            tri_list.clear()
