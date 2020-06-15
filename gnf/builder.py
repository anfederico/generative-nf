import os
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Data processing functions ----------------------------------------------------

def strip_process(x):
    x = x.replace(' ', '')
    return x

def split_process(x):
    s = x.split('->')
    return s[0], s[1]

def split_params(x):
    s = [i.split('=') for i in x.split('|')]
    d = {i[0].replace(' ', '') : i[1].replace(' ', '') for i in s}
    return d

def read_data(csv):
    df = pd.read_csv(csv, header=0)
    if ('process' not in list(df.columns)) | ('module' not in list(df.columns)):
        raise ValueError("Must have process and module columns defined")

    # Optionally include labels
    if 'label' not in list(df.columns):
        df['label'] = df.process.apply(lambda x: split_process(x)[1].lstrip())

    # Optionally include keyword arguments
    if 'params' not in list(df.columns):
        df['params'] = ''

    df = df[['process', 'label', 'module', 'params']]
    return df

# Tree building functions ----------------------------------------------------

from anytree import Node, LevelOrderIter, RenderTree, AsciiStyle

class Generative_Node(Node):
    separator = '->'

def new_node(name, **kwargs):
    node = Generative_Node(name, **kwargs)
    return(node)

def set_node(node, **kwargs):
    for k, v in kwargs.items():
        setattr(node, k, v)
    return(node)

def get_node(nodes, name):
    try:
        node = nodes[name]
    except KeyError:
        node = new_node(name)
        nodes[name] = node
    return nodes, node

def build_tree(df):
    nodes = {}

    # For each interaction
    for i, row in df.iterrows():
        x = row['process']

        if x == '' or '->' not in x:
            continue 

        s1, s2 = split_process(strip_process(x))

        if s1 == '':
            nodes[s2] = new_node(s2)
        else:
            nodes, node_p = get_node(nodes, s1)
            nodes, node_c = get_node(nodes, s2)
            node_c.parent = node_p

    # As every node has just one parent...
    # the easiest way to handle edge parameters...
    # is to store them in the child
    for i, row in df.iterrows():
        x, label, module, params = row['process'], row['label'], row['module'], row['params']
        
        # Grab child node for each process
        s1, s2 = split_process(strip_process(x))
        node = nodes[s2]

        # Create kwargs
        kwargs = split_params(params)
        kwargs['child'] = node.name
        if not node.is_root:
            kwargs['parent'] = node.parent.name        

        nodes[s2] = set_node(node, 
                             label=label, 
                             module=module, 
                             params=params,
                             kwargs=kwargs)

    roots = [node for process, node in nodes.items() if node.is_root]
    if len(roots) > 1:
        raise ValueError("Multiple roots detected...")
    else:
        tree = roots[0]
    return tree

def print_tree(tree):
    for pre, fill, node in RenderTree(tree, style=AsciiStyle()):
        print("{0}{1} [{2}]".format(pre, node.label, node.module))
        if node.params != '':
            kwargs = split_params(node.params)
            for k,v in kwargs.items():
                print("{0}{1}: {2}".format(fill, k, v))
            print("{0}".format(fill))

def render_tree(tree, *args):
    return RenderTree(tree, style=AsciiStyle()).by_attr(*args)

def traverse_tree(tree):
    return LevelOrderIter(tree)
