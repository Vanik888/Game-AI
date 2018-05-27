import os

from graphviz import render
from collections import defaultdict

current_dir = os.path.abspath(os.path.dirname(__name__))
plots_dir = os.path.join(current_dir, 'plots')


def plotter(tree, plot_name):
    global plots_dir
    dot_file = os.path.join(plots_dir, '{}.dot'.format(plot_name))

    with open(dot_file, 'w') as f:
        f.write('digraph Tree {\n'
                'node [shape=box, style="filled", color="black"] ;\n')

    dependencies = defaultdict(list)
    node = tree.root
    root = 0
    print_node(node, dot_file, root, dependencies, depth=0)
    write_dependencies(dependencies, dot_file)
    with open(dot_file, 'a') as f:
        f.write('}\n')

    render('dot', 'png', dot_file)


def print_node(node, file_name, root, dependencies, depth):
    colors = ['#2980d1', '#90d129']

    with open(file_name, 'a') as f:
        f.write('{} [label=<name = {name}<br/>\n'
                'value = {value}<br/>\n'
                '>, fillcolor="{color}"] ;\n'
                .format(root, name=node.name, value=node.val,
                        color=colors[depth % 2]))
        if not node.child_list:
            return

    for c in node.child_list:
        new_root = check_dependencies(dependencies, root)
        dependencies[root].append(new_root)
        print_node(c, file_name, new_root, dependencies, depth=depth+1)


def write_dependencies(dependencies, file_name):
    with open(file_name, 'a') as f:
        for key, val in dependencies.items():
            for v in val:  # 4 -> 6 [labeldistance=2.5, labelangle=-45, headlabel="No"] ;
                f.write('{} -> {} ;\n'.format(key, v))


def check_dependencies(dependencies, root):
    new_root = root + 1
    for key, value in dependencies.items():
        if new_root == key:
            new_root += 1
        if new_root in value:
            new_root = max(value) + 1
    return new_root
