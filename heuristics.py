import csv

records = []
with open('occupancy_GH.csv', newline='') as f:
    records = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)
    ]

records_deduplicated = []

current_occupancy = None
for record in records:
    occupancy = record['crowdedness']
    if current_occupancy != occupancy:
        current_occupancy = occupancy
        records_deduplicated.append(record)

with open('occupancy_GH_deduplicated.csv', 'w') as f:
    dict_writer = csv.DictWriter(f, records_deduplicated[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(records_deduplicated)
print(records)
