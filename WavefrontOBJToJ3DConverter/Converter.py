import sys
import WavefrontOBJFile
import J3DFile

class Converter:
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path

    def convert(self):
        input_file = WavefrontOBJFile.WavefrontOBJFile()
        input_file.load_file(self.input_path)
        output_file = J3DFile.J3DFile()

        # Create J3DFile.Model based on WavefrontOBJFile.Object.
        for i, obj in enumerate(input_file.objects):
            model = J3DFile.Model()
            model.set_name(obj.name)
            model.set_offset(0, 0, 0)
            model.index = output_file.model_num
            model.set_model_index(model.index + 1 if i < len(input_file.objects) - 1 else -1, model.index - 1, -1, -1)
            model.set_use_tex(obj.mat.tex_name is not None)
            model.set_render_order(0)
            # Convert from WavefrontOBJFile.Vertex to J3DFile.Vertex.
            verts: list[J3DFile.Vertex] = []
            for vert in obj.verts:
                o_vert = J3DFile.Vertex()
                o_vert.set_pos(vert.pos[0], vert.pos[1], vert.pos[2])
                o_vert.set_uv(vert.uv[0], vert.uv[1])
                o_vert.set_normal(vert.normal[0], vert.normal[1], vert.normal[2])
                verts.append(o_vert)
            # Convert from WavefrontOBJFile.Triangle to J3DFile.Triangle.
            tris: list[J3DFile.Triangle] = []
            for tri in obj.tris:
                o_tri = J3DFile.Triangle()
                o_tri.set_indices(tri.indices[0], tri.indices[1], tri.indices[2])
                tris.append(o_tri)
            output_file.add_model(model, verts, tris)

        # Convert from WavefrontOBJFile.Material to J3DFile.Material.
        for i, mat in enumerate(input_file.mats):
            if mat.tex_name is not None:
                output_file.add_texture(mat.tex_name)
            o_mat = J3DFile.Material()
            o_mat.set_ambient_color(mat.ambient[0], mat.ambient[1], mat.ambient[2], mat.ambient[3])
            o_mat.set_diffuse_color(mat.diffuse[0], mat.diffuse[1], mat.diffuse[2], mat.diffuse[3])
            o_mat.set_specular_color(mat.specular[0], mat.specular[1], mat.specular[2], mat.specular[3])
            o_mat.set_emissive_color(mat.emissive[0], mat.emissive[1], mat.emissive[2], mat.emissive[3])
            o_mat.set_shininess(mat.shininess)
            output_file.add_material(o_mat)

        # Prepare J3DFile.tri_tex_indices.
        output_file.init_tri_tex_indices()
        for i, obj in enumerate(input_file.objects):
            if obj.mat.tex_name is not None:
                output_file.bind_model_texture(output_file.models[i], output_file.get_tex_by_name(obj.mat.tex_name[:-4]))

        # Serialize J3DFile.
        f = open(self.output_path, 'wb')
        output_file.serialize(f)
        f.close()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        conv: Converter = Converter(sys.argv[1], sys.argv[2])
        conv.convert()
    else:
        conv: Converter = Converter("C:\\Users\\yanfang_a\\Documents\\default.obj", "C:\\Users\\yanfang_a\\Documents\\default.J3D")
        conv.convert()

# Usage:
#   py Converter.py <input WavefrontOBJ file path> <output J3D file path>
