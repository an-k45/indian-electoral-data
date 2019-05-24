# Script to obtain all relations between PCs and ACs
# Source data: http://www.eci.gov.in/files/file/3931-delimitation-of-parliamentary-assembly-constituencies-order-2008/

import PyPDF2

delimitation_pdf = open(
    '../srcdata/Delimitation of Parliamentary & Assembly Constituencies Order - 2008 (English).pdf', 'rb')
delimitation_reader = PyPDF2.PdfFileReader(delimitation_pdf)

sample_page_object = delimitation_reader.getPage(29)
sample_page_read = " ".join(sample_page_object.extractText().split())

cut_off_word = "Name Extent of Parliamentary Constituencies"
cut_off_index = sample_page_read.find(cut_off_word)
if cut_off_index != -1:
    sample_page_read = sample_page_read[(cut_off_index + len(cut_off_word)):]

final_page_read = sample_page_read.replace(".", ".\n")

print(final_page_read)

delimitation_pdf.close()
