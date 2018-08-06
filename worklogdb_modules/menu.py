import collections
import datetime
import os
import sys
import time

import worklogdb_modules.customutils as customutils
import worklogdb_modules.entry as entry
import worklogdb_modules.logdatabase as log_database
import worklogdb_modules.search as search



class Menu:
    """User IO and management."""
    SEPARATOR = "-"*50+"\n"

    def __init__(self):
        self.options = collections.OrderedDict([("Clear Text",{"shortcut": "c", "call": self.clear_text}),
                                               ("New Entry", {"shortcut": "ne", "call": self.write_entry}),
                                               ("Search Entries", {"shortcut": "se", "call": self.search_entries}),
                                               ("Exit the program", {"shortcut": "e", "call": self.exit_program})])

    def run(self):
        while True:
            self.display_main_menu()
            user_choice = input("Enter an option: ")
            if user_choice in [each['shortcut'] for each in self.options.values()]:
                action = [each['call'] for each in self.options.values() if user_choice == each['shortcut']]
                action[0]()
            else:
                print("{} is not a valid choice".format(user_choice))

    def display_main_menu(self):
        """The main menu."""
        self.clear_text()
        print(self.SEPARATOR, "Greetings!  Here are our options.")
        for name, method in self.options.items():
            print("Type {} to {}.  {}"
                  .format(method["shortcut"],
                          method["call"].__name__.replace("_", " "),
                          method["call"].__doc__))

    def clear_text(self):
        """Removes prior interaction with the program."""
        print("Clearing...")
        return os.system('cls' if os.name == 'nt' else 'clear')

    def write_entry(self):
        """Write a single entry to file."""
        print(self.SEPARATOR, "Please fill out the following to write an entry to file.")
        attempt = 3
        while attempt > 0:
            try:
                title = self._get_title_from_user()
                start_time = self._get_start_date_from_user()
                time_spent = self._get_time_spent_from_user()
                notes = self._get_details_from_user()
                new_entry = entry.Entry(title, start_time, time_spent, notes)
                log_database.write_new_entry(new_entry)
            except Exception as exc:
                print(exc)
                attempt -= 1
            else:
                print(new_entry)
                print("Entry was successful!  Heading back to the main menu.")
                time.sleep(3)
                break

    def search_entries(self):
        """Search all available entries based on user criterias."""
        search_options = {"by date": ["date", "by_date"],
                          "by time spent": ["time spent", "by_time_spent"],
                          "exact": ["exact", "exact"],
                          "by employee": ["employee", "employee"]}
        print(self.SEPARATOR, "Please select a method to search for entries.")
        for key, value in search_options.items():
            print("Type {} to search using {}.".format(value[0], key))
        search_selection = input("Selection:")
        if search_selection.lower() == "date":
            self._search_date()
        elif search_selection.lower() == "time spent":
            self._search_time_spent()
        elif search_selection.lower() == "exact":
            self._search_by_word()
        elif search_selection.lower() == "regex":
            self._search_employee()
        else:
            print("That is not a valid selection.")
            self.search_entries()


    def _search_date(self):
        entries = log_database.get_all_entries()
        start_time_selection = input("Which date?  Use {} format. Options: {}".
                                     format(entry.Entry.date_format,
                                            [str(entry.start_date)+', ' for entry in entries]))
        search_engine = search.Search(entries)
        try:
            returned_entries = search_engine.by_date(start_time_selection)
            if len(returned_entries) > 0:
                self._page_entries(returned_entries)
                return "All entries have been viewed."
            else:
                return "No entries meet that criteria."
        except Exception as err:
            print(err)
            return self._search_date()

    def _search_time_spent(self):
        entries = log_database.get_all_entries()
        time_spent_selection = input("How long?  Use an integer. Options: {}".
                                     format([str(entry.time_spent) + ', ' for entry in entries]))
        search_engine = search.Search(entries)
        try:
            returned_entries = search_engine.by_time_spent(time_spent_selection)
            if len(returned_entries) > 0:
                self._page_entries(returned_entries)
                return "All entries have been viewed."
            else:
                return "No entries meet that criteria."
        except Exception as err:
            print(err)
            return self._search_time_spent()

    def _search_by_word(self):
        entries = log_database.get_all_entries()
        exact_selection = input("Type the phrase to search for.")
        search_engine = search.Search(entries)
        try:
            returned_entries = search_engine.words_in_entry(exact_selection)
            if len(returned_entries) > 0:
                self._page_entries(returned_entries)
                return "All entries have been viewed."
            else:
                return "No entries meet that criteria."
        except Exception as err:
            print(err)
            return self._search_by_word()

    def _search_employee(self):
        entries = log_database.get_all_entries()
        employee_name = input("Type the employee's name.Options: {}".
                                     format([str(entry.employee_name) + ', ' for entry in entries]))
        search_engine = search.Search(entries)
        try:
            returned_entries = search_engine.by_employee_name(employee_name)
            if len(returned_entries) > 0:
                self._page_entries(returned_entries)
                return "All entries have been viewed."
            else:
                return "No entries meet that criteria."
        except Exception as err:
            print(err)
            return self._search_employee()

    def _get_title_from_user(self):
        title = input("Please enter a title for this entry:")
        if title:
            return title
        else:
            return self._get_title_from_user()

    def _get_start_date_from_user(self):
        try:
            start_time = input("Please enter a start time for the task in the following format {}.  "
                               "Or type 'now' to stamp with current date and time:"
                               .format(entry.Entry.date_format))
            if start_time.lower() == "now":
                start_time = datetime.datetime.now().strftime(entry.Entry.date_format)
            customutils.generate_proper_date_from_string(start_time, entry.Entry.date_format)
            return start_time
        except:
            print("Format was invalid.  Please try again.")
            return self._get_start_date_from_user()

    def _get_time_spent_from_user(self):
        try:
            time_spent = input("Please enter a number of minutes applied to the task:")
            int(time_spent)
            return time_spent
        except:
            print("Please enter valid integer.")
            return self._get_time_spent_from_user()

    def _get_details_from_user(self):
        notes = input("Enter details:")
        return notes

    def _show_all_employees(self, entries):
        matching_entries = []
        for each in entries:
            matching_entries.append(each.employee_name)
        return matching_entries

    def _show_all_dates(self, entries):
        matching_entries = []
        for each in entries:
            matching_entries.append(each.start_date)
        return matching_entries

    def _show_all_time_spent(self, entries):
        matching_entries = []
        for each in entries:
                matching_entries.append(each.time_spent)
        return matching_entries

    def _page_entries(self, entries, start = 0):
        """Prompts user to page through search results."""
        while True:
            current_entry_position = start
            print(self.SEPARATOR)
            print(entries[current_entry_position])
            print(self.SEPARATOR)
            next_entry_prompt = input("To view next entry type N. To view previous type P.  To exit, type e.")
            if next_entry_prompt == 'N' and current_entry_position < len(entries):
                current_entry_position+=1
                self._page_entries(entries, current_entry_position)
            elif next_entry_prompt == 'P' and current_entry_position > 0:
                current_entry_position -= 1
                self._page_entries(entries, current_entry_position)
            elif next_entry_prompt == 'e':
                self.clear_text()
                break
            else:
                print("Incorrect selection, please try again.")
                return self._page_entries(entries, current_entry_position)

    def exit_program(self):
        """Exits the program."""
        print("Have a nice day.")
        sys.exit(0)

