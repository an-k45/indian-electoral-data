import csv


def main():
    # 0:ST_NAME,1:YEAR,2:AC_NO,3:AC_NAME,4:AC_TYPE,5:#,6:NAME,7:SEX,8:AGE,9:CATEGORY,10:PARTY,11:VOTES,12:ELECTORS
    with open("../../srcdata/assembly/assembly_results_data.csv", "r") as assembly_csv:
        assembly_data = list(csv.reader(assembly_csv))
    assembly_csv.close()
    columns, constituencies = assembly_data[:1][0], assembly_data[1:]

    constituencies.sort(key=lambda x: (x[0], x[1], int(x[2]), int(x[5])))
    with open("../../srcdata/assembly/assembly_results_data.csv", "w") as assembly_csv:
        assembly_writer = csv.writer(assembly_csv)
        assembly_writer.writerow(columns)
        for i in range(len(constituencies)):
            assembly_writer.writerow(constituencies[i])
    assembly_csv.close()


if __name__ == "__main__":
    main()
