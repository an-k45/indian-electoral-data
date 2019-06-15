import csv


def main():
    # 0:ST_NAME,1:YEAR,2:AC_NO,3:ELECTORS
    with open("../../srcdata/assembly/assembly_electors_data.csv", "r") as electors_csv:
        electors_data = list(csv.reader(electors_csv))
    electors_csv.close()
    columns, constituencies = electors_data[:1][0], electors_data[1:]

    constituencies.sort(key=lambda x: (x[0], x[1], int(x[2])))
    with open("../../srcdata/assembly/assembly_electors_data.csv", "w") as electors_csv:
        electors_writer = csv.writer(electors_csv)
        electors_writer.writerow(columns)
        for i in range(len(constituencies)):
            electors_writer.writerow(constituencies[i])
    electors_csv.close()


if __name__ == "__main__":
    main()
