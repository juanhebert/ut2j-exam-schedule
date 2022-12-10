import csv
from datetime import datetime
from ics import Calendar, Event
from os import makedirs, path
from zoneinfo import ZoneInfo
import toml

config = toml.load("config.toml")
timezone = config["timezone"]
in_file = config["in_file"]
out_file = config["out_file"]
subject_codes = config["subject_codes"]
location = config["location"]

c = Calendar()
tzinfo = ZoneInfo(timezone)

with open(in_file) as calendarFile:
    reader = csv.reader(calendarFile)
    exams = [row for row in reader if row[4] in subject_codes]

for row in exams:
    datetime_format = "%d/%m/%Y %H:%M"
    start_string = "{} {}".format(row[1], row[2])
    start_datetime = datetime.strptime(start_string, datetime_format)
    start_datetime = start_datetime.replace(tzinfo=tzinfo)
    end_string = "{} {}".format(row[1], row[3])
    end_datetime = datetime.strptime(end_string, datetime_format)
    end_datetime = end_datetime.replace(tzinfo=tzinfo)

    e = Event()
    e.name = "{} ({})".format(row[5], row[4])
    e.begin = start_datetime
    e.end = end_datetime
    e.location = location
    if len(row[7]) > 0:
        e.description = "Salle: {}".format(row[7])
    else:
        e.description = "Modalité: {}".format(row[9].lower())
    c.events.add(e)

# Create the out directory if it doesn't exist
makedirs(path.dirname(out_file), exist_ok=True)

with open(out_file, "w") as schedule_file:
    schedule_file.writelines(c.serialize_iter())
