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
    return "reds9", str(level)


def create_graph(data: list) -> pgv.AGraph:
    graph = pgv.AGraph(strict=False, directed=True, outputorder='edgesfirst')
    data.sort(key=lambda item: item["transfers"])
    max_trans = data[len(data) - 1]["transfers"]
    for item in data:
        n_from = item["league_from"]
        n_to = item["league_to"]
        trans = item["transfers"]
        # ---- nodes ----
        scale = 4
        if not graph.has_node(n_from):
            graph.add_node(n_from, width=scale, height=scale, fontcolor="transparent")
        if not graph.has_node(n_to):
            graph.add_node(n_to, width=scale, height=scale, fontcolor="transparent")
        # ---- edges ----
        # colorscheme, color = "x11", "black"
        colorscheme, color = color_blue_weighted(trans, max_trans)
        trans /= 7
        graph.add_edge(n_from, n_to, penwidth=trans, color=color, colorscheme=colorscheme)
    return graph


if __name__ == "__main__":
    path_in = os.path.join("./data_extract", "league_transfer.csv")

    graph = create_graph(read_data(path_in))
    # graph = create_graph(read_data("./data_extract/extract.csv"))
    graph.graph_attr["scale"] = "5"
    graph.draw("drawings/leagues_empty.svg", prog="fdp")

