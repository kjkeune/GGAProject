import os
import csv

def extract_clubs_in_league() -> dict:
    club_league = {}
    for filename in os.listdir("./data"):
        league = os.path.splitext(filename)[0]
        if league == "all_data":
            continue
        path_in = os.path.join("./data", filename)
        # read cvs file
        with open(path_in, errors="ignore") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                club_league[row["club_name"]] = league
    return club_league

def extract_league(league, from_year, to_year):
    clubs_trans = {}
    clubs_in_league = set()
    path = os.path.join("data", league) + ".csv"
    # read cvs file and extract data
    with open(path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            clubs_in_league.add(row["club_name"])
            # only known clubs
            if row["club_involved_name"] == "Unknown":
                continue
            # timespan
            if not (from_year <= int(row["year"]) <= to_year):
                continue 
            # determine direction of transfer
            if row["transfer_movement"] == "out":
                transfer = (row["club_name"],row["club_involved_name"])
            elif row["transfer_movement"] == "in":
                transfer = (row["club_involved_name"], row["club_name"])
            # add transfer to data
            if not transfer in clubs_trans:
                clubs_trans[transfer] = 1
            else:
                clubs_trans[transfer] += 1
    # setup list and split data
    in_league = []
    out_league = []
    for item in clubs_trans.items():
        row = {"club_from":item[0][0], "club_to":item[0][1], "transfers":item[1]}
        if item[0][0] in clubs_in_league and item[0][1] in clubs_in_league:
            in_league.append(row)
        else:
            out_league.append(row)
    return in_league, out_league