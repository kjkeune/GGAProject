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
    # read cvs file
    with open(path_in) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            transfer = (row["club_name"],row["club_involved_name"])
            if not transfer in data:
                data[transfer] = 1
            else:
                data[transfer] += 1
    # write data to cvs file
    with open(path_out, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["club_name","club_involved_name","transfers"])
        for item in data.items():
            writer.writerow([item[0][0], item[0][1], item[1]])
    print(f"Data written to {path_out}")