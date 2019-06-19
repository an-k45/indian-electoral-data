import csv
from typing import List, Dict, Tuple


def build_override(data: List[List[str]]) -> Dict[Tuple[str, str, str, str], List[str]]:
    """ Return a dictionary where the key is a tuple of the state name, year, constituency ID, and rank mapped to a
    value that is a list of what the constituency should be changed to. """
    override_pairs = {}
    for i in range(1, len(data)):
        year = data[i][1] if len(data[i][1]) == 4 else (data[i][1][3:] + data[i][1][:3])
        override_pairs[(data[i][0].upper(), year, data[i][2], data[i][5])] = data[i]
    return override_pairs


def merge_constituency_data(new_data: List[str], prev_data: List[str]) -> List[str]:
    """ Return the mesh between the new and prev data such that electors are included and votes are a number value. """
    new_data[0] = new_data[0].upper()
    try:
        new_data[11] = "" if new_data[11] == "-" else new_data[11]
    except IndexError:
        new_data.append("")
    new_data[1] = new_data[1] if len(new_data[1][1]) == 4 else (prev_data[1])
    new_data.append(prev_data[12] if prev_data[12] != ":" else "")
    return new_data


def main():
    # 0:ST_NAME,1:YEAR,2:AC_NO,3:AC_NAME,4:AC_TYPE,5:#,6:NAME,7:SEX,8:AGE,9:CATEGORY,10:PARTY,11:VOTES,12:ELECTORS
    with open("../../srcdata/assembly/assembly_results_data.csv", "r") as assembly_csv:
        constituencies = list(csv.reader(assembly_csv))
    assembly_csv.close()

    # 0:ST_NAME,1:YEAR,2:AC_NO,3:AC_NAME,4:AC_TYPE,5:#,6:NAME,7:SEX,8:AGE,9:CATEGORY,10:PARTY,11:VOTES
    with open("override.csv", "r") as override_csv:
        override_data = list(csv.reader(override_csv))
    override_csv.close()

    override = build_override(override_data)

    for i in range(1, len(constituencies)):
        try:
            # Fix inconsistencies by replacing them with the proper data
            key = (constituencies[i][0], constituencies[i][1], constituencies[i][2], constituencies[i][5])
            new_data = override[key]
            constituencies[i] = merge_constituency_data(new_data, constituencies[i])
        except KeyError:
            pass
        finally:
            # Fix the improper parsing of NOTA
            if constituencies[i][6] == "None of the Above":
                constituencies[i][6], constituencies[i][7], constituencies[i][8], constituencies[i][9] = \
                    "NONE OF THE ABOVE", "", "", ""

    with open("../../srcdata/assembly/assembly_results_data.csv", "w") as assembly_csv:
        assembly_writer = csv.writer(assembly_csv)
        for i in range(len(constituencies)):
            assembly_writer.writerow(constituencies[i])
    assembly_csv.close()


if __name__ == "__main__":
    main()
