import sys
import WavefrontOBJFile
import J3DFile

class HierarchyTreeNode:
    def __init__(self):
        self.root: HierarchyTreeNode = None
        self.parent: HierarchyTreeNode = None
        self.children: list[HierarchyTreeNode] = []
        self.full_name: str = None
        self.node_name: str = None
        self.node_data = None

    @staticmethod
    def create_node(root_node: "HierarchyTreeNode", node_path: str):
        if root_node is None:
            # this is the root node itself.
            new_node = HierarchyTreeNode()
            new_node.full_name = ""
            new_node.node_name = ""
            return new_node
        else:
            existing_node = root_node.find_node(node_path)
            if existing_node is not None:
                return existing_node

            tree_nodes: list[str] = node_path.split('.')
            # Create parent nodes if they don't exist yet.
            cur_node = root_node
            cur_path = ""
            i = 0
            while i < len(tree_nodes):
                if cur_path == "":
                    cur_path = tree_nodes[0]
                else:
                    cur_path += "." + tree_nodes[i]
                child_node = cur_node.find_child(tree_nodes[i])
                if child_node is None:
                    child_node = HierarchyTreeNode()
                    child_node.root = root_node
                    child_node.full_name = cur_path
                    child_node.node_name = cur_path[cur_path.rfind('.')+1:]
                    cur_node.add_child(child_node)
                cur_node = child_node
                i += 1
            return cur_node

    def add_child(self, child: "HierarchyTreeNode"):
        self.children.append(child)
        child.parent = self

    def get_child_index(self, child: "HierarchyTreeNode"):
        for i, c in enumerate(self.children):
            if c == child:
                return i

    def get_child(self, index: int):
        if index < 0 or index >= len(self.children):
            return None
        return self.children[index]

    def get_sibling_index(self):
        if self.parent is None:
            return 0
        return self.parent.get_child_index(self)

    def get_prev_sibling(self):
        if self.parent is None:
            return None
        return self.parent.get_child(self.get_sibling_index() - 1)

    def get_next_sibling(self):
        if self.parent is None:
            return None
        return self.parent.get_child(self.get_sibling_index() + 1)

    def find_child(self, name: str):
        for child in self.children:
            if child.node_name == name:
                return child
        return None

    def find_node(self, node_path: str):
        if self.full_name == "" or node_path.startswith(self.full_name):
            tree_nodes = node_path.split('.')
            cur_node = self
            cur_path = self.full_name
            i = (0 if self.full_name == "" else self.full_name.count('.') + 1)
            while i < len(tree_nodes):
                if cur_path == "":
                    cur_path = tree_nodes[0]
                else:
                    cur_path += "." + tree_nodes[i]
                child_node = cur_node.find_child(tree_nodes[i])
                if child_node is None:
                    return None
                cur_node = child_node
                i += 1
            return cur_node
        else:
            return None

    def set_node_data(self, node_data):
        self.node_data = node_data

    def calc_node_data(self):
        parent_offset: list[float] = None
        relative_offset: list[float] = None

        if self.parent is not None and self.parent.node_data is not None:
            # This is not root node nor root's child node.
            parent_offset = self.parent.node_data[2]
        else:
            parent_offset = [0, 0, 0]
        if self.parent is not None:
            # This is not root node.
            relative_offset: list[float] = self.node_data[1]
            self.set_node_data((self.node_data[0], self.node_data[1], [parent_offset[0] + relative_offset[0], parent_offset[1] + relative_offset[1], parent_offset[2] + relative_offset[2]]))

        for child in self.children:
            child.calc_node_data()

    def deep_first_search(self):
        if self.parent is not None:
            yield self
        for child in self.children:
            yield from child.deep_first_search()

