from collections import defaultdict


def print_node(node, file_name, root, dependencies):
    color = ['#399de506', '#e58139b0']

    with open(file_name, 'a') as f:
        f.write('{} [label=<player={player}<br/>\n'
                'winner = {winner}<br/>\n'
                '>, fillcolor="{color}"] ;\n'
                .format(root, player=node.p, winner=node.winner,
                        color=color[int(node.p)]))
        if not node.child_list:
            return

    for c in node.child_list:
        new_root = check_dependencies(dependencies, root)
        dependencies[root].append(new_root)
        print_node(c, file_name, new_root, dependencies)


def write_dependencies(dependencies, file_name):
    with open(file_name, 'a') as f:
        for key, val in dependencies.items():
            for v in val: #4 -> 6 [labeldistance=2.5, labelangle=-45, headlabel="No"] ;
                f.write('{} -> {} ;\n'.format(key, v))


def graphVis(tree, file_name):
    with open(file_name, 'w') as f:
        f.write('digraph Tree {\n'
                'node [shape=box, style="filled", color="black"] ;\n')

        node = tree.root
    dependencies = defaultdict(list)
    root = 0
    print_node(node, file_name, root, dependencies)
    write_dependencies(dependencies, file_name)

    with open(file_name, 'a') as f:
        f.write('}\n')


def check_dependencies(dependencies, root):
    new_root = root + 1
    for key, value in dependencies.items():
        if new_root == key:
            new_root += 1
        if new_root in value:
            new_root = max(value) + 1
    return new_root
