import csv
from typing import List, Union, Dict


def get_formatted_result(constituency: List[Union[str, int]], turnout_data: Dict[str, int], rename_pairs: Dict[str, str]
                         ) -> List[Union[str, int]]:
    """ Return the constituency data as a listed formatted as
    [YEAR, STATE, PC, NAME, SEX, PARTY, AGE, CATEGORY, VOTES, ELECTORS, #] """
    constituency_name = " ".join(constituency[5].split()).upper()
    state_name = constituency[1].upper()
    return [2014,
            state_name if state_name not in rename_pairs.keys() else rename_pairs[state_name],
            constituency_name if constituency_name not in rename_pairs.keys() else rename_pairs[constituency_name],
            constituency[7].upper(),
            constituency[8].upper(),
            constituency[11].upper(),
            constituency[10],
            constituency[6].upper(),
            constituency[12],
            turnout_data["".join([constituency[4], constituency_name])],
            constituency[13]]


def get_number_from_indian_number(in_num: str) -> int:
    """ Return the integer value of an Indian formatted number, ie. '1,00,000' to 100000 """
    return int(in_num.replace(",", ""))


def main():
    with open("../../srcdata/parliament/parliament_elections_2014_data.csv", 'r') as parliament_2014_csv:
        results_2014 = list(csv.reader(parliament_2014_csv))
    parliament_2014_csv.close()

    with open("../../srcdata/parliament/pc-wise-turnout.csv", 'r') as turnout_csv:
        turnout_2014 = list(csv.reader(turnout_csv))
    turnout_csv.close()
    turnout_data = {"".join([turnout_2014[i][1], turnout_2014[i][2].upper()]):get_number_from_indian_number(turnout_2014[i][9])
                    for i in range(1, len(turnout_2014))}

    with open("rename.csv", 'r') as rename_csv:
        rename = list(csv.reader(rename_csv))
    rename_csv.close()
    rename_pairs = {rename[i][1]:rename[i][2] for i in range(1, len(rename))}

    parliament_results_csv = open("../../srcdata/parliament/parliament_elections_data.csv", 'a')
    parliament_results_writer = csv.writer(parliament_results_csv)

    formatted_2014_results = [get_formatted_result(results_2014[i], turnout_data, rename_pairs)
                              for i in range(1, len(results_2014))]
    formatted_2014_results.sort(key=lambda x: (x[1], x[2]))

    for i in range(len(formatted_2014_results)):
        # parliament_results_writer.writerow(formatted_2014_results[i])
        print(formatted_2014_results[i])

    parliament_results_csv.close()


if __name__ == "__main__":
    main()
