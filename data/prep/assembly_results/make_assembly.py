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
    'AC_NAME',
    'AC_TYPE',
    '#',
    'NAME',
    'SEX',
    'AGE',
    'CATEGORY',
    'PARTY',
    'VOTES',
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

    headers, last_ac_no, start_parsing = None, 0, False
    rows = 0
    for line in open(filename):
        if not start_parsing:
            # DETAILED RESULTS. Ignore all lines before this phrase
            if 'DETAILED RESULTS' in line:
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
        # If the row mentions a Constituency, or begins with 3+ spaces and a number,
        if line.startswith('Constituency') or re.match('\s{18,}\d+\s*\.\s*\w', line):
            # Ignore the word Constituency, and any non-digits, at the beginning.
            # Remove anything that occurs after 3 spaces. e.g. Total electors are added at the end
            ac = re.sub('Constituency[^\d]*', '', line, re.I).strip()
            ac = re.sub('NUMBER *OF *SEATS.*', '', ac, re.I).strip()
            ac = re.sub('TOTAL *ELECTORS', '', ac, re.I).strip()
            # Sometimes, there's just a blank word Constituency -- ignore these.
            if not ac:
                continue

            # Get the AC number, name and type
            match = re.match(r'(\d+)[^A-Za-z]*([A-Za-z0-9 \.\-\(\)]*)', ac)
            ac_no = int(match.group(1))
            ac_name_type = match.group(2).strip().upper()
            match = re.search(r'\((SC|ST|GEN|BL)\)', ac_name_type)
            if match:
                start, end = match.start(), match.end()
                ac_name = ac_name_type[:start].strip()
                ac_type = ac_name_type[start + 1:end - 1]
            else:
                ac_name = ac_name_type
                ac_type = 'GEN'

            # Get the total number of electors 
            total_electors = ac.split()[-1]

            # Ensure that AC number is consecutive for the same
            if ac_no > last_ac_no + 1:
                logging.warn('AC No skipped: %s %s: %d to %d',
                             state, year, last_ac_no, ac_no)
            last_ac_no = ac_no
            continue

        # HEADER ROW
        # Only header lines have both CANDIDATE and PARTY mentioned
        if re.search(r'CANDIDATE.*PARTY', line):
            # Ignore Name & Address... just consider everything else after that
            headers = re.sub('^.*CANDIDATE(.*NAME)?(.*ADDRESS)?', '', line.strip()).split()
            # Standardise headers
            headers = [header_map.get(h, h) for h in headers]
            continue

        # CANDIDATE ROW
        # If the row starts with a number, it's probably a candidate.
        # Some exceptions: West Bengal 1951: "14 - Page 16 of 38". Ignore page numbers
        # TODO: The candidate name is often split over 2 rows. Handle that.
        match = re.match(r'^\s{,20}([\d\,]+)\D.*?(\w.*)', line)
        if match and not ('Page ' in line and ' of ' in line):
            # Note: not all fields are one word.
            # E.g. "Aa S P" is a UP party. But we'll correct these manually.
            fields = line.strip().split()

            # If candidate is uncontested, the last field (%) is often missing. e.g. Nagaland 1998
            # Replace this with 100%
            if len(fields) and 'uncontested' in fields[-1].lower() and headers[-2] == 'VOTES':
                fields.append('100%')

            fields = dict(zip(headers, fields[len(fields) - len(headers):]))
            rank = match.group(1).replace(',', '')
            name = match.group(2).split('  ')[0].strip()

            # Some 2008-2009 elections have TWO numbers before the name (prev year rank?)
            # E.g. Chhattisgarh 2008, Delhi 2008, J&K 2008, Arunachal Pradesh 2009, etc
            # If the first part of name is a number (with decimal or comma), use that as rank
            parts = name.split()
            first_part = parts[0].replace('.', '').replace(',', '')
            if first_part.isdigit():
                rank, name = first_part, ' '.join(parts[1:])

            out.writerow([
                state,
                year,
                ac_no,
                ac_name,
                ac_type,
                rank,
                name,
                # Punjab 1997 uses 'W' instead of 'F' for gender
                fields.get('SEX', '').replace('W', 'F'),
                fields.get('AGE', ''),
                fields.get('CATEGORY', ''),
                fields.get('PARTY', ''),
                fields.get('VOTES', '').lower().replace('uncontested', ''),
                total_electors
            ])
            rows += 1

    if rows < 2:
        logging.warn('Only %d candidates: %s %s' % (rows, state, year))


logging.basicConfig(level=logging.WARNING)
with open('../../srcdata/assembly/assembly_results_data.csv', 'w') as f:
    out = csv.writer(f, lineterminator='\n')
    out.writerow(columns)
    for filename in glob.glob('../../srcdata/assembly/results*.txt'):
        pdf_parse(filename, out)
