#!/usr/bin/python
import os
import datetime
from peewee import *
import worklogdb_modules.entry as entry

dirname = os.path.dirname(__file__)
DATABASE = os.path.join(dirname, '../database/log.db')
db = SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        database = db

class Entry(BaseModel):
    title = CharField()
    start_date = DateField()
    time_spent = IntegerField()
    employee_name = CharField()
    notes = CharField(null=True)


def get_all_entries():
    entries = []
    for each in Entry.select():
        entries.append(entry.Entry(each.title,
                                   each.start_date,
                                   each.time_spent,
                                   each.employee_name,
                                   each.notes))
    return entries

def get_specific_entries(columns, where_clause):
    entries = []
    for each in Entry.select(columns).where(where_clause):
        entries.append(entry.Entry(each.title,
                                   each.start_date,
                                   each.time_spent,
                                   each.employee_name,
                                   each.notes))
    return entries

def write_new_entry(entry_input):
    Entry.create(title = entry_input.title,
                 start_date = entry_input.start_date,
                 time_spent = entry_input.time_spent,
                 employee_name = entry_input.employee_name,
                 notes = entry_input.notes)

def bootstrap_database():
    with db:
        db.create_tables([Entry], safe = True)



