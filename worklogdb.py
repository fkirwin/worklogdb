import worklogdb_modules.menu as menu


##TODO: Need to create a menu.  Menu - two functionalities to add or search for entries.
##TODO: Employee search should show all employees to search by.
##TODO: Date search should display all available dates in the DB.
##TODO: Time Spent search also needs to have a list of all the options to select from.
##TODO: Records are easily readable after searching.  Need paging and autoclearing.   Show date, employee name, task name, time spent, and notes.
##TODO: 50% test coverage minimum

if __name__ == '__main__':
    menu = menu.Menu()
    menu.run()