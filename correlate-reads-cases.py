import sys
from collections import defaultdict
import datetime

read_counts = defaultdict(int)
covid_counts = defaultdict(int)

plant_counties = {
    "HTP": "Los Angeles",
    "SJ": "Los Angeles",
    "JWPCP": "Los Angeles",
    "OC": "Orange",
    "PL": "San Diego",
    "SB": "San Diego",
    "NC": "San Diego",
}

county_pops = {
    "Los Angeles": 10040000,
    "Orange": 3170000,
    "San Diego": 3324000,
}

county_cases = {}

fname_covid_count = defaultdict(int)
with open('unenriched-covid-counts-by-sample.txt') as inf:
    for line in inf:
        count, fname = line.strip().split()
        fname_covid_count[fname] = int(count)


fname_to_sampleid = {}
with open("unenriched-fname-to-sampleid.txt") as inf:
    for line in inf:
        fname, sampleid = line.strip().split()
        fname_to_sampleid[fname] = sampleid

sample_covid_count = {}
for fname in fname_to_sampleid:
    sample_covid_count[fname_to_sampleid[fname]] = fname_covid_count[fname]
        
with open("sample.plant.date.enrichment.reads") as inf:
    for line in inf:
        line = line.strip()
        if '20' not in line:
            continue

        sample_id, plant, mdy, enrichment, count = line.split()
        if enrichment != "Unenriched": continue

        count = int(count)

        m,d,y = mdy.split(".")

        county = plant_counties[plant]

        key = county, "%s-%s-%s" % (y, m.zfill(2), d.zfill(2))
        read_counts[key] += count
        covid_counts[key] += sample_covid_count[sample_id]

with open("county.counts") as inf:
    for line in inf:
        line = line.strip().split(',')
        county = line[5]

        column = 13
        day = datetime.date.fromisoformat('2020-01-22')
        prev = 0
        latest = [0]*7
        
        while column < len(line):
            case_count = int(line[column])
            delta = case_count - prev
            latest.pop(0)
            latest.append(delta)

            county_cases[
                county,
                # https://www.jefftk.com/p/careful-with-trailing-averages
                str(day - datetime.timedelta(days=3))
            ] = sum(latest)/7
            
            day = day + datetime.timedelta(days=1)
            column += 1
            prev = case_count
       
        
for county_day, read_count in read_counts.items():
    cases = county_cases[county_day]

    county, day = county_day
    pop = county_pops[county]
    covid_reads = covid_counts[county_day]

    print("%s\t%s\t%f\t%.7f\t%s\t%s" % (
        county, day, cases, cases/pop, read_count, covid_reads))
