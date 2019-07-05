import csv
from typing import List


def get_last_id(constituency_type: str) -> int:
    """ Return the last ID of the constituency type passed in. """
    with open("../datasets/" + constituency_type + ".csv", "r") as in_csv:
        constituencies = list(csv.reader(in_csv))
        last_id = constituencies[-1][0]
    in_csv.close()

    return int(last_id)


def get_pc(constituency: List[str], pc_id: int, delimitation: int) -> List[str]:
    """ Return the constituency passed parsed into a parliamentary constituency formatted as
    [ID, NAME, STATE_ID, CODE, CATEGORY, DELIMITATION]. """
    return [pc_id,
            constituency[4],
            constituency[0],
            constituency[3],
            constituency[5],
            delimitation]


def get_ac(constituency: List[str], ac_id: int, delimitation: int) -> List[str]:
    """ Return the constituency passed parsed into a assembly constituency formatted as
    [ID, NAME, STATE_ID, CODE, CATEGORY, DELIMITATION]. """
    return [ac_id,
            constituency[7],
            constituency[0],
            constituency[6],
            constituency[8],
            delimitation]


def append_constituencies(input_file: str, delimitation: int):
    # 0:ST_CODE,1:ST_ABBR,2:ST_NAME,3:PC_CODE,4:PC_NAME,5:PC_TYPE,6:AC_CODE,7:AC_NAME,8:AC_TYPE
    with open(input_file, "r") as in_csv:
        constituencies = list(csv.reader(in_csv))
    in_csv.close()

    pc_id, ac_id = get_last_id("parliament"), get_last_id("assembly")

    pc_csv, ac_csv, pc_to_ac_csv = open('../datasets/parliament.csv', 'a'), \
                                   open('../datasets/assembly.csv', 'a'), \
                                   open('../datasets/pc_to_ac.csv', 'a')
    pc_writer, ac_writer, pc_to_ac_writer = csv.writer(pc_csv), csv.writer(ac_csv), csv.writer(pc_to_ac_csv)

    last_pc = ()
    for i in range(1, len(constituencies)):
        state, pc_code = constituencies[i][0], constituencies[i][3]
        if (state, pc_code) != last_pc:
            pc_id += 1
            last_pc = (state, pc_code)
            pc_writer.writerow(get_pc(constituencies[i], pc_id, delimitation))

        ac_id += 1
        ac_writer.writerow(get_ac(constituencies[i], ac_id, delimitation))

        pc_to_ac_writer.writerow([pc_id, ac_id])

    pc_csv.close()
    ac_csv.close()
    pc_to_ac_csv.close()


if __name__ == '__main__':
    append_constituencies("../srcdata/delimitation/andhra-bifurcation-2014.csv", 2018)
