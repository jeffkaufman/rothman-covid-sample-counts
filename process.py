import sys
from collections import defaultdict
import datetime

counts = defaultdict(int)

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

        
        counts[county, "%s-%s-%s" % (y, m.zfill(2), d.zfill(2))] += count

with open("county.counts") as inf:
    for line in inf:
        line = line.strip().split(',')
        county = line[5]

        column = 13
        day = datetime.date.fromisoformat('2020-01-22')
        prev = 0
        latest = [0]*7
        
        while column < len(line):
            count = int(line[column])
            delta = count - prev
            latest.pop(0)
            latest.append(delta)

            county_cases[
                county,
                # https://www.jefftk.com/p/careful-with-trailing-averages
                str(day - datetime.timedelta(days=3))
            ] = sum(latest)/7
            
            day = day + datetime.timedelta(days=1)
            column += 1
            prev = count
       
        
for county_day, count in counts.items():
    cases = county_cases[county_day]

    county, day = county_day
    pop = county_pops[county]

    print("%s\t%s\t%f\t%.7f\t%s" % (
        county,day, cases, cases/pop, count))
