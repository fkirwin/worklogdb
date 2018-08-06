import collections
import datetime
import os
import sys

import worklogdb_modules.customutils as customutils
import worklogdb_modules.customutils as entry
import worklogdb_modules.log_database as log_database
import worklogdb_modules.search as search



class Menu:
    """User IO and management."""
    SEPARATOR = "-"*50+"\n"

    def __init__(self):
        self.options = collections.OrderedDict([("Clear Text",{"shortcut": "c", "call": self.clear_text}),
                                               ("New Entry", {"shortcut": "ne", "call": self.write_entry}),
                                               ("Search Entries", {"shortcut": "se", "call": self.search_entries}),
                                               ("Exit the program", {"shortcut": "e", "call": self.exit_program})])
        log_database.bootstrap_database()
        ##self.log_database = log.Log(self.DEFAULT_LOG)

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
                self.log_connection.write_new_entry(new_entry)
            except Exception as exc:
                print(exc)
                attempt -= 1
            else:
                print(str(new_entry))
                print("Entry was successful!  Heading back to the main menu.")
                break

    def search_entries(self):
        """Search all available entries based on user criterias."""
        search_options = {"by date": ["date", "by_date"],
                          "by time spent": ["time spent", "by_time_spent"],
                          "exact": ["exact", "exact"],
                          "regex": ["regex", "regex"]}
        search_engine = search.Search(self.log_connection.get_entries())
        print(self.SEPARATOR, "Please select a method to search for entries.")
        for key, value in search_options.items():
            print("Type {} to search using {}.".format(value[0], key))
        search_selection = input("Selection:")
        if search_selection.lower() == "date":
            search_results = self._search_date(search_engine)
            if isinstance(search_results, list) and len(search_results) > 0:
                for each in search_results:
                    print(each)
            else:
                print(search_results)
        elif search_selection.lower() == "time spent":
            search_results = self._search_time_spent(search_engine)
            if isinstance(search_results, list) and len(search_results) > 0:
                for each in search_results:
                    print(each)
            else:
                print(search_results)
        elif search_selection.lower() == "exact":
            search_results = self._search_exact(search_engine)
            if isinstance(search_results, list) and len(search_results) > 0:
                for each in search_results:
                    print(each)
            else:
                print(search_results)
        elif search_selection.lower() == "regex":
            search_results = self._search_regex(search_engine)
            if isinstance(search_results, list) and len(search_results) > 0:
                for each in search_results:
                    print(each)
            else:
                print(search_results)
        else:
            print("That is not a valid selection.")
            self.search_entries()

    def _search_date(self, search_engine):
        start_time_selection = input("Which date?  Use {} format.".format(entry.Entry.date_format))
        try:
            returned_entries = search_engine.by_date(start_time_selection)
            if len(returned_entries) > 0:
                return returned_entries
            else:
                return "No entries meet that criteria."
        except Exception as err:
            print(err)
            return self._search_date(search_engine)

    def _search_time_spent(self, search_engine):
        time_spent_selection = input("How long?  Use an integer.")
        try:
            returned_entries = search_engine.by_time_spent(time_spent_selection)
            if len(returned_entries) > 0:
                return returned_entries
            else:
                return "No entries meet that criteria."
        except Exception as err:
            print(err)
            return self._search_time_spent(search_engine)

    def _search_exact(self, search_engine):
        exact_selection = input("Type the exact title or note.")
        try:
            returned_entries = search_engine.exact(exact_selection)
            if len(returned_entries) > 0:
                return returned_entries
            else:
                return "No entries meet that criteria."
        except Exception as err:
            print(err)
            return self._search_exact()

    def _search_regex(self, search_engine):
        regex_selection = input("Type the pattern.")
        try:
            returned_entries = search_engine.regex(regex_selection)
            if len(returned_entries) > 0:
                return returned_entries
            else:
                return "No entries meet that criteria."
        except Exception as err:
            print(err)
            return self._search_regex()

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

    def __show_available_dates(self):
        pass

    def __show_available_times_spent(self):
        pass

    def __show_available_employee_entries(self):
        pass

    def exit_program(self):
        """Exits the program."""
        print("Have a nice day.")
        sys.exit(0)

