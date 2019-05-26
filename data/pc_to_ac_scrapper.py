# Script to obtain all relations between PCs and ACs
# Source data: http://www.eci.gov.in/files/file/3931-delimitation-of-parliamentary-assembly-constituencies-order-2008/

import PyPDF2
import re


def cut_header_information(constituency_data: str) -> str:
    """ Return, if applicable, the string of data inputted past the table header information.
    """
    cut_off_word = "Constituencies 1"
    cut_off_index = constituency_data.find(cut_off_word)
    return constituency_data[(cut_off_index + len("Constituencies ")):] if cut_off_index != -1 else constituency_data


delimitation_pdf = open(
    '../srcdata/Delimitation of Parliamentary & Assembly Constituencies Order - 2008 (English).pdf', 'rb')
delimitation_reader = PyPDF2.PdfFileReader(delimitation_pdf)

sample_page_object = delimitation_reader.getPage(334)
sample_page_read = sample_page_object.extractText()

# Remove unnecessary characters or information, ie. (SC), spaces, etc.
sample_page_read = sample_page_read.replace('\n', "")
sample_page_read = " ".join(sample_page_read.split())
sample_page_read = cut_header_information(sample_page_read)
# TODO Redo this with regex, accounting for spaces on all sides, and catching the exact contents inside brackets.
for item in [" (ST)", " (SC)", "(ST)", "(SC)", " (Urban)", " (Rural)", " -", "- ", "-"]:
    sample_page_read = sample_page_read.replace(item, "")
sample_page_read = sample_page_read.replace(" and", ",")

# Create sub-lists where each PC has its associated ACs
sample_page_read = re.split("\.\s+\d+", sample_page_read)
sample_page_read = [sample_page_read[i].split(", ") for i in range(len(sample_page_read))]
# Remove any numbers or periods.
for i in range(len(sample_page_read)):
    for j in range(len(sample_page_read[i])):
        sample_page_read[i][j] = re.sub("\d*", "", sample_page_read[i][j])
        sample_page_read[i][j] = re.sub("\.*", "", sample_page_read[i][j])
# Separate the PC stringed with a single AC
for i in range(len(sample_page_read)):
    split_off_constituencies = sample_page_read[i][0].split()
    sample_page_read[i][0] = split_off_constituencies[0]
    sample_page_read[i].insert(1, split_off_constituencies[1])

# print(sample_page_read)
for lok_sabha_seat in sample_page_read:
    print(lok_sabha_seat)

delimitation_pdf.close()

