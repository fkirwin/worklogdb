import datetime
import sys
import unittest.mock
from contextlib import redirect_stdout
from io import StringIO

import logdatabase as logdatabase

import menu as menu


class TestUM(unittest.TestCase):
    positive_entry_message = "All entries have been viewed."
    negative_entry_message = "No entries meet that criteria."
    test_menu = menu.Menu()
    test_entry = logdatabase.Entry(title="test",
                                   start_date="1999-01-01",
                                   time_spent=1,
                                   employee_name="Dan",
                                   notes="test notes")

    def setUp(self):
        logdatabase.bootstrap_database()
        logdatabase.Entry.write_new_entry(self.test_entry)

    def tearDown(self):
        logdatabase.teardown_datanase()

    def test_display_main_menu(self):
        f = StringIO()
        with redirect_stdout(f):
            self.test_menu.display_main_menu()
        out = f.getvalue()
        self.assertIn("Greetings!  Here are our options.", out)

    def test_display_clear_text(self):
        f = StringIO()
        with redirect_stdout(f):
            self.test_menu.clear_text()
        out = f.getvalue()
        self.assertIn("", out)

    def test_write_entry(self):
        db_count = len(logdatabase.Entry.get_all_entries())
        f = StringIO("test2\n1999-01-01\n1000\nBarry\ntest notes")
        sys.stdin = f
        self.assertIsNone(self.test_menu.write_entry())
        self.assertEqual(db_count + 1, len(logdatabase.Entry.get_all_entries()))

    def test_search_date(self):
        sys.stdin = StringIO("1800-01-01")
        self.assertNotEqual(self.test_menu._search_date(), None)

    def test_search_time_spent(self):
        sys.stdin = StringIO("0")
        self.assertNotEqual(self.test_menu._search_time_spent(), None)

    def test_search_by_word(self):
        sys.stdin = StringIO("ksldfkjsdkjfdjkfjk")
        self.assertNotEqual(self.test_menu._search_by_word(), None)

    def test_search_employee(self):
        sys.stdin = StringIO("Larry")
        self.assertNotEqual(self.test_menu._search_employee(), None)

    def test_get_title_from_user(self):
        sys.stdin = StringIO("test")
        self.assertNotEqual(self.test_menu._get_title_from_user(), "none")

    def test_get_start_date_from_user(self):
        sys.stdin = StringIO("now")
        self.assertEqual(self.test_menu._get_start_date_from_user(),
                         datetime.datetime.strptime(datetime.datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d"))

        sys.stdin = StringIO("1999-01-01")
        self.assertEqual(self.test_menu._get_start_date_from_user().strftime("%Y-%m-%d"), "1999-01-01")

    def test_get_time_spent_from_user(self):
        sys.stdin = StringIO("1")
        self.assertEqual(self.test_menu._get_time_spent_from_user(), "1")

    def test_get_employee_from_user(self):
        sys.stdin = StringIO("dan")
        self.assertEqual(self.test_menu._get_employee_from_user(), "dan")

    def test_get_notes_from_user(self):
        sys.stdin = StringIO("notes")
        self.assertEqual(self.test_menu._get_employee_from_user(), "notes")

    def test_exit(self):
        with self.assertRaises(SystemExit):
            self.test_menu.exit_program()


if __name__ == '__main__':
    unittest.main()
