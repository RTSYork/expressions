#!/usr/bin/env python3

from pycparser import parse_file, c_ast
import pygraphviz as pgv
import sys


def add_node(graph, node_id, node_label, parent_id=None, edge_label='', color=''):
	print(node_id, node_label.replace('\n', ' '))
	graph.add_node(node_id, style='filled', fillcolor=color, label=node_label)
	if parent_id != None:
		graph.add_edge(parent_id, node_id, label=edge_label)


def parse_node(graph, node, parent_id=None, edge_label='', color='white'):
	global counter
	counter += 1

	node_id = str(counter)
	node_label = type(node).__name__
	subgraph = graph

	for attr in node.attr_names:
		val = getattr(node, attr)
		node_label += '\n{}: {}'.format(attr, val)

	if isinstance(node, c_ast.Assignment):
		color = 'green'
		subgraph = graph.subgraph(name='cluster' + node_id)
	elif isinstance(node, c_ast.UnaryOp):
		color = 'green'
		subgraph = graph.subgraph(name='cluster' + node_id)
	elif isinstance(node, c_ast.Return):
		color = 'red'
		subgraph = graph.subgraph(name='cluster' + node_id)
	elif isinstance(node, c_ast.FuncDef):
		if node.decl.name == 'main':
			color = 'yellow'
	elif isinstance(node, c_ast.Compound):
		subgraph = graph.subgraph(name='cluster' + node_id)

	for child in node.children():
		parse_node(subgraph, child[1], node_id, child[0], color)

	add_node(graph, node_id, node_label, parent_id, edge_label, color)


filename = sys.argv[1]

ast = parse_file(filename, use_cpp=True)

ast_graph = pgv.AGraph()

counter = 0

parse_node(ast_graph, ast)

print(ast_graph.subgraphs())

ast_graph.layout('dot')
ast_graph.write(filename+'-subgraphs.dot')
ast_graph.draw(filename+'-subgraphs.png')
