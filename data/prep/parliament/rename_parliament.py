import csv


def main():
    # incoming parliament seats: 0:ID,1:NAME,2:STATE_ID,3:CODE,4:CATEGORY,5:DELIMITATION
    with open("../../datasets/parliament.csv", "r") as parliament_csv:
        parliament_seats = list(csv.reader(parliament_csv))
    parliament_csv.close()

    with open("rename.csv", 'r') as rename_csv:
        rename = list(csv.reader(rename_csv))
    rename_csv.close()
    rename = [rename[i] for i in range(len(rename)) if rename[i][0] == "PC"]
    rename_pairs = {rename[i][1]: rename[i][2] for i in range(1, len(rename))}

    for i in range(1, len(parliament_seats)):
        if parliament_seats[i][1] in rename_pairs.keys():
            parliament_seats[i][1] = rename_pairs[parliament_seats[i][1]]

    with open("../../datasets/parliament.csv", "w") as parliament_csv:
        parliament_writer = csv.writer(parliament_csv)
        parliament_writer.writerows(parliament_seats)
    parliament_csv.close()


if __name__ == "__main__":
    main()
