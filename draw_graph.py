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

def color_blue_weighted(trans, max):
    level = math.ceil((trans / max) * 7) + 2
    return "blues9", str(level)

def create_graph(data: list) -> pgv.AGraph:
    graph = pgv.AGraph(strict=False, directed=True)
    data.sort(key=lambda item: item["transfers"])
    max_trans = data[len(data)-1]["transfers"]
    for item in data:
        n_from = item["club_from"]
        n_to = item["club_to"]
        trans = item["transfers"]
        # ---- nodes ----
        if not graph.has_node(n_from):
            graph.add_node(n_from)
        if not graph.has_node(n_to):
            graph.add_node(n_to)
        # ---- edges ----
        #colorscheme, color = "x11", "black"
        colorscheme, color = color_blue_weighted(trans, max_trans)
        graph.add_edge(n_from, n_to, weight=trans, color=color, colorscheme=colorscheme)
    return graph       

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", type=str)
    args = parser.parse_args()
    path_in = os.path.join("./data_extract", args.inputfile)

    graph = create_graph(read_data(path_in))
    graph.graph_attr["scale"] = "5"
    graph.draw("drawings/graph_twopi_cbw.pdf", prog="twopi")

    