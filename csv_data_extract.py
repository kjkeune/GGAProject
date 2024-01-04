import argparse
import os
import csv

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", type=str)
    parser.add_argument("outputfile", type=str)
    args = parser.parse_args()
    path_in = os.path.join("./data", args.inputfile)
    path_out = os.path.join("./data_extract", args.outputfile)
    data = {}
    allowed_clubs = set()
    # read cvs file
    with open(path_in) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            allowed_clubs.add(row["club_name"])
            # only known clubs
            if row["club_involved_name"] == "Unknown":
                continue
            # timespan
            if int(row["year"]) <= 2021:
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
            #if not item[0][1] in allowed_clubs or not item[0][0] in allowed_clubs:
            #    continue
            writer.writerow([item[0][0], item[0][1], item[1]])
    print(f"Data written to {path_out}")