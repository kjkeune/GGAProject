import math
import pygraphviz as pgv
import os
from data_extract import *

ALL_LEAGUES = ["1-bundesliga", "eredivisie", "liga-nos", "ligue-1","premier-league","premier-liga","primera-division","serie-a"]

def league_transfers(data_in, leagues):
    club_league = extract_clubs_in_league()
    league_trans = {}
    for item in data_in:
        c_from = item["club_from"]
        c_to = item["club_to"]
        trans = item["transfers"]
        try:
            l_from = club_league[c_from]
            l_to = club_league[c_to]
            if not l_from in leagues or not l_to in leagues:
                continue
            transfer = (l_from, l_to)
            if not transfer in league_trans:
                league_trans[transfer] = trans
            else:
                league_trans[transfer] += trans
        except KeyError:
            continue
    data_out = []
    for item in league_trans.items():
        data_out.append({"league_from":item[0][0], "league_to":item[0][1], "transfers":item[1]})
    return data_out

def color_weighted(color_hue, trans, max_trans):
    min_sat = 0.15
    sat = (1 - min_sat) * (trans / max_trans) + min_sat
    return "x11", f"{color_hue} {sat} 1"

def penwidth_weighted(trans, max_trans):
    max_width = 10
    min_width = 0.2
    penwidth = max_width * (trans / max_trans)
    if penwidth < min_width:
        penwidth = min_width
    return penwidth

def color_blue_weighted(trans, max):
    level = math.ceil((trans / max) * 7) + 2
    return "blues9", str(level)

def draw_inleague_graph(league, outdir, data, layout, scale):
    # sort data by transfers, determine maximum
    graph = pgv.AGraph(strict=False, directed=True)
    data.sort(key=lambda item: item["transfers"])
    max_trans = data[len(data)-1]["transfers"]
    # iterate through data
    for item in data:
        n_from = item["club_from"]
        n_to = item["club_to"]
        trans = item["transfers"]
        # ---- customize nodes ----
        if not graph.has_node(n_from):
            graph.add_node(n_from, style="filled", fillcolor="white", fontsize=16)
        if not graph.has_node(n_to):
            graph.add_node(n_to, style="filled", fillcolor="white", fontsize=16)
        # ---- customize edges ----
        #colorscheme, color = "x11", "black"
        colorscheme, color = color_weighted(0.61, trans, max_trans)
        penwidth = penwidth_weighted(trans, max_trans)
        graph.add_edge(n_from, n_to, penwidth=penwidth, color=color, colorscheme=colorscheme)
    graph.graph_attr["outputorder"] = "edgesfirst"
    graph.graph_attr["bgcolor"] = "transparent"
    graph.graph_attr["splines"] = "false"
    graph.graph_attr["scale"] = str(scale)
    path_out = os.path.join(outdir, league + ".svg")
    graph.draw(path_out, prog=layout)
    
def draw_outleague_graph(outdir, data, layout, scale): 
    graph = pgv.AGraph(strict=False, directed=True)
    data.sort(key=lambda item: item["transfers"])
    max_trans = data[len(data) - 1]["transfers"]
    for item in data:
        n_from = item["league_from"]
        n_to = item["league_to"]
        trans = item["transfers"]
        # ---- nodes ----
        size = 5
        if not graph.has_node(n_from):
            graph.add_node(n_from, shape="rectangle", width=size, height=size, fontsize=24, style="filled", fillcolor="white")#, fontcolor="transparent")
        if not graph.has_node(n_to):
            graph.add_node(n_to, shape="rectangle", width=size, height=size, fontsize=24, style="filled", fillcolor="white")#, fontcolor="transparent")
        # ---- edges ----
        colorscheme, color = color_weighted(0.09, trans, max_trans)
        penwidth = penwidth_weighted(trans, max_trans)
        graph.add_edge(n_from, n_to, penwidth=penwidth, color=color, colorscheme=colorscheme)
    graph.graph_attr["outputorder"] = "edgesfirst"
    graph.graph_attr["bgcolor"] = "gray98"
    graph.graph_attr["splines"] = "false"
    graph.graph_attr["scale"] = str(scale)
    path_out = os.path.join(outdir, "leagues_empty.svg")
    graph.draw(path_out, prog=layout)

def create_drawings(leagues: list, outdir, from_year=1990, to_year=2022, layout_out="twopi", scale_out=9, layout_in="neato", scale_in=8):
    # create output dir
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    d_outleague = []
    # create inleague graphs
    for league in leagues:
        d_in, d_out = extract_league(league, from_year, to_year)
        draw_inleague_graph(league, outdir, d_in, layout_in, scale_in)
        d_outleague.extend(d_out)
    # create outleague graph
    draw_outleague_graph(outdir, league_transfers(d_outleague, leagues), layout_out, scale_out)
    

if __name__=="__main__":
    create_drawings(ALL_LEAGUES, "drawings/test")
    

    