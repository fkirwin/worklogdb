import logdatabase as ld

import menu as m

if __name__ == '__main__':
    ld.bootstrap_database()
    menu = m.Menu()
    menu.run()
