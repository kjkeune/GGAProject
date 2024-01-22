import math
import pygraphviz as pgv
import argparse
import os
import csv
import math
import pygraphviz as pgv
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
    graph = pgv.AGraph(strict=False, directed=True, outputorder='edgesfirst')
    data.sort(key=lambda item: item["transfers"])
    max_trans = data[len(data) - 1]["transfers"]
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
        # colorscheme, color = "x11", "black"
        colorscheme, color = color_blue_weighted(trans, max_trans)
        trans /= 2
        graph.add_edge(n_from, n_to, penwidth=trans, color=color, colorscheme=colorscheme)
    return graph


for filename in os.listdir("./data"):
    if filename == "all_data.csv":
        continue
    path_in = os.path.join("./data", filename)
    path_out = os.path.join("./data_extract", filename)
    data = {}
    allowed_clubs = set()
    # read cvs file
    with open(path_in, errors="ignore", encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            allowed_clubs.add(row["club_name"])
            # recent years only
            if int(row["year"]) < 2020:
                continue
            # only known clubs
            if row["club_involved_name"] == "Unknown":
                continue
            # determine direction of transfer
            if row["transfer_movement"] == "out":
                transfer = (row["club_name"],row["club_involved_name"])
            elif row["transfer_movement"] == "in":
                transfer = (row["club_involved_name"], row["club_name"])
            # add transfer to data
            if not transfer in data:
                data[transfer] = 1
            else:
                data[transfer] += 1
    # write data to cvs file
    with open(path_out, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["club_from","club_to","transfers"])
        for item in data.items():
            if not item[0][1] in allowed_clubs or not item[0][0] in allowed_clubs:
                continue
            writer.writerow([item[0][0], item[0][1], item[1]])
    print(f"Data written to {path_out}")

    path_in = os.path.join(path_out)
    graph = create_graph(read_data(path_in))
    graph.graph_attr["scale"] = "5"
    path_out = filename.split(".")[0]
    graph.draw("./drawings/" + path_out + ".svg", prog="neato")


