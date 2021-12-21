import csv
import json
import datetime


hall_ids = ('BK', 'BR', 'GH', 'DC', 'MC', 'JE', 'PC', 'SM', 'TD', 'SY', 'ES', 'TC', 'BF', 'MY')
"""
records = []
with open('occupancy_raw.csv', newline='') as f:
    records = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)
    ]
records = sorted(records, key=lambda record: record['datetime'])

records_deduplicated = []

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
"""

with open('occupancy_raw_deduplicated.csv', newline='') as f:
    records = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)
    ]
records = sorted(records, key=lambda record: record['datetime'])

meal_times = [
    {'name': 'Breakfast', 'start': '08:00', 'end': '11:00'},
    {'name': 'Lunch', 'start': '11:00', 'end': '13:30'},
    {'name': 'Dinner', 'start': '17:00', 'end': '19:30'},
]

def get_current_meal(hall_id, timestamp):
    time = timestamp.strftime('%H:%M')
    is_weekend = (timestamp.weekday() >= 5)
    if is_weekend:
        if '08:00' <= time <= '10:30':
            if hall_id in ('GH', 'ES', 'MC'):
                return {'name': 'Breakfast', 'start': '08:00', 'end': '10:30'}
        elif '11:00' <= time <= '13:30':
            # TODO: call it Brunch instead?
            return {'name': 'Lunch', 'start': '11:00', 'end': '13:30'}
        elif '17:00' <= time <= '19:00':
            return {'name': 'Dinner', 'start': '17:00', 'end': '19:00'}
    else:
        if hall_id in ('TD', 'BF', 'PC', 'DC', 'JE', 'GH', 'BK', 'TC'):
            if hall_id == 'DC':
                if '08:00' <= time <= '10:30':
                    return {'name': 'Breakfast', 'start': '08:00', 'end': '10:30'}
            else:
                if '08:00' <= time <= '11:00':
                    return {'name': 'Breakfast', 'start': '08:00', 'end': '11:00'}
        else:
            if '07:30' <= time <= '10:30':
                return {'name': 'Breakfast', 'start': '07:30', 'end': '10:30'}

        if hall_id == 'DC' and '11:00' <= time <= '13:30':
            return {'name': 'Lunch', 'start': '11:00', 'end': '13:30'}
        elif hall_id == 'GH' and '11:30' <= time <= '14:30':
            return {'name': 'Lunch', 'start': '11:30', 'end': '14:30'}
        elif hall_id == 'TC' and '11:30' <= time <= '15:00':
            return {'name': 'Lunch', 'start': '11:30', 'end': '15:00'}
        elif '11:30' <= time <= '13:30':
            return {'name': 'Lunch', 'start': '11:30', 'end': '13:30'}

        if hall_id in ('ES', 'MC') and '17:00' <= time <= '20:00':
            return {'name': 'Dinner', 'start': '17:00', 'end': '20:00'}
        elif '17:00' <= time <= '19:30':
            return {'name': 'Dinner', 'start': '17:00', 'end': '19:30'}

    return None


meals = []
current_meals = {hall_id: None for hall_id in hall_ids}

date_epoch = datetime.date(2019, 4, 30)


for record in records:
    hall_id = record['dhall']
    timestamp = datetime.datetime.strptime(record['datetime'], '%Y-%m-%d %H:%M:%S.%f')
    date_int = (timestamp.date() - date_epoch).days
    time = timestamp.strftime('%H:%M')
    if current_meals[hall_id] is not None:
        if current_meals[hall_id]['end'] < time:
            meals.append(current_meals[hall_id])
            current_meals[hall_id] = None
        else:
            current_meals[hall_id]['records'].append(record)

    if current_meals[hall_id] is None:
        chosen_meal = get_current_meal(hall_id, timestamp)
        if chosen_meal is None:
            print('Found record outside meal time')
            print(record)
            continue
        current_meals[hall_id] = {
            'date': timestamp.strftime('%Y-%m-%d'),
            'date_int': date_int,
            'hall_id': hall_id,
            'name': chosen_meal['name'],
            'is_weekend': int(timestamp.weekday() >= 5),
            'is_family_dinner': int(chosen_meal['name'] == 'Dinner' and timestamp.weekday() == 6),
            'start': chosen_meal['start'],
            'end': chosen_meal['end'],
            'records': [record],
        }

meals = sorted(meals, key=lambda meal: (meal['date'], meal['start'], meal['hall_id']))

with open('meals.json', 'w') as f:
    json.dump(meals, f)

def time_elapsed(start_time: datetime.time, end_time: datetime.time):
    date = datetime.date(1, 1, 1)
    start_datetime = datetime.datetime.combine(date, start_time)
    end_datetime = datetime.datetime.combine(date, end_time)
    #print(start_datetime)
    #print(end_datetime)
    #print(end_datetime - start_datetime)
    #print((end_datetime - start_datetime).total_seconds())
    return (end_datetime - start_datetime).total_seconds()

for i, meal in enumerate(meals):
    total_occupancy = 0
    max_occupancy = 0
    start = datetime.datetime.strptime(meal['start'], '%H:%M').time()
    end = datetime.datetime.strptime(meal['end'], '%H:%M').time()

    last_occupancy = 0
    last_time = start
    for record in meal.pop('records'):
        occupancy = int(record['crowdedness'])
        time = datetime.datetime.strptime(record['datetime'], '%Y-%m-%d %H:%M:%S.%f').time()

        total_occupancy += time_elapsed(last_time, time) * last_occupancy
        last_time = time
        last_occupancy = occupancy

        if occupancy > max_occupancy:
            max_occupancy = occupancy

    total_occupancy += time_elapsed(last_time, end) * last_occupancy
    average_occupancy = total_occupancy / time_elapsed(start, end)
    meal['average_occupancy'] = average_occupancy
    meal['max_occupancy'] = max_occupancy

    meals[i] = meal

with open('meals.csv', 'w') as f:
    dict_writer = csv.DictWriter(f, meals[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(meals)
