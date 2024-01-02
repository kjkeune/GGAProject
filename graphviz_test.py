import pygraphviz as pgv

g = pgv.AGraph()
g.add_cycle(['1','2','3','4','5'])
g.add_edge('2','5')
g.add_edge('3','5')
g.add_edge('1','4')
g.add_node('6')
g.add_edge('1','6')
g.add_edge('4','6')
g.add_node('7')
g.add_edge('6','7')

g.graph_attr["scale"] = "3.4"
g.draw("graph.pdf", prog="neato")