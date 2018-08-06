import datetime

import worklogdb_modules.customutils as customutils

class Entry:
    """A class representing an entry object."""
    msg = "Title: {} {} Total Duration: {} {} Started: {} {} Notes: {} {} Employee Name: {} {}"
    date_format = "%m-%d-%Y"

    def __init__(self, _title, _start_date, _time_spent, _employee_name, _notes=None):
        self._title = _title
        self._start_date = self.__handle_date(_start_date)
        self._time_spent = self.__handle_time_spent(_time_spent)
        self._employee_name = _employee_name
        self._notes = _notes

    def __str__(self):
        if self._time_spent:
            return_msg = self.msg.format(self._title, self.row_delim,
                                         datetime.datetime.strftime(self._start_date, self.date_format), self.row_delim,
                                         str(self._time_spent) + " minutes", self.row_delim,
                                         self._employee_name, self.row_delim,
                                         self._notes, self.row_delim)
        return return_msg

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, start_time):
        self._start_date = self.__handle_date(start_time)

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, notes):
        self._notes = notes

    @property
    def time_spent(self):
        return self._time_spent

    @time_spent.setter
    def time_spent(self, time_minutes):
        self._time_spent = self.__handle_time_spent(time_minutes)

    @property
    def employee_name(self):
        return self._employee_name

    @employee_name.setter
    def employee_name(self, employee_name):
        self._employee_name = employee_name

    def __handle_date(self, target_date):
        try:
            if isinstance(target_date, str):
                return customutils.generate_proper_date_from_string(target_date, self.date_format)
            else:
                return customutils.generate_proper_date_from_date(target_date, self.date_format)
        except Exception as err:
            raise err

    def __handle_time_spent(self, time_spent):
        try:
            r_time_spent = int(time_spent)
            return r_time_spent
        except Exception as err:
            raise err
