# This script was adapted from the tutorial by DataMeet at
# https://github.com/datameet/india-election-data/blob/master/assembly-elections/election.ipynb

import csv
import glob
import re
import os
import logging

columns = [
    'ST_NAME',
    'YEAR',
    'AC_NO',
    'ELECTORS'
]

header_map = {
    'GORY': 'CATEGORY',
    'TOTAL': 'VOTES'
}


def pdf_parse(filename, out):
    name = filename.split('.')[0].split('-')
    state = ' '.join(s.upper() for s in name[:-1])
    year = name[-1].strip()

    last_ac_no, start_parsing, in_electors_section = 0, False, False
    rows = 0
    for line in open(filename):
        if not start_parsing:
            # CONSTITUENCY DATA. Ignore all lines before this phrase
            if 'CONSTITUENCY DATA' in line:
                start_parsing = True
            # Exceptions: goa-1989.txt, uttar-pradesh-1996.txt, gujarat-2012.txt (image file)
            if re.search('CANDIDATE.*PARTY.*VOTES', line):
                start_parsing = True
            if not start_parsing:
                continue
        else:
            # Uttar Pradesh 2002 has a Statistical report at the END of the PDF. Ignore it.
            if 'STATISTICAL REPORT' in line:
                start_parsing = False
                continue

        # CONSTITUENCY NAME
        # If the row contains the constituency name and is not a date.
        if re.search(r'\d+\s*-\s*[a-zA-Z]+', line) \
                and not re.search(r'\d+\s*-\s*[a-zA-Z]+-\s*\d+', line) \
                and not re.search(r'\d+\s*-\s*\d+-\s*\d+', line):
            # Ignore the word constituency, extra numbers, and the Field7 residue.
            ac = re.sub(r'CONSTITUENCY[^\d]*', '', line, re.I).strip()
            ac = ac.replace("Field7:", "")
            # Ignore blank words caught.
            if not ac:
                continue

            # Get the AC number
            match = re.search(r'\d+', ac)
            ac_no = int(match.group(0))

            # Ensure that AC number is consecutive for the same
            if ac_no > last_ac_no + 1:
                logging.warn('AC No skipped: %s %s: %d to %d',
                             state, year, last_ac_no, ac_no)
            last_ac_no = ac_no
            continue

        if "ELECTORS" in line and "ELECTORS WHO VOTED" not in line:
            in_electors_section = True
            continue

        if re.search(r'\d+\s*\.\s*TOTAL', line) and in_electors_section:
            total_electors = line.split()[-1]

            out.writerow([
                state,
                year,
                ac_no,
                total_electors if total_electors != "TOTAL" else -1
            ])

            in_electors_section = False
            continue

        if "DETAILED RESULTS" in line:
            break


logging.basicConfig(level=logging.WARNING)
with open('../../srcdata/assembly/assembly_electors_data.csv', 'w') as f:
    out = csv.writer(f, lineterminator='\n')
    out.writerow(columns)
    for filename in glob.glob('../../srcdata/assembly/results/*.txt'):
        pdf_parse(filename, out)
