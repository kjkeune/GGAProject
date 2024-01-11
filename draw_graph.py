import math
import pygraphviz as pgv
import os
from data_extract import *

def color_weighted(color_hue, trans, max):
    min_sat = 0.15
    sat = (1 - min_sat) * (trans / max) + min_sat
    return "x11", f"{color_hue} {sat} 1"

def color_blue_weighted(trans, max):
    level = math.ceil((trans / max) * 7) + 2
    return "blues9", str(level)

def add_league_subgraph(graph: pgv.AGraph, league, data) -> pgv.AGraph:
    # sort data by transfers, determine maximum
    subnodes = []
    data.sort(key=lambda item: item["transfers"])
    max_trans = data[len(data)-1]["transfers"]
    # iterate through data
    for item in data:
        n_from = item["club_from"]
        n_to = item["club_to"]
        trans = item["transfers"]
        # ---- customize nodes ----
        if not graph.has_node(n_from):
            subnodes.append(n_from)
            graph.add_node(n_from)
        if not graph.has_node(n_to):
            subnodes.append(n_to)
            graph.add_node(n_to)
        # ---- customize edges ----
        #colorscheme, color = "x11", "black"
        colorscheme, color = color_weighted(0.61, trans, max_trans)
        graph.add_edge(n_from, n_to, penwidth=trans/2, weight=trans, color=color, colorscheme=colorscheme) 
    subgraph = graph.add_subgraph(subnodes, league, cluster=True)
    return subgraph
    

def draw_graph(leagues: list, outfile, from_year=1990, to_year=2022, layout="neato", scale=7) -> pgv.AGraph:
    path_out = os.path.join("drawings", outfile)
    graph = pgv.AGraph(strict=False, directed=True)
    out_league = []
    for league in leagues:
        d_in, d_out = extract_league(league, from_year, to_year)
        g_l = add_league_subgraph(graph, league, d_in)
        out_league.extend(d_out)
    graph.graph_attr["outputorder"] = "edgesfirst"
    graph.graph_attr["splines"] = "false"
    graph.graph_attr["scale"] = str(scale)
    graph.draw(path_out, prog=layout)

if __name__=="__main__":
    draw_graph(["1-bundesliga", "championship"],"test.pdf")
    

    