import sys
import logging

from trees import tree1, values1, tree2, values2
from plotter import plotter

logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format='%(levelname)s | %(asctime)s | %(message)s')
logger = logging.getLogger('Logger from Task 2.2')


class Node:
    def __init__(self, name, val, child_list=[]):
        self.name = name
        self.val = val
        self.child_list = child_list

    def __repr__(self):
        return '<Node %s = %s>' % (self.name, self.val)


class Tree:
    def __init__(self):
        self.root = None

    def build_tree_from_dict(self, struct, values):
        sorted_dict = dict(sorted(struct.items(), key=lambda kv: kv[0]))
        root_name = list(sorted_dict.keys())[0]

        self._build_tree_from_dict(sorted_dict, values, root_name)

    def _build_tree_from_dict(self, struct, values, nodename):
        child_list = struct.get(nodename, [])
        val = values.get(nodename, None)

        node = Node(nodename, val)
        if self.root is None:
            self.root = node

        _child_list = []
        for c in child_list:
            c_node = self._build_tree_from_dict(struct, values, c)
            _child_list.append(c_node)
        node.child_list = _child_list

        return node

    def pretraverse(self):
        self._pretraverse(self.root)

    def _pretraverse(self, node, offset=0):
        print('%s%s=%s' % (' '*offset, node.name, getattr(node, 'val', '')))

        for c in node.child_list:
            self._pretraverse(c, offset+1)

    def min_max(self):
        self.root.val = self.mmax(self.root, player=1)

    def mmax(self, node, player):
        if not node.child_list:
            return node.val
        else:
            child_values = []
            for c in node.child_list:
                child_values.append(self.mmin(c, player=player*(-1)))
            node.val = max(child_values)
            return node.val

    def mmin(self, node, player):
        if not node.child_list:
            return node.val
        else:
            child_values = []
            for c in node.child_list:
                child_values.append(self.mmax(c, player=player*(-1)))
            node.val = min(child_values)
            return node.val


if __name__ == '__main__':
    tr1 = Tree()
    tr1.build_tree_from_dict(tree1, values1)
    tr1.pretraverse()
    tr1.min_max()
    tr1.pretraverse()
    logger.info('Tree 2:')
    tr2 = Tree()
    tr2.build_tree_from_dict(tree2, values2)
    tr2.pretraverse()
    tr2.min_max()
    tr2.pretraverse()
    plotter(tr1, 'tree1')
    plotter(tr2, 'tree2')
