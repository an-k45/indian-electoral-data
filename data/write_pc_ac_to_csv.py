import csv
from typing import List, Union


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


def get_parliament_constituency(constituency: List[str]) -> List[Union[int, str]]:
    """ Return the parliamentary constituency contained in the format
    [ID, NAME, STATE_ID, CODE, CATEGORY, DELIMITATION] with ID set to 0. """
    return [0,
            constituency[4],
            constituency[0],
            constituency[3],
            constituency[5],
            2008]


def get_assembly_constituency(constituency: List[str]) -> List[Union[int, str]]:
    """ Return the assembly constituency contained in the format
    [ID, NAME, STATE_ID, CODE, CATEGORY, DELIMITATION] with ID set to 0. """
    return [0,
            constituency[7],
            constituency[0],
            constituency[6],
            constituency[8],
            2008]


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

    parliament_csv, assembly_csv, pc_to_ac_csv = \
        open('parliament.csv', 'w'), open('assembly.csv', 'w'), open('pc_to_ac.csv', 'w')
    parliament_writer, assembly_writer, pc_to_ac_writer = \
        csv.writer(parliament_csv), csv.writer(assembly_csv), csv.writer(pc_to_ac_csv)
    parliament_writer.writerow(["ID", "CODE", "NAME", "DELIMITATION", "STATE_ID", "CATEGORY"])
    assembly_writer.writerow(["ID", "CODE", "NAME", "DELIMITATION", "STATE_ID", "CATEGORY"])
    pc_to_ac_writer.writerow(["PC_ID", "AC_ID"])

    parliament_constituency_id, seen_parliamentary_constituencies = 0, []
    for i in range(1, len(constituencies_data)):
        if (constituencies_data[i][3], constituencies_data[i][4]) not in seen_parliamentary_constituencies:
            parliament_constituency_id += 1
            seen_parliamentary_constituencies.append((constituencies_data[i][3], constituencies_data[i][4]))
            parliament_constituency = get_parliament_constituency(constituencies_data[i])
            parliament_constituency[0] = parliament_constituency_id
            parliament_writer.writerow(parliament_constituency)

        assembly_constituency = get_assembly_constituency(constituencies_data[i])
        assembly_constituency[0] = i
        assembly_writer.writerow(assembly_constituency)

        pc_to_ac = [parliament_constituency_id, i]
        pc_to_ac_writer.writerow(pc_to_ac)

    parliament_csv.close()
    assembly_csv.close()
    pc_to_ac_csv.close()


if __name__ == "__main__":
    main()