class Converter:
    def __init__(self, input_path: str, output_path: str, consider_hierarchy: bool):
        self.input_path = input_path
        self.output_path = output_path
        self.enable_hierarchy = consider_hierarchy

    def convert(self):
        input_file = WavefrontOBJFile.WavefrontOBJFile()
        input_file.load_file(self.input_path)
        output_file = J3DFile.J3DFile()

        root: HierarchyTreeNode = None
        if self.enable_hierarchy:
            # Construct hierarchy tree of WavefrontOBJFile.Object.
            root = HierarchyTreeNode.create_node(None, None)
            for obj in input_file.objects:
                if obj.name.find('(') != -1:
                    components = obj.name.split('(')
                    node_path = components[0]
                    offset_components = components[1].removesuffix(')').split(',')
                    node = HierarchyTreeNode.create_node(root, node_path)
                    node.set_node_data((obj, [float(offset_components[0]), float(offset_components[1]), float(offset_components[2])]))
                else:
                    node_path = obj.name
                    node = HierarchyTreeNode.create_node(root, node_path)
                    node.set_node_data((obj, [0, 0, 0]))
            # Calculate offsets.
            root.calc_node_data()

        # Create J3DFile.Model based on WavefrontOBJFile.Object.
        if self.enable_hierarchy:
            node_indices = {}
            i = 0
            for node in root.deep_first_search():
                node_indices[node] = i
                i += 1
            for node in root.deep_first_search():
                obj: WavefrontOBJFile.Object = node.node_data[0]
                model = J3DFile.Model()
                model.set_name(node.node_name)
                model.set_offset(node.node_data[1][0], node.node_data[1][1], node.node_data[1][2])
                model.index = output_file.model_num

                next_sibling = node.get_next_sibling()
                prev_sibling = node.get_prev_sibling()
                parent = node.parent if node.parent != root else None
                child = node.get_child(0)
                model.set_model_index(
                    node_indices[next_sibling] if next_sibling is not None else -1,
                    node_indices[prev_sibling] if prev_sibling is not None else -1,
                    node_indices[parent] if parent is not None else -1,
                    node_indices[child] if child is not None else -1
                )
                model.set_use_tex(obj.mat.tex_name is not None)
                model.set_mat_index(obj.mat.index)
                total_offset = node.node_data[2]
                # Convert from WavefrontOBJFile.Vertex to J3DFile.Vertex.
                verts: list[J3DFile.Vertex] = []
                for vert in obj.verts:
                    o_vert = J3DFile.Vertex()
                    o_vert.set_pos(vert.pos[0] - total_offset[0], vert.pos[1] - total_offset[1], vert.pos[2] - total_offset[2])
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
        else:
            for i, obj in enumerate(input_file.objects):
                model = J3DFile.Model()
                model.set_name(obj.name)
                model.set_offset(0, 0, 0)
                model.index = output_file.model_num
                model.set_model_index(model.index + 1 if i < len(input_file.objects) - 1 else -1, model.index - 1, -1, -1)
                model.set_use_tex(obj.mat.tex_name is not None)
                model.set_mat_index(obj.mat.index)
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
        if self.enable_hierarchy:
            for node in root.deep_first_search():
                obj: WavefrontOBJFile.Object = node.node_data[0]
                print(node.node_name)
                print(obj.mat.tex_name)
                if obj.mat.tex_name is not None:
                    output_file.bind_model_texture(output_file.models[node_indices[node]], output_file.get_tex_by_name(obj.mat.tex_name[:-4]))
        else:
            for i, obj in enumerate(input_file.objects):
                if obj.mat.tex_name is not None:
                    output_file.bind_model_texture(output_file.models[i], output_file.get_tex_by_name(obj.mat.tex_name[:-4]))

        # Serialize J3DFile.
        f = open(self.output_path, 'wb')
        output_file.serialize(f)
        f.close()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        conv: Converter = Converter(sys.argv[1], sys.argv[2], False)
        conv.convert()
    elif len(sys.argv) == 4:
        conv: Converter = Converter(sys.argv[2], sys.argv[3], (sys.argv[1].lower() == "-h"))
        conv.convert()
    else:
        conv: Converter = Converter("C:\\Users\\yanfang_a\\Documents\\default.obj", "C:\\Users\\yanfang_a\\Documents\\default.J3D", True)
        conv.convert()

# Usage:
#   py Converter.py [-h] <input WavefrontOBJ file path> <output J3D file path>
#       -h: Consider hierarchy naming and offset: Object name should be like A.B.C(x,y,z) to represent hierarchy and offset of the object.
#           Offset is related to its parent object.

