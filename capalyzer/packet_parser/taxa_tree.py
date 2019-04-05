
from os import environ
from os.path import join, dirname
import gzip


NCBI_DELIM = '\t|'  # really...
NAMES_ENV_VAR = 'CAPALYZER_NCBI_NAMES'
NODES_ENV_VAR = 'CAPALYZER_NCBI_NODES'
NAMES_DEF = join(dirname(__file__), 'ncbi_tree/names.dmp.gz')
NODES_DEF = join(dirname(__file__), 'ncbi_tree/nodes.dmp.gz')


class NCBITaxaTree:

    def __init__(self, parent_map, names_to_nodes, nodes_to_name):
        self.parent_map = parent_map
        self.names_to_nodes = names_to_nodes
        self.nodes_to_name = nodes_to_name

    def _node(self, taxon_name):
        return self.names_to_nodes[taxon_name]

    def _name(self, node_num):
        return self.nodes_to_name[node_num]['name']

    def ancestors(self, taxon):
        """Return a list of all ancestors of the taxon starting with the taxon itself."""
        parents = [taxon]
        parent_num = self.parent_map[self._node(taxon)]
        while parent_num:
            parents.append(self.nodes_to_name[parent_num]['name'])
            parent_num = self.parent_map[parent_num]
        return parents

    def parent(self, taxon):
        """Return the name of the parent taxon."""
        return self._name(self.parent_map[self._node(taxon)])

    def phyla(self, taxon):
        """Return the phyla for the given taxon."""
        parent_num = self.parent_map[self._node(taxon)]
        while parent_num:
            if 'phylum' == self.nodes_to_name[parent_num]['rank']:
                return self.nodes_to_name[parent_num]['name']
            parent_num = self.parent_map[parent_num]
        raise KeyError(f'Phyla for taxa {taxon} not found.')

    def _tree(self, taxa):
        queue, tree = {self._node(el) for el in taxa}, {}
        root = None
        while len(queue):
            cur_node = queue.pop()
            parent_node = self.parent_map[cur_node]
            if cur_node not in tree:
                tree[cur_node] = {'parent': parent_node, 'children': set()}
            if not parent_node:
                root = cur_node
                continue
            try:
                tree[parent_node]['children'].add(cur_node)
            except KeyError:
                tree[parent_node] = {
                    'parent': self.parent_map[parent_node],
                    'children': set([cur_node])
                }
            queue.add(parent_node)
        return root, tree

    def taxa_sort(self, taxa):
        """Return a list with all elements of taxa in DFS order."""
        taxa, sort = set(taxa), []
        root, tree = self._tree(taxa)

        def dfs(node):
            for child_node in tree[node]['children']:
                child = self._name(child_node)
                if child in taxa:
                    sort.append(child)
                dfs(child_node)
        dfs(root)  # typically 1 is the root node
        return sort

    @classmethod
    def parse_files(cls, names_filename=None, nodes_filename=None):
        """Return a tree parsed from the given files."""
        names_filename = names_filename if names_filename else environ.get(NAMES_ENV_VAR, NAMES_DEF)
        nodes_filename = nodes_filename if nodes_filename else environ.get(NODES_ENV_VAR, NODES_DEF)
        with gzip.open(names_filename) as names_file, gzip.open(nodes_filename) as nodes_file:
            names_to_nodes, nodes_to_name = {}, {}
            for line in names_file:
                line = line.decode('utf-8')
                tkns = [tkn.strip() for tkn in line.strip().split(NCBI_DELIM)]
                if tkns[3] != 'scientific name':
                    continue
                node, name = tkns[:2]
                names_to_nodes[name] = node
                nodes_to_name[node] = {'name': name, 'rank': None}

            parent_map = {}
            for line in nodes_file:
                line = line.decode('utf-8')
                tkns = [tkn.strip() for tkn in line.strip().split(NCBI_DELIM)]
                node, parent, rank = tkns[:3]
                nodes_to_name[node]['rank'] = rank
                if node == parent:  # NCBI has a self loop at the root
                    parent = None
                parent_map[node] = parent

        return cls(parent_map, names_to_nodes, nodes_to_name)
