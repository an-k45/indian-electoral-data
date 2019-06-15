import csv
from typing import List, Dict, Union


def get_result_row(result: List[str], parliament_ids: Dict[str, int]) -> List[Union[str, int]]:
    """ Return the result formatted as [ID, PC_ID, YEAR, NAME, SEX, AGE, PARTY, VOTES, ELECTORS, RANK] with ID set to 0,
    where the incoming result is formatted as [YEAR, STATE, PC, NAME, SEX, PARTY, AGE, CATEGORY, VOTES, ELECTORS, #].
    """
    try:
        seat_id = parliament_ids[result[2]] if int(result[0]) >= 2009 else ''
    except KeyError:
        seat_id = ''
    return [0,
            seat_id,
            result[0],
            result[3],
            result[4] if not result[4] == "NULL" else "",
            result[6] if not result[6] == "NULL" else "",
            result[5],
            result[8],
            result[9],
            result[10]]


def main():
    # incoming results: 0:YEAR,1:STATE,2:PC,3:NAME,4:SEX,5:PARTY,6:AGE,7:CATEGORY,8:VOTES,9:ELECTORS,10:#
    # incoming parliament seats: 0:ID,1:NAME,2:STATE_ID,3:CODE,4:CATEGORY,5:DELIMITATION
    with open("../srcdata/parliament/parliament_elections_data.csv", "r") as incoming_results_csv:
        incoming_results = list(csv.reader(incoming_results_csv))
    incoming_results_csv.close()

    with open("../datasets/parliament.csv", "r") as parliament_csv:
        parliament_seats = list(csv.reader(parliament_csv))
    parliament_csv.close()

    parliament_ids = {parliament_seats[i][1]:parliament_seats[i][0] for i in range(1, len(parliament_seats))}

    # NOTE: The relationship between pre-2008 seats to their result is lost here, and needs to be reestablished
    # by using source files above.
    with open("../datasets/parliament_results.csv", "w") as outgoing_results_csv:
        results_writer = csv.writer(outgoing_results_csv)
        results_writer.writerow(["ID", "PC_ID", "NAME", "SEX", "AGE", "PARTY", "VOTES", "ELECTORS", "RANK"])
        for i in range(1, len(incoming_results)):
            result_row = get_result_row(incoming_results[i], parliament_ids)
            result_row[0] = i
            results_writer.writerow(result_row)

    outgoing_results_csv.close()


if __name__ == "__main__":
    main()
