import os
import csv

# MATCHING CLUBS TO THEIR LEAGUES
clubs_in_leagues = {}
for filename in os.listdir("./data"):
    if filename == "all_data.csv":
        continue
    clubs_in_leagues[filename] = set()
    path_in = os.path.join("./data", filename)
    # read cvs file
    with open(path_in, errors="ignore") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            clubs_in_leagues[filename].add((row["club_name"]))

path_in = os.path.join("./data", "all_data.csv")
path_out = os.path.join("./data_extract", "league_transfer.csv")
data = {}
allowed_clubs = set()
# read cvs file
with open(path_in, errors="ignore") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        allowed_clubs.add(row["club_name"])
        # only recent years
        if row["year"] == "year":
            continue
        if int(row["year"]) < 2020:
            continue
        # only known clubs
        if row["club_involved_name"] == "Unknown":
            continue
        # determine direction of transfer
        if row["transfer_movement"] == "out":
            transfer = (row["club_name"], row["club_involved_name"])
        elif row["transfer_movement"] == "in":
            transfer = (row["club_involved_name"], row["club_name"])
        # add transfer to data
        receiving_league = None
        sending_league = None
        for league, clubs in clubs_in_leagues.items():
            if transfer[0] in clubs:
                sending_league = league
            if transfer[1] in clubs:
                receiving_league = league
        if receiving_league is None or sending_league is None:
            continue
        if receiving_league == sending_league:
            continue
        transfer = (sending_league, receiving_league)
        if not transfer in data:
            data[transfer] = 1
        else:
            data[transfer] += 1
# write data to cvs file
with open(path_out, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["league_from", "league_to", "transfers"])
    for item in data.items():
        writer.writerow([item[0][0], item[0][1], item[1]])
print(f"Data written to {path_out}")