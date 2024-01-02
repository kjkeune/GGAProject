import pygraphviz as pgv
import argparse
import os
import csv

def create_graph(data) -> pgv.AGraph:
    graph = pgv.AGraph(strict=False, directed=True)
    for item in data:
        if not graph.has_node(item["club_from"]):
            graph.add_node(item["club_from"])
        if not graph.has_node(item["club_to"]):
            graph.add_node(item["club_to"])
        graph.add_edge(item["club_from"], item["club_to"], weight=int(item["transfers"]))
    return graph
        

def read_data(path) -> list:
    data = []
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", type=str)
    args = parser.parse_args()
    path_in = os.path.join("./data_extract", args.inputfile)
    graph = create_graph(read_data(path_in))
    graph.graph_attr["scale"] = "5"
    graph.draw("graph.pdf", prog="neato")

    