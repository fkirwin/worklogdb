import collections
import os
import sys
import time

import logdatabase as log_database

import customutils as customutils


class Menu:
    """User IO and management."""
    SEPARATOR = "-"*50+"\n"

    def __init__(self):
        self.options = collections.OrderedDict([("Clear Text",{"shortcut": "c", "call": self.clear_text}),
                                               ("New Entry", {"shortcut": "ne", "call": self.write_entry}),
                                               ("Search Entries", {"shortcut": "se", "call": self.search_entries}),
                                               ("Exit the program", {"shortcut": "e", "call": self.exit_program})])
        self.positive_entry_message = "All entries have been viewed."
        self.negative_entry_message = "No entries meet that criteria."

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
                new_entry = log_database.Entry()
                new_entry.title = self._get_title_from_user()
                new_entry.start_date = self._get_start_date_from_user()
                new_entry.time_spent = self._get_time_spent_from_user()
                new_entry.employee_name = self._get_employee_from_user()
                new_entry.notes = self._get_notes_from_user()
                log_database.Entry.write_new_entry(new_entry)
            except Exception as exc:
                print(exc)
                attempt -= 1
            else:
                print(new_entry)
                print("Entry was successful!  Heading back to the main menu.")
                time.sleep(5)
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
            print(self._search_date())
            time.sleep(5)
        elif search_selection.lower() == "time spent":
            print(self._search_time_spent())
            time.sleep(5)
        elif search_selection.lower() == "exact":
            print(self._search_by_word())
            time.sleep(5)
        elif search_selection.lower() == "employee":
            print(self._search_employee())
            time.sleep(5)
        else:
            print("That is not a valid selection.")
            time.sleep(5)
            self.search_entries()

    def _search_date(self):
        """Searches DB by the date entered by the user."""
        dates = log_database.Entry.get_available_values_for_entries("start_date")
        start_date_selection = input("Select a date from the list or type now to access today's entries."
                                     "Options: {}".format([",".join([str(date)]) for date in dates]))
        try:
            start_date = customutils.handle_date(start_date_selection, log_database.Entry.date_format)
            returned_entries = log_database.Entry.get_specific_entries(log_database.Entry.start_date == start_date)
            if len(returned_entries) > 0:
                self._page_entries(returned_entries)
                return self.positive_entry_message
            else:
                return self.negative_entry_message
        except Exception as err:
            print(err)
            time.sleep(5)
            return self._search_date()

    def _search_time_spent(self):
        """Searches DB by the time spent entered by the user."""
        times_spent = log_database.Entry.get_available_values_for_entries("time_spent")
        time_spent_selection = input("How long?  Use an integer. Options: {}".
                                     format([",".join([str(options)]) for options in times_spent]))
        try:
            returned_entries = log_database.Entry.get_specific_entries(log_database.Entry.time_spent == time_spent_selection)
            if len(returned_entries) > 0:
                self._page_entries(returned_entries)
                return self.positive_entry_message
            else:
                return self.negative_entry_message
        except Exception as err:
            print(err)
            time.sleep(5)
            return self._search_time_spent()

    def _search_by_word(self):
        """Searches DB by the phrase entered by the user."""
        exact_selection = input("Type the phrase to search for.")
        try:
            returned_entries = log_database.Entry.get_specific_entries((log_database.Entry.title.contains(exact_selection))
                                                                       | (log_database.Entry.notes.contains(exact_selection)))
            if len(returned_entries) > 0:
                self._page_entries(returned_entries)
                return self.positive_entry_message
            else:
                return self.negative_entry_message
        except Exception as err:
            print(err)
            time.sleep(5)
            return self._search_by_word()

    def _search_employee(self):
        """Searches DB by the employee entered by the user."""
        employees = log_database.Entry.get_available_values_for_entries("employee_name")
        employee = input("Type the employee's name. Options: {}".
                         format([",".join([str(employee)]) for employee in employees]))
        try:
            returned_entries = log_database.Entry.get_specific_entries(log_database.Entry.employee_name.contains(employee))
            if len(returned_entries) > 0:
                self._page_entries(returned_entries)
                return self.positive_entry_message
            else:
                return self.negative_entry_message
        except Exception as err:
            print(err)
            time.sleep(5)
            return self._search_employee()

    def _get_title_from_user(self):
        title = input("Please enter a title for this entry:")
        if title:
            return title
        else:
            return self._get_title_from_user()

    def _get_start_date_from_user(self):
        try:
            start_time = input("Please enter or search for a start time in the following format {}.  "
                               "Or type 'now' to stamp with current date and time:"
                               .format(log_database.Entry.date_format))
            return customutils.handle_date(start_time, log_database.Entry.date_format)
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

    def _get_employee_from_user(self):
        employee = input("Enter employee name:")
        if employee:
            return employee
        else:
            return self._get_employee_from_user()

    def _get_notes_from_user(self):
        notes = input("Enter notes:")
        return notes

    def _page_entries(self, entries):
        """Prompts user to page through search results."""
        last = "LAST ENTRY"
        first = "FIRST ENTRY"
        only = "ONLY ENTRY"
        current_entry_position = 0
        while True:
            if current_entry_position == 0 and current_entry_position == len(entries) - 1:
                self.clear_text()
                print(only + self.SEPARATOR)
                print(entries[current_entry_position])
                print(only + self.SEPARATOR)
            elif current_entry_position == 0:
                self.clear_text()
                print(first + self.SEPARATOR)
                print(entries[current_entry_position])
                print(first + self.SEPARATOR)
            elif current_entry_position == len(entries) - 1:
                self.clear_text()
                print(last + self.SEPARATOR)
                print(entries[current_entry_position])
                print(last + self.SEPARATOR)
            else:
                self.clear_text()
                print(self.SEPARATOR)
                print(entries[current_entry_position])
                print(self.SEPARATOR)
            next_entry_prompt = input("To view next entry type N. To view previous type P.  To exit, type e.")
            if next_entry_prompt == 'N' and current_entry_position < len(entries) - 1:
                current_entry_position += 1
            elif next_entry_prompt == 'P' and current_entry_position > 0:
                current_entry_position -= 1
            elif next_entry_prompt == 'e':
                break
            else:
                print("You have reached the start or finish of the search or entered an improper command. Please try again.")
                time.sleep(5)

    def exit_program(self):
        """Exits the program."""
        print("Have a nice day.")
        sys.exit(0)

