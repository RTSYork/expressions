#!/usr/bin/env python3

import pycparser
from pycparser import c_ast
import pygraphviz as pgv
import sys


def add_node(node_id, node_label, parent_id=None, edge_label='', color=''):
	print(node_id, node_label.replace('\n', ' '))
	graph.add_node(node_id, style='filled', fillcolor=color, label=node_label)
	if parent_id is not None:
		graph.add_edge(parent_id, node_id, label=edge_label)


def parse_node(node, parent_id=None, edge_label=''):
	global counter
	counter += 1

	node_id = str(counter)
	color = 'white'
	node_label = type(node).__name__

	for attr in node.attr_names:
		val = getattr(node, attr)
		node_label += '\n{}: {}'.format(attr, val)

	add_node(node_id, node_label, parent_id, edge_label, color)

	for child in node.children():
		parse_node(child[1], node_id, edge_label=child[0])


filename = sys.argv[1]

ast = pycparser.parse_file(filename, use_cpp=True)

graph = pgv.AGraph()

counter = 0

parse_node(ast)

graph.layout('dot')
graph.write(filename+'.dot')
graph.draw(filename+'.png')
