import csv
from typing import List, Dict, Tuple


def get_ac_id(constituency_ids: Dict[Tuple[str, str, str], str], result: List[str]) -> str:
    """ Return the assembly constituency ID that matches the data in the result passed in. """
    if len(result[1]) != 4 or int(result[1]) < 2008 or \
       (int(result[1]) == 2008 and result[0] in ["TRIPURA", "MEGHALAYA", "NAGALAND"]):
        return ""
    else:
        try:
            result[1] = "2018" if int(result[1]) >= 2018 and result[0] in ["ANDHRA PRADESH", "TELANGANA"] else "2008"
            return constituency_ids[(result[0], result[2], result[1])]
        except KeyError:
            state_match = {"JAMMU AND KASHMIR": "JAMMU & KASHMIR",
                           "DELHI": "NCT OF DELHI"}
            return constituency_ids[(state_match[result[0]], result[2], result[1])]


def get_parsed_result(result: List[str], ac_id: str, result_id: int) -> List[str]:
    """ Parse result to return a list formatted as [ID, PC_ID, NAME, SEX, AGE, PARTY, VOTES, ELECTORS, RANK] """
    parsed_result = [result_id,
                     ac_id,
                     result[6],
                     result[7],
                     result[8],
                     result[10],
                     result[11],
                     result[12],
                     result[5]]
    return parsed_result


def main():
    # 0:ST_NAME,1:YEAR,2:AC_NO,3:AC_NAME,4:AC_TYPE,5:#,6:NAME,7:SEX,8:AGE,9:CATEGORY,10:PARTY,11:VOTES,12:ELECTORS
    with open("../srcdata/assembly/assembly_results_data.csv", "r") as assembly_results_csv:
        results = list(csv.reader(assembly_results_csv))
    assembly_results_csv.close()

    # 0:ID,1:NAME,2:STATE_ID,3:CODE,4:CATEGORY,5:DELIMITATION
    with open("../datasets/assembly.csv", "r") as assembly_csv:
        constituencies = list(csv.reader(assembly_csv))
    assembly_csv.close()

    # 0:ID,1:NAME,2:ABBREVIATION,4:STATUS
    with open("../datasets/states.csv", "r") as states_csv:
        states = list(csv.reader(states_csv))
    states_csv.close()

    state_ids = {states[i][0]: states[i][1] for i in range(1, len(states))}  # Key: state ID, value: state name
    constituency_ids = {(state_ids[constituencies[i][2]], constituencies[i][3], constituencies[i][5]):
                        constituencies[i][0] for i in range(1, len(constituencies))}
    # Key: (state name, ac_code, year), value: ac_id

    parsed_results = [["ID", "PC_ID", "NAME", "SEX", "AGE", "PARTY", "VOTES", "ELECTORS", "RANK"]]
    for i in range(1, len(results)):
        parsed_results.append(get_parsed_result(results[i], get_ac_id(constituency_ids, results[i]), i))

    # output: 0:ID,1:PC_ID,2:NAME,3:SEX,4:AGE,5:PARTY,6:VOTES,7:ELECTORS,8:RANK
    with open("../datasets/assembly_results.csv", "w") as assembly_results_csv:
        assembly_results_writer = csv.writer(assembly_results_csv)
        for i in range(len(parsed_results)):
            assembly_results_writer.writerow(parsed_results[i])
    assembly_results_csv.close()


if __name__ == "__main__":
    main()
