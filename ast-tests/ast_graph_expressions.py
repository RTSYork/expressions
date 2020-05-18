#!/usr/bin/env python3

import pycparser
from pycparser import c_ast
import pygraphviz as pgv
import sys


def add_node(graph, node_id, node_label, parent_id=None, edge_label='', color='', inverse=False, shape='', dir='', style='filled'):
	print(node_id, node_label.replace('\n', ' '))
	graph.add_node(node_id, fillcolor=color, label=node_label, shape=shape, style=style)
	if parent_id is not None:
		if inverse:
			graph.add_edge(node_id, parent_id, label=edge_label, dir=dir)
		else:
			graph.add_edge(parent_id, node_id, label=edge_label, dir=dir)


def add_order(node_id):
	global order_id
	ordering.add_edge(order_id, node_id, style='invis')
	order_id = node_id


def parse_node(graph, expression, node, parent_id=None, edge_label='', color='white'):
	global counter
	global order_id
	counter += 1

	node_id = str(counter)
	node_label = type(node).__name__
	subgraph = graph
	e = expression
	shape = ''
	inverse = False
	expression_parent_id = parent_id
	draw_node = True
	node_style = 'filled'

	for attr in node.attr_names:
		val = getattr(node, attr)
		node_label += '\n{}: {}'.format(attr, val)

	expression_label = node_label

	if isinstance(node, c_ast.Assignment):
		color = 'green'
		subgraph = graph.subgraph(name='cluster' + node_id)
		if e is None:
			e = expressions
			expression_parent_id = None
			add_order(node_id)
			e = e.subgraph(name='cluster' + node_id)
			node_style += ',bold'
		expression_label = node.op
	elif isinstance(node, c_ast.UnaryOp):
		color = 'green'
		subgraph = graph.subgraph(name='cluster' + node_id)
		if node.op in ('++', 'p++', '--', 'p--'):
			if e is None:
				e = expressions
				expression_parent_id = None
				add_order(node_id)
				e = e.subgraph(name='cluster' + node_id)
				node_style += ',bold'
				expression_label = node.op
	elif isinstance(node, c_ast.Decl):
		color = 'green'
		subgraph = graph.subgraph(name='cluster' + node_id)
		if node.init is not None:
			if e is None:
				e = expressions
				expression_parent_id = None
				add_order(node_id)
				e = e.subgraph(name='cluster' + node_id)
				node_style += ',bold'
				expression_label = '='
	elif isinstance(node, c_ast.Return):
		color = 'red'
		subgraph = graph.subgraph(name='cluster' + node_id)
		if e is None:
			e = expressions
			expression_parent_id = None
			add_order(node_id)
			e = e.subgraph(name='cluster' + node_id)
			node_style += ',bold'
		shape = 'square'
		expression_label = '\\<ret\\>'
	elif isinstance(node, c_ast.BinaryOp):
		color = 'yellow'
		expression_label = node.op
	elif isinstance(node, c_ast.Constant):
		shape = 'square'
		color = 'pink'
		expression_label = node.value
	elif isinstance(node, c_ast.ID):
		shape = 'square'
		color = 'lightblue'
		expression_label = node.name
	elif isinstance(node, c_ast.TypeDecl):
		shape = 'square'
		color = 'lightblue'
		if node.declname is not None:
			expression_label = node.declname
	elif isinstance(node, c_ast.IdentifierType):
		e = None

	if edge_label in ('lvalue', 'type'):
		inverse = True

	if e is not None:
		add_node(e, node_id, expression_label, expression_parent_id, '', color, inverse=inverse, shape=shape, dir='back', style=node_style)

	for child in node.children():
		parse_node(subgraph, e, child[1], node_id, child[0], color)

	add_node(graph, node_id, node_label, parent_id, edge_label, color)


filename = sys.argv[1]

ast = pycparser.parse_file(filename, use_cpp=True)

ast_graph = pgv.AGraph()
expressions = pgv.AGraph(newrank='true')
expressions.add_node('rank1', label='', style='invisible')
expressions.add_node('rank2', label='', style='invisible')

counter = 0

expressions.add_edge('rank1', 'rank2', style='invis')
ordering = expressions.subgraph(rank = 'same', rankdir = 'LR')
order_id = 'rank2'

parse_node(ast_graph, None, ast)

expressions.add_node('end', label='', style='invisible')
ordering.add_edge(order_id, 'end', style='invis')

# ast_graph.layout('dot')
# ast_graph.write(filename+'-subgraphs.dot')
# ast_graph.draw(filename+'-subgraphs.png')

expressions.layout('dot')
expressions.write(filename+'-expressions.dot')
expressions.draw(filename+'-expressions.png')
