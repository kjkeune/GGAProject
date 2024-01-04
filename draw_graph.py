import math
import pygraphviz as pgv
import argparse
import os
import csv

def read_data(path) -> list:
    data = []
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["transfers"] = int(row["transfers"])
            data.append(row)
    return data

def color_blue_weighted2(trans, max):
    hue = 0.61
    min_sat = 0.15
    sat = (1 - min_sat) * (trans / max) + min_sat
    return "x11", f"{hue} {sat} 1"

def color_blue_weighted(trans, max):
    level = math.ceil((trans / max) * 7) + 2
    return "blues9", str(level)

def draw_graph(data: list, path) -> pgv.AGraph:
    graph = pgv.AGraph(strict=False, directed=True)
    # sort data by transfers, determine maximum
    data.sort(key=lambda item: item["transfers"])
    max_trans = data[len(data)-1]["transfers"]
    # iterate through data
    for item in data:
        n_from = item["club_from"]
        n_to = item["club_to"]
        trans = item["transfers"]
        # ---- customize nodes ----
        if not graph.has_node(n_from):
            graph.add_node(n_from)
        if not graph.has_node(n_to):
            graph.add_node(n_to)
        # ---- customize edges ----
        #colorscheme, color = "x11", "black"
        colorscheme, color = color_blue_weighted2(trans, max_trans)
        graph.add_edge(n_from, n_to, penwidth=trans/2, weight=trans, color=color, colorscheme=colorscheme)
    #---- customize graph ----
    graph.graph_attr["scale"] = "7"
    graph.graph_attr["outputorder"] = 'edgesfirst'
    graph.graph_attr["splines"] = "false"
    graph.draw(path, prog="twopi")     

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", type=str)
    parser.add_argument("outputfile", type=str)
    args = parser.parse_args()
    path_in = os.path.join("data_extract", args.inputfile)
    path_out = os.path.join("drawings", args.outputfile)
    draw_graph(read_data(path_in),path_out)
    

    