import csv
from typing import List


def get_state_data_from_constituency(constituency: List[str]) -> List[str]:
    """ Return the state's data in this constituency formatted as [ID, NAME, ABBREVIATION, STATUS]. """
    return [constituency[0],
            constituency[2],
            constituency[1],
            "STATE" if constituency[0][0] == "S" else "UNION TERRITORY"]


def get_states_data(constituencies: List[List[str]]) -> List[List[str]]:
    """ Return a list of lists where each sublist is a state's data formatted as [ID, NAME, ABBREVIATION, STATUS]. """
    states = []
    found_states = []
    for i in range(len(constituencies)):
        if constituencies[i][0] not in found_states and not constituencies[i][0] == "ST_CODE":
            found_states.append(constituencies[i][0])
            states.append(get_state_data_from_constituency(constituencies[i]))
    return states


def main():
    with open('2008-constituencies.csv', 'r') as cons_csv:
        constituencies_data = list(csv.reader(cons_csv))
    cons_csv.close()

    states_data = [["ID", "NAME", "ABBREVIATION", "STATUS"]]
    with open('states.csv', 'w') as states_csv:
        states_data.extend(get_states_data(constituencies_data))
        writer = csv.writer(states_csv)
        writer.writerows(states_data)
    states_csv.close()


if __name__ == "__main__":
    main()
