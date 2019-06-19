import csv
import re


def main():
    # 0:ST_NAME,1:YEAR,2:AC_NO,3:AC_NAME,4:AC_TYPE,5:#,6:NAME,7:SEX,8:AGE,9:CATEGORY,10:PARTY,11:VOTES,12:ELECTORS
    with open("../../srcdata/assembly/assembly_results_data.csv", "r") as assembly_csv:
        constituencies = list(csv.reader(assembly_csv))
    assembly_csv.close()

    for i in range(1, len(constituencies)):
        # Clean up various parties names listed as "['', 'PARTY']" instead of PARTY
        if re.match(r'\[.*\]', constituencies[i][10]):
            constituencies[i][10] = constituencies[i][10][6:-2]

        # Remove (SC) (ST) tags from contestant names and put them in the person's data.
        if "(SC)" in constituencies[i][6] or "(ST)" in constituencies[i][6]:
            constituencies[i][6], constituencies[i][9] = constituencies[i][6][:-5], constituencies[i][6][-3:-1]

        # Standardize contestant names where there are spaces on either side of a period, ie. 'A . B . NAME'
        if re.match(r'([a-zA-Z]\s\.\s)+', constituencies[i][6]):
            constituencies[i][6] = constituencies[i][6].replace(" . ", ". ")

    with open("../../srcdata/assembly/assembly_results_data.csv", "w") as assembly_csv:
        assembly_writer = csv.writer(assembly_csv)
        for i in range(len(constituencies)):
            assembly_writer.writerow(constituencies[i])
    assembly_csv.close()


if __name__ == "__main__":
    main()
