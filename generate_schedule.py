import csv
from datetime import datetime
from ics import Calendar, Event
from os import makedirs, path
from zoneinfo import ZoneInfo
import toml

config = toml.load("config.toml")
timezone = ZoneInfo(config["timezone"])
in_file = config["in_file"]
out_file = config["out_file"]
subject_codes = config["subject_codes"]
location = config["location"]


def make_datetime(date, time):
    datestring_format = "%d/%m/%Y %H:%M"
    datestring = "{} {}".format(date, time)
    return datetime.strptime(datestring, datestring_format).replace(tzinfo=timezone)


def make_exam(row):
    date = row[1]
    start = row[2]
    end = row[3]
    code = row[4]
    name = row[5]
    room = row[7]
    return {
        "name": "{} ({})".format(name, code),
        "description": "Salle: {}".format(room) if len(room) > 0 else "Non-présentiel",
        "start": make_datetime(date, start),
        "end": make_datetime(date, end),
    }


def make_calendar(exams):
    c = Calendar()
    for exam in exams:
        e = Event()
        e.created = datetime.now()
        e.name = exam["name"]
        e.begin = exam["start"]
        e.end = exam["end"]
        e.location = location
        e.description = exam["description"]
        c.events.add(e)
    return c


if __name__ == "__main__":
    with open(in_file) as calendarFile:
        reader = csv.reader(calendarFile)
        exams = [make_exam(row) for row in reader if row[4] in subject_codes]
    c = make_calendar(exams)
    # Create the out directory if it doesn't exist
    makedirs(path.dirname(out_file), exist_ok=True)
    with open(out_file, "w") as schedule_file:
        schedule_file.writelines(c.serialize_iter())
