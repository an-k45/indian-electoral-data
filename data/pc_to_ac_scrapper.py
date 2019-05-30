# Script to obtain all relations between PCs and ACs
# Source data: http://www.eci.gov.in/files/file/3931-delimitation-of-parliamentary-assembly-constituencies-order-2008/

# Due to the data formatting inconsistency in the source file, this is a base script which was modified slightly between
# scrapes to collect data accordingly.


import sys
import PyPDF2
import re
from typing import List


def cut_header_information(constituency_data: str) -> str:
    """ Return, if applicable, the string of data inputted past the table header information.
    """
    cut_off_word = "of Parliamentary Constituencies"
    cut_off_index = constituency_data.find(cut_off_word)
    return constituency_data[(cut_off_index + len(cut_off_word) + 1):] if cut_off_index != -1 else constituency_data


def make_data_parseable(constituency_data: str) -> str:
    """ Return a string without newlines, arbitrary spacing, with abbreviations replaced, and otherwise standardized so
    as to be easily parsed afterward. Do not remove numbers.
    """
    parseable_constituencies = constituency_data.replace('\n', "")
    parseable_constituencies = " ".join(parseable_constituencies.split())
    parseable_constituencies = cut_header_information(parseable_constituencies)
    parseable_constituencies = re.sub(r"\s*-\s*", "", parseable_constituencies)
    parseable_constituencies = parseable_constituencies.replace(" and", ",")
    # 'and' is sometimes '&'. Some constituencies use 'and' as part of their name.

    # Replace abbreviations.
    parseable_constituencies = parseable_constituencies.replace("Cantt.", "Cantonment")

    return parseable_constituencies


def remove_numbers(constituency_lists: List[List[str]]) -> None:
    """ Remove all numbers from the constituency lists passed.
    """
    for i in range(len(constituency_lists)):
        for j in range(len(constituency_lists[i])):
            constituency_lists[i][j] = re.sub(r"\d*", "", constituency_lists[i][j])


def find_split_index(constituency_list: List[str]) -> int:
    """ Return the index of the index at which the list can be broken into two separate constituencies. Return -1 if the
    split point cannot be discerned.
    """
    if len(constituency_list) <= 2:
        return 0
    # If there is an (SC), (ST), etc. tag that isn't the last item, then that is the split index.
    for i in range(len(constituency_list) - 1):
        if re.match(r"\([a-zA-Z]\)", constituency_list[i]):
            return i
    # For most pages of data, the last complete upper case word is the split index.
    for i in range(1, len(constituency_list)):
        if constituency_list[i - 1].isupper() and not constituency_list[i].isupper():
            return i - 1
    return -1


def split_first_constituency(constituency_lists: List[List[str]]) -> None:
    """ Split the item at the 0th index in every sublist, since no comma was there to split it in the original read.
    """
    for i in range(len(constituency_lists)):
        split_constituencies = constituency_lists[i][0].split()
        split_index = find_split_index(split_constituencies)
        if split_index == -1:
            split_index = input("Input breakpoint for: " + str(split_constituencies))
        constituency_lists[i][0] = " ".join(split_constituencies[:(split_index + 1)])
        constituency_lists[i].insert(1, " ".join(split_constituencies[(split_index + 1):]))


delimitation_pdf = open(
    '../srcdata/Delimitation of Parliamentary & Assembly Constituencies Order - 2008 (English).pdf', 'rb')
delimitation_reader = PyPDF2.PdfFileReader(delimitation_pdf)

constituency_page_object = delimitation_reader.getPage(29)
constituency_page_data = constituency_page_object.extractText()

# Clean up the extracted text into parseable format, keeping numbers for later parsing patterns.
constituency_page_data = make_data_parseable(constituency_page_data)

# Create a list of lists where each list has a PC and all associated AC's.
split_constituency_data = re.split(r"\.\s+\d+", constituency_page_data)
pc_to_ac_lists = [split_constituency_data[i].split(", ") for i in range(len(split_constituency_data))]
remove_numbers(pc_to_ac_lists)
split_first_constituency(pc_to_ac_lists)

# print(pc_to_ac_lists)
for pc in pc_to_ac_lists:
    print(pc)

delimitation_pdf.close()

valid_reading = input("Is this a valid reading? Y/N: ")
if valid_reading != 'Y':
    print("Exiting...")
    sys.exit()
