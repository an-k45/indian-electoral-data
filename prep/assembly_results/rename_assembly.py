import csv
from typing import List, Dict


def build_rename_dict(data: List[str], data_type: str) -> Dict[str, List[str]]:
    """ Take the rename pairings in format [Column, ST_NAME, Field, Value] and return a dictionary where the key is the
    incoming value and the value the target for constituencies. """
    rename_pairs = {}
    for i in range(1, len(data)):
        if data[i][0] != data_type:
            continue
        rename_pairs[data[i][2]] = [data[i][1], data[i][3]]
    return rename_pairs


def main():
    # 0:ST_NAME,1:YEAR,2:AC_NO,3:AC_NAME,4:AC_TYPE,5:#,6:NAME,7:SEX,8:AGE,9:CATEGORY,10:PARTY,11:VOTES,12:ELECTORS
    with open("../../srcdata/assembly/assembly_results_data.csv", "r") as assembly_csv:
        constituencies = list(csv.reader(assembly_csv))
    assembly_csv.close()

    # 0:Column,1:ST_NAME,2:Field,3:Value
    with open("rename.csv", "r") as rename_csv:
        rename = list(csv.reader(rename_csv))
    rename_csv.close()

    rename_constituencies = build_rename_dict(rename, "AC_NAME")
    rename_parties = build_rename_dict(rename, "PARTY")

    for i in range(1, len(constituencies)):
        try:
            # Update the constituency only if it falls in the correct state.
            cur_ac = constituencies[i][3]
            constituencies[i][3] = rename_constituencies[cur_ac][1] if \
                constituencies[i][0] == rename_constituencies[cur_ac][0].upper() else cur_ac
        except KeyError:
            pass

        try:
            constituencies[i][10] = rename_parties[constituencies[i][10]]
        except KeyError:
            pass

    with open("../../srcdata/assembly/assembly_results_data.csv", "w") as assembly_csv:
        assembly_writer = csv.writer(assembly_csv)
        for i in range(len(constituencies)):
            assembly_writer.writerow(constituencies[i])
    assembly_csv.close()


if __name__ == "__main__":
    main()
