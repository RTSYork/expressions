#!/usr/bin/env python3

import pycparser
from pycparser import c_ast
import pygraphviz as pgv
import argparse


def add_node(graph, node_id, node_label, parent_id=None, edge_label='', color='', invert=False, shape='', direction='', style='filled'):
	if verbosity > 1:
		print(node_id, node_label.replace('\n', ' '))

	# Add node to graph
	graph.add_node(node_id, fillcolor=color, label=node_label, shape=shape, style=style)

	# Create edge to or from parent (if it exists), depending on inversion
	if parent_id is not None:
		if invert:
			graph.add_edge(node_id, parent_id, label=edge_label, dir=direction)
		else:
			graph.add_edge(parent_id, node_id, label=edge_label, dir=direction)


def add_order(node_id):
	global order_id
	ordering.add_edge(order_id, node_id, style='invis')
	order_id = node_id


def parse_node(graph, expression, node, parent_id=None, edge_label='', color='white'):
	global counter
	global order_id
	counter += 1

	# Set up default options for node
	node_id = str(counter)
	node_label = type(node).__name__
	subgraph = graph
	e = expression
	shape = ''
	invert = False
	expression_parent_id = parent_id
	ast_node_style = 'filled'
	expression_node_style = 'filled'
	coordinate = str(node.coord).split('/')[-1]

	# Add any attributes to the node label (e.g. name, op, type, etc.)
	for attr in node.attr_names:
		val = getattr(node, attr)
		node_label += '\n{}: {}'.format(attr, val)

	expression_label = node_label

	# Deal with various different node types by changing the defaults and creating expressions
	if isinstance(node, c_ast.Assignment):
		# Colour assigment in green, and create expression around it
		color = 'green'
		subgraph = graph.subgraph(name='cluster' + node_id, label=coordinate)
		if e is None:
			e = expressions
			expression_parent_id = None
			add_order(node_id)
			e = e.subgraph(name='cluster' + node_id, label=coordinate)
			expression_node_style += ',bold'
		expression_label = node.op
	elif isinstance(node, c_ast.UnaryOp):
		# Colour unary operator in green, and create new expression around it if increment or decrement
		color = 'green'
		if node.op in ('++', 'p++', '--', 'p--'):
			subgraph = graph.subgraph(name='cluster' + node_id, label=coordinate)
			if e is None:
				e = expressions
				expression_parent_id = None
				add_order(node_id)
				e = e.subgraph(name='cluster' + node_id, label=coordinate)
				expression_node_style += ',bold'
				expression_label = node.op
		else:
			subgraph = graph.subgraph(name='cluster' + node_id, style="dashed", label=coordinate)
	elif isinstance(node, c_ast.Decl):
		# Colour declaration in green, and create new expression around it if an initialiser
		color = 'green'
		if node.init is not None:
			subgraph = graph.subgraph(name='cluster' + node_id, label=coordinate)
			if e is None:
				e = expressions
				expression_parent_id = None
				add_order(node_id)
				e = e.subgraph(name='cluster' + node_id, label=coordinate)
				expression_node_style += ',bold'
				expression_label = '='
		else:
			subgraph = graph.subgraph(name='cluster' + node_id, style="dashed", label=coordinate)
	elif isinstance(node, c_ast.Return):
		# Colour return in red, and create new expression around it
		color = 'red'
		subgraph = graph.subgraph(name='cluster' + node_id, label=coordinate)
		if e is None:
			e = expressions
			expression_parent_id = None
			add_order(node_id)
			e = e.subgraph(name='cluster' + node_id, label=coordinate)
			expression_node_style += ',bold'
		shape = 'square'
		expression_label = '\\<ret\\>'
	elif isinstance(node, c_ast.BinaryOp):
		# Colour binary operator in yellow
		color = 'yellow'
		expression_label = node.op
	elif isinstance(node, c_ast.Constant):
		# Colour constant operator in pink
		shape = 'square'
		color = 'pink'
		expression_label = node.value
	elif isinstance(node, c_ast.ID):
		# Colour identifier in light blue
		shape = 'square'
		color = 'lightblue'
		expression_label = node.name
	elif isinstance(node, c_ast.TypeDecl):
		# Colour type declarations in light blue
		shape = 'square'
		color = 'lightblue'
		if node.declname is not None:
			expression_label = node.declname
	elif isinstance(node, c_ast.IdentifierType):
		# Don't include type identifiers in expression graphs
		e = None

	# Invert the direction of lvalue edges to show them opposite (above) rvalues in expressions
	if edge_label in ('lvalue', 'type'):
		invert = True

	# If parsing a node that is part of an expression, add it to the current expression subgraph
	if e is not None:
		add_node(e, node_id, expression_label, expression_parent_id, '', color, invert=invert, shape=shape,
		         direction='back', style=expression_node_style)
	else:
		ast_node_style += ',dashed'

	# Recursively parse the children of this node
	for child in node.children():
		parse_node(subgraph, e, child[1], node_id, child[0], color)

	# Add this node to the AST graph (or subgraph)
	add_node(graph, node_id, node_label, parent_id, edge_label, color, style=ast_node_style)


parser = argparse.ArgumentParser(description='Extract expressions from C source.')
parser.add_argument('source_file')
parser.add_argument('-t', '--ast', metavar='output_file', help='output AST graph to this file')
parser.add_argument('-e', '--expressions', metavar='output_file', help='output expression graphs to this file')
parser.add_argument('-p', '--png', action='store_true', default=0, help='output PNG file')
parser.add_argument('-d', '--dot', action='store_true', default=0, help='output DOT file')
parser.add_argument('-v', '--verbose', action='count', default=0, help='verbose output')
args = parser.parse_args()

source_filename = args.source_file
ast_output = args.ast
expressions_output = args.expressions
output_png = args.png
output_dot = args.dot
verbosity = args.verbose

if verbosity > 0:
	print(f"Parsing file '{source_filename}'...")

ast = pycparser.parse_file(source_filename, use_cpp=True)

if verbosity > 0:
	print(f"Constructing graphs...")

# Create graph for expressions
ast_graph = pgv.AGraph()
expressions = pgv.AGraph(newrank='true')

# Set up vertical alignment and deterministic left-right ordering of source file statements
expressions.add_node('rank1', label='', style='invis', width=0)
expressions.add_node('rank2', label='', style='invis', width=0)
expressions.add_edge('rank1', 'rank2', style='invis')
ordering = expressions.subgraph(rank='same', rankdir='LR')
order_id = 'rank2'

# Recursively parse the AST for expressions
counter = 0
parse_node(ast_graph, None, ast)

# Add final node on right-hand-side to complete left-right ordering
expressions.add_node('end', label='', style='invis', width=0)
ordering.add_edge(order_id, 'end', style='invis')

if ast_output is not None:
	ast_graph.layout('dot')
	if output_dot:
		if verbosity > 0:
			print(f"Outputting AST graph to '{ast_output}.dot'...")
		ast_graph.write(ast_output + '.dot')
	if output_png:
		if verbosity > 0:
			print(f"Outputting AST graph to '{ast_output}.png'...")
		ast_graph.draw(ast_output + '.png')

if expressions_output is not None:
	expressions.layout('dot')
	if output_dot:
		if verbosity > 0:
			print(f"Outputting expression graphs to '{expressions_output}.dot'...")
		expressions.write(expressions_output + '.dot')
	if output_png:
		if verbosity > 0:
			print(f"Outputting expression graphs to '{expressions_output}.png'...")
		expressions.draw(expressions_output + '.png')

if verbosity > 0:
	print('Done.')
