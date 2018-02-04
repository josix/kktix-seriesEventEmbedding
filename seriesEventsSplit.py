from collections import defaultdict

event_dict = defaultdict(list)
# { int("event_id"): ["type", "title", "startTime", endTime]}
with open('./eventTimeList.data', 'rt') as fin:
    for line in fin:
        event_id, *detail = line.strip().split(',')
        if not event_id:
            continue
        event_dict[int(event_id)] = detail

with open('./seriesEvents.data', 'rt') as fin:
    i = 0
    for line in fin:
        i += 1
        event_id, *series_events = line.strip().split(',')
        event_id = int(event_id)
        print()
        print(event_id, series_events)
        for event in series_events:
            print(event,event_dict[int(event)])
        if i == 10:
            break
