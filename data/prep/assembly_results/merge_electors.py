import csv
from typing import List, Dict, Union


def build_electors(data: List[List[Union[str]]]) -> Dict[str, Dict[str, Dict[str, List[str]]]]:
    """ Take a list of lists where each sublist is formatted [STATE, YEAR, AC_NO, ELECTORS] Return a three depth
    dictionary, where the initial key is the state name, the next the year, and then the constituency ID, to refer to
    the specified electors value. """
    electors_dict = {}
    for i in range(1, len(data)):
        state = data[i][0]
        year = data[i][1]
        ac_no = data[i][2]
        electors = data[i][3]
        if state not in electors_dict.keys():
            electors_dict[state] = {}
        if year not in electors_dict[state].keys():
            electors_dict[state][year] = {}
        if ac_no not in electors_dict[state][year].keys():
            electors_dict[state][year][ac_no] = []
        electors_dict[state][year][ac_no].append(electors)

    return electors_dict


def main():
    # 0:ST_NAME,1:YEAR,2:AC_NO,3:AC_NAME,4:AC_TYPE,5:#,6:NAME,7:SEX,8:AGE,9:CATEGORY,10:PARTY,11:VOTES,12:ELECTORS
    with open("../../srcdata/assembly/assembly_results_data.csv", "r") as assembly_csv:
        constituencies = list(csv.reader(assembly_csv))
    assembly_csv.close()

    with open("../../srcdata/assembly/assembly_electors_data.csv", "r") as electors_csv:
        electors_data = list(csv.reader(electors_csv))
    electors_csv.close()

    electors = build_electors(electors_data)

    for i in range(1, len(constituencies)):
        try:
            state = constituencies[i][0]
            year = str(constituencies[i][1])
            ac_no = str(constituencies[i][2])
            constituencies[i][12] = electors[state][year][ac_no][0]
        except KeyError:
            # All data past 2006 had electors written properly, and key errors only appear past 2006.
            pass

    with open("../../srcdata/assembly/assembly_results_data.csv", "w") as assembly_csv:
        assembly_writer = csv.writer(assembly_csv)
        for i in range(len(constituencies)):
            assembly_writer.writerow(constituencies[i])
    assembly_csv.close()


if __name__ == "__main__":
    main()
