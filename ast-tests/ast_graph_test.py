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
	node_label = None

	color = 'white'
	
	if isinstance(node, c_ast.FileAST):
		node_label = 'FileAST'
		parse_node(node.ext, node_id, 'ext')
	elif isinstance(node, c_ast.Decl):
		node_label = 'Decl\n{}'.format(node.name)
		parse_node(node.type, node_id, 'type')
		parse_node(node.init, node_id, 'init')
	elif isinstance(node, c_ast.TypeDecl):
		node_label = 'TypeDecl\n{}'.format(node.declname)
		parse_node(node.type, node_id, 'type')
	elif isinstance(node, c_ast.PtrDecl):
		node_label = 'PtrDecl'
		parse_node(node.type, node_id, 'type')
	elif isinstance(node, c_ast.ArrayDecl):
		node_label = 'ArrayDecl'
		parse_node(node.type, node_id, 'type')
		parse_node(node.dim, node_id, 'dim')
	elif isinstance(node, c_ast.IdentifierType):
		node_label = 'IdentifierType\n{}'.format(node.names)
	elif isinstance(node, c_ast.FuncDef):
		node_label = 'FuncDef'
		parse_node(node.decl, node_id, 'decl')
		parse_node(node.body, node_id, 'body')
	elif isinstance(node, c_ast.FuncDecl):
		node_label = 'FuncDecl'
		parse_node(node.args, node_id, 'args')
		parse_node(node.type, node_id, 'type')
	elif isinstance(node, c_ast.ParamList):
		node_label = 'ParamList'
		parse_node(node.params, node_id, 'params')
	elif isinstance(node, c_ast.Typename):
		node_label = 'Typename\n{}'.format(node.name)
		parse_node(node.type, node_id, 'type')
	elif isinstance(node, c_ast.Compound):
		node_label = 'Compound'
		parse_node(node.block_items, node_id, 'block_items')
	elif isinstance(node, c_ast.Assignment):
		node_label = 'Assignment\n{}'.format(node.op)
		parse_node(node.lvalue, node_id, 'lvalue')
		parse_node(node.rvalue, node_id, 'rvalue')
	elif isinstance(node, c_ast.UnaryOp):
		node_label = 'UnaryOp\n{}'.format(node.op)
		parse_node(node.expr, node_id, 'expr')
	elif isinstance(node, c_ast.BinaryOp):
		node_label = 'BinaryOp\n{}'.format(node.op)
		parse_node(node.left, node_id, 'left')
		parse_node(node.right, node_id, 'right')
	elif isinstance(node, c_ast.ID):
		node_label = 'ID\n{}'.format(node.name)
	elif isinstance(node, c_ast.Constant):
		node_label = 'Constant\n{} {}'.format(node.type, node.value)
	elif isinstance(node, c_ast.Return):
		node_label = 'Return'
		parse_node(node.expr, node_id, 'expr')
	elif isinstance(node, c_ast.FuncCall):
		node_label = 'FuncCall'
		parse_node(node.name, node_id, 'name')
		parse_node(node.args, node_id, 'args')
	elif isinstance(node, c_ast.ExprList):
		node_label = 'ExprList'
		parse_node(node.exprs, node_id, 'expr')
	elif isinstance(node, c_ast.If):
		node_label = 'If'
		parse_node(node.cond, node_id, 'cond')
		parse_node(node.iftrue, node_id, 'iftrue')
		parse_node(node.iffalse, node_id, 'iffalse')
	elif isinstance(node, c_ast.TernaryOp):
		node_label = 'TernaryOp'
		parse_node(node.cond, node_id, 'cond')
		parse_node(node.iftrue, node_id, 'iftrue')
		parse_node(node.iffalse, node_id, 'iffalse')
	elif isinstance(node, c_ast.While):
		node_label = 'While'
		parse_node(node.cond, node_id, 'cond')
		parse_node(node.stmt, node_id, 'stmt')
	elif isinstance(node, c_ast.DoWhile):
		node_label = 'DoWhile'
		parse_node(node.cond, node_id, 'cond')
		parse_node(node.stmt, node_id, 'stmt')
	elif isinstance(node, c_ast.For):
		node_label = 'For'
		parse_node(node.init, node_id, 'init')
		parse_node(node.cond, node_id, 'cond')
		parse_node(node.next, node_id, 'next')
		parse_node(node.stmt, node_id, 'stmt')
	elif isinstance(node, c_ast.Switch):
		node_label = 'Switch'
		parse_node(node.cond, node_id, 'cond')
		parse_node(node.stmt, node_id, 'stmt')
	elif isinstance(node, c_ast.Case):
		node_label = 'Case'
		parse_node(node.expr, node_id, 'expr')
		parse_node(node.stmts, node_id, 'stmts')
	elif isinstance(node, c_ast.Default):
		node_label = 'Default'
		parse_node(node.stmts, node_id, 'stmts')
	elif isinstance(node, c_ast.Break):
		node_label = 'Break'
	elif isinstance(node, c_ast.Continue):
		node_label = 'Continue'
	elif isinstance(node, c_ast.EmptyStatement):
		node_label = 'EmptyStatement'
	elif isinstance(node, c_ast.EllipsisParam):
		node_label = 'EllipsisParam'
	elif isinstance(node, c_ast.Struct):
		node_label = 'Struct\n{}'.format(node.name)
		parse_node(node.decls, node_id, 'decls')
	elif isinstance(node, c_ast.Union):
		node_label = 'Union\n{}'.format(node.name)
		parse_node(node.decls, node_id, 'decls')
	elif isinstance(node, c_ast.Typedef):
		node_label = 'Typedef\n{}'.format(node.name)
		parse_node(node.type, node_id, 'type')
	elif isinstance(node, c_ast.DeclList):
		node_label = 'DeclList'
		parse_node(node.decls, node_id, 'decls')
	elif isinstance(node, c_ast.Label):
		node_label = 'Label\n{}'.format(node.name)
		parse_node(node.stmt, node_id, 'stmt')
	elif isinstance(node, c_ast.Goto):
		node_label = 'Goto\n{}'.format(node.name)
	elif isinstance(node, c_ast.StructRef):
		node_label = 'StructRef\n{}'.format(node.type)
		parse_node(node.name, node_id, 'name')
		parse_node(node.field, node_id, 'field')
	elif isinstance(node, c_ast.Cast):
		node_label = 'Cast'
		parse_node(node.to_type, node_id, 'to_type')
		parse_node(node.expr, node_id, 'expr')
	elif isinstance(node, c_ast.Pragma):
		node_label = 'Pragma\n{}'.format(node.string)
	elif isinstance(node, list):
		for i in range(len(node)):
			parse_node(node[i], parent_id, '{}[{}]'.format(edge_label, i))
	elif node is None:
		node_label = 'None'
		color = 'grey'
	else:
		node_label = str(type(node))
		color = 'red'

	if node_label is not None:
		add_node(node_id, node_label, parent_id, edge_label, color)


filename = sys.argv[1]

ast = pycparser.parse_file(filename, use_cpp=True)

graph = pgv.AGraph()

counter = 0

parse_node(ast)

graph.layout('dot')
graph.write(filename+'.dot')
graph.draw(filename+'.png')
