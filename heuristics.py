import csv
import datetime


records = []
with open('occupancy_raw.csv', newline='') as f:
    records = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)
    ]

records_deduplicated = []

hall_ids = ('BK', 'BR', 'GH', 'DC', 'MC', 'JE', 'PC', 'SM', 'TD', 'SY', 'ES', 'TC', 'BF', 'MY')
current_occupancies = {hall_id: None for hall_id in hall_ids}
last_update_timestamps = {hall_id: None for hall_id in hall_ids}
delays = []
for record in records:
    if record['dhall'] == 'PM':
        record['dhall'] = 'MY'
    hall_id = record['dhall']
    occupancy = record['crowdedness']
    if current_occupancies[hall_id] != occupancy:
        timestamp = datetime.datetime.strptime(record['datetime'], '%Y-%m-%d %H:%M:%S.%f')
        if last_update_timestamps[hall_id] is not None:
            delay = timestamp - last_update_timestamps[hall_id]
            #delays.append(delay)
        else:
            delay = None
        print(f'Change from {current_occupancies[hall_id]} to {occupancy} observed after {delay}')
        current_occupancies[hall_id] = occupancy
        last_update_timestamps[hall_id] = timestamp
        records_deduplicated.append(record)

delays = sorted(delays)
print([str(delay) for delay in delays[:100]])

with open('occupancy_raw_deduplicated.csv', 'w') as f:
    dict_writer = csv.DictWriter(f, records_deduplicated[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(records_deduplicated)
