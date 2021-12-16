import csv
import json
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

#delays = sorted(delays)
#print([str(delay) for delay in delays[:100]])

with open('occupancy_raw_deduplicated.csv', 'w') as f:
    dict_writer = csv.DictWriter(f, records_deduplicated[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(records_deduplicated)

records = records_deduplicated

meal_times = [
    {'name': 'Breakfast', 'start': '08:00', 'end': '11:00'},
    {'name': 'Lunch', 'start': '11:00', 'end': '13:30'},
    {'name': 'Dinner', 'start': '17:00', 'end': '19:30'},
]

meals = []
current_meals = {hall_id: None for hall_id in hall_ids}

for record in records:
    hall_id = record['dhall']
    timestamp = datetime.datetime.strptime(record['datetime'], '%Y-%m-%d %H:%M:%S.%f')
    time = timestamp.strftime('%H:%M')
    if current_meals[hall_id] is not None:
        if current_meals[hall_id]['end'] < time:
            meals.append(current_meals[hall_id])
            current_meals[hall_id] = None
        else:
            current_meals[hall_id]['records'].append(record)

    if current_meals[hall_id] is None:
        chosen_meal = None
        for meal_time in meal_times:
            if meal_time['start'] <= time <= meal_time['end']:
                chosen_meal = meal_time
        if chosen_meal is None:
            print('Found record outside meal time')
            print(record)
            continue
        current_meals[hall_id] = {
            'hall_id': hall_id,
            'name': chosen_meal['name'],
            'start': chosen_meal['start'],G
            'end': chosen_meal['end'],
            'records': [record],
        }

with open('meals.json', 'w') as f:
    json.dump(meals, f)

for meal in meals:
    total_occupancy = 0
    start = datetime.datetime.strptime(meal['start'], '%H:%M').time()
    end = datetime.datetime.strptime(meal['end'], '%H:%M').time()
    total_time = (end - start)

    last_occupancy = 0
    last_end = start
    for record in meal.pop('records'):
        occupancy = record['crowdedness']
        time = datetime.datetime.strptime(record['datetime'], '%Y-%m-%d %H:%M:%S.%f')
        last_end =
