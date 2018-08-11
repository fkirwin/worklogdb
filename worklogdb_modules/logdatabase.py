#!/usr/bin/python
import os

from peewee import *

dirname = os.path.dirname(__file__)
DATABASE = os.path.join(dirname, '../database/log.db')
db = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = db


class Entry(BaseModel):
    row_delim = '\n'
    msg = "Title: {} {} Total Duration: {} {} Started: {} {} Employee Name: {} {} Notes: {} {}"
    date_format = "%Y-%m-%d"
    title = CharField()
    start_date = DateField()
    time_spent = IntegerField()
    employee_name = CharField()
    notes = CharField(null=True)

    def __str__(self):
        return_msg = self.msg.format(self.title, self.row_delim,
                                     str(self.time_spent) + " minutes", self.row_delim,
                                     str(self.start_date), self.row_delim,
                                     self.employee_name, self.row_delim,
                                     self.notes, self.row_delim)
        return return_msg

    @classmethod
    def get_all_entries(cls):
        tmp = []
        for each in Entry.select():
            tmp.append(each)
        return tmp

    @classmethod
    def get_specific_entries(cls, where_clause):
        tmp = []
        for each in Entry.select().where(where_clause):
            tmp.append(each)
        return tmp

    @classmethod
    def get_available_values_for_entries(cls, disctinct_column):
        tmp = []
        column_obj = getattr(cls, disctinct_column)
        for each in Entry.select(column_obj).distinct():
            tmp.append(getattr(each, disctinct_column))
        return tmp

    @classmethod
    def write_new_entry(cls, entry_input):
        Entry.create(title=entry_input.title,
                     start_date=entry_input.start_date,
                     time_spent=entry_input.time_spent,
                     employee_name=entry_input.employee_name,
                     notes=entry_input.notes)


def bootstrap_database():
    with db:
        db.create_tables([Entry], safe=True)

def teardown_datanase():
    with db:
        db.drop_tables([Entry])
