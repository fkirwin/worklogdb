import datetime
import re

import worklogdb_modules.customutils as customutils
import worklogdb_modules.entry as entry


class Search:
    """Represents a search that can be performed on the data."""
    def __init__(self, entries=None):
        # Playing with REGEX.  Probably not the best approach.
        self.options = {funct: funct for funct in re.findall(r"\b\w+(?<!_{2})\b", str(Search.__dict__.keys()))
                        if funct != "dict_keys"}
        if not entries:
            self.entries = []
        else:
            self.entries = entries

    def __str__(self):
        return_string = list(self.options.keys())
        return "Search Options: \n" + "\n".join(return_string)

    def by_date(self, date):
        matching_entries = []
        formatted_datetime = datetime.datetime.strptime(date, entry.Entry.date_format)
        for each in self.entries:
            if customutils.generate_proper_date_from_date(each.start_date, entry.Entry.date_format).date() == formatted_datetime.date():
                matching_entries.append(each)
        return matching_entries

    def by_time_spent(self, str_time_spent):
        matching_entries = []
        for each in self.entries:
            if each.time_spent == int(str_time_spent):
                matching_entries.append(each)
        return matching_entries

    def words_in_entry(self, exact_phrase):
        matching_entries = []
        for each in self.entries:
            if (exact_phrase in each.notes) or (exact_phrase in each.title):
                matching_entries.append(each)
        return matching_entries

    def employee(self, target_employee):
        matching_entries = []
        for each in self.entries:
            if target_employee == each.employee_name:
                matching_entries.append(each)
        return matching_entries
