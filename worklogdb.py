import worklogdb_modules.menu as m
import worklogdb_modules.logdatabase as ld


if __name__ == '__main__':
    ld.bootstrap_database()
    menu = m.Menu()
    menu.run()
