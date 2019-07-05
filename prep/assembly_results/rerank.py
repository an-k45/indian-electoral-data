import csv
from copy import deepcopy
from typing import List


def build_constituency_groups(constituencies: List[List[str]]) -> List[List[List[str]]]:
    """ Return a depth three list where each sublist is a collection of each result of a constituency's election. """
    groups = []
    for i in range(1, len(constituencies)):
        if constituencies[i][5] == '1':
            groups.append([constituencies[i]])
        else:
            groups[-1].append(constituencies[i])
    return groups


def ranked_properly(result_groups: List[List[str]]) -> bool:
    """ Return whether or not the given result group is ranked properly by votes to listed rank. """
    copied_groups = deepcopy(result_groups)
    copied_groups.sort(key=lambda x: int(x[11] if x[11] != '' else '0'), reverse=True)
    return copied_groups == result_groups


def rerank_constituencies(result_groups: List[List[str]]) -> List[List[str]]:
    """ Return result_groups where it is sorted by vote number and all rank values are adjusted appropriately. """
    result_groups.sort(key=lambda x: int(x[11] if x[11] != '' else '0'), reverse=True)
    for i in range(len(result_groups)):
        result_groups[i][5] = str(i + 1)
    return result_groups


def main():
    # 0:ST_NAME,1:YEAR,2:AC_NO,3:AC_NAME,4:AC_TYPE,5:#,6:NAME,7:SEX,8:AGE,9:CATEGORY,10:PARTY,11:VOTES,12:ELECTORS
    with open("../../srcdata/assembly/assembly_results_data.csv", "r") as assembly_csv:
        constituencies = list(csv.reader(assembly_csv))
    assembly_csv.close()

    constituency_groups = build_constituency_groups(constituencies)

    for i in range(len(constituency_groups)):
        if not ranked_properly(constituency_groups[i]):
            constituency_groups[i] = rerank_constituencies(constituency_groups[i])

    constituencies = [constituencies[0]] + [constituency for group in constituency_groups for constituency in group]

    with open("../../srcdata/assembly/assembly_results_data.csv", "w") as assembly_csv:
        assembly_writer = csv.writer(assembly_csv)
        for i in range(len(constituencies)):
            assembly_writer.writerow(constituencies[i])
    assembly_csv.close()


if __name__ == "__main__":
    main()
